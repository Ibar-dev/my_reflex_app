import reflex as rx

class CookieState(rx.State):
	# Variables de estado simples inicializadas a False
	cookies_accepted: bool = False
	show_settings: bool = False
	
	# Tipos específicos de cookies
	essential_cookies: bool = True  # Siempre true, no se puede desactivar
	analytics_cookies: bool = False
	marketing_cookies: bool = False
	
	# Cookies de persistencia como strings
	cookies_accepted_store: str = rx.Cookie(name="astrotech_cookies_accepted", path="/")
	analytics_store: str = rx.Cookie(name="astrotech_analytics", path="/")
	marketing_store: str = rx.Cookie(name="astrotech_marketing", path="/")
	
	def on_load(self):
		"""Carga las preferencias desde cookies al inicializar"""
		# Solo establecer como aceptado si explícitamente está en "1"
		if self.cookies_accepted_store == "1":
			self.cookies_accepted = True
			self.analytics_cookies = (self.analytics_store == "1")
			self.marketing_cookies = (self.marketing_store == "1")
		else:
			# Primera visita o no hay cookies - mostrar banner
			self.cookies_accepted = False
			self.analytics_cookies = False
			self.marketing_cookies = False
	
	@rx.var
	def should_show_banner(self) -> bool:
		"""Determina si se debe mostrar el banner de cookies"""
		return not self.cookies_accepted

	def accept_all(self):
		"""Acepta todas las cookies"""
		self.cookies_accepted = True
		self.analytics_cookies = True
		self.marketing_cookies = True
		self.show_settings = False
		# Guardar en cookies
		self.cookies_accepted_store = "1"
		self.analytics_store = "1"
		self.marketing_store = "1"

	def reject_all(self):
		"""Rechaza cookies no esenciales"""
		self.cookies_accepted = True  # Marca como procesado
		self.analytics_cookies = False
		self.marketing_cookies = False
		self.show_settings = False
		# Guardar en cookies
		self.cookies_accepted_store = "1"
		self.analytics_store = "0"
		self.marketing_store = "0"

	def accept_essential_only(self):
		"""Acepta solo cookies esenciales"""
		self.cookies_accepted = True
		self.analytics_cookies = False
		self.marketing_cookies = False
		self.show_settings = False
		# Guardar en cookies
		self.cookies_accepted_store = "1"
		self.analytics_store = "0"
		self.marketing_store = "0"

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
		# Guardar en cookies
		self.cookies_accepted_store = "1"
		self.analytics_store = "1" if self.analytics_cookies else "0"
		self.marketing_store = "1" if self.marketing_cookies else "0"
		
	def toggle_analytics(self, value: bool):
		"""Activa/desactiva cookies de análisis"""
		self.analytics_cookies = value
		
	def toggle_marketing(self, value: bool):
		"""Activa/desactiva cookies de marketing"""
		self.marketing_cookies = value