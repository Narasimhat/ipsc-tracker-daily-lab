# iPSC Tracker — Copilot Instructions

Purpose: give AI coding assistants the minimal, high-value knowledge to be productive in this repository.

## Core Contract

**Inputs:** edits to Python files (Streamlit UI in `app.py`, DB helpers in `db.py`, optional deployment configs)  
**Outputs:** small, focused code changes, tests or migration updates, and short PR descriptions that reference files changed  
**Error modes:** keep UI backward compatible; do not remove DB columns without adding migration logic in `init_db()`

## Architecture Overview

**Read these files first:**
- `app.py` — single Streamlit UI; tabs implement Add/History/Thaw/Weekend/Dashboard/Settings. Authentication required at top via `from auth import require_authentication`
- `db.py` — SQLite-first data access, schema, helper functions (e.g., `get_conn()`, `init_db()`, `insert_log()`, `get_vial_lifecycle()`)
- `Dockerfile` & `docker-compose.yml` — production runtime: Streamlit on port 8080 with persistent `./data` volume
- `ARCHIVE/.github/copilot-instructions.md` — legacy detailed guidance (this file merges key points)

## Key Conventions & Patterns

**Authentication:** `require_authentication()` must remain invoked before UI code in `app.py`. Don't bypass.

**DB init/migration:** any schema change must be reflected in `db.init_db()`. Add migration steps there:
```python
# Example: adding new column
cur.execute("PRAGMA table_info(logs)")
cols = {row[1] for row in cur.fetchall()}
if "new_column" not in cols:
    cur.execute("ALTER TABLE logs ADD COLUMN new_column TEXT")
```

**Data persistence:** storage controlled by `DATA_ROOT` env var (default: repo dir). DB file is `ipsc_tracker.db`, images in `IMAGES_DIR`.

**Thaw ID format:** use `generate_enhanced_thaw_id(conn, date, operator, cell_type)` — don't invent alternate formats.

**Auto-add references:** UI calls `add_ref_value(conn, kind, name)` when users create new cell lines/events/vessels — preserve this.

**Session state keys:** `st.session_state['form_values']`, `['pending_thaw_id']`, `['my_name']`, `['auto_filled_from_thaw']` are used throughout.

## Code Examples

**Auto-fill from thaw:**
```python
thaw_info = get_thaw_latest_info(conn, thaw_id)
st.session_state.form_values = thaw_info  # Pre-populate form
```

**Insert log entry:**
```python
payload = {
    "date": log_date.isoformat(),
    "cell_line": cell_line_final,
    "event_type": event_type,
    # ... see insert_log() column list in db.py
}
insert_log(conn, payload)
```

## Developer Workflows

**Local development:**
```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

**Docker deployment (recommended for teams):**
```bash
docker-compose up -d --build
# Data persists in ./data, backups in ./backups
```

**Database switching:** Code auto-detects PostgreSQL when `DATABASE_URL` env or `st.secrets['supabase']['connection_string']` present.

## Integration Points

- **GitHub backup:** optional `github_backup.py` auto-restore/backups (silently fails when unavailable)
- **Docker health:** Streamlit path `/_stcore/health` used in container healthchecks
- **Core dependencies:** streamlit, pandas, pillow, openpyxl, psycopg2-binary (see `requirements.txt`)

## Testing & Verification

**Smoke test:** run `streamlit run app.py` → Add Entry → save log → confirm `./data/ipsc_tracker.db` updated  
**Container test:** `docker-compose up --build` then check `docker-compose logs -f` for startup messages  
**DB check:** open `./data/ipsc_tracker.db` with sqlite3 and verify table structure after migrations

## What to Avoid

- Don't change schema without updating `init_db()` migration logic
- Don't bypass `auth.py` wrapper — keep `require_authentication()` in place  
- Don't write files outside `DATA_ROOT` (breaks backups and Docker volumes)

---
*Files referenced: `app.py`, `db.py`, `auth.py`, `Dockerfile`, `docker-compose.yml`, `requirements.txt`*