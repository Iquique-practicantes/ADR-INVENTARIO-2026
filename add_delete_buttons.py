"""
Script para agregar el botón de borrar en los templates restantes
"""
import re

templates_config = [
    {
        'file': r'C:\Users\hleri\OneDrive\Escritorio\Inventario ADR 2026\Inventario ADR 2026\templates\modulos\monitor.html',
        'model_name': 'monitor',
        'form_id': 'clearFormMonitor',
        'function_name': 'confirmClearMonitor',
        'mensaje': 'Monitores',
        'upload_url': 'upload_excel_monitor'
    },
    {
        'file': r'C:\Users\hleri\OneDrive\Escritorio\Inventario ADR 2026\Inventario ADR 2026\templates\modulos\audio.html',
        'model_name': 'audio',
        'form_id': 'clearFormAudio',
        'function_name': 'confirmClearAudio',
        'mensaje': 'Audio',
        'upload_url': 'upload_excel_audio'
    },
    {
        'file': r'C:\Users\hleri\OneDrive\Escritorio\Inventario ADR 2026\Inventario ADR 2026\templates\modulos\tablet.html',
        'model_name': 'tablet',
        'form_id': 'clearFormTablet',
        'function_name': 'confirmClearTablet',
        'mensaje': 'Tablets',
        'upload_url': 'upload_excel_tablet'
    },
    {
        'file': r'C:\Users\hleri\OneDrive\Escritorio\Inventario ADR 2026\Inventario ADR 2026\templates\modulos\bodega_adr.html',
        'model_name': 'bodegaadr',
        'form_id': 'clearFormBodega',
        'function_name': 'confirmClearBodega',
        'mensaje': 'Bodega ADR',
        'upload_url': 'upload_excel_bodega_adr'
    },
    {
        'file': r'C:\Users\hleri\OneDrive\Escritorio\Inventario ADR 2026\Inventario ADR 2026\templates\modulos\azotea_adr.html',
        'model_name': 'azotea',
        'form_id': 'clearFormAzotea',
        'function_name': 'confirmClearAzotea',
        'mensaje': 'Azotea',
        'upload_url': 'upload_excel_azotea'
    },
    {
        'file': r'C:\Users\hleri\OneDrive\Escritorio\Inventario ADR 2026\Inventario ADR 2026\templates\modulos\equipos_isla.html',
        'model_name': 'equiposisla',
        'form_id': 'clearFormEquiposIsla',
        'function_name': 'confirmClearEquiposIsla',
        'mensaje': 'Equipos Isla',
        'upload_url': 'upload_excel_equipos_isla'
    },
    {
        'file': r'C:\Users\hleri\OneDrive\Escritorio\Inventario ADR 2026\Inventario ADR 2026\templates\modulos\switch_de_red.html',
        'model_name': 'switchdered',
        'form_id': 'clearFormSwitchDeRed',
        'function_name': 'confirmClearSwitchDeRed',
        'mensaje': 'Switch de Red',
        'upload_url': 'upload_excel_switch_de_red'
    }
]

for config in templates_config:
    try:
        with open(config['file'], 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Buscar el patrón de "Subir Excel" y agregar el botón después
        button_html = f'''        {{% if group_name_singular == 'ADR' or group_name_singular == 'Operador ADR' %}}
        <form id="{config['form_id']}" method="POST" action="{{% url 'clear_inventory' '{config['model_name']}' %}}" style="display: inline;">
          {{% csrf_token %}}
          <button type="button" onclick="{config['function_name']}()" 
                  class="w-full sm:w-auto text-center bg-gradient-to-br from-red-600 to-red-900 hover:from-red-500 hover:to-red-700 text-white px-4 h-10 leading-10 rounded shadow-sm">
            <i class="fas fa-trash-alt"></i> Borrar Todo
          </button>
        </form>
        {{% endif %}}'''
        
        # Buscar donde está el botón de "Subir Excel" y agregar después
        pattern = rf"'{config['upload_url']}'"
        if pattern in content:
            # Buscar el cierre del tag </a> después del upload_url
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if pattern in line:
                    # Buscar el siguiente </a>
                    for j in range(i, min(i+5, len(lines))):
                        if '</a>' in lines[j]:
                            # Agregar el botón después del </a>
                            lines.insert(j+1, button_html)
                            break
                    break
            
            content = '\n'.join(lines)
        
        # Agregar el script JavaScript al final antes de {% endblock content %}
        js_script = f'''<script>
function {config['function_name']}() {{
    if (confirm('¿Estás seguro de que deseas eliminar TODOS los registros de {config['mensaje']}? Esta acción no se puede deshacer.')) {{
        document.getElementById('{config['form_id']}').submit();
    }}
}}
</script>'''
        
        # Buscar {% endblock content %} y agregar el script antes
        content = content.replace('{%endblock content %}', f'''{js_script}
{{% endblock content %}}''')
        
        with open(config['file'], 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✓ {config['file'].split('\\')[-1]} - Botón agregado")
    except Exception as e:
        print(f"✗ {config['file'].split('\\')[-1]} - Error: {e}")

print("\n¡Proceso completado!")
