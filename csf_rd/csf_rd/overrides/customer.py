import frappe
from frappe import _
import re

def validate_rnc_format(doc, method):
	"""Validar formato de RNC en Customer"""
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
			
			# Crear o actualizar registro en DGII Customer
			create_or_update_dgii_customer(doc)

def create_or_update_dgii_customer(customer_doc):
	"""Crear o actualizar registro en DGII Customer"""
	try:
		# Buscar si ya existe un registro DGII Customer para este RNC
		existing_dgii_customer = frappe.get_value(
			"DGII Customer",
			{"rnc": customer_doc.tax_id, "company": customer_doc.company},
			"name"
		)
		
		if existing_dgii_customer:
			# Actualizar registro existente
			dgii_customer = frappe.get_doc("DGII Customer", existing_dgii_customer)
			dgii_customer.customer_name = customer_doc.customer_name
			dgii_customer.email = customer_doc.email_id
			dgii_customer.phone = customer_doc.mobile_no or customer_doc.phone
			dgii_customer.address = get_customer_address(customer_doc)
			dgii_customer.save()
		else:
			# Crear nuevo registro
			dgii_customer = frappe.get_doc({
				"doctype": "DGII Customer",
				"company": customer_doc.company,
				"rnc": customer_doc.tax_id,
				"customer_name": customer_doc.customer_name,
				"email": customer_doc.email_id,
				"phone": customer_doc.mobile_no or customer_doc.phone,
				"address": get_customer_address(customer_doc),
				"customer_type": "Individual" if customer_doc.customer_type == "Individual" else "Company"
			})
			dgii_customer.insert()
			
	except Exception as e:
		frappe.log_error(f"Error creating DGII Customer: {str(e)}", "DGII Customer Creation")

def get_customer_address(customer_doc):
	"""Obtener dirección del cliente"""
	address_parts = []
	
	if customer_doc.customer_primary_address:
		address_doc = frappe.get_doc("Address", customer_doc.customer_primary_address)
		address_parts.append(address_doc.address_line1 or "")
		address_parts.append(address_doc.address_line2 or "")
		address_parts.append(address_doc.city or "")
		address_parts.append(address_doc.state or "")
		address_parts.append(address_doc.country or "")
	
	return ", ".join([part for part in address_parts if part])
