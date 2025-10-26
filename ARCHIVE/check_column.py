import sqlite3

conn = sqlite3.connect('ipsc_tracker.db')
cursor = conn.cursor()
cursor.execute('PRAGMA table_info(logs)')
columns = [row[1] for row in cursor.fetchall()]
print('linked_thaw_id field exists:', 'linked_thaw_id' in columns)
if 'linked_thaw_id' in columns:
    print('SUCCESS: Column added successfully')
else:
    print('ERROR: Column not found')
conn.close()