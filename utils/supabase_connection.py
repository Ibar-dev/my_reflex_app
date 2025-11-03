"""
Utilidad para conectar con Supabase y gestionar la base de datos de vehículos.
Versión optimizada para producción - Lee variables de entorno directamente.
"""
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from typing import List, Dict
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SupabaseConnection:
    """Gestor de conexión a Supabase PostgreSQL"""
    
    def __init__(self):
        # ✅ CAMBIO CRÍTICO: Cargar desde .env solo en desarrollo
        try:
            from dotenv import load_dotenv
            # Solo cargar .env si estamos en desarrollo
            env = os.getenv("RX_ENV", "DEV")
            if env != "PROD":
                load_dotenv()
                logger.info("📁 Cargando variables desde .env (modo desarrollo)")
        except ImportError:
            logger.info("📦 dotenv no disponible (producción)")
        
        # Leer variables de entorno (ahora funcionan en prod y dev)
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.host = os.getenv("DB_HOST")
        self.port = os.getenv("DB_PORT")
        self.dbname = os.getenv("DB_NAME")
        self.connection = None
        self.cursor = None
        
        # ✅ Diagnóstico mejorado
        env_status = {
            "DB_USER": "✅" if self.user else "❌",
            "DB_PASSWORD": "✅" if self.password else "❌",
            "DB_HOST": "✅" if self.host else "❌",
            "DB_PORT": "✅" if self.port else "❌",
            "DB_NAME": "✅" if self.dbname else "❌",
        }
        logger.info(f"[SUPABASE] Variables de entorno: {env_status}")
        
        # Verificar que todas las variables estén configuradas
        missing_vars = [k for k, v in env_status.items() if v == "❌"]
        if missing_vars:
            logger.error(f"[SUPABASE] ❌ Variables faltantes: {missing_vars}")
            print(f"[SUPABASE] ❌ CRÍTICO: Faltan variables: {missing_vars}")
    
    def connect(self):
        """Establece conexión con la base de datos"""
        # Verificar que tenemos todas las credenciales
        if not all([self.user, self.password, self.host, self.port, self.dbname]):
            logger.error("[SUPABASE] ❌ Credenciales incompletas")
            print("[SUPABASE] ❌ ERROR: Credenciales de Supabase no configuradas")
            print("[SUPABASE] Configura las variables de entorno en Reflex Dashboard")
            return False
        
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
            logger.info("[SUPABASE] ✅ Conexión exitosa")
            print("[SUPABASE] ✅ Conectado correctamente")
            return True
        except Exception as e:
            logger.error(f"[SUPABASE] ❌ Error al conectar: {e}")
            print(f"[SUPABASE] ❌ ERROR DE CONEXIÓN: {e}")
            return False
    
    def disconnect(self):
        """Cierra la conexión"""
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
            logger.info("[SUPABASE] 🔌 Conexión cerrada")
        except Exception as e:
            logger.error(f"[SUPABASE] Error al cerrar: {e}")
    
    def execute_query(self, query: str, params: tuple = None) -> List[Dict]:
        """Ejecuta una consulta SELECT y devuelve resultados"""
        try:
            self.cursor.execute(query, params)
            results = self.cursor.fetchall()
            logger.info(f"[SUPABASE] ✅ Query ejecutada: {len(results)} resultados")
            return results
        except Exception as e:
            logger.error(f"[SUPABASE] ❌ Error en consulta: {e}")
            print(f"[SUPABASE] ❌ ERROR EN QUERY: {e}")
            return []
    
    def execute_update(self, query: str, params: tuple = None) -> bool:
        """Ejecuta INSERT, UPDATE o DELETE"""
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
            logger.info("[SUPABASE] ✅ Operación ejecutada")
            return True
        except Exception as e:
            logger.error(f"[SUPABASE] ❌ Error en operación: {e}")
            print(f"[SUPABASE] ❌ ERROR: {e}")
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
        print("❌ Error de conexión. Verifica tus credenciales")
        print("\nEn PRODUCCIÓN, configura las variables en:")
        print("https://console.reflex.run → Settings → Environment Variables")
        return False


if __name__ == "__main__":
    print("🧪 Probando conexión con Supabase...")
    test_connection()