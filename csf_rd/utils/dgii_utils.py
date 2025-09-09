import frappe
from frappe import _
import requests
import json

def validate_rnc_with_dgii(rnc):
	"""Validar RNC con DGII usando el servidor Node.js"""
	try:
		# Obtener configuración de DGII
		dgii_settings = frappe.get_doc("DGII Settings", {"company": frappe.defaults.get_user_default("Company")})
		
		response = requests.post(
			f"{dgii_settings.dgii_server_url}/api/dgii/validate-rnc",
			json={"rnc": rnc},
			timeout=dgii_settings.timeout or 30
		)
		
		if response.status_code == 200:
			data = response.json()
			return {
				"success": data.get("success", False),
				"error": data.get("error"),
				"data": data.get("data")
			}
		else:
			return {
				"success": False,
				"error": f"HTTP {response.status_code}"
			}
			
	except Exception as e:
		return {
			"success": False,
			"error": str(e)
		}

def validate_ncf_with_dgii(ncf):
	"""Validar NCF con DGII usando el servidor Node.js"""
	try:
		# Obtener configuración de DGII
		dgii_settings = frappe.get_doc("DGII Settings", {"company": frappe.defaults.get_user_default("Company")})
		
		response = requests.post(
			f"{dgii_settings.dgii_server_url}/api/dgii/validate-ncf",
			json={"ncf": ncf},
			timeout=dgii_settings.timeout or 30
		)
		
		if response.status_code == 200:
			data = response.json()
			return {
				"success": data.get("success", False),
				"error": data.get("error"),
				"data": data.get("data")
			}
		else:
			return {
				"success": False,
				"error": f"HTTP {response.status_code}"
			}
			
	except Exception as e:
		return {
			"success": False,
			"error": str(e)
		}

def generate_ecf_qr_code(rnc_emisor, rnc_comprador, encf, monto_total, fecha_emision, fecha_firma, codigo_seguridad, environment="test"):
	"""Generar código QR para eCF"""
	try:
		# Obtener configuración de DGII
		dgii_settings = frappe.get_doc("DGII Settings", {"company": frappe.defaults.get_user_default("Company")})
		
		response = requests.post(
			f"{dgii_settings.dgii_server_url}/api/dgii/generate-qr-ecf",
			json={
				"rncEmisor": rnc_emisor,
				"rncComprador": rnc_comprador,
				"encf": encf,
				"montoTotal": monto_total,
				"fechaEmision": fecha_emision,
				"fechaFirma": fecha_firma,
				"codigoSeguridad": codigo_seguridad,
				"environment": environment
			},
			timeout=dgii_settings.timeout or 30
		)
		
		if response.status_code == 200:
			data = response.json()
			return {
				"success": data.get("success", False),
				"error": data.get("error"),
				"qr_url": data.get("data", {}).get("qrUrl")
			}
		else:
			return {
				"success": False,
				"error": f"HTTP {response.status_code}"
			}
			
	except Exception as e:
		return {
			"success": False,
			"error": str(e)
		}

def format_rnc(rnc):
	"""Formatear RNC con guiones"""
	if not rnc:
		return ""
	
	# Remover guiones existentes
	clean_rnc = rnc.replace('-', '')
	
	# Agregar guiones según el formato
	if len(clean_rnc) == 9:
		return f"{clean_rnc[:3]}-{clean_rnc[3:6]}-{clean_rnc[6:]}"
	elif len(clean_rnc) == 11:
		return f"{clean_rnc[:3]}-{clean_rnc[3:6]}-{clean_rnc[6:9]}-{clean_rnc[9:]}"
	else:
		return clean_rnc

def get_dgii_server_status():
	"""Verificar estado del servidor DGII"""
	try:
		# Obtener configuración de DGII
		dgii_settings = frappe.get_doc("DGII Settings", {"company": frappe.defaults.get_user_default("Company")})
		
		response = requests.get(
			f"{dgii_settings.dgii_server_url}/health",
			timeout=10
		)
		
		if response.status_code == 200:
			data = response.json()
			return {
				"success": True,
				"status": data.get("status"),
				"timestamp": data.get("timestamp"),
				"version": data.get("version")
			}
		else:
			return {
				"success": False,
				"error": f"HTTP {response.status_code}"
			}
			
	except Exception as e:
		return {
			"success": False,
			"error": str(e)
		}
