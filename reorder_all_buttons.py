#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script to add and reorder buttons in all inventory templates
Order: Agregar Activo - Descargar Excel - Subir Excel - Borrar Todo
"""

templates = [
    {
        'file': r'C:\Users\hleri\OneDrive\Escritorio\Inventario ADR 2026\Inventario ADR 2026\templates\modulos\all_in_one.html',
        'model_name': 'allinone',
        'add_url': 'add_all_in_one',
        'upload_url': 'upload_excel_all_in_one',
        'clear_form_id': 'clearFormAllInOne',
        'clear_function': 'confirmClearAllInOne'
    },
    {
        'file': r'C:\Users\hleri\OneDrive\Escritorio\Inventario ADR 2026\Inventario ADR 2026\templates\modulos\all_in_one_adm.html',
        'model_name': 'allinoneadmin',
        'add_url': 'add_all_in_one_adm',
        'upload_url': 'upload_excel_all_in_one_adm',
        'clear_form_id': 'clearFormAllInOneAdm',
        'clear_function': 'confirmClearAllInOneAdm'
    },
    {
        'file': r'C:\Users\hleri\OneDrive\Escritorio\Inventario ADR 2026\Inventario ADR 2026\templates\modulos\notebooks.html',
        'model_name': 'notebook',
        'add_url': 'add_notebook',
        'upload_url': 'upload_excel_notebook',
        'clear_form_id': 'clearFormNotebooks',
        'clear_function': 'confirmClearNotebooks'
    },
    {
        'file': r'C:\Users\hleri\OneDrive\Escritorio\Inventario ADR 2026\Inventario ADR 2026\templates\modulos\mini_pc.html',
        'model_name': 'minipc',
        'add_url': 'add_mini_pc',
        'upload_url': 'upload_excel_minipc',
        'clear_form_id': 'clearFormMiniPC',
        'clear_function': 'confirmClearMiniPC'
    },
    {
        'file': r'C:\Users\hleri\OneDrive\Escritorio\Inventario ADR 2026\Inventario ADR 2026\templates\modulos\proyectores.html',
        'model_name': 'proyector',
        'add_url': 'add_proyector',
        'upload_url': 'upload_excel_proyector',
        'clear_form_id': 'clearFormProyectores',
        'clear_function': 'confirmClearProyectores'
    },
    {
        'file': r'C:\Users\hleri\OneDrive\Escritorio\Inventario ADR 2026\Inventario ADR 2026\templates\modulos\monitor.html',
        'model_name': 'monitor',
        'add_url': 'add_monitor',
        'upload_url': 'upload_excel_monitor',
        'clear_form_id': 'clearFormMonitor',
        'clear_function': 'confirmClearMonitor'
    },
    {
        'file': r'C:\Users\hleri\OneDrive\Escritorio\Inventario ADR 2026\Inventario ADR 2026\templates\modulos\audio.html',
        'model_name': 'audio',
        'add_url': 'add_audio',
        'upload_url': 'upload_excel_audio',
        'clear_form_id': 'clearFormAudio',
        'clear_function': 'confirmClearAudio'
    },
    {
        'file': r'C:\Users\hleri\OneDrive\Escritorio\Inventario ADR 2026\Inventario ADR 2026\templates\modulos\tablet.html',
        'model_name': 'tablet',
        'add_url': 'add_tablet',
        'upload_url': 'upload_excel_tablet',
        'clear_form_id': 'clearFormTablet',
        'clear_function': 'confirmClearTablet'
    },
    {
        'file': r'C:\Users\hleri\OneDrive\Escritorio\Inventario ADR 2026\Inventario ADR 2026\templates\modulos\bodega_adr.html',
        'model_name': 'bodegaadr',
        'add_url': 'add_bodega_adr',
        'upload_url': 'upload_excel_bodega_adr',
        'clear_form_id': 'clearFormBodega',
        'clear_function': 'confirmClearBodega'
    },
    {
        'file': r'C:\Users\hleri\OneDrive\Escritorio\Inventario ADR 2026\Inventario ADR 2026\templates\modulos\azotea_adr.html',
        'model_name': 'azotea',
        'add_url': 'add_azotea',
        'upload_url': 'upload_excel_azotea',
        'clear_form_id': 'clearFormAzotea',
        'clear_function': 'confirmClearAzotea'
    },
    {
        'file': r'C:\Users\hleri\OneDrive\Escritorio\Inventario ADR 2026\Inventario ADR 2026\templates\modulos\equipos_isla.html',
        'model_name': 'equiposisla',
        'add_url': 'add_equipos_isla',
        'upload_url': 'upload_excel_equipos_isla',
        'clear_form_id': 'clearFormEquiposIsla',
        'clear_function': 'confirmClearEquiposIsla'
    },
    {
        'file': r'C:\Users\hleri\OneDrive\Escritorio\Inventario ADR 2026\Inventario ADR 2026\templates\modulos\switch_de_red.html',
        'model_name': 'switchdered',
        'add_url': 'add_switch_de_red',
        'upload_url': 'upload_excel_switch_de_red',
        'clear_form_id': 'clearFormSwitchDeRed',
        'clear_function': 'confirmClearSwitchDeRed'
    }
]

button_template = """      {# BOTONES: AGREGAR / DESCARGAR / SUBIR / BORRAR #}
      {% if notebooks or page_obj or items or True %}
      <div class="flex gap-3 md:ml-6 shrink-0">
        {% if group_name_singular == 'ADR' or group_name_singular == 'Operador ADR' %}
        <a href="{{% url '{add_url}' %}}" class="inline-flex items-center justify-center px-4 h-10 rounded bg-gradient-to-br from-red-600 to-red-900 hover:from-red-500 hover:to-red-700 text-white shadow-sm">
          <i class="fas fa-plus"></i> Agregar Activo
        </a>
        {% endif %}
        <a href="{{% url 'descargar_excel' '{model_name}' %}}" class="inline-flex items-center justify-center px-4 h-10 rounded bg-gradient-to-br from-green-600 to-green-900 hover:from-green-500 hover:to-green-700 text-white shadow-sm">
          Descargar Excel
        </a>
        <a href="{{% url '{upload_url}' %}}" class="inline-flex items-center justify-center px-4 h-10 rounded bg-gradient-to-br from-green-600 to-green-900 hover:from-green-500 hover:to-green-700 text-white shadow-sm">
          Subir Excel
        </a>
        {% if group_name_singular == 'ADR' or group_name_singular == 'Operador ADR' %}
        <form id="{clear_form_id}" method="POST" action="{{% url 'clear_inventory' '{model_name}' %}}" style="display: inline;">
          {{% csrf_token %}}
          <button type="button" onclick="{clear_function}()" 
                  class="inline-flex items-center justify-center px-4 h-10 rounded bg-gradient-to-br from-red-600 to-red-900 hover:from-red-500 hover:to-red-700 text-white shadow-sm">
            <i class="fas fa-trash-alt"></i> Borrar Todo
          </button>
        </form>
        {% endif %}
      </div>
      {% endif %}"""

import re

for template in templates:
    try:
        with open(template['file'], 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Create the new button section
        new_buttons = button_template.format(
            add_url=template['add_url'],
            model_name=template['model_name'],
            upload_url=template['upload_url'],
            clear_form_id=template['clear_form_id'],
            clear_function=template['clear_function']
        )
        
        # Find and replace the existing button section
        # Pattern: from {# BOTONES or {# Derecha until </div> before </form> or </div></div>
        pattern = r'{#.*?BOTONES.*?#}.*?<div class="flex gap-3.*?</div>\s*{% endif %}'
        
        if re.search(pattern, content, re.DOTALL):
            content = re.sub(pattern, new_buttons, content, flags=re.DOTALL)
            
            with open(template['file'], 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"OK: {template['file'].split(chr(92))[-1]}")
        else:
            print(f"SKIP: {template['file'].split(chr(92))[-1]} - Pattern not found")
            
    except Exception as e:
        print(f"ERROR: {template['file'].split(chr(92))[-1]} - {e}")

print("\nDone!")
