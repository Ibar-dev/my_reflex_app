"""
Estado del formulario de contacto AstroTech - CORREGIDO
======================================================

SOLUCIÓN: Handlers simplificados sin yield para inputs reactivos
"""

import reflex as rx
import re
import asyncio

class ContactState(rx.State):
    """
    Estado que maneja el formulario de contacto - VERSIÓN CORREGIDA
    """
    
    # Campos del formulario
    name: str = ""
    email: str = ""
    phone: str = ""
    message: str = ""
    
    # Estados del formulario
    is_loading: bool = False
    show_success: bool = False

    # Estados de verificación de usuario
    is_registered: bool = False
    user_info: dict = {}

    # Campos de error
    email_error: str = ""
    phone_error: str = ""
    form_error: str = ""
    
    def handle_name_change(self, value: str):
        """Handler corregido para el nombre"""
        print(f"🔄 Cambiando nombre: '{value}'")  # Debug
        self.name = value
        
    def handle_email_change(self, value: str):
        """Handler corregido para el email"""
        print(f"[CONTACT] Cambiando email: '{value}'")  # Debug
        self.email = value
        if value and not self.validate_email(value):
            self.email_error = "Formato de email inválido"
        else:
            self.email_error = ""
            # Verificar si el email está registrado cuando sea válido
            if value and self.validate_email(value):
                self.check_user_registration(value)
        
    def handle_phone_change(self, value: str):
        """Handler corregido para el teléfono"""
        print(f"📱 Cambiando teléfono: '{value}'")  # Debug
        self.phone = value
        if value and not self.validate_phone(value):
            self.phone_error = "Formato de teléfono inválido"
        else:
            self.phone_error = ""
    def handle_message_change(self, value: str):
        """Handler corregido para el mensaje"""
        print(f"💬 Cambiando mensaje: '{value}'")  # Debug
        self.message = value
    
    def check_user_registration(self, email: str):
        """
        Verifica si un email está registrado en la base de datos de usuarios
        """
        try:
            from models.user import UserService

            print(f"[CONTACT] Verificando registro de usuario: {email}")

            # Usar servicio optimizado para consistencia
            result = UserService.find_by_email(email)

            if result["success"] and result["found"]:
                self.is_registered = True
                self.user_info = result["user"]
                print(f"[CONTACT] Usuario registrado encontrado: {result['user']['nombre']}")
            else:
                self.is_registered = False
                self.user_info = {}
                print(f"[CONTACT] Usuario no registrado: {email}")

        except Exception as e:
            print(f"[CONTACT] Error verificando registro de usuario: {e}")
            self.is_registered = False
            self.user_info = {}

    async def submit_form(self):
        """Procesar el envío del formulario - INTEGRADO CON EMAIL Y VERIFICACIÓN"""
        print("🚀 Enviando formulario...")  # Debug

        # Limpiar errores anteriores
        self.form_error = ""
        self.email_error = ""
        self.phone_error = ""

        # Validar campos requeridos
        if not self.name.strip():
            self.form_error = "El nombre es obligatorio"
            return

        if not self.email.strip():
            self.form_error = "El email es obligatorio"
            return

        if not self.message.strip():
            self.form_error = "El mensaje es obligatorio"
            return

        # Validar formato de email
        if not self.validate_email(self.email):
            self.email_error = "Formato de email inválido"
            return

        # Validar teléfono si se proporciona
        if self.phone and not self.validate_phone(self.phone):
            self.phone_error = "Formato de teléfono inválido"
            return

        # Verificar registro de usuario (última verificación antes de enviar)
        self.check_user_registration(self.email)

        # Activar estado de carga
        self.is_loading = True

        try:
            # ENVIAR EMAIL REAL CON INFORMACIÓN DE REGISTRO
            from utils.email_service import send_contact_form_email

            print(f"[CONTACT] Enviando email a Astrotechreprogramaciones@gmail.com...")
            print(f"[CONTACT] Usuario registrado: {self.is_registered}")

            email_result = await send_contact_form_email(
                name=self.name,
                email=self.email,
                phone=self.phone,
                message=self.message,
                is_registered=self.is_registered,
                user_info=self.user_info
            )

            if email_result["success"]:
                print(f"[CONTACT] Email enviado correctamente: {email_result['message']}")

                # Mostrar éxito
                self.show_success = True
                self.is_loading = False

                # Limpiar formulario
                self.reset_form()

                # Ocultar mensaje de éxito después de 5 segundos
                await asyncio.sleep(5)
                self.show_success = False
            else:
                # Error en el envío del email
                print(f"[CONTACT] Error enviando email: {email_result['message']}")
                self.form_error = f"Error al enviar: {email_result['message']}"
                self.is_loading = False

        except Exception as e:
            # Manejo de errores generales
            self.is_loading = False
            self.form_error = f"Error al enviar: {str(e)}"
            print(f"[CONTACT] Error en submit_form: {e}")
    
    def reset_form(self):
        """Reiniciar el formulario a su estado inicial"""
        self.name = ""
        self.email = ""
        self.phone = ""
        self.message = ""
        self.email_error = ""
        self.phone_error = ""
        self.form_error = ""
        # Resetear estados de verificación
        self.is_registered = False
        self.user_info = {}
    
    def validate_email(self, email: str) -> bool:
        """Validar formato de email"""
        if not email:
            return False
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_pattern, email) is not None
    
    def validate_phone(self, phone: str) -> bool:
        """Validar formato de teléfono"""
        if not phone:
            return True  # Teléfono es opcional
        
        # Limpiar el teléfono de espacios y caracteres especiales
        clean_phone = re.sub(r'[\s\-\(\)]', '', phone)
        
        # Patrones para teléfonos españoles
        patterns = [
            r'^(\+34|0034)[6789]\d{8}$',  # Móviles españoles con prefijo
            r'^[6789]\d{8}$',             # Móviles españoles sin prefijo
            r'^(\+34|0034)9\d{8}$',       # Fijos españoles con prefijo
            r'^9\d{8}$',                  # Fijos españoles sin prefijo
        ]
        
        return any(re.match(pattern, clean_phone) for pattern in patterns)