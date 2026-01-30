#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Fix agregar button in equipos_isla and switch_de_red"""

files = [
    (r'C:\Users\hleri\OneDrive\Escritorio\Inventario ADR 2026\Inventario ADR 2026\templates\modulos\equipos_isla.html', 'add_equipos_isla'),
    (r'C:\Users\hleri\OneDrive\Escritorio\Inventario ADR 2026\Inventario ADR 2026\templates\modulos\switch_de_red.html', 'add_switch_de_red')
]

button_template = """        <a href="{{% url '{url_name}' %}}" class="inline-flex items-center justify-center px-4 h-10 rounded bg-gradient-to-br from-red-600 to-red-900 hover:from-red-500 hover:to-red-700 text-white shadow-sm">
          <i class="fas fa-plus"></i> Agregar Activo
        </a>
"""

for filepath, url_name in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Find the line with </form> after clearForm and add button before {% endif %}
    new_lines = []
    added = False
    
    for i, line in enumerate(lines):
        new_lines.append(line)
        
        # Look for </form> that closes the clearForm
        if '</form>' in line and not added:
            # Check if this is the clearForm
            if i > 0 and ('clearForm' in ''.join(lines[max(0, i-5):i])):
                # Add the button right after </form>, before {% endif %}
                button = button_template.format(url_name=url_name)
                new_lines.append(button)
                added = True
                print(f"Added button to {filepath.split(chr(92))[-1]} after line {i+1}")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

print("\nDone!")
