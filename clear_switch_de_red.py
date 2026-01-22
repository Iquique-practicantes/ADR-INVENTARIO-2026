"""
Script para eliminar todos los registros de Switch de Red
"""
import pymysql
pymysql.version_info = (2, 2, 2, "final", 0)
pymysql.install_as_MySQLdb()

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from adr.models import SwitchDeRed

count = SwitchDeRed.objects.count()
print(f"Registros actuales en Switch de Red: {count}")

if count > 0:
    SwitchDeRed.objects.all().delete()
    print(f"Se eliminaron {count} registros.")
else:
    print("No hay registros para eliminar.")

print("Listo! La tabla Switch de Red esta vacia.")
