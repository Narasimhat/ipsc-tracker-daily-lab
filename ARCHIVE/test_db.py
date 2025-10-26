import db

try:
    conn = db.get_conn()
    print("Database connection: OK")
    
    cell_lines = db.get_ref_values(conn, 'cell_line')
    print(f"Cell lines count: {len(cell_lines) if cell_lines else 0}")
    print(f"Cell lines: {cell_lines}")
    
    event_types = db.get_ref_values(conn, 'event_type')
    print(f"Event types count: {len(event_types) if event_types else 0}")
    print(f"Event types: {event_types}")
    
    # Test thaw options
    thaw_options = db.get_active_thaw_options(conn, "")
    print(f"Thaw options count: {len(thaw_options) if thaw_options else 0}")
    
    conn.close()
    print("All database functions working!")
    
except Exception as e:
    print(f"Database error: {e}")
    import traceback
    traceback.print_exc()