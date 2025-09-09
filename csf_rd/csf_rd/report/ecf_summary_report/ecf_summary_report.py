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
			"fieldname": "monto_total",
			"label": _("Monto Total"),
			"fieldtype": "Currency",
			"width": 120
		},
		{
			"fieldname": "status",
			"label": _("Estado"),
			"fieldtype": "Data",
			"width": 100
		},
		{
			"fieldname": "track_id",
			"label": _("Track ID"),
			"fieldtype": "Data",
			"width": 150
		},
		{
			"fieldname": "creation_date",
			"label": _("Fecha Envío"),
			"fieldtype": "Datetime",
			"width": 150
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
			ecf.monto_total,
			ecf.status,
			ecf.track_id,
			ecf.creation_date
		FROM `tabeCF Document` ecf
		WHERE ecf.docstatus != 2
		{conditions}
		ORDER BY ecf.creation_date DESC
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
	
	if filters.get("rnc_comprador"):
		conditions += " AND ecf.rnc_comprador = %(rnc_comprador)s"
	
	return conditions

def get_totals(data):
	"""Calcular totales del reporte"""
	total_amount = sum(flt(row.monto_total) for row in data if row.monto_total)
	
	totals = [
		{
			"ncf": "",
			"rnc_comprador": "",
			"customer_name": "<b>TOTAL</b>",
			"fecha_emision": "",
			"monto_total": total_amount,
			"status": "",
			"track_id": "",
			"creation_date": ""
		}
	]
	
	return totals
