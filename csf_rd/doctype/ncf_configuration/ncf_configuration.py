import frappe
from frappe.model.document import Document
from frappe import _

class NCFConfiguration(Document):
	def validate(self):
		self.validate_sequences()
		self.validate_company()
	
	def validate_sequences(self):
		"""Validar que las secuencias estén configuradas correctamente"""
		if not self.ncf_sequences:
			frappe.throw(_("Debe configurar al menos una secuencia de NCF"))
		
		# Validar que no haya duplicados
		types = [seq.ncf_type for seq in self.ncf_sequences]
		if len(types) != len(set(types)):
			frappe.throw(_("No puede haber tipos de NCF duplicados"))
	
	def validate_company(self):
		"""Validar que solo haya una configuración por empresa"""
		existing = frappe.get_value(
			"NCF Configuration",
			{"company": self.company, "name": ["!=", self.name]},
			"name"
		)
		
		if existing:
			frappe.throw(_(f"Ya existe una configuración de NCF para la empresa {self.company}"))
	
	def get_next_sequence(self, ncf_type):
		"""Obtener siguiente secuencia para un tipo de NCF"""
		for seq in self.ncf_sequences:
			if seq.ncf_type == ncf_type:
				seq.current_sequence += 1
				self.save()
				return seq.current_sequence
		
		frappe.throw(_(f"No se encontró configuración para el tipo de NCF: {ncf_type}"))
	
	def get_ncf_types(self):
		"""Obtener tipos de NCF configurados"""
		return [seq.ncf_type for seq in self.ncf_sequences]
