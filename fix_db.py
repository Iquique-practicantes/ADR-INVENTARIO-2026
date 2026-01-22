import os
import pymysql
pymysql.version_info = (2, 2, 2, "final", 0)
pymysql.install_as_MySQLdb()

import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

def fix_table():
    with connection.cursor() as cursor:
        try:
            print("Intentando corregir la tabla adr_equiposisla...")
            # MySQL syntax to add AUTO_INCREMENT
            # Necesitamos saber el tipo actual, asumimos bigint(20) ya que inspectdb dijo BigIntegerField.
            cursor.execute("ALTER TABLE adr_equiposisla MODIFY id bigint(20) NOT NULL AUTO_INCREMENT;")
            print("ÉXITO: Se ha añadido AUTO_INCREMENT a adr_equiposisla.id")
        except Exception as e:
            print(f"ERROR: {e}")

if __name__ == '__main__':
    fix_table()
