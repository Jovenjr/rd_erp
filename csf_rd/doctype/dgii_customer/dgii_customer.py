import frappe
from frappe.model.document import Document
from frappe import _
import requests
import json

class DGIICustomer(Document):
	def validate(self):
		self.validate_rnc_format()
		self.validate_required_fields()
	
	def validate_rnc_format(self):
		"""Validar formato de RNC"""
		if self.rnc:
			import re
			rnc_pattern = r'^\d{9}$|^\d{11}$'
			if not re.match(rnc_pattern, self.rnc.replace('-', '')):
				frappe.throw(_("Formato de RNC inválido. Debe ser 9 o 11 dígitos"))
	
	def validate_required_fields(self):
		"""Validar campos requeridos"""
		if not self.rnc:
			frappe.throw(_("RNC es requerido"))
		
		if not self.customer_name:
			frappe.throw(_("Nombre del cliente es requerido"))
	
	def before_save(self):
		"""Antes de guardar"""
		# Formatear RNC
		if self.rnc:
			self.rnc = self.rnc.replace('-', '')
	
	def sync_with_dgii(self):
		"""Sincronizar con directorio de clientes de DGII"""
		try:
			# Obtener configuración de DGII
			dgii_settings = frappe.get_doc("DGII Settings", {"company": self.company})
			
			# Llamar al servidor Node.js para obtener directorio de clientes
			response = requests.get(
				f"{dgii_settings.dgii_server_url}/api/ecf/customer-directory/{self.rnc}",
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
					directory_data = data["data"]
					self.dgii_response = json.dumps(directory_data)
					self.is_authorized = True
					self.save()
					frappe.msgprint(_("Cliente sincronizado exitosamente con DGII"))
					return directory_data
				else:
					frappe.throw(_(f"Error al sincronizar: {data.get('error')}"))
			else:
				frappe.throw(_(f"Error de conexión: {response.status_code}"))
				
		except requests.exceptions.RequestException as e:
			frappe.throw(_(f"Error de conexión: {str(e)}"))
		except Exception as e:
			frappe.throw(_(f"Error: {str(e)}"))
	
	def validate_rnc_with_dgii(self):
		"""Validar RNC con DGII"""
		try:
			dgii_settings = frappe.get_doc("DGII Settings", {"company": self.company})
			
			response = requests.post(
				f"{dgii_settings.dgii_server_url}/api/dgii/validate-rnc",
				json={"rnc": self.rnc},
				timeout=dgii_settings.timeout or 30
			)
			
			if response.status_code == 200:
				data = response.json()
				if data.get("success"):
					frappe.msgprint(_("RNC válido"))
					return True
				else:
					frappe.throw(_(f"RNC inválido: {data.get('error')}"))
			else:
				frappe.throw(_(f"Error de conexión: {response.status_code}"))
				
		except Exception as e:
			frappe.throw(_(f"Error: {str(e)}"))
