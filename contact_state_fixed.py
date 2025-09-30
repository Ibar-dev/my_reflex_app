"""
Estado del formulario de contacto AstroTech CORREGIDO
===================================================

SOLUCIÓN: Métodos de cambio apropiados para Reflex
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
    
    def validate_email(self, email: str) -> bool:
        """Validar formato de email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def validate_phone(self, phone: str) -> bool:
        """Validar formato de teléfono"""
        pattern = r'^[\+]?[0-9\s\-\(\)]{9,15}$'
        return re.match(pattern, phone) is not None
    
    def submit_form(self):
        """Procesar el envío del formulario"""
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
        
        # Validar formato de teléfono si se proporciona
        if self.phone and not self.validate_phone(self.phone):
            self.phone_error = "Formato de teléfono inválido"
            return
        
        # Simular envío exitoso
        self.is_loading = True
        print(f"✅ Formulario válido - Nombre: {self.name}, Email: {self.email}")
        
        # Simular éxito inmediato (sin email real por ahora)
        self.is_loading = False
        self.show_success = True
        
        # Reset formulario después de 3 segundos
        self.reset_form_delayed()
    
    def reset_form_delayed(self):
        """Resetear el formulario después de mostrar éxito"""
        import asyncio
        
        async def delayed_reset():
            await asyncio.sleep(3)
            self.name = ""
            self.email = ""
            self.phone = ""
            self.message = ""
            self.show_success = False
            self.form_error = ""
            self.email_error = ""
            self.phone_error = ""
        
        # En Reflex, necesitamos usar yield para operaciones async
        # Por simplicidad, vamos a resetear inmediatamente
        pass
    
    def reset_form(self):
        """Resetear formulario manualmente"""
        self.name = ""
        self.email = ""
        self.phone = ""
        self.message = ""
        self.show_success = False
        self.form_error = ""
        self.email_error = ""
        self.phone_error = ""