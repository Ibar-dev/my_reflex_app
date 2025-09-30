#!/usr/bin/env python3
"""
Script de prueba para validar las funciones del formulario de contacto
=====================================================

Verifica que las validaciones funcionen correctamente.
"""

import re

def validate_email(email: str) -> bool:
    """
    Validar formato de email usando regex
    
    Args:
        email: Email a validar
        
    Returns:
        bool: True si el email es válido
    """
    if not email:
        return False
    
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_pattern, email) is not None

def validate_phone(phone: str) -> bool:
    """
    Validar formato de teléfono español
    
    Args:
        phone: Teléfono a validar
        
    Returns:
        bool: True si el teléfono es válido
    """
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

def test_contact_validations():
    """Prueba las validaciones del formulario de contacto"""
    
    print("🧪 Pruebas de validación del formulario de contacto")
    print("=" * 60)
    
    # Prueba validación de email
    print("\n📧 Pruebas de validación de email:")
    emails_test = [
        ("usuario@ejemplo.com", True),
        ("test@gmail.com", True),
        ("correo.invalido", False),
        ("@dominio.com", False),
        ("usuario@", False),
        ("", False)
    ]
    
    all_email_tests_passed = True
    for email, expected in emails_test:
        result = validate_email(email)
        status = "✅" if result == expected else "❌"
        if result != expected:
            all_email_tests_passed = False
        print(f"  {status} '{email}' -> {result} (esperado: {expected})")
    
    # Prueba validación de teléfono
    print("\n📱 Pruebas de validación de teléfono:")
    phones_test = [
        ("+34 612 345 678", True),   # Móvil con prefijo
        ("612345678", True),         # Móvil sin prefijo
        ("91 234 56 78", True),      # Fijo
        ("+34 91 234 56 78", True),  # Fijo con prefijo
        ("123456", False),           # Muy corto
        ("abc123def", False),        # Con letras
        ("", True)                   # Vacío (opcional)
    ]
    
    all_phone_tests_passed = True
    for phone, expected in phones_test:
        result = validate_phone(phone)
        status = "✅" if result == expected else "❌"
        if result != expected:
            all_phone_tests_passed = False
        print(f"  {status} '{phone}' -> {result} (esperado: {expected})")
    
    print("\n🎯 Resumen de pruebas:")
    email_status = "✅ PASARON" if all_email_tests_passed else "❌ FALLARON"
    phone_status = "✅ PASARON" if all_phone_tests_passed else "❌ FALLARON"
    print(f"  Validación de email: {email_status}")
    print(f"  Validación de teléfono: {phone_status}")
    
    if all_email_tests_passed and all_phone_tests_passed:
        print("\n🎉 ¡Todas las validaciones funcionan correctamente!")
        return True
    else:
        print("\n⚠️  Hay problemas con algunas validaciones.")
        return False

if __name__ == "__main__":
    test_contact_validations()