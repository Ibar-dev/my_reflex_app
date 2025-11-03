"""
Utilidad para conectar con Supabase y gestionar la base de datos de vehículos.
"""
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os
from typing import List, Dict, Optional
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_dotenv()

class SupabaseConnection:
    """Gestor de conexión a Supabase PostgreSQL"""
    
    def __init__(self):
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.host = os.getenv("DB_HOST")
        self.port = os.getenv("DB_PORT")
        self.dbname = os.getenv("DB_NAME")
        self.connection = None
        self.cursor = None
    
    def connect(self):
        """Establece conexión con la base de datos"""
        try:
            self.connection = psycopg2.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                dbname=self.dbname,
                sslmode='require',  # Supabase requiere SSL
                cursor_factory=RealDictCursor  # Devuelve diccionarios
            )
            self.cursor = self.connection.cursor()
            logger.info("✅ Conexión exitosa a Supabase")
            return True
        except Exception as e:
            logger.error(f"❌ Error al conectar con Supabase: {e}")
            return False
    
    def disconnect(self):
        """Cierra la conexión"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        logger.info("🔌 Conexión cerrada")
    
    def execute_query(self, query: str, params: tuple = None) -> List[Dict]:
        """Ejecuta una consulta SELECT y devuelve resultados"""
        try:
            self.cursor.execute(query, params)
            results = self.cursor.fetchall()
            return results
        except Exception as e:
            logger.error(f"❌ Error en consulta: {e}")
            return []
    
    def execute_update(self, query: str, params: tuple = None) -> bool:
        """Ejecuta INSERT, UPDATE o DELETE"""
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
            logger.info("✅ Operación ejecutada correctamente")
            return True
        except Exception as e:
            logger.error(f"❌ Error en operación: {e}")
            self.connection.rollback()
            return False

# Instancia global
db = SupabaseConnection()


def test_connection():
    """Prueba de conexión a Supabase"""
    print("\n" + "=" * 60)
    print("🧪 PROBANDO CONEXIÓN A SUPABASE")
    print("=" * 60)
    
    if db.connect():
        result = db.execute_query("SELECT NOW() as current_time;")
        if result:
            print(f"✅ Conexión exitosa")
            print(f"⏰ Hora actual del servidor: {result[0]['current_time']}")
        db.disconnect()
        return True
    else:
        print("❌ Error de conexión. Verifica tus credenciales en .env")
        return False


if __name__ == "__main__":
    print("🧪 Probando conexión con Supabase...")
    test_connection()
