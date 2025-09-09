import frappe
from frappe import _

def execute():
	"""Update DGII custom fields"""
	
	# Add RNC field to Customer if not exists
	if not frappe.db.exists("Custom Field", {"fieldname": "rnc", "dt": "Customer"}):
		frappe.get_doc({
			"doctype": "Custom Field",
			"dt": "Customer",
			"fieldname": "rnc",
			"fieldtype": "Data",
			"label": "RNC",
			"insert_after": "tax_id",
			"description": "RNC (Registro Nacional de Contribuyentes) - 9 o 11 dígitos"
		}).insert()
	
	# Add RNC field to Supplier if not exists
	if not frappe.db.exists("Custom Field", {"fieldname": "rnc", "dt": "Supplier"}):
		frappe.get_doc({
			"doctype": "Custom Field",
			"dt": "Supplier",
			"fieldname": "rnc",
			"fieldtype": "Data",
			"label": "RNC",
			"insert_after": "tax_id",
			"description": "RNC (Registro Nacional de Contribuyentes) - 9 o 11 dígitos"
		}).insert()
	
	# Add NCF field to Sales Invoice if not exists
	if not frappe.db.exists("Custom Field", {"fieldname": "ncf", "dt": "Sales Invoice"}):
		frappe.get_doc({
			"doctype": "Custom Field",
			"dt": "Sales Invoice",
			"fieldname": "ncf",
			"fieldtype": "Data",
			"label": "NCF",
			"insert_after": "tax_id",
			"description": "NCF (Número de Comprobante Fiscal) - Letra + 11 dígitos"
		}).insert()
	
	# Add DGII Status field to Sales Invoice if not exists
	if not frappe.db.exists("Custom Field", {"fieldname": "dgii_status", "dt": "Sales Invoice"}):
		frappe.get_doc({
			"doctype": "Custom Field",
			"dt": "Sales Invoice",
			"fieldname": "dgii_status",
			"fieldtype": "Select",
			"label": "DGII Status",
			"insert_after": "ncf",
			"options": "Draft\nSent\nAccepted\nRejected\nError",
			"read_only": 1
		}).insert()
	
	frappe.db.commit()
