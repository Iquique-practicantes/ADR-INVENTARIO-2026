filepath = r'C:\Users\hleri\OneDrive\Escritorio\Inventario ADR 2026\Inventario ADR 2026\adr\views.py'

with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines, 1):
    if 'class EliminadosListView' in line:
        print(f"Found at line {i}: {line.strip()}")
        # Print next 20 lines
        for j in range(i, min(i+20, len(lines))):
            print(f"{j+1}: {lines[j].rstrip()}")
