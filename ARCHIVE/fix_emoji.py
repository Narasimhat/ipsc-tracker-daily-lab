#!/usr/bin/env python3

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the malformed emoji in the success message
lines = content.split('\n')
for i, line in enumerate(lines):
    if 'st.success(f"� {prev.get' in line:
        lines[i] = line.replace('�', '🔗')
        break

content = '\n'.join(lines)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Fixed malformed emoji in linked thaw display')