"""
Estado del formulario de contacto AstroTech - CORREGIDO
======================================================

SOLUCIÓN: Handlers simplificados sin yield para inputs reactivos
"""

import reflex as rx
import re

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
    
    # Campos de error
    email_error: str = ""
    phone_error: str = ""
    form_error: str = ""
    
    async def handle_name_change(self, value: str):
        """Handler async para el nombre"""
        print(f"🔄 Cambiando nombre: '{value}'")
        self.name = value

    async def handle_email_change(self, value: str):
        """Handler async para el email"""
        print(f"📧 Cambiando email: '{value}'")
        self.email = value
        if value and not self.validate_email(value):
            self.email_error = "Formato de email inválido"
        else:
            self.email_error = ""

    async def handle_phone_change(self, value: str):
        """Handler async para el teléfono"""
        print(f"📱 Cambiando teléfono: '{value}'")
        self.phone = value
        if value and not self.validate_phone(value):
            self.phone_error = "Formato de teléfono inválido"
        else:
            self.phone_error = ""

    async def handle_message_change(self, value: str):
        """Handler async para el mensaje"""
        print(f"💬 Cambiando mensaje: '{value}'")
        self.message = value
    
    # ✅ AÑADIDO: Método para cerrar modal
    def close_modal(self):
        """Cerrar modal de éxito"""
        self.show_success = False
    
    async def submit_form(self):
        """Procesar el envío del formulario - Integrado con email_service"""
        print("🚀 Enviando formulario...")

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

        # Activar estado de carga
        self.is_loading = True

        try:
            from utils.email_service import email_sender
            import asyncio
            import concurrent.futures
            
            # Enviar email (bloqueante, usar run_in_executor)
            loop = asyncio.get_event_loop()
            success = await loop.run_in_executor(
                None,
                lambda: email_sender.send_email(
                    name=self.name,
                    email=self.email,
                    phone=self.phone,
                    message=self.message
                )
            )

            if not success:
                self.form_error = "Error al enviar el email. Intenta de nuevo."
                self.is_loading = False
                return

            print(f"✅ Email enviado correctamente")
            self.show_success = True
            self.is_loading = False
            self.reset_form()
            
            # Cerrar modal automáticamente después de 5 segundos
            await asyncio.sleep(5)
            self.show_success = False
            
        except Exception as e:
            self.is_loading = False
            self.form_error = f"Error al enviar: {str(e)}"
            print(f"❌ Error en submit_form: {e}")
    
    def reset_form(self):
        """Reiniciar el formulario a su estado inicial"""
        self.name = ""
        self.email = ""
        self.phone = ""
        self.message = ""
        self.email_error = ""
        self.phone_error = ""
        self.form_error = ""
    
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