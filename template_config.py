"""
Script para agregar botones de borrar contenido a los templates de inventario
"""

templates_config = [
    {
        'file': 'proyectores.html',
        'model_name': 'proyector',
        'form_id': 'clearFormProyectores',
        'function_name': 'confirmClearProyectores',
        'mensaje': 'Proyectores'
    },
    {
        'file': '  monitor.html',
        'model_name': 'monitor',
        'form_id': 'clearFormMonitor',
        'function_name': 'confirmClearMonitor',
        'mensaje': 'Monitores'
    },
    {
        'file': 'audio.html',
        'model_name': 'audio',
        'form_id': 'clearFormAudio',
        'function_name': 'confirmClearAudio',
        'mensaje': 'Audio'
    },
    {
        'file': 'tablet.html',
        'model_name': 'tablet',
        'form_id': 'clearFormTablet',
        'function_name': 'confirmClearTablet',
        'mensaje': 'Tablets'
    },
    {
        'file': 'bodega_adr.html',
        'model_name': 'bodegaadr',
        'form_id': 'clearFormBodega',
        'function_name': 'confirmClearBodega',
        'mensaje': 'Bodega ADR'
    },
    {
        'file': 'azotea_adr.html',
        'model_name': 'azotea',
        'form_id': 'clearFormAzotea',
        'function_name': 'confirmClearAzotea',
        'mensaje': 'Azotea'
    },
    {
        'file': 'equipos_isla.html',
        'model_name': 'equiposisla',
        'form_id': 'clearFormEquiposIsla',
        'function_name': 'confirmClearEquiposIsla',
        'mensaje': 'Equipos Isla'
    },
    {
        'file': 'switch_de_red.html',
        'model_name': 'switchdered',
        'form_id': 'clearFormSwitchDeRed',
        'function_name': 'confirmClearSwitchDeRed',
        'mensaje': 'Switch de Red'
    }
]

print("Configuración de templates lista para modificar")
print(f"Total de templates: {len(templates_config)}")
