# Script to add Agregar Activo button to top bar
import re

files = [
    (r'C:\Users\hleri\OneDrive\Escritorio\Inventario ADR 2026\Inventario ADR 2026\templates\modulos\equipos_isla.html', 'add_equipos_isla'),
    (r'C:\Users\hleri\OneDrive\Escritorio\Inventario ADR 2026\Inventario ADR 2026\templates\modulos\switch_de_red.html', 'add_switch_de_red')
]

for filepath, url_name in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Find the line with "Borrar Todo" button closing and add "Agregar Activo" after it
    new_lines = []
    for i, line in enumerate(lines):
        new_lines.append(line)
        
        # Check if this is the line after the Borrar Todo button closes
        if '</form>' in line and i > 0 and 'clearForm' in lines[i-2]:
            # Check if next line is {% endif %}
            if i+1 < len(lines) and '{% endif %}' in lines[i+1]:
                # Add Agregar Activo button before the endif
                button_html = f'''        <a href="{{% url '{url_name}' %}}" class="inline-flex items-center justify-center px-4 h-10 rounded bg-gradient-to-br from-red-600 to-red-900 hover:from-red-500 hover:to-red-700 text-white shadow-sm">
          <i class="fas fa-plus"></i> Agregar Activo
        </a>
'''
                new_lines.append(button_html)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print(f"Updated {filepath.split('/')[-1]}")

print("Done!")
