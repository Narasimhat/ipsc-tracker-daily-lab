import db

conn = db.get_conn()
try:
    cell_lines = db.get_ref_values(conn, 'cell_line')
    event_types = db.get_ref_values(conn, 'event_type')
    thaw_options_all = db.get_active_thaw_options(conn, '')
    thaw_options_filtered = db.get_active_thaw_options(conn, cell_lines[0] if cell_lines else '')

    print('Cell lines:', cell_lines)
    print('Event types:', event_types)
    print('All thaw options count:', len(thaw_options_all))
    for t in thaw_options_all:
        print('-', t['thaw_id'], t['cell_line'], t['status'], t['days_since_thaw'])
    print('\nFiltered thaw options count:', len(thaw_options_filtered))
    for t in thaw_options_filtered:
        print('-', t['thaw_id'], t['cell_line'], t['status'], t['days_since_thaw'])

finally:
    conn.close()