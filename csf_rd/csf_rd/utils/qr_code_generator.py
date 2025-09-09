import frappe
from frappe import _
import qrcode
import io
import base64

def generate_ecf_qr_code(rnc_emisor, rnc_comprador, encf, monto_total, fecha_emision, fecha_firma, codigo_seguridad, environment="test"):
	"""Generar código QR para eCF usando la librería qrcode"""
	try:
		# Importar función de DGII utils
		from csf_rd.csf_rd.utils.dgii_utils import generate_ecf_qr_code as dgii_generate_qr
		
		# Usar el servidor Node.js para generar la URL del QR
		result = dgii_generate_qr(
			rnc_emisor, rnc_comprador, encf, monto_total, 
			fecha_emision, fecha_firma, codigo_seguridad, environment
		)
		
		if result.get("success") and result.get("qr_url"):
			# Generar imagen QR localmente
			qr = qrcode.QRCode(
				version=1,
				error_correction=qrcode.constants.ERROR_CORRECT_L,
				box_size=10,
				border=4,
			)
			qr.add_data(result["qr_url"])
			qr.make(fit=True)
			
			# Crear imagen
			img = qr.make_image(fill_color="black", back_color="white")
			
			# Convertir a base64
			buffer = io.BytesIO()
			img.save(buffer, format='PNG')
			img_str = base64.b64encode(buffer.getvalue()).decode()
			
			return {
				"success": True,
				"qr_url": result["qr_url"],
				"qr_image": f"data:image/png;base64,{img_str}"
			}
		else:
			return result
			
	except Exception as e:
		return {
			"success": False,
			"error": str(e)
		}

def generate_fc_qr_code(rnc_emisor, encf, monto_total, codigo_seguridad, environment="test"):
	"""Generar código QR para Factura de Consumo"""
	try:
		# Importar función de DGII utils
		from csf_rd.csf_rd.utils.dgii_utils import generate_fc_qr_code as dgii_generate_fc_qr
		
		# Usar el servidor Node.js para generar la URL del QR
		result = dgii_generate_fc_qr(
			rnc_emisor, encf, monto_total, codigo_seguridad, environment
		)
		
		if result.get("success") and result.get("qr_url"):
			# Generar imagen QR localmente
			qr = qrcode.QRCode(
				version=1,
				error_correction=qrcode.constants.ERROR_CORRECT_L,
				box_size=10,
				border=4,
			)
			qr.add_data(result["qr_url"])
			qr.make(fit=True)
			
			# Crear imagen
			img = qr.make_image(fill_color="black", back_color="white")
			
			# Convertir a base64
			buffer = io.BytesIO()
			img.save(buffer, format='PNG')
			img_str = base64.b64encode(buffer.getvalue()).decode()
			
			return {
				"success": True,
				"qr_url": result["qr_url"],
				"qr_image": f"data:image/png;base64,{img_str}"
			}
		else:
			return result
			
	except Exception as e:
		return {
			"success": False,
			"error": str(e)
		}
