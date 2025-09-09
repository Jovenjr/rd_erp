import frappe
from frappe import _
import re

def validate_rnc_format(doc, method):
	"""Validar formato de RNC en Sales Invoice"""
	if doc.tax_id:
		# Verificar si es un RNC (9 o 11 dígitos)
		rnc_pattern = r'^\d{9}$|^\d{11}$'
		if re.match(rnc_pattern, doc.tax_id.replace('-', '')):
			# Es un RNC, validar formato
			formatted_rnc = doc.tax_id.replace('-', '')
			if len(formatted_rnc) not in [9, 11]:
				frappe.throw(_("RNC debe tener 9 o 11 dígitos"))
			
			# Actualizar el campo con formato limpio
			doc.tax_id = formatted_rnc

def send_to_dgii(doc, method):
	"""Enviar factura a DGII automáticamente al confirmar"""
	try:
		# Verificar si la factura tiene RNC (es un cliente fiscal)
		if not doc.tax_id:
			return
		
		# Verificar si ya existe un eCF Document para esta factura
		existing_ecf = frappe.get_value(
			"eCF Document",
			{"sales_invoice": doc.name},
			"name"
		)
		
		if existing_ecf:
			# Actualizar eCF existente
			ecf_doc = frappe.get_doc("eCF Document", existing_ecf)
		else:
			# Crear nuevo eCF Document
			ecf_doc = frappe.get_doc({
				"doctype": "eCF Document",
				"company": doc.company,
				"sales_invoice": doc.name,
				"ncf": generate_ncf(doc),
				"rnc_emisor": get_company_rnc(doc.company),
				"rnc_comprador": doc.tax_id,
				"fecha_emision": doc.posting_date,
				"monto_total": doc.grand_total
			})
			ecf_doc.insert()
		
		# Enviar a DGII
		ecf_doc.send_to_dgii()
		
	except Exception as e:
		frappe.log_error(f"Error sending invoice to DGII: {str(e)}", "DGII Send Error")
		# No lanzar excepción para no bloquear la confirmación de la factura

def generate_ncf(sales_invoice):
	"""Generar NCF basado en el tipo de factura"""
	# Obtener configuración de secuencias de NCF
	ncf_config = frappe.get_doc("NCF Configuration", {"company": sales_invoice.company})
	
	# Determinar tipo de NCF basado en el tipo de factura
	ncf_type = "A"  # Factura de Crédito Fiscal por defecto
	
	if sales_invoice.is_consolidated:
		ncf_type = "B"  # Factura de Consumo
	
	# Generar secuencia
	sequence = get_next_ncf_sequence(sales_invoice.company, ncf_type)
	
	# Formatear NCF: Tipo + Secuencia de 11 dígitos
	ncf = f"{ncf_type}{sequence:011d}"
	
	return ncf

def get_next_ncf_sequence(company, ncf_type):
	"""Obtener siguiente secuencia de NCF"""
	# Obtener última secuencia usada
	last_sequence = frappe.get_value(
		"eCF Document",
		{
			"company": company,
			"ncf": ["like", f"{ncf_type}%"]
		},
		"ncf",
		order_by="creation desc"
	)
	
	if last_sequence:
		# Extraer secuencia del último NCF
		last_seq = int(last_sequence[1:])  # Remover el tipo y obtener secuencia
		return last_seq + 1
	else:
		# Primera secuencia
		return 1

def get_company_rnc(company):
	"""Obtener RNC de la empresa"""
	company_doc = frappe.get_doc("Company", company)
	return company_doc.tax_id
