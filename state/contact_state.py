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
    
    def handle_name_change(self, value: str):
        """Handler corregido para el nombre"""
        print(f"🔄 Cambiando nombre: '{value}'")  # Debug
        self.name = value
        
    def handle_email_change(self, value: str):
        """Handler corregido para el email"""
        print(f"📧 Cambiando email: '{value}'")  # Debug
        self.email = value
        if value and not self.validate_email(value):
            self.email_error = "Formato de email inválido"
        else:
            self.email_error = ""
        
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
    
    async def submit_form(self):
        """Procesar el envío del formulario - Listo para backend"""
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
        
        # Activar estado de carga
        self.is_loading = True
        
        try:
            # TODO: INTEGRAR ENDPOINT DEL BACKEND AQUÍ
            # Ejemplo:
            # response = await send_contact_email({
            #     "name": self.name,
            #     "email": self.email,
            #     "phone": self.phone,
            #     "message": self.message
            # })
            
            # Por ahora, simulamos un delay de red
            import asyncio
            await asyncio.sleep(1.5)
            
            # Log de datos listos para backend
            print(f"✅ Formulario válido")
            print(f"📧 Datos listos para enviar al backend:")
            print(f"   - Nombre: {self.name}")
            print(f"   - Email: {self.email}")
            print(f"   - Teléfono: {self.phone or 'No proporcionado'}")
            print(f"   - Mensaje: {self.message[:50]}...")
            
            # Mostrar éxito
            self.show_success = True
            self.is_loading = False
            
            # Limpiar formulario
            self.reset_form()
            
            # Ocultar mensaje de éxito después de 5 segundos
            await asyncio.sleep(5)
            self.show_success = False
        except Exception as e:
            # Manejo de errores
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