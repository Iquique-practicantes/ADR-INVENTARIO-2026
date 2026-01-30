"""
Script para agregar columna # (ID) y paginación a todos los templates de inventario
"""
import os
import re

# Directorio de templates
TEMPLATES_DIR = r'c:\Users\hleri\OneDrive\Escritorio\Inventario ADR 2026\Inventario ADR 2026\templates\modulos'

# Templates a modificar (excluimos switch_de_red porque ya lo hicimos)
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

def add_id_column_and_pagination(filepath):
    """Agrega columna # y paginación a un template"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # 1. Agregar columna # en el thead
    # Buscar el primer <th> después de <thead>
    thead_pattern = r'(<thead[^>]*>\s*<tr>\s*)(<th\s)'
    if re.search(thead_pattern, content):
        content = re.sub(
            thead_pattern,
            r'\1<th class="px-2 py-3 text-center w-12">#</th>\n            \2',
            content,
            count=1
        )
        print(f"[OK] Agregada columna # en thead de {os.path.basename(filepath)}")
    
    # 2. Agregar celda # en el tbody
    # Buscar el primer <td> después de {% for ... in items %} o similar
    tbody_pattern = r'({% for \w+ in \w+ %}\s*<tr[^>]*>\s*)(<td\s)'
    if re.search(tbody_pattern, content):
        content = re.sub(
            tbody_pattern,
            r'\1<td class="px-1 py-1 text-center text-gray-600 font-mono text-xs">{{ forloop.counter|add:page_obj.start_index|add:"-1" }}</td>\n            \2',
            content,
            count=1
        )
        print(f"[OK] Agregada celda # en tbody de {os.path.basename(filepath)}")
    
    # 3. Incrementar colspan en mensaje de "No hay registros"
    # Buscar el colspan y aumentarlo en 1
    colspan_pattern = r'colspan="(\d+)"'
    def increment_colspan(match):
        current = int(match.group(1))
        return f'colspan="{current + 1}"'
    
    content = re.sub(colspan_pattern, increment_colspan, content)
    
    # 4. Agregar include de paginación antes del cierre de </div> principal
    # Buscar el patrón: {% endwith %}\n</div>\n<script>
    pagination_pattern = r'({% endwith %}\s*)(</div>\s*<script>)'
    if re.search(pagination_pattern, content):
        content = re.sub(
            pagination_pattern,
            r'\1\n  {# Controles de Paginación #}\n  {% include \'partials/pagination.html\' %}\n\2',
            content
        )
        print(f"[OK] Agregada paginacion a {os.path.basename(filepath)}")
    
    # Solo escribir si hubo cambios
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"[DONE] Modificado: {os.path.basename(filepath)}\n")
        return True
    else:
        print(f"[SKIP] Sin cambios en: {os.path.basename(filepath)}\n")
        return False

def main():
    modified_count = 0
    
    for template in TEMPLATES:
        filepath = os.path.join(TEMPLATES_DIR, template)
        if os.path.exists(filepath):
            if add_id_column_and_pagination(filepath):
                modified_count += 1
        else:
            print(f"[ERROR] No encontrado: {template}")
    
    print(f"\n[SUCCESS] Total de templates modificados: {modified_count}/{len(TEMPLATES)}")

if __name__ == '__main__':
    main()
