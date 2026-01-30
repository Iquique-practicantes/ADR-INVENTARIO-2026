"""
Script para corregir el error de comillas escapadas en los includes de paginación
"""
import os
import re

TEMPLATES_DIR = r'c:\Users\hleri\OneDrive\Escritorio\Inventario ADR 2026\Inventario ADR 2026\templates\modulos'

TEMPLATES = [
    'all_in_one.html',
    'all_in_one_adm.html',
    'notebooks.html',
    'mini_pc.html',
    'proyectores.html',
    'monitor.html',
    'audio.html',
    'tablet.html',
    'bodega_adr.html',
    'azotea_adr.html',
    'equipos_isla.html',
]

def fix_pagination_include(filepath):
    """Corrige las comillas escapadas en el include de paginación"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Reemplazar {% include \'partials/pagination.html\' %} con la versión correcta
    content = content.replace(
        "{% include \\'partials/pagination.html\\' %}",
        '{% include "partials/pagination.html" %}'
    )
    
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"[FIXED] {os.path.basename(filepath)}")
        return True
    else:
        print(f"[SKIP] {os.path.basename(filepath)} - No errors found")
        return False

def main():
    fixed_count = 0
    
    for template in TEMPLATES:
        filepath = os.path.join(TEMPLATES_DIR, template)
        if os.path.exists(filepath):
            if fix_pagination_include(filepath):
                fixed_count += 1
        else:
            print(f"[ERROR] Not found: {template}")
    
    print(f"\n[SUCCESS] Fixed {fixed_count}/{len(TEMPLATES)} templates")

if __name__ == '__main__':
    main()
