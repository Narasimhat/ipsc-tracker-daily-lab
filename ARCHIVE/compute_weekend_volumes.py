#!/usr/bin/env python3
"""
Compute weekend media volumes from the project's SQLite DB.
Sums volumes per cell_line for upcoming Saturday and Sunday (or specific dates if provided via env).
Outputs results to stdout and writes weekend_media_volumes.txt.
"""
import os
import sqlite3
from datetime import date, timedelta

# Helper to find a .db file in workspace
def find_db_file():
    candidates = []
    for root, dirs, files in os.walk('.'):
        for f in files:
            if f.endswith('.db') or f.endswith('.sqlite'):
                candidates.append(os.path.join(root, f))
    # prefer ipsc_tracker.db if present
    for c in candidates:
        if os.path.basename(c) == 'ipsc_tracker.db':
            return c
    return candidates[0] if candidates else None

# Next weekend (Saturday and Sunday)
def next_weekend_dates(today=None):
    today = today or date.today()
    # day of week: Monday=0 ... Sunday=6
    days_ahead = (5 - today.weekday()) % 7
    saturday = today + timedelta(days=days_ahead)
    sunday = saturday + timedelta(days=1)
    return saturday, sunday


def aggregate_volumes(db_path, saturday, sunday):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Attempt to find a date column name; common names: date, log_date, created_at
    # Also check for volume and cell_line columns
    # We'll query pragma_table_info to check columns of logs table
    table_name = None
    # try common table name 'logs'
    cand_tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
    if 'logs' in cand_tables:
        table_name = 'logs'
    else:
        # fallback: first table
        table_name = cand_tables[0] if cand_tables else None

    if not table_name:
        raise RuntimeError('No tables found in DB')

    cols = [r['name'] for r in cur.execute(f"PRAGMA table_info({table_name})").fetchall()]
    # find date col
    date_col = None
    for c in ['date', 'log_date', 'created_at', 'entry_date', 'timestamp']:
        if c in cols:
            date_col = c
            break
    if not date_col:
        # try columns with 'date' in name
        for c in cols:
            if 'date' in c:
                date_col = c
                break
    if not date_col:
        raise RuntimeError('No date column found in logs table; columns: ' + ','.join(cols))

    if 'volume' not in cols:
        raise RuntimeError('No volume column found in logs table; columns: ' + ','.join(cols))
    if 'cell_line' not in cols and 'cell_line_id' not in cols and 'cell_line_name' not in cols:
        raise RuntimeError('No cell_line-like column found in logs table; columns: ' + ','.join(cols))

    # determine exact cell_line column
    cell_col = 'cell_line' if 'cell_line' in cols else ('cell_line_id' if 'cell_line_id' in cols else 'cell_line_name')

    def iso(d):
        return d.strftime('%Y-%m-%d')

    results = {iso(saturday):{}, iso(sunday):{}}

    for day in [saturday, sunday]:
        day_iso = iso(day)
        # Try to find rows where date matches day (compare date part)
        q = f"SELECT {cell_col} as cell_line, SUM(volume) as total_volume FROM {table_name} WHERE DATE({date_col}) = ? GROUP BY {cell_col}"
        try:
            rows = cur.execute(q, (day_iso,)).fetchall()
        except Exception:
            # fallback: if date_col stored as TEXT in same format
            q = f"SELECT {cell_col} as cell_line, SUM(volume) as total_volume FROM {table_name} WHERE {date_col} = ? GROUP BY {cell_col}"
            rows = cur.execute(q, (day_iso,)).fetchall()
        for r in rows:
            cell = r['cell_line'] if r['cell_line'] else 'UNSPECIFIED'
            vol = r['total_volume'] if r['total_volume'] else 0
            results[day_iso][cell] = vol

    conn.close()
    return results


def format_results(results):
    lines = []
    for day in sorted(results.keys()):
        lines.append(f"{day}:")
        if results[day]:
            for cell, vol in sorted(results[day].items()):
                lines.append(f"  {cell}: {vol} mL")
        else:
            lines.append("  (no media entries found)")
        lines.append("")
    return '\n'.join(lines)


def main():
    db = find_db_file()
    if not db:
        print('No SQLite DB file found in workspace. Place your .db in the project root or update script.')
        return
    sat, sun = next_weekend_dates()
    results = aggregate_volumes(db, sat, sun)
    out = format_results(results)
    print('Weekend media volume summary (automatically detected DB: ' + db + ')\n')
    print(out)
    with open('weekend_media_volumes.txt', 'w', encoding='utf-8') as f:
        f.write('Weekend media volume summary\n')
        f.write(out)
    print('\nWrote weekend_media_volumes.txt')

if __name__ == '__main__':
    main()
