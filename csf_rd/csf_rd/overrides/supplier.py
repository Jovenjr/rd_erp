import frappe
from frappe import _
import re

def validate_rnc_format(doc, method):
	"""Validar formato de RNC en Supplier"""
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
