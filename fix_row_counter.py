# Script para corregir la columna # en todos los templates
import os

TEMPLATES_DIR = r'c:\Users\hleri\OneDrive\Escritorio\Inventario ADR 2026\Inventario ADR 2026\templates\modulos'

# Patron incorrecto (que no funciona) y correcto
OLD_PATTERN = '{{ forloop.counter|add:page_obj.start_index|add:"-1" }}'
NEW_PATTERN = '{{ forloop.counter }}'

# Tambien corregir el patron con saltos de linea
OLD_PATTERN_MULTILINE = '''{{
              forloop.counter|add:page_obj.start_index|add:"-1" }}'''

templates = [
    'switch_de_red.html',
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

for template in templates:
    filepath = os.path.join(TEMPLATES_DIR, template)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        # Reemplazar patron normal
        content = content.replace(OLD_PATTERN, NEW_PATTERN)
        # Reemplazar patron con salto de linea
        content = content.replace(OLD_PATTERN_MULTILINE, NEW_PATTERN)
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'[FIXED] {template}')
        else:
            print(f'[SKIP] {template}')
    else:
        print(f'[NOT FOUND] {template}')

print('\nDone!')
