import frappe
from frappe.model.document import Document
from frappe import _
import requests
import json
from datetime import datetime

class ECFDocument(Document):
	def validate(self):
		self.validate_required_fields()
		self.validate_ncf_format()
		self.validate_rnc_format()
	
	def validate_required_fields(self):
		"""Validar campos requeridos"""
		if not self.sales_invoice:
			frappe.throw(_("Debe seleccionar una factura de venta"))
		
		if not self.rnc_emisor:
			frappe.throw(_("RNC del emisor es requerido"))
		
		if not self.rnc_comprador:
			frappe.throw(_("RNC del comprador es requerido"))
	
	def validate_ncf_format(self):
		"""Validar formato de NCF"""
		if self.ncf:
			import re
			ncf_pattern = r'^[A-Z]\d{11}$'
			if not re.match(ncf_pattern, self.ncf):
				frappe.throw(_("Formato de NCF inválido. Debe ser una letra seguida de 11 dígitos"))
	
	def validate_rnc_format(self):
		"""Validar formato de RNC"""
		rnc_pattern = r'^\d{9}$|^\d{11}$'
		import re
		
		if self.rnc_emisor and not re.match(rnc_pattern, self.rnc_emisor.replace('-', '')):
			frappe.throw(_("Formato de RNC emisor inválido"))
		
		if self.rnc_comprador and not re.match(rnc_pattern, self.rnc_comprador.replace('-', '')):
			frappe.throw(_("Formato de RNC comprador inválido"))
	
	def before_save(self):
		"""Antes de guardar"""
		if not self.creation_date:
			self.creation_date = datetime.now()
	
	def send_to_dgii(self):
		"""Enviar documento a DGII"""
		try:
			# Obtener configuración de DGII
			dgii_settings = frappe.get_doc("DGII Settings", {"company": self.company})
			
			# Preparar datos de la factura
			invoice_data = self.prepare_invoice_data()
			
			# Llamar al servidor Node.js
			response = requests.post(
				f"{dgii_settings.dgii_server_url}/api/ecf/send",
				json={
					"certificate": dgii_settings.certificate_content or dgii_settings.certificate_path,
					"password": dgii_settings.certificate_password,
					"environment": dgii_settings.environment.lower(),
					"invoiceData": invoice_data,
					"rncEmisor": self.rnc_emisor,
					"noEcf": self.ncf
				},
				timeout=dgii_settings.timeout or 30
			)
			
			if response.status_code == 200:
				data = response.json()
				if data.get("success"):
					self.track_id = data["data"]["trackId"]
					self.status = "Sent"
					self.dgii_response = json.dumps(data["data"])
					self.save()
					frappe.msgprint(_("Documento enviado exitosamente a DGII"))
					return True
				else:
					frappe.throw(_(f"Error al enviar: {data.get('error')}"))
			else:
				frappe.throw(_(f"Error de conexión: {response.status_code}"))
				
		except requests.exceptions.RequestException as e:
			frappe.throw(_(f"Error de conexión: {str(e)}"))
		except Exception as e:
			frappe.throw(_(f"Error: {str(e)}"))
	
	def check_status(self):
		"""Verificar estado del documento en DGII"""
		try:
			if not self.track_id:
				frappe.throw(_("No hay track ID para verificar"))
			
			dgii_settings = frappe.get_doc("DGII Settings", {"company": self.company})
			
			response = requests.get(
				f"{dgii_settings.dgii_server_url}/api/ecf/status/{self.track_id}",
				params={
					"certificate": dgii_settings.certificate_content or dgii_settings.certificate_path,
					"password": dgii_settings.certificate_password,
					"environment": dgii_settings.environment.lower()
				},
				timeout=dgii_settings.timeout or 30
			)
			
			if response.status_code == 200:
				data = response.json()
				if data.get("success"):
					status_data = data["data"]
					self.status = status_data.get("estado", "Unknown")
					self.dgii_response = json.dumps(status_data)
					self.save()
					frappe.msgprint(_(f"Estado actualizado: {self.status}"))
					return status_data
				else:
					frappe.throw(_(f"Error al verificar estado: {data.get('error')}"))
			else:
				frappe.throw(_(f"Error de conexión: {response.status_code}"))
				
		except Exception as e:
			frappe.throw(_(f"Error: {str(e)}"))
	
	def prepare_invoice_data(self):
		"""Preparar datos de la factura para envío a DGII"""
		# Obtener datos de la factura de venta
		sales_invoice = frappe.get_doc("Sales Invoice", self.sales_invoice)
		
		# Preparar estructura de datos para DGII
		invoice_data = {
			"Encabezado": {
				"Version": "1.0",
				"RNCEmisor": self.rnc_emisor,
				"RNCComprador": self.rnc_comprador,
				"eNCF": self.ncf,
				"FechaEmision": sales_invoice.posting_date.strftime("%d-%m-%Y"),
				"FechaFirma": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
				"TipoIngresos": "01",  # Ingresos por operaciones de venta
				"CodigoSeguridad": self.codigo_seguridad or "",
				"Estado": "1"  # 1 = Normal, 2 = Modificado, 3 = Anulado
			},
			"DetalleItems": [],
			"DetallePagos": [],
			"DetalleDescuentos": [],
			"DetalleImpuestosAdicionales": [],
			"DetalleReferencias": []
		}
		
		# Agregar items
		for item in sales_invoice.items:
			item_data = {
				"Linea": {
					"NumeroLinea": item.idx,
					"CodigoItem": item.item_code,
					"Cantidad": item.qty,
					"UnidadMedida": "UND",  # Unidad por defecto
					"PrecioUnitario": item.rate,
					"MontoItem": item.amount,
					"DescripcionItem": item.description or item.item_name
				}
			}
			invoice_data["DetalleItems"].append(item_data)
		
		# Agregar totales
		invoice_data["Resumen"] = {
			"TotalItems": len(sales_invoice.items),
			"SubTotal": sales_invoice.net_total,
			"Descuento": sales_invoice.discount_amount or 0,
			"ImpuestoAdicional": 0,
			"SubTotalMenosDescuento": sales_invoice.net_total - (sales_invoice.discount_amount or 0),
			"TotalITBIS": sales_invoice.total_taxes_and_charges or 0,
			"Total": sales_invoice.grand_total
		}
		
		return invoice_data
	
	def generate_qr_code(self):
		"""Generar código QR para el documento"""
		try:
			dgii_settings = frappe.get_doc("DGII Settings", {"company": self.company})
			
			response = requests.post(
				f"{dgii_settings.dgii_server_url}/api/dgii/generate-qr-ecf",
				json={
					"rncEmisor": self.rnc_emisor,
					"rncComprador": self.rnc_comprador,
					"encf": self.ncf,
					"montoTotal": self.monto_total,
					"fechaEmision": self.fecha_emision.strftime("%d-%m-%Y") if self.fecha_emision else "",
					"fechaFirma": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
					"codigoSeguridad": self.codigo_seguridad or "",
					"environment": dgii_settings.environment.lower()
				},
				timeout=dgii_settings.timeout or 30
			)
			
			if response.status_code == 200:
				data = response.json()
				if data.get("success"):
					self.qr_code_url = data["data"]["qrUrl"]
					self.save()
					frappe.msgprint(_("Código QR generado exitosamente"))
					return data["data"]["qrUrl"]
				else:
					frappe.throw(_(f"Error al generar QR: {data.get('error')}"))
			else:
				frappe.throw(_(f"Error de conexión: {response.status_code}"))
				
		except Exception as e:
			frappe.throw(_(f"Error: {str(e)}"))
