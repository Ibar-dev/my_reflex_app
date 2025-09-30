"""
Estado de contacto simplificado para debugging
"""

import reflex as rx

class SimpleContactState(rx.State):
    """Estado simplificado para probar inputs"""
    
    # Campos básicos
    test_name: str = ""
    test_email: str = ""
    test_message: str = ""
    
    def update_name(self, value: str):
        """Actualizar nombre"""
        self.test_name = value
        print(f"Nombre actualizado: {value}")  # Debug
        
    def update_email(self, value: str):
        """Actualizar email"""
        self.test_email = value
        print(f"Email actualizado: {value}")  # Debug
        
    def update_message(self, value: str):
        """Actualizar mensaje"""
        self.test_message = value
        print(f"Mensaje actualizado: {value}")  # Debug