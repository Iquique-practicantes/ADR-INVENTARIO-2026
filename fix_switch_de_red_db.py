"""
Script para arreglar el atributo AUTO_INCREMENT en la tabla adr_switchdered
"""
import pymysql
pymysql.version_info = (2, 2, 2, "final", 0)
pymysql.install_as_MySQLdb()

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.db import connection

def fix_auto_increment():
    with connection.cursor() as cursor:
        # Verificar el estado actual
        cursor.execute("SHOW CREATE TABLE adr_switchdered")
        print("Estado actual de la tabla:")
        print(cursor.fetchone()[1])
        print("\n" + "="*50 + "\n")
        
        # Arreglar PRIMARY KEY y AUTO_INCREMENT
        print("Agregando PRIMARY KEY y AUTO_INCREMENT...")
        cursor.execute("ALTER TABLE adr_switchdered ADD PRIMARY KEY (id)")
        cursor.execute("ALTER TABLE adr_switchdered MODIFY id BIGINT AUTO_INCREMENT")
        
        # Verificar el resultado
        cursor.execute("SHOW CREATE TABLE adr_switchdered")
        print("Estado después de la corrección:")
        print(cursor.fetchone()[1])
        
    print("\n✓ Corrección aplicada exitosamente!")

if __name__ == "__main__":
    fix_auto_increment()
