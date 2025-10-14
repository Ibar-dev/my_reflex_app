import reflex as rx

class CookieState(rx.State):
	cookies_accepted: bool = rx.Cookie(name="cookies_accepted", path="/")
	show_settings: bool = False

	def accept_all(self):
		self.cookies_accepted = True
		self.show_settings = False

	def reject_all(self):
		self.cookies_accepted = False
		self.show_settings = False
		# Si quieres borrar la cookie al rechazar, también puedes hacer rx.remove_cookies("cookies_accepted")[1]

	def open_config(self):
		self.show_settings = True
	
	def set_show_settings(self, value: bool):
		self.show_settings = value