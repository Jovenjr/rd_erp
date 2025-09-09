import frappe
from frappe import _
from frappe.utils import flt, getdate, formatdate
from frappe.model.document import Document

def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	return columns, data

def get_columns():
	return [
		{
			"fieldname": "ncf",
			"label": _("NCF"),
			"fieldtype": "Data",
			"width": 120
		},
		{
			"fieldname": "rnc_comprador",
			"label": _("RNC Comprador"),
			"fieldtype": "Data",
			"width": 120
		},
		{
			"fieldname": "customer_name",
			"label": _("Cliente"),
			"fieldtype": "Data",
			"width": 200
		},
		{
			"fieldname": "fecha_emision",
			"label": _("Fecha Emisión"),
			"fieldtype": "Date",
			"width": 100
		},
		{
			"fieldname": "subtotal",
			"label": _("Subtotal"),
			"fieldtype": "Currency",
			"width": 120
		},
		{
			"fieldname": "itbis",
			"label": _("ITBIS"),
			"fieldtype": "Currency",
			"width": 120
		},
		{
			"fieldname": "total",
			"label": _("Total"),
			"fieldtype": "Currency",
			"width": 120
		},
		{
			"fieldname": "status",
			"label": _("Estado DGII"),
			"fieldtype": "Data",
			"width": 100
		}
	]

def get_data(filters):
	conditions = get_conditions(filters)
	
	query = """
		SELECT 
			ecf.ncf,
			ecf.rnc_comprador,
			ecf.customer_name,
			ecf.fecha_emision,
			si.net_total as subtotal,
			si.total_taxes_and_charges as itbis,
			si.grand_total as total,
			ecf.status
		FROM `tabeCF Document` ecf
		INNER JOIN `tabSales Invoice` si ON ecf.sales_invoice = si.name
		WHERE ecf.docstatus != 2
		{conditions}
		ORDER BY ecf.fecha_emision DESC
	""".format(conditions=conditions)
	
	data = frappe.db.sql(query, filters, as_dict=1)
	
	# Agregar totales
	totals = get_totals(data)
	data.extend(totals)
	
	return data

def get_conditions(filters):
	conditions = ""
	
	if filters.get("company"):
		conditions += " AND ecf.company = %(company)s"
	
	if filters.get("from_date"):
		conditions += " AND ecf.fecha_emision >= %(from_date)s"
	
	if filters.get("to_date"):
		conditions += " AND ecf.fecha_emision <= %(to_date)s"
	
	if filters.get("status"):
		conditions += " AND ecf.status = %(status)s"
	
	return conditions

def get_totals(data):
	"""Calcular totales del reporte"""
	subtotal = sum(flt(row.subtotal) for row in data if row.subtotal)
	itbis = sum(flt(row.itbis) for row in data if row.itbis)
	total = sum(flt(row.total) for row in data if row.total)
	
	totals = [
		{
			"ncf": "",
			"rnc_comprador": "",
			"customer_name": "<b>TOTAL</b>",
			"fecha_emision": "",
			"subtotal": subtotal,
			"itbis": itbis,
			"total": total,
			"status": ""
		}
	]
	
	return totals
