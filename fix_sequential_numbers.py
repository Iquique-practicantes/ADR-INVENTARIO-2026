# Script para corregir la columna # con numeracion sucesiva entre paginas
import os

TEMPLATES_DIR = r'c:\Users\hleri\OneDrive\Escritorio\Inventario ADR 2026\Inventario ADR 2026\templates\modulos'

# Patron actual (solo forloop.counter) - cambiarlo a formula sucesiva
OLD_PATTERN = '{{ forloop.counter }}'
NEW_PATTERN = '{{ forloop.counter0|add:page_obj.start_index }}'

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

fixed_count = 0
for template in templates:
    filepath = os.path.join(TEMPLATES_DIR, template)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Solo reemplazar el primero (el de la columna #, no otros usos de forloop.counter)
        if OLD_PATTERN in content:
            # Buscar el contexto correcto: dentro de la celda de ID
            # Reemplazar solo la primera ocurrencia que esta en la td de #
            new_content = content.replace(
                '<td class="px-1 py-1 text-center text-gray-600 font-mono text-xs">{{ forloop.counter }}</td>',
                '<td class="px-1 py-1 text-center text-gray-600 font-mono text-xs">{{ forloop.counter0|add:page_obj.start_index }}</td>'
            )
            
            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f'[FIXED] {template}')
                fixed_count += 1
            else:
                print(f'[SKIP - pattern not matched] {template}')
        else:
            print(f'[SKIP - no pattern] {template}')
    else:
        print(f'[NOT FOUND] {template}')

print(f'\nDone! Fixed {fixed_count} templates.')
