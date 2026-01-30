#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script to add delete buttons to remaining inventory templates
"""

import os
import re

# Configuration for each template
templates_config = [
    {
        'file': 'monitor.html',
        'model_name': 'monitor',
        'form_id': 'clearFormMonitor',
        'function_name': 'confirmClearMonitor',
        'mensaje': 'Monitores',
        'search_pattern': "upload_excel_monitor"
    },
    {
        'file': 'audio.html',
        'model_name': 'audio',
        'form_id': 'clearFormAudio',
        'function_name': 'confirmClearAudio',
        'mensaje': 'Audio',
        'search_pattern': "upload_excel_audio"
    },
    {
        'file': 'tablet.html',
        'model_name': 'tablet',
        'form_id': 'clearFormTablet',
        'function_name': 'confirmClearTablet',
        'mensaje': 'Tablets',
        'search_pattern': "upload_excel_tablet"
    },
    {
        'file': 'bodega_adr.html',
        'model_name': 'bodegaadr',
        'form_id': 'clearFormBodega',
        'function_name': 'confirmClearBodega',
        'mensaje': 'Bodega ADR',
        'search_pattern': "upload_excel_bodega_adr"
    },
    {
        'file': 'azotea_adr.html',
        'model_name': 'azotea',
        'form_id': 'clearFormAzotea',
        'function_name': 'confirmClearAzotea',
        'mensaje': 'Azotea',
        'search_pattern': "upload_excel_azotea"
    },
    {
        'file': 'equipos_isla.html',
        'model_name': 'equiposisla',
        'form_id': 'clearFormEquiposIsla',
        'function_name': 'confirmClearEquiposIsla',
        'mensaje': 'Equipos Isla',
        'search_pattern': "upload_excel_equipos_isla"
    },
    {
        'file': 'switch_de_red.html',
        'model_name': 'switchdered',
        'form_id': 'clearFormSwitchDeRed',
        'function_name': 'confirmClearSwitchDeRed',
        'mensaje': 'Switch de Red',
        'search_pattern': "upload_excel_switch_de_red"
    }
]

base_path = r'C:\Users\hleri\OneDrive\Escritorio\Inventario ADR 2026\Inventario ADR 2026\templates\modulos'

for config in templates_config:
    file_path = os.path.join(base_path, config['file'])
    
    try:
        # Read the file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if button already exists
        if config['form_id'] in content:
            print(f"SKIP {config['file']}: Button already exists")
            continue
        
        # Create the button HTML
        button_html = f"""        {{% if group_name_singular == 'ADR' or group_name_singular == 'Operador ADR' %}}
        <form id="{config['form_id']}" method="POST" action="{{% url 'clear_inventory' '{config['model_name']}' %}}" style="display: inline;">
          {{% csrf_token %}}
          <button type="button" onclick="{config['function_name']}()" 
                  class="w-full sm:w-auto text-center bg-gradient-to-br from-red-600 to-red-900 hover:from-red-500 hover:to-red-700 text-white px-4 h-10 leading-10 rounded shadow-sm">
            <i class="fas fa-trash-alt"></i> Borrar Todo
          </button>
        </form>
        {{% endif %}}"""
        
        # Find where to insert the button (after "Subir Excel" button)
        pattern = f"'{config['search_pattern']}'"
        if pattern in content:
            # Find the closing </a> tag after the upload button
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if pattern in line:
                    # Look for the next </a>
                    for j in range(i, min(i + 10, len(lines))):
                        if '</a>' in lines[j]:
                            # Insert button after this line
                            lines.insert(j + 1, button_html)
                            break
                    break
            content = '\n'.join(lines)
        
        # Add JavaScript function before {% endblock content %}
        js_script = f"""<script>
function {config['function_name']}() {{
    if (confirm('¿Estás seguro de que deseas eliminar TODOS los registros de {config['mensaje']}? Esta acción no se puede deshacer.')) {{
        document.getElementById('{config['form_id']}').submit();
    }}
}}
</script>"""
        
        # Insert script before {% endblock content %}
        content = content.replace('{% endblock content %}', f"""{js_script}
{{% endblock content %}}""")
        
        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"OK {config['file']}: Button added successfully")
        
    except Exception as e:
        print(f"ERROR {config['file']}: {str(e)}")

print("\nProcess completed!")
