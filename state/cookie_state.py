import reflex as rx

class CookieState(rx.State):
	cookies_accepted: bool = rx.Cookie(name="cookies_accepted", path="/", default=False)
	show_settings: bool = False
	
	# Tipos específicos de cookies
	essential_cookies: bool = True  # Siempre true, no se puede desactivar
	analytics_cookies: bool = rx.Cookie(name="analytics_cookies", path="/", default=False) 
	marketing_cookies: bool = rx.Cookie(name="marketing_cookies", path="/", default=False)

	def accept_all(self):
		"""Acepta todas las cookies"""
		self.cookies_accepted = True
		self.analytics_cookies = True
		self.marketing_cookies = True
		self.show_settings = False

	def reject_all(self):
		"""Rechaza cookies no esenciales"""
		self.cookies_accepted = True  # Marca como procesado
		self.analytics_cookies = False
		self.marketing_cookies = False
		self.show_settings = False

	def accept_essential_only(self):
		"""Acepta solo cookies esenciales"""
		self.cookies_accepted = True
		self.analytics_cookies = False
		self.marketing_cookies = False
		self.show_settings = False

	def open_config(self):
		"""Abre el modal de configuración"""
		self.show_settings = True
	
	def set_show_settings(self, value: bool):
		"""Controla la visibilidad del modal"""
		self.show_settings = value
		
	def save_custom_settings(self):
		"""Guarda configuración personalizada del modal"""
		self.cookies_accepted = True
		self.show_settings = False
		# analytics_cookies y marketing_cookies se actualizan automáticamente
		# desde los checkboxes del modal
		
	def toggle_analytics(self, value: bool):
		"""Activa/desactiva cookies de análisis"""
		self.analytics_cookies = value
		
	def toggle_marketing(self, value: bool):
		"""Activa/desactiva cookies de marketing"""
		self.marketing_cookies = value