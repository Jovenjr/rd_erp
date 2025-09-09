import frappe
from frappe import _

def get_context(context):
	"""Get context for DGII Customer Registration web form"""
	context.title = _("DGII Customer Registration")
	context.no_cache = 1
	
	# Add any additional context variables here
	context.countries = frappe.get_all("Country", fields=["name", "country_name"])
	
	return context

@frappe.whitelist(allow_guest=True)
def register_dgii_customer(customer_data):
	"""Register a new DGII customer via web form"""
	try:
		# Validate required fields
		required_fields = ['customer_name', 'rnc', 'email', 'phone']
		for field in required_fields:
			if not customer_data.get(field):
				frappe.throw(_(f"Field {field} is required"))
		
		# Validate RNC format
		import re
		rnc_pattern = r'^\d{9}$|^\d{11}$'
		if not re.match(rnc_pattern, customer_data.get('rnc', '').replace('-', '')):
			frappe.throw(_("Invalid RNC format. Must be 9 or 11 digits"))
		
		# Create DGII Customer record
		dgii_customer = frappe.get_doc({
			"doctype": "DGII Customer",
			"customer_name": customer_data.get('customer_name'),
			"rnc": customer_data.get('rnc').replace('-', ''),
			"email": customer_data.get('email'),
			"phone": customer_data.get('phone'),
			"address": customer_data.get('address', ''),
			"customer_type": customer_data.get('customer_type', 'Individual'),
			"company": frappe.defaults.get_user_default("Company")
		})
		
		dgii_customer.insert()
		
		# Sync with DGII if requested
		if customer_data.get('sync_with_dgii'):
			dgii_customer.sync_with_dgii()
		
		return {
			"success": True,
			"message": _("Customer registered successfully"),
			"customer_id": dgii_customer.name
		}
		
	except Exception as e:
		frappe.log_error(f"Error registering DGII customer: {str(e)}", "DGII Customer Registration")
		return {
			"success": False,
			"message": str(e)
		}
