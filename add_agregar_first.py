"""
Simple script to add Agregar Activo button as FIRST button in all templates
"""
import re

templates = [
    (r'C:\Users\hleri\OneDrive\Escritorio\Inventario ADR 2026\Inventario ADR 2026\templates\modulos\all_in_one.html', 'add_all_in_one', "{% if all_in_ones or page_obj %}"),
    (r'C:\Users\hleri\OneDrive\Escritorio\Inventario ADR 2026\Inventario ADR 2026\templates\modulos\all_in_one_adm.html', 'add_all_in_one_adm', "{% if all_in_ones_adm or page_obj %}"),
    (r'C:\Users\hleri\OneDrive\Escritorio\Inventario ADR 2026\Inventario ADR 2026\templates\modulos\notebooks.html', 'add_notebook', "{% if notebooks or page_obj %}"),
    (r'C:\Users\hleri\OneDrive\Escritorio\Inventario ADR 2026\Inventario ADR 2026\templates\modulos\mini_pc.html', 'add_mini_pc', "{% if minis_pcs or page_obj %}"),
    (r'C:\Users\hleri\OneDrive\Escritorio\Inventario ADR 2026\Inventario ADR 2026\templates\modulos\proyectores.html', 'add_proyector', "{% if proyectores or page_obj %}"),
    (r'C:\Users\hleri\OneDrive\Escritorio\Inventario ADR 2026\Inventario ADR 2026\templates\modulos\monitor.html', 'add_monitor', None),
    (r'C:\Users\hleri\OneDrive\Escritorio\Inventario ADR 2026\Inventario ADR 2026\templates\modulos\audio.html', 'add_audio', None),
    (r'C:\Users\hleri\OneDrive\Escritorio\Inventario ADR 2026\Inventario ADR 2026\templates\modulos\tablet.html', 'add_tablet', None),
    (r'C:\Users\hleri\OneDrive\Escritorio\Inventario ADR 2026\Inventario ADR 2026\templates\modulos\bodega_adr.html', 'add_bodega_adr', None),
    (r'C:\Users\hleri\OneDrive\Escritorio\Inventario ADR 2026\Inventario ADR 2026\templates\modulos\azotea_adr.html', 'add_azotea', None),
]

agregar_button = """        {% if group_name_singular == 'ADR' or group_name_singular == 'Operador ADR' %}
        <a href="{{% url '{url_name}' %}}" class="inline-flex items-center justify-center px-4 h-10 rounded bg-gradient-to-br from-red-600 to-red-900 hover:from-red-500 hover:to-red-700 text-white shadow-sm">
          <i class="fas fa-plus"></i> Agregar Activo
        </a>
        {% endif %}
"""

for filepath, url_name, condition in templates:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if Agregar Activo already exists
        if 'Agregar Activo' in content:
            print(f"SKIP: {filepath.split(chr(92))[-1]} - Already has Agregar Activo")
            continue
        
        # Find the first <a href that contains descargar_excel
        pattern = r'(\s*<a href="{% url \'descargar_excel\')'
        match = re.search(pattern, content)
        
        if match:
            # Insert the Agregar button before the Descargar Excel button
            button = agregar_button.format(url_name=url_name)
            insert_pos = match.start()
            content = content[:insert_pos] + button + content[insert_pos:]
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"OK: {filepath.split(chr(92))[-1]} - Added Agregar Activo button")
        else:
            print(f"SKIP: {filepath.split(chr(92))[-1]} - Pattern not found")
    
    except Exception as e:
        print(f"ERROR: {filepath.split(chr(92))[-1]} - {e}")

print("\nDone!")
