import frappe
from frappe.model.document import Document
from frappe import _
import requests
import json

class DGIISettings(Document):
	def validate(self):
		self.validate_certificate()
		self.validate_environment()
	
	def validate_certificate(self):
		"""Validar que el certificado sea válido"""
		if not self.certificate_path and not self.certificate_content:
			frappe.throw(_("Debe proporcionar un certificado"))
	
	def validate_environment(self):
		"""Validar configuración del ambiente"""
		if not self.environment:
			self.environment = "test"
	
	def test_connection(self):
		"""Probar conexión con DGII"""
		try:
			# Llamar al servidor Node.js para probar autenticación
			response = requests.post(
				f"{self.dgii_server_url}/api/auth/authenticate",
				json={
					"certificate": self.certificate_content or self.certificate_path,
					"password": self.certificate_password,
					"environment": self.environment
				},
				timeout=30
			)
			
			if response.status_code == 200:
				data = response.json()
				if data.get("success"):
					frappe.msgprint(_("Conexión exitosa con DGII"))
					return True
				else:
					frappe.throw(_(f"Error de autenticación: {data.get('error')}"))
			else:
				frappe.throw(_(f"Error de conexión: {response.status_code}"))
				
		except requests.exceptions.RequestException as e:
			frappe.throw(_(f"Error de conexión: {str(e)}"))
	
	def get_environment_url(self):
		"""Obtener URL del ambiente configurado"""
		environments = {
			"test": "https://ecf.dgii.gov.do/Testecf",
			"cert": "https://ecf.dgii.gov.do/Certecf", 
			"prod": "https://ecf.dgii.gov.do/ecf"
		}
		return environments.get(self.environment, environments["test"])
