with open(r'C:\Users\hleri\OneDrive\Escritorio\Inventario ADR 2026\Inventario ADR 2026\templates\modulos\equipos_isla.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the specific pattern
old_pattern = """        </form>
        {% endif %}
      </div>"""

new_pattern = """        </form>
        <a href="{% url 'add_equipos_isla' %}" class="inline-flex items-center justify-center px-4 h-10 rounded bg-gradient-to-br from-red-600 to-red-900 hover:from-red-500 hover:to-red-700 text-white shadow-sm">
          <i class="fas fa-plus"></i> Agregar Activo
        </a>
        {% endif %}
      </div>"""

content = content.replace(old_pattern, new_pattern)

with open(r'C:\Users\hleri\OneDrive\Escritorio\Inventario ADR 2026\Inventario ADR 2026\templates\modulos\equipos_isla.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated equipos_isla.html")

# Now switch_de_red
with open(r'C:\Users\hleri\OneDrive\Escritorio\Inventario ADR 2026\Inventario ADR 2026\templates\modulos\switch_de_red.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_pattern2 = """        </form>
        {% endif %}
      </div>"""

new_pattern2 = """        </form>
        <a href="{% url 'add_switch_de_red' %}" class="inline-flex items-center justify-center px-4 h-10 rounded bg-gradient-to-br from-red-600 to-red-900 hover:from-red-500 hover:to-red-700 text-white shadow-sm">
          <i class="fas fa-plus"></i> Agregar Activo
        </a>
        {% endif %}
      </div>"""

content = content.replace(old_pattern2, new_pattern2)

with open(r'C:\Users\hleri\OneDrive\Escritorio\Inventario ADR 2026\Inventario ADR 2026\templates\modulos\switch_de_red.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated switch_de_red.html")
print("Done!")
