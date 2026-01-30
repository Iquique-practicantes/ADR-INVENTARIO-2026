import os
import django
from django.conf import settings

# Setup Django environment
import pymysql
pymysql.version_info = (2, 2, 2, "final", 0)
pymysql.install_as_MySQLdb()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

try:
    from adr.views import MODELS_DICT
    print("MODELS_DICT found!")
    print("Keys:", list(MODELS_DICT.keys()))
except ImportError:
    print("MODELS_DICT not found in adr.views")
    # Try to find where it might be
    import adr.views
    print("Dir of adr.views:", dir(adr.views))
except Exception as e:
    print(f"Error: {e}")
