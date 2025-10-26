import os
import shutil
import sqlite3
from contextlib import closing
from datetime import datetime, date
from typing import Dict, Any, List, Optional, Tuple


# Allow overriding storage root (for server deployments with persistent disks)
DATA_ROOT = os.environ.get("DATA_ROOT", os.path.dirname(__file__))
DB_PATH = os.path.join(DATA_ROOT, "ipsc_tracker.db")
IMAGES_DIR = os.path.join(DATA_ROOT, "images")


def ensure_dirs() -> None:
    os.makedirs(IMAGES_DIR, exist_ok=True)


def get_conn(db_path: Optional[str] = None) -> sqlite3.Connection:
    path = db_path or DB_PATH
    conn = sqlite3.connect(path, detect_types=sqlite3.PARSE_DECLTYPES, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    # Improve reliability for concurrent reads
    try:
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA foreign_keys=ON")
    except Exception:
        pass
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    with closing(conn.cursor()) as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                display_name TEXT,
                created_at TEXT NOT NULL
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                cell_line TEXT,
                event_type TEXT,
                passage INTEGER,
                vessel TEXT,
                location TEXT,
                medium TEXT,
                cell_type TEXT,
                notes TEXT,
                operator TEXT,
                thaw_id TEXT,
                cryo_vial_position TEXT,
                image_path TEXT,
                assigned_to TEXT,
                next_action_date TEXT,
                created_by TEXT NOT NULL,
                created_at TEXT NOT NULL,
                volume REAL,
                experiment_type TEXT,
                experiment_stage TEXT,
                experimental_conditions TEXT,
                protocol_reference TEXT,
                outcome_status TEXT,
                success_metrics TEXT,
                linked_thaw_id TEXT
            )
            """
        )
        
        # Experimental workflows table
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS experimental_workflows (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                workflow_name TEXT UNIQUE NOT NULL,
                description TEXT,
                typical_stages TEXT,
                expected_duration_days INTEGER,
                success_criteria TEXT,
                created_at TEXT NOT NULL
            )
            """
        )
        
        # Reference tables for dropdowns
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS cell_lines (
                name TEXT PRIMARY KEY,
                created_at TEXT NOT NULL
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS event_types (
                name TEXT PRIMARY KEY,
                created_at TEXT NOT NULL
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS vessels (
                name TEXT PRIMARY KEY,
                created_at TEXT NOT NULL
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS locations (
                name TEXT PRIMARY KEY,
                created_at TEXT NOT NULL
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS cell_types (
                name TEXT PRIMARY KEY,
                created_at TEXT NOT NULL
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS culture_media (
                name TEXT PRIMARY KEY,
                created_at TEXT NOT NULL
            )
            """
        )
        
        # New reference tables for experimental workflows
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS experiment_types (
                name TEXT PRIMARY KEY,
                category TEXT,
                description TEXT,
                typical_duration_days INTEGER,
                success_criteria TEXT,
                created_at TEXT NOT NULL
            )
            """
        )
        
        # Weekend planning tables
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS weekend_schedules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                weekend_date TEXT NOT NULL,
                assignee TEXT NOT NULL,
                created_by TEXT NOT NULL,
                created_at TEXT NOT NULL,
                UNIQUE(weekend_date, assignee)
            )
            """
        )
        
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS user_calibers (
                username TEXT PRIMARY KEY,
                caliber_level TEXT NOT NULL,
                updated_by TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
        
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS custom_weekend_work (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                work_type TEXT NOT NULL,
                description TEXT NOT NULL,
                hours REAL NOT NULL,
                assignee TEXT NOT NULL,
                work_date TEXT NOT NULL,
                priority TEXT NOT NULL,
                created_by TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        
        # Migrations: add columns if missing (BEFORE creating indexes)
        cur.execute("PRAGMA table_info(logs)")
        cols = {row[1] for row in cur.fetchall()}
        if "cell_type" not in cols:
            cur.execute("ALTER TABLE logs ADD COLUMN cell_type TEXT")
        if "assigned_to" not in cols:
            cur.execute("ALTER TABLE logs ADD COLUMN assigned_to TEXT")
        if "next_action_date" not in cols:
            cur.execute("ALTER TABLE logs ADD COLUMN next_action_date TEXT")
        if "volume" not in cols:
            cur.execute("ALTER TABLE logs ADD COLUMN volume REAL")
        if "experiment_type" not in cols:
            cur.execute("ALTER TABLE logs ADD COLUMN experiment_type TEXT")
        if "experiment_stage" not in cols:
            cur.execute("ALTER TABLE logs ADD COLUMN experiment_stage TEXT")
        if "experimental_conditions" not in cols:
            cur.execute("ALTER TABLE logs ADD COLUMN experimental_conditions TEXT")
        if "protocol_reference" not in cols:
            cur.execute("ALTER TABLE logs ADD COLUMN protocol_reference TEXT")
        if "outcome_status" not in cols:
            cur.execute("ALTER TABLE logs ADD COLUMN outcome_status TEXT")
        if "success_metrics" not in cols:
            cur.execute("ALTER TABLE logs ADD COLUMN success_metrics TEXT")
        if "linked_thaw_id" not in cols:
            cur.execute("ALTER TABLE logs ADD COLUMN linked_thaw_id TEXT")
        
        # Migrate experiment_types table if needed
        cur.execute("PRAGMA table_info(experiment_types)")
        exp_cols = {row[1] for row in cur.fetchall()}
        if "typical_duration_days" not in exp_cols:
            cur.execute("ALTER TABLE experiment_types ADD COLUMN typical_duration_days INTEGER")
        if "success_criteria" not in exp_cols:
            cur.execute("ALTER TABLE experiment_types ADD COLUMN success_criteria TEXT")
        
        # Create indexes AFTER all columns exist
        cur.execute("CREATE INDEX IF NOT EXISTS idx_logs_thaw_id ON logs (thaw_id)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_logs_linked_thaw_id ON logs (linked_thaw_id)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_logs_created_at ON logs (created_at)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_logs_created_by ON logs (created_by)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_logs_experiment_type ON logs (experiment_type)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_logs_assigned_to ON logs (assigned_to)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_logs_next_action_date ON logs (next_action_date)")
        
        conn.commit()

    # Seed default event types if empty
    with closing(conn.cursor()) as cur:
        cur.execute("SELECT COUNT(*) FROM event_types")
        count = cur.fetchone()[0]
        if count == 0:
            defaults = [
                "Observation",
                "Media Change",
                "Split",
                "Thawing",
                "Cryopreservation",
                "Experimental Treatment",
                "Protocol Start",
                "Protocol Checkpoint",
                "Protocol Completion",
                "Quality Control",
                "Harvest",
                "Analysis",
                "Other",
            ]
            now = datetime.utcnow().isoformat()
            cur.executemany(
                "INSERT OR IGNORE INTO event_types (name, created_at) VALUES (?, ?)",
                [(d, now) for d in defaults],
            )
            conn.commit()

    # Seed default experiment types
    with closing(conn.cursor()) as cur:
        cur.execute("SELECT COUNT(*) FROM experiment_types")
        exp_count = cur.fetchone()[0]
        if exp_count == 0:
            now = datetime.utcnow().isoformat()
            experiment_defaults = [
                ("Genome Editing", "Gene Modification", "CRISPR/Cas9, TALENs, or other genome editing approaches"),
                ("Single Cell Cloning", "Cell Isolation", "Isolation and expansion of individual cell clones"),
                ("Cardiac Differentiation", "Differentiation", "Differentiation of iPSCs into cardiomyocytes"),
                ("Neural Differentiation", "Differentiation", "Differentiation into neural cell types"),
                ("Hepatocyte Differentiation", "Differentiation", "Differentiation into liver cells"),
                ("Organoid Formation", "3D Culture", "Generation of 3D tissue organoids"),
                ("Drug Screening", "Pharmacology", "Compound testing and drug discovery"),
                ("Disease Modeling", "Research", "Modeling disease conditions in vitro"),
                ("Reprogramming", "Cell Conversion", "Converting cells to iPSCs or other cell types"),
                ("Immunotherapy Prep", "Therapeutic", "Preparing cells for immunotherapy applications"),
                ("Transplantation Prep", "Therapeutic", "Preparing cells for transplantation"),
                ("Biomarker Analysis", "Analysis", "Expression analysis and biomarker studies"),
                ("Electrophysiology", "Functional Analysis", "Electrical activity measurements"),
                ("Metabolic Analysis", "Functional Analysis", "Metabolic profiling and analysis"),
                ("Standard Maintenance", "Maintenance", "Regular culture maintenance without specific experimental goals")
            ]
            cur.executemany(
                "INSERT OR IGNORE INTO experiment_types (name, category, description, created_at) VALUES (?, ?, ?, ?)",
                [(name, cat, desc, now) for name, cat, desc in experiment_defaults],
            )
            conn.commit()

    # Seed default experimental workflows
    with closing(conn.cursor()) as cur:
        cur.execute("SELECT COUNT(*) FROM experimental_workflows")
        workflow_count = cur.fetchone()[0]
        if workflow_count == 0:
            now = datetime.utcnow().isoformat()
            workflow_defaults = [
                ("CRISPR Genome Editing", "Complete CRISPR/Cas9 editing workflow", "Transfection,Selection,Screening,Validation,Expansion", 21, "Successful editing confirmed by sequencing"),
                ("Cardiac Differentiation Protocol", "iPSC to cardiomyocyte differentiation", "Mesoderm Induction,Cardiac Specification,Maturation,Characterization", 30, "Beating cardiomyocytes with cardiac markers"),
                ("Single Cell Cloning", "Isolation and expansion of clones", "Single Cell Isolation,Clone Expansion,Screening,Validation", 28, "Stable clonal lines established"),
                ("Neural Differentiation", "iPSC to neural cell differentiation", "Neural Induction,Patterning,Maturation,Analysis", 35, "Neural markers positive, functional activity"),
                ("Organoid Formation", "3D organoid generation", "Aggregation,Differentiation,Maturation,Analysis", 45, "Organized tissue structure with appropriate markers"),
                ("Drug Screening Protocol", "Compound testing workflow", "Cell Preparation,Treatment,Analysis,Validation", 14, "Dose-response curves and statistical significance"),
            ]
            cur.executemany(
                "INSERT OR IGNORE INTO experimental_workflows (workflow_name, description, typical_stages, expected_duration_days, success_criteria, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                [(name, desc, stages, duration, criteria, now) for name, desc, stages, duration, criteria in workflow_defaults],
            )
            conn.commit()

    # Seed default cell types if empty
    with closing(conn.cursor()) as cur:
        cur.execute("SELECT COUNT(*) FROM cell_types")
        ct_count = cur.fetchone()[0]
        if ct_count == 0:
            now = datetime.utcnow().isoformat()
            cell_type_defaults = [
                "iPSC", "NPC", "Cardiomyocyte", "Neuron", "Hepatocyte", 
                "Astrocyte", "Oligodendrocyte", "Endothelial", "Fibroblast",
                "Mesenchymal Stem Cell", "Organoid", "Mixed Population"
            ]
            cur.executemany(
                "INSERT OR IGNORE INTO cell_types (name, created_at) VALUES (?, ?)",
                [(d, now) for d in cell_type_defaults],
            )
            conn.commit()

    # Seed default culture media if empty
    with closing(conn.cursor()) as cur:
        cur.execute("SELECT COUNT(*) FROM culture_media")
        cm_count = cur.fetchone()[0]
        if cm_count == 0:
            now = datetime.utcnow().isoformat()
            media_defaults = [
                "StemFlex", "mTeSR1", "E8", "E6", "RPMI1640", "DMEM", "Neurobasal",
                "Cardiac Differentiation Medium", "Neural Induction Medium", 
                "Organoid Medium", "Maintenance Medium", "Selection Medium"
            ]
            cur.executemany(
                "INSERT OR IGNORE INTO culture_media (name, created_at) VALUES (?, ?)",
                [(d, now) for d in media_defaults],
            )
            conn.commit()


def get_or_create_user(conn: sqlite3.Connection, username: str, display_name: Optional[str] = None) -> Dict[str, Any]:
    username = username.strip()
    if not username:
        raise ValueError("Username required")
    with closing(conn.cursor()) as cur:
        cur.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = cur.fetchone()
        if row:
            return dict(row)
        cur.execute(
            "INSERT INTO users (username, display_name, created_at) VALUES (?, ?, ?)",
            (username, display_name or username, datetime.utcnow().isoformat()),
        )
        conn.commit()
        return {
            "id": cur.lastrowid,
            "username": username,
            "display_name": display_name or username,
            "created_at": datetime.utcnow().isoformat(),
        }


def delete_user(conn: sqlite3.Connection, username: str) -> None:
    username = username.strip()
    if not username:
        return
    with closing(conn.cursor()) as cur:
        cur.execute("DELETE FROM users WHERE username = ?", (username,))
        conn.commit()


def get_all_users(conn: sqlite3.Connection) -> List[str]:
    """Get all usernames from the users table"""
    try:
        with closing(conn.cursor()) as cur:
            cur.execute("SELECT username FROM users ORDER BY username")
            rows = cur.fetchall()
            return [row[0] for row in rows]
    except sqlite3.Error:
        return []


def generate_thaw_id_for_date(conn: sqlite3.Connection, d: date) -> str:
    """Generate simple thaw ID for backward compatibility"""
    day = d.strftime("%Y%m%d")
    with closing(conn.cursor()) as cur:
        cur.execute(
            "SELECT COUNT(*) FROM logs WHERE event_type = 'Thawing' AND date = ?",
            (d.isoformat(),),
        )
        count = cur.fetchone()[0] or 0
    return f"TH-{day}-{count + 1:03d}"


def generate_enhanced_thaw_id(conn: sqlite3.Connection, d: date, operator: str = "", cell_type: str = "") -> str:
    """Generate enhanced thaw ID with operator and cell type information
    
    Format: TH-YYYYMMDD-[OPERATOR_INITIALS]-[CELL_TYPE_ABBREV]-001
    Examples:
    - TH-20251025-JD-iPSC-001  (John Doe, iPSC)
    - TH-20251025-AS-FIBRO-002 (Anna Smith, Fibroblast)
    - TH-20251025-001 (fallback if no operator/cell_type)
    """
    day = d.strftime("%Y%m%d")
    
    # Create operator initials (first letter of each word, max 3 chars)
    operator_code = ""
    if operator:
        parts = operator.strip().split()
        if len(parts) >= 2:
            # First name + Last name initials
            operator_code = (parts[0][0] + parts[-1][0]).upper()
        elif len(parts) == 1:
            # Single name, take first 2 chars
            operator_code = parts[0][:2].upper()
    
    # Create cell type abbreviation
    cell_type_code = ""
    if cell_type:
        cell_type_clean = cell_type.strip().upper()
        if cell_type_clean in ["IPSC", "iPSC"]:
            cell_type_code = "iPSC"
        elif cell_type_clean in ["FIBROBLAST", "FIBRO"]:
            cell_type_code = "FIBRO"
        elif cell_type_clean in ["NPC", "NEURAL"]:
            cell_type_code = "NPC"
        elif cell_type_clean in ["CARDIOMYOCYTE", "CARDIO", "CM"]:
            cell_type_code = "CARDIO"
        elif cell_type_clean in ["HEPATOCYTE", "HEPATO", "HEP"]:
            cell_type_code = "HEPATO"
        elif cell_type_clean in ["ENDOTHELIAL", "ENDO", "EC"]:
            cell_type_code = "ENDO"
        else:
            # Generic abbreviation - take first 5 chars
            cell_type_code = cell_type_clean[:5]
    
    # Build the base ID pattern
    if operator_code and cell_type_code:
        base_pattern = f"TH-{day}-{operator_code}-{cell_type_code}"
        search_pattern = f"{base_pattern}-%"
    elif operator_code:
        base_pattern = f"TH-{day}-{operator_code}"
        search_pattern = f"{base_pattern}-%"
    elif cell_type_code:
        base_pattern = f"TH-{day}-{cell_type_code}"
        search_pattern = f"{base_pattern}-%"
    else:
        # Fallback to simple format
        return generate_thaw_id_for_date(conn, d)
    
    # Count existing thaw IDs with this pattern
    with closing(conn.cursor()) as cur:
        cur.execute(
            "SELECT COUNT(*) FROM logs WHERE event_type = 'Thawing' AND date = ? AND thaw_id LIKE ?",
            (d.isoformat(), search_pattern),
        )
        count = cur.fetchone()[0] or 0
    
    return f"{base_pattern}-{count + 1:03d}"


def insert_log(conn: sqlite3.Connection, payload: Dict[str, Any]) -> int:
    cols = [
        "date",
        "cell_line",
        "event_type",
        "passage",
        "vessel",
        "location",
        "medium",
        "cell_type",
        "notes",
        "operator",
        "thaw_id",
        "cryo_vial_position",
        "image_path",
        "assigned_to",
        "next_action_date",
        "volume",
        "experiment_type",
        "experiment_stage",
        "experimental_conditions",
        "protocol_reference",
        "outcome_status",
        "success_metrics",
        "linked_thaw_id",
        "created_by",
        "created_at",
    ]
    values = [payload.get(c) for c in cols]
    with closing(conn.cursor()) as cur:
        cur.execute(
            f"INSERT INTO logs ({', '.join(cols)}) VALUES ({', '.join(['?']*len(cols))})",
            values,
        )
        conn.commit()
        return cur.lastrowid


def query_logs(
    conn: sqlite3.Connection,
    *,
    user: Optional[str] = None,
    event_type: Optional[str] = None,
    thaw_id: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    cell_line_contains: Optional[str] = None,
) -> List[Dict[str, Any]]:
    where: List[str] = []
    params: List[Any] = []
    if user:
        where.append("created_by = ?")
        params.append(user)
    if event_type and event_type != "(any)":
        where.append("event_type = ?")
        params.append(event_type)
    if thaw_id:
        where.append("thaw_id = ?")
        params.append(thaw_id)
    if start_date:
        where.append("date >= ?")
        params.append(start_date.isoformat())
    if end_date:
        where.append("date <= ?")
        params.append(end_date.isoformat())
    if cell_line_contains:
        where.append("LOWER(cell_line) LIKE ?")
        params.append(f"%{cell_line_contains.lower()}%")

    where_sql = (" WHERE " + " AND ".join(where)) if where else ""
    sql = "SELECT * FROM logs" + where_sql + " ORDER BY date ASC, created_at ASC"
    with closing(conn.cursor()) as cur:
        cur.execute(sql, tuple(params))
        rows = cur.fetchall()
    return [dict(r) for r in rows]


def list_distinct_thaw_ids(conn: sqlite3.Connection) -> List[str]:
    with closing(conn.cursor()) as cur:
        cur.execute("SELECT DISTINCT thaw_id FROM logs WHERE thaw_id IS NOT NULL AND thaw_id <> '' ORDER BY thaw_id")
        rows = cur.fetchall()
    return [r[0] for r in rows]


def get_active_thaw_options(conn: sqlite3.Connection, cell_line: str = "") -> List[Dict[str, Any]]:
    """Get active thaw IDs with current status for linking to new entries
    
    Returns list of dictionaries with thaw_id, cell_line, current_passage, 
    last_event, last_date, days_since_thaw, and status information
    """
    with closing(conn.cursor()) as cur:
        if cell_line:
            # Get thaw IDs for specific cell line
            query = """
                SELECT DISTINCT t.thaw_id, t.cell_line, t.date as thaw_date,
                       l.passage as current_passage, l.event_type as last_event, 
                       l.date as last_date, l.vessel, l.location
                FROM logs t
                LEFT JOIN (
                    SELECT thaw_id, passage, event_type, date, vessel, location,
                           ROW_NUMBER() OVER (PARTITION BY thaw_id ORDER BY date DESC, id DESC) as rn
                    FROM logs 
                    WHERE thaw_id IS NOT NULL AND thaw_id != ''
                ) l ON t.thaw_id = l.thaw_id AND l.rn = 1
                WHERE t.thaw_id IS NOT NULL AND t.thaw_id != '' 
                  AND t.event_type = 'Thawing' 
                  AND t.cell_line = ?
                ORDER BY t.date DESC, t.thaw_id DESC
                LIMIT 10
            """
            cur.execute(query, (cell_line,))
        else:
            # Get all recent thaw IDs
            query = """
                SELECT DISTINCT t.thaw_id, t.cell_line, t.date as thaw_date,
                       l.passage as current_passage, l.event_type as last_event, 
                       l.date as last_date, l.vessel, l.location
                FROM logs t
                LEFT JOIN (
                    SELECT thaw_id, passage, event_type, date, vessel, location,
                           ROW_NUMBER() OVER (PARTITION BY thaw_id ORDER BY date DESC, id DESC) as rn
                    FROM logs 
                    WHERE thaw_id IS NOT NULL AND thaw_id != ''
                ) l ON t.thaw_id = l.thaw_id AND l.rn = 1
                WHERE t.thaw_id IS NOT NULL AND t.thaw_id != '' 
                  AND t.event_type = 'Thawing'
                ORDER BY t.date DESC, t.thaw_id DESC
                LIMIT 20
            """
            cur.execute(query)
        
        rows = cur.fetchall()
        
        results = []
        for row in rows:
            thaw_id, cell_line_db, thaw_date, current_passage, last_event, last_date, vessel, location = row
            
            # Calculate days since thaw
            try:
                from datetime import datetime, date
                if isinstance(thaw_date, str):
                    thaw_dt = datetime.fromisoformat(thaw_date).date()
                else:
                    thaw_dt = thaw_date
                days_since = (date.today() - thaw_dt).days
            except:
                days_since = 0
            
            # Determine status
            status = "Active"
            if last_event == "Cryopreservation":
                status = "Cryopreserved"
            elif days_since > 30:
                status = "Old"
            elif days_since > 14:
                status = "Aged"
            
            results.append({
                'thaw_id': thaw_id,
                'cell_line': cell_line_db,
                'thaw_date': thaw_date,
                'current_passage': current_passage or 1,
                'last_event': last_event or 'Thawing',
                'last_date': last_date or thaw_date,
                'vessel': vessel or '',
                'location': location or '',
                'days_since_thaw': days_since,
                'status': status
            })
        
        return results


def get_thaw_latest_info(conn: sqlite3.Connection, thaw_id: str) -> Dict[str, Any]:
    """Get the latest entry information for a specific thaw ID for auto-filling forms
    
    Returns a dictionary with the most recent values for passage, vessel, location,
    medium, cell_type, and other relevant fields for the specified thaw ID
    """
    with closing(conn.cursor()) as cur:
        # Get the most recent entry for this thaw ID
        query = """
            SELECT cell_line, passage, vessel, location, medium, cell_type, 
                   volume, notes, operator, date, event_type,
                   experimental_conditions, protocol_reference, success_metrics,
                   experiment_type, experiment_stage, outcome_status
            FROM logs 
            WHERE thaw_id = ? 
            ORDER BY date DESC, id DESC 
            LIMIT 1
        """
        cur.execute(query, (thaw_id,))
        row = cur.fetchone()
        
        if row:
            (cell_line, passage, vessel, location, medium, cell_type, 
             volume, notes, operator, date, event_type,
             experimental_conditions, protocol_reference, success_metrics,
             experiment_type, experiment_stage, outcome_status) = row
            
            # Calculate suggested next passage for splits
            next_passage = passage
            if passage and event_type == "Split":
                try:
                    next_passage = int(passage) + 1
                except (ValueError, TypeError):
                    next_passage = passage
            
            return {
                'cell_line': cell_line or '',
                'passage': next_passage or 1,
                'vessel': vessel or '',
                'location': location or '',
                'medium': medium or '',
                'cell_type': cell_type or '',
                'volume': volume or 0.0,
                'notes': '',  # Start with blank notes for new entry
                'operator': operator or '',
                'last_date': date or '',
                'last_event': event_type or '',
                'experimental_conditions': experimental_conditions or '',
                'protocol_reference': protocol_reference or '',
                'success_metrics': success_metrics or '',
                'experiment_type': experiment_type or '',
                'experiment_stage': experiment_stage or '',
                'outcome_status': outcome_status or ''
            }
        else:
            # Return empty defaults if no entries found
            return {
                'cell_line': '',
                'passage': 1,
                'vessel': '',
                'location': '',
                'medium': '',
                'cell_type': '',
                'volume': 0.0,
                'notes': '',
                'operator': '',
                'last_date': '',
                'last_event': '',
                'experimental_conditions': '',
                'protocol_reference': '',
                'success_metrics': '',
                'experiment_type': '',
                'experiment_stage': '',
                'outcome_status': ''
            }


def _ref_table_for(kind: str) -> str:
    mapping = {
        "cell_line": "cell_lines",
        "event_type": "event_types",
        "vessel": "vessels",
        "location": "locations",
    "cell_type": "cell_types",
    "culture_medium": "culture_media",
    }
    if kind not in mapping:
        raise ValueError("Unsupported ref kind")
    return mapping[kind]


def get_ref_values(conn: sqlite3.Connection, kind: str) -> List[str]:
    table = _ref_table_for(kind)
    with closing(conn.cursor()) as cur:
        cur.execute(f"SELECT name FROM {table} ORDER BY name COLLATE NOCASE ASC")
        rows = cur.fetchall()
    return [r[0] for r in rows]


def add_ref_value(conn: sqlite3.Connection, kind: str, name: str) -> None:
    table = _ref_table_for(kind)
    with closing(conn.cursor()) as cur:
        cur.execute(
            f"INSERT OR IGNORE INTO {table} (name, created_at) VALUES (?, ?)",
            (name.strip(), datetime.utcnow().isoformat()),
        )
        conn.commit()


def delete_ref_value(conn: sqlite3.Connection, kind: str, name: str) -> None:
    table = _ref_table_for(kind)
    with closing(conn.cursor()) as cur:
        cur.execute(f"DELETE FROM {table} WHERE name = ?", (name.strip(),))
        conn.commit()


def rename_ref_value(conn: sqlite3.Connection, kind: str, old_name: str, new_name: str) -> None:
    table = _ref_table_for(kind)
    with closing(conn.cursor()) as cur:
        cur.execute(
            f"UPDATE {table} SET name = ? WHERE name = ?",
            (new_name.strip(), old_name.strip()),
        )
        conn.commit()


def backup_now(dest_root: Optional[str] = None) -> str:
    """Create a timestamped backup of the DB and images directory.

    Returns the backup folder path.
    """
    root = dest_root or os.path.join(os.path.dirname(__file__), "backups")
    os.makedirs(root, exist_ok=True)
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    out_dir = os.path.join(root, f"backup_{ts}")
    os.makedirs(out_dir, exist_ok=True)
    # Copy DB
    if os.path.exists(DB_PATH):
        shutil.copy2(DB_PATH, os.path.join(out_dir, os.path.basename(DB_PATH)))
    # Copy images (shallow copy maintaining structure)
    if os.path.isdir(IMAGES_DIR):
        img_out = os.path.join(out_dir, "images")
        os.makedirs(img_out, exist_ok=True)
        for root_dir, dirs, files in os.walk(IMAGES_DIR):
            rel = os.path.relpath(root_dir, IMAGES_DIR)
            target_dir = os.path.join(img_out, rel if rel != "." else "")
            os.makedirs(target_dir, exist_ok=True)
            for f in files:
                src = os.path.join(root_dir, f)
                dst = os.path.join(target_dir, f)
                try:
                    shutil.copy2(src, dst)
                except Exception:
                    # Skip unreadable files
                    pass
    return out_dir


def list_distinct_values(
    conn: sqlite3.Connection,
    column: str,
    *,
    cell_line: Optional[str] = None,
    limit: int = 10,
) -> List[str]:
    if column not in {
        "cell_line",
        "event_type",
        "vessel",
        "location",
        "medium",
        "cell_type",
        "operator",
        "assigned_to",
    }:
        raise ValueError("Unsupported column for distinct values")
    where = "WHERE {col} IS NOT NULL AND {col} <> ''".format(col=column)
    params: List[Any] = []
    if cell_line and column != "cell_line":
        where += " AND cell_line = ?"
        params.append(cell_line)
    sql = f"SELECT {column}, COUNT(*) as cnt FROM logs {where} GROUP BY {column} ORDER BY cnt DESC LIMIT {limit}"
    with closing(conn.cursor()) as cur:
        cur.execute(sql, tuple(params))
        rows = cur.fetchall()
    return [r[0] for r in rows]


def get_last_log_for_cell_line(conn: sqlite3.Connection, cell_line: str) -> Optional[Dict[str, Any]]:
    with closing(conn.cursor()) as cur:
        cur.execute(
            "SELECT * FROM logs WHERE cell_line = ? ORDER BY date DESC, created_at DESC LIMIT 1",
            (cell_line,),
        )
        row = cur.fetchone()
    return dict(row) if row else None


def get_last_log_for_line_event(conn: sqlite3.Connection, cell_line: str, event_type: str) -> Optional[Dict[str, Any]]:
    with closing(conn.cursor()) as cur:
        cur.execute(
            """
            SELECT * FROM logs
            WHERE cell_line = ? AND event_type = ?
            ORDER BY date DESC, created_at DESC
            LIMIT 1
            """,
            (cell_line, event_type),
        )
        row = cur.fetchone()
    return dict(row) if row else None


def get_recent_logs_for_cell_line(
    conn: sqlite3.Connection,
    cell_line: str,
    limit: int = 10,
) -> List[Dict[str, Any]]:
    with closing(conn.cursor()) as cur:
        cur.execute(
            """
            SELECT * FROM logs
            WHERE cell_line = ?
            ORDER BY date DESC, created_at DESC
            LIMIT ?
            """,
            (cell_line, limit),
        )
        rows = cur.fetchall()
    return [dict(r) for r in rows]


def predict_next_passage(conn: sqlite3.Connection, cell_line: str) -> Optional[int]:
    last = get_last_log_for_cell_line(conn, cell_line)
    if not last:
        return None
    try:
        p = int(last.get("passage") or 0)
        return p + 1 if p > 0 else None
    except Exception:
        return None


def top_values(
    conn: sqlite3.Connection,
    column: str,
    *,
    cell_line: Optional[str] = None,
    limit: int = 3,
) -> List[str]:
    vals = list_distinct_values(conn, column, cell_line=cell_line, limit=limit)
    return vals


def suggest_next_event(conn: sqlite3.Connection, cell_line: str) -> Optional[str]:
    # Heuristic: look at last event; suggest likely follow-up
    last = get_last_log_for_cell_line(conn, cell_line)
    if not last:
        return None
    last_evt = (last.get("event_type") or "").lower()
    mapping = {
        "thawing": "Observation",
        "observation": "Media Change",
        "media change": "Observation",
        "split": "Observation",
        "cryopreservation": "Observation",
    }
    return mapping.get(last_evt)


def delete_log(conn: sqlite3.Connection, log_id: int) -> bool:
    """Delete a log entry by ID. Returns True if successful, False if not found."""
    with closing(conn.cursor()) as cur:
        # First check if the log exists and get image path for cleanup
        cur.execute("SELECT image_path FROM logs WHERE id = ?", (log_id,))
        row = cur.fetchone()
        if not row:
            return False
        
        image_path = row[0] if row else None
        
        # Delete the log entry
        cur.execute("DELETE FROM logs WHERE id = ?", (log_id,))
        
        # Clean up associated image file if it exists
        if image_path and os.path.exists(image_path):
            try:
                os.remove(image_path)
            except Exception:
                # Image deletion failed, but log deletion succeeded
                pass
        
        conn.commit()
        return True


def update_log(conn: sqlite3.Connection, log_id: int, payload: Dict[str, Any]) -> bool:
    """Update a log entry by ID. Returns True if successful, False if not found."""
    with closing(conn.cursor()) as cur:
        # Check if the log exists
        cur.execute("SELECT id FROM logs WHERE id = ?", (log_id,))
        if not cur.fetchone():
            return False
        
        # Build update query dynamically based on provided fields
        cols = [
            "date", "cell_line", "event_type", "passage", "vessel", "location", 
            "medium", "cell_type", "notes", "operator", "thaw_id", 
            "cryo_vial_position", "image_path", "assigned_to", "next_action_date", "volume"
        ]
        
        # Only update fields that are provided in the payload
        update_cols = []
        values = []
        for col in cols:
            if col in payload:
                update_cols.append(f"{col} = ?")
                values.append(payload[col])
        
        if not update_cols:
            return False  # No fields to update
        
        # Add the ID for the WHERE clause
        values.append(log_id)
        
        sql = f"UPDATE logs SET {', '.join(update_cols)} WHERE id = ?"
        cur.execute(sql, values)
        conn.commit()
        return True


def get_log_by_id(conn: sqlite3.Connection, log_id: int) -> Optional[Dict[str, Any]]:
    """Get a single log entry by ID."""
    with closing(conn.cursor()) as cur:
        cur.execute("SELECT * FROM logs WHERE id = ?", (log_id,))
        row = cur.fetchone()
    return dict(row) if row else None


def get_template_entries(conn: sqlite3.Connection, cell_line: Optional[str] = None, event_type: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
    """Get template-worthy entries (commonly used combinations) for copying."""
    where_conditions = []
    params = []
    
    if cell_line:
        where_conditions.append("cell_line = ?")
        params.append(cell_line)
    
    if event_type:
        where_conditions.append("event_type = ?")
        params.append(event_type)
    
    where_clause = " WHERE " + " AND ".join(where_conditions) if where_conditions else ""
    
    # Get most recent entries grouped by common field combinations
    sql = f"""
    SELECT *, COUNT(*) as usage_count 
    FROM logs {where_clause}
    GROUP BY cell_line, event_type, vessel, location, medium, cell_type
    ORDER BY usage_count DESC, date DESC
    LIMIT ?
    """
    params.append(limit)
    
    with closing(conn.cursor()) as cur:
        cur.execute(sql, params)
        rows = cur.fetchall()
    return [dict(r) for r in rows]


def get_recent_entries_by_operator(conn: sqlite3.Connection, operator: str, limit: int = 10) -> List[Dict[str, Any]]:
    """Get recent entries by a specific operator for copying personal patterns."""
    with closing(conn.cursor()) as cur:
        cur.execute(
            "SELECT * FROM logs WHERE operator = ? ORDER BY date DESC, created_at DESC LIMIT ?",
            (operator, limit)
        )
        rows = cur.fetchall()
    return [dict(r) for r in rows]


def get_entries_by_pattern(conn: sqlite3.Connection, **pattern_filters) -> List[Dict[str, Any]]:
    """Get entries matching specific patterns (vessel type, medium, etc.)."""
    where_conditions = []
    params = []
    
    for field, value in pattern_filters.items():
        if value and field in ['cell_line', 'event_type', 'vessel', 'location', 'medium', 'cell_type', 'operator']:
            where_conditions.append(f"{field} = ?")
            params.append(value)
    
    if not where_conditions:
        return []
    
    where_clause = " WHERE " + " AND ".join(where_conditions)
    sql = f"SELECT * FROM logs {where_clause} ORDER BY date DESC LIMIT 20"
    
    with closing(conn.cursor()) as cur:
        cur.execute(sql, params)
        rows = cur.fetchall()
    return [dict(r) for r in rows]


def save_entry_template(conn: sqlite3.Connection, name: str, template_data: Dict[str, Any], created_by: str) -> None:
    """Save an entry template for future reuse."""
    with closing(conn.cursor()) as cur:
        # First create templates table if it doesn't exist
        cur.execute("""
            CREATE TABLE IF NOT EXISTS entry_templates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                template_data TEXT NOT NULL,
                created_by TEXT NOT NULL,
                created_at TEXT NOT NULL,
                usage_count INTEGER DEFAULT 0
            )
        """)
        
        import json
        cur.execute(
            "INSERT OR REPLACE INTO entry_templates (name, template_data, created_by, created_at, usage_count) VALUES (?, ?, ?, ?, COALESCE((SELECT usage_count FROM entry_templates WHERE name = ?), 0))",
            (name, json.dumps(template_data), created_by, datetime.utcnow().isoformat(), name)
        )
        conn.commit()


def get_entry_templates(conn: sqlite3.Connection, created_by: Optional[str] = None) -> List[Dict[str, Any]]:
    """Get saved entry templates."""
    with closing(conn.cursor()) as cur:
        # Create table if it doesn't exist
        try:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS entry_templates (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    template_data TEXT NOT NULL,
                    created_by TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    usage_count INTEGER DEFAULT 0
                )
            """)
            conn.commit()
        except:
            pass
        
        if created_by:
            cur.execute("SELECT * FROM entry_templates WHERE created_by = ? ORDER BY usage_count DESC, created_at DESC", (created_by,))
        else:
            cur.execute("SELECT * FROM entry_templates ORDER BY usage_count DESC, created_at DESC")
        
        rows = cur.fetchall()
    
    import json
    templates = []
    for row in rows:
        try:
            template = dict(row)
            template['template_data'] = json.loads(template['template_data'])
            templates.append(template)
        except:
            continue
    return templates


def increment_template_usage(conn: sqlite3.Connection, template_name: str) -> None:
    """Increment usage count for a template."""
    with closing(conn.cursor()) as cur:
        cur.execute("UPDATE entry_templates SET usage_count = usage_count + 1 WHERE name = ?", (template_name,))
        conn.commit()


def delete_entry_template(conn: sqlite3.Connection, template_name: str, created_by: str) -> bool:
    """Delete an entry template."""
    with closing(conn.cursor()) as cur:
        cur.execute("DELETE FROM entry_templates WHERE name = ? AND created_by = ?", (template_name, created_by))
        conn.commit()
        return cur.rowcount > 0


def get_vial_lifecycle(conn: sqlite3.Connection, thaw_id: str) -> Dict[str, Any]:
    """Get complete lifecycle information for a vial (thaw ID)."""
    with closing(conn.cursor()) as cur:
        # Get all events for this thaw ID, ordered chronologically
        cur.execute("""
            SELECT * FROM logs 
            WHERE thaw_id = ? 
            ORDER BY date ASC, created_at ASC
        """, (thaw_id,))
        events = [dict(row) for row in cur.fetchall()]
        
        if not events:
            return {}
        
        # Calculate lifecycle statistics
        thaw_event = None
        latest_event = None
        passage_progression = []
        culture_days = 0
        
        for event in events:
            if event.get('event_type') == 'Thawing':
                thaw_event = event
            latest_event = event
            
            if event.get('passage'):
                passage_progression.append({
                    'date': event.get('date'),
                    'passage': event.get('passage'),
                    'event_type': event.get('event_type'),
                    'vessel': event.get('vessel'),
                    'medium': event.get('medium')
                })
        
        # Calculate culture duration
        if thaw_event and latest_event:
            from datetime import datetime
            try:
                thaw_date = datetime.fromisoformat(thaw_event.get('date'))
                latest_date = datetime.fromisoformat(latest_event.get('date'))
                culture_days = (latest_date - thaw_date).days
            except:
                culture_days = 0
        
        return {
            'thaw_id': thaw_id,
            'events': events,
            'thaw_event': thaw_event,
            'latest_event': latest_event,
            'passage_progression': passage_progression,
            'culture_days': culture_days,
            'total_events': len(events),
            'current_passage': latest_event.get('passage') if latest_event else None,
            'current_vessel': latest_event.get('vessel') if latest_event else None,
            'current_medium': latest_event.get('medium') if latest_event else None,
            'current_location': latest_event.get('location') if latest_event else None
        }


def get_vial_analytics(conn: sqlite3.Connection, thaw_id: str) -> Dict[str, Any]:
    """Get analytics and insights for a vial's lifecycle."""
    lifecycle = get_vial_lifecycle(conn, thaw_id)
    if not lifecycle:
        return {}
    
    events = lifecycle['events']
    
    # Analyze passage intervals
    passage_intervals = []
    split_events = [e for e in events if e.get('event_type') == 'Split' and e.get('passage')]
    
    for i in range(1, len(split_events)):
        prev_event = split_events[i-1]
        curr_event = split_events[i]
        try:
            from datetime import datetime
            prev_date = datetime.fromisoformat(prev_event.get('date'))
            curr_date = datetime.fromisoformat(curr_event.get('date'))
            interval = (curr_date - prev_date).days
            passage_intervals.append(interval)
        except:
            continue
    
    # Analyze culture conditions
    media_used = list(set([e.get('medium') for e in events if e.get('medium')]))
    vessels_used = list(set([e.get('vessel') for e in events if e.get('vessel')]))
    locations_used = list(set([e.get('location') for e in events if e.get('location')]))
    
    # Event frequency analysis
    event_types = {}
    for event in events:
        event_type = event.get('event_type', 'Unknown')
        event_types[event_type] = event_types.get(event_type, 0) + 1
    
    return {
        'thaw_id': thaw_id,
        'passage_intervals': passage_intervals,
        'avg_passage_interval': sum(passage_intervals) / len(passage_intervals) if passage_intervals else 0,
        'media_used': media_used,
        'vessels_used': vessels_used,
        'locations_used': locations_used,
        'event_frequency': event_types,
        'total_splits': event_types.get('Split', 0),
        'total_observations': event_types.get('Observation', 0),
        'media_changes': event_types.get('Media Change', 0)
    }


def get_active_vials(conn: sqlite3.Connection, days_threshold: int = 30) -> List[Dict[str, Any]]:
    """Get all active vials (thawed but not cryopreserved within threshold days)."""
    with closing(conn.cursor()) as cur:
        # Get all thaw IDs that have thawing events
        cur.execute("""
            SELECT DISTINCT thaw_id FROM logs 
            WHERE event_type = 'Thawing' AND thaw_id IS NOT NULL AND thaw_id != ''
        """)
        thaw_ids = [row[0] for row in cur.fetchall()]
        
        active_vials = []
        for thaw_id in thaw_ids:
            lifecycle = get_vial_lifecycle(conn, thaw_id)
            if not lifecycle:
                continue
                
            # Check if vial is still active (no recent cryopreservation)
            latest_event = lifecycle['latest_event']
            is_active = True
            
            # Check for cryopreservation events
            cryo_events = [e for e in lifecycle['events'] if e.get('event_type') == 'Cryopreservation']
            if cryo_events:
                # If there's a recent cryopreservation, consider it inactive
                latest_cryo = max(cryo_events, key=lambda x: x.get('date', ''))
                try:
                    from datetime import datetime, timedelta
                    cryo_date = datetime.fromisoformat(latest_cryo.get('date'))
                    cutoff_date = datetime.now() - timedelta(days=days_threshold)
                    if cryo_date > cutoff_date:
                        is_active = False
                except:
                    pass
            
            if is_active:
                active_vials.append(lifecycle)
        
        return active_vials


def get_vial_alerts(conn: sqlite3.Connection, thaw_id: str) -> List[Dict[str, str]]:
    """Generate alerts and recommendations for a vial."""
    lifecycle = get_vial_lifecycle(conn, thaw_id)
    analytics = get_vial_analytics(conn, thaw_id)
    alerts = []
    
    if not lifecycle:
        return alerts
    
    # Check for overdue splits (high passage number)
    current_passage = lifecycle.get('current_passage')
    if current_passage and current_passage > 10:
        alerts.append({
            'type': 'warning',
            'message': f'High passage number (P{current_passage}). Consider cryopreservation or differentiation.'
        })
    
    # Check for excessive splits since thawing - genetic stability alert
    split_count = sum(1 for e in lifecycle.get('events', []) if e.get('event_type') == 'Split')
    if split_count > 10:
        alerts.append({
            'type': 'critical',
            'message': f'⚠️ CRITICAL: {split_count} splits since thawing! Consider: 1) Thaw fresh vial, 2) Karyotype analysis for genetic stability, 3) Cryopreserve if healthy.'
        })
    elif split_count > 8:
        alerts.append({
            'type': 'warning', 
            'message': f'Approaching split limit ({split_count}/10). Plan to thaw new vial or check karyotype soon.'
        })
    
    # Check for long culture periods without splits
    avg_interval = analytics.get('avg_passage_interval', 0)
    culture_days = lifecycle.get('culture_days', 0)
    
    if avg_interval > 0 and culture_days > avg_interval * 1.5:
        alerts.append({
            'type': 'info',
            'message': f'Culture duration ({culture_days} days) exceeds average split interval. Consider splitting.'
        })
    
    # Check for missing recent observations
    recent_events = [e for e in lifecycle['events'][-3:]]  # Last 3 events
    has_recent_observation = any(e.get('event_type') == 'Observation' for e in recent_events)
    
    if not has_recent_observation and lifecycle['total_events'] > 2:
        alerts.append({
            'type': 'info',
            'message': 'No recent observations recorded. Consider adding culture status update.'
        })
    
    return alerts


def get_experimental_workflows(conn: sqlite3.Connection) -> List[Dict[str, Any]]:
    """Get all available experimental workflows."""
    with closing(conn.cursor()) as cur:
        cur.execute("SELECT * FROM experimental_workflows ORDER BY workflow_name")
        rows = cur.fetchall()
    return [dict(r) for r in rows]


def get_experiment_types(conn: sqlite3.Connection, category: Optional[str] = None) -> List[Dict[str, Any]]:
    """Get available experiment types, optionally filtered by category."""
    with closing(conn.cursor()) as cur:
        if category:
            cur.execute("SELECT * FROM experiment_types WHERE category = ? ORDER BY name", (category,))
        else:
            cur.execute("SELECT * FROM experiment_types ORDER BY category, name")
        rows = cur.fetchall()
    return [dict(r) for r in rows]


def get_experimental_journey(conn: sqlite3.Connection, thaw_id: str) -> Dict[str, Any]:
    """Get the complete experimental journey for a vial, organized by experiment types."""
    lifecycle = get_vial_lifecycle(conn, thaw_id)
    if not lifecycle:
        return {}
    
    events = lifecycle['events']
    
    # Group events by experiment type
    experimental_phases = {}
    maintenance_events = []
    
    for event in events:
        exp_type = event.get('experiment_type')
        if exp_type:
            if exp_type not in experimental_phases:
                experimental_phases[exp_type] = []
            experimental_phases[exp_type].append(event)
        else:
            maintenance_events.append(event)
    
    # Analyze each experimental phase
    phase_analysis = {}
    for exp_type, phase_events in experimental_phases.items():
        phase_start = min(phase_events, key=lambda x: x.get('date', ''))
        phase_end = max(phase_events, key=lambda x: x.get('date', ''))
        
        # Calculate phase duration
        try:
            start_date = datetime.fromisoformat(phase_start.get('date'))
            end_date = datetime.fromisoformat(phase_end.get('date'))
            duration = (end_date - start_date).days
        except:
            duration = 0
        
        # Get unique stages in this phase
        stages = list(set([e.get('experiment_stage') for e in phase_events if e.get('experiment_stage')]))
        
        # Check completion status
        completion_events = [e for e in phase_events if e.get('event_type') == 'Protocol Completion']
        is_completed = len(completion_events) > 0
        
        # Get success metrics
        success_metrics = [e.get('success_metrics') for e in phase_events if e.get('success_metrics')]
        
        phase_analysis[exp_type] = {
            'events': phase_events,
            'start_date': phase_start.get('date'),
            'end_date': phase_end.get('date'),
            'duration_days': duration,
            'stages': stages,
            'is_completed': is_completed,
            'success_metrics': success_metrics,
            'total_events': len(phase_events)
        }
    
    return {
        'thaw_id': thaw_id,
        'experimental_phases': phase_analysis,
        'maintenance_events': maintenance_events,
        'total_experimental_phases': len(experimental_phases),
        'active_experiments': [exp for exp, data in phase_analysis.items() if not data['is_completed']]
    }


def get_experiment_success_rate(conn: sqlite3.Connection, experiment_type: str) -> Dict[str, Any]:
    """Calculate success rates and metrics for a specific experiment type."""
    with closing(conn.cursor()) as cur:
        # Get all vials that have attempted this experiment
        cur.execute("""
            SELECT DISTINCT thaw_id FROM logs 
            WHERE experiment_type = ? AND thaw_id IS NOT NULL AND thaw_id != ''
        """, (experiment_type,))
        thaw_ids = [row[0] for row in cur.fetchall()]
        
        if not thaw_ids:
            return {'experiment_type': experiment_type, 'total_attempts': 0}
        
        successful_experiments = 0
        total_duration = 0
        success_metrics_list = []
        
        for thaw_id in thaw_ids:
            journey = get_experimental_journey(conn, thaw_id)
            if experiment_type in journey.get('experimental_phases', {}):
                phase_data = journey['experimental_phases'][experiment_type]
                if phase_data['is_completed']:
                    successful_experiments += 1
                    total_duration += phase_data['duration_days']
                    success_metrics_list.extend(phase_data['success_metrics'])
        
        success_rate = (successful_experiments / len(thaw_ids)) * 100 if thaw_ids else 0
        avg_duration = total_duration / successful_experiments if successful_experiments > 0 else 0
        
        return {
            'experiment_type': experiment_type,
            'total_attempts': len(thaw_ids),
            'successful_completions': successful_experiments,
            'success_rate_percent': success_rate,
            'average_duration_days': avg_duration,
            'success_metrics': success_metrics_list
        }


def add_experimental_workflow(conn: sqlite3.Connection, name: str, description: str, stages: str, duration: int, criteria: str) -> None:
    """Add a new experimental workflow."""
    with closing(conn.cursor()) as cur:
        cur.execute(
            "INSERT OR REPLACE INTO experimental_workflows (workflow_name, description, typical_stages, expected_duration_days, success_criteria, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (name, description, stages, duration, criteria, datetime.utcnow().isoformat())
        )
        conn.commit()


def get_experiment_recommendations(conn: sqlite3.Connection, thaw_id: str) -> List[Dict[str, str]]:
    """Get experiment recommendations based on vial history and current state."""
    lifecycle = get_vial_lifecycle(conn, thaw_id)
    journey = get_experimental_journey(conn, thaw_id)
    recommendations = []
    
    if not lifecycle:
        return recommendations
    
    current_passage = lifecycle.get('current_passage', 0)
    culture_days = lifecycle.get('culture_days', 0)
    completed_experiments = [exp for exp, data in journey.get('experimental_phases', {}).items() if data['is_completed']]
    active_experiments = journey.get('active_experiments', [])
    
    # Passage-based recommendations
    if current_passage <= 5:
        recommendations.append({
            'type': 'info',
            'category': 'Timing',
            'message': 'Low passage cells ideal for genome editing experiments (CRISPR, TALENs)'
        })
    
    if 5 <= current_passage <= 15:
        recommendations.append({
            'type': 'info',
            'category': 'Differentiation',
            'message': 'Good passage range for differentiation protocols (cardiac, neural, hepatic)'
        })
    
    if current_passage > 15:
        recommendations.append({
            'type': 'warning',
            'category': 'Quality',
            'message': 'High passage - consider using for drug screening or final experiments before discarding'
        })
    
    # Culture duration recommendations
    if culture_days > 21 and not active_experiments:
        recommendations.append({
            'type': 'info',
            'category': 'Timing',
            'message': 'Extended culture time - ideal for starting differentiation protocols'
        })
    
    # Experiment history recommendations
    if 'Genome Editing' in completed_experiments and 'Single Cell Cloning' not in completed_experiments:
        recommendations.append({
            'type': 'suggestion',
            'category': 'Next Step',
            'message': 'Consider single cell cloning to isolate edited clones'
        })
    
    if not any('Differentiation' in exp for exp in completed_experiments) and current_passage < 20:
        recommendations.append({
            'type': 'suggestion',
            'category': 'Opportunity',
            'message': 'Consider differentiation experiments to explore cell potential'
        })
    
    return recommendations


def get_weekend_tasks(conn: sqlite3.Connection, start_date: str, end_date: str, assigned_to: Optional[str] = None) -> List[Dict[str, Any]]:
    """Get all weekend tasks between start_date and end_date, optionally filtered by assignee."""
    with closing(conn.cursor()) as cur:
        if assigned_to:
            cur.execute("""
                SELECT l.*, v.current_vessel, v.current_medium, v.current_location, v.culture_days, v.current_passage
                FROM logs l
                LEFT JOIN (
                    SELECT thaw_id,
                           MAX(CASE WHEN vessel IS NOT NULL AND vessel != '' THEN vessel END) as current_vessel,
                           MAX(CASE WHEN medium IS NOT NULL AND medium != '' THEN medium END) as current_medium,
                           MAX(CASE WHEN location IS NOT NULL AND location != '' THEN location END) as current_location,
                           JULIANDAY('now') - JULIANDAY(MIN(date)) as culture_days,
                           MAX(CASE WHEN passage IS NOT NULL THEN passage END) as current_passage
                    FROM logs 
                    WHERE thaw_id IS NOT NULL AND thaw_id != ''
                    GROUP BY thaw_id
                ) v ON l.thaw_id = v.thaw_id
                WHERE l.next_action_date BETWEEN ? AND ? 
                AND l.assigned_to = ?
                ORDER BY l.next_action_date, l.cell_line
            """, (start_date, end_date, assigned_to))
        else:
            cur.execute("""
                SELECT l.*, v.current_vessel, v.current_medium, v.current_location, v.culture_days, v.current_passage
                FROM logs l
                LEFT JOIN (
                    SELECT thaw_id,
                           MAX(CASE WHEN vessel IS NOT NULL AND vessel != '' THEN vessel END) as current_vessel,
                           MAX(CASE WHEN medium IS NOT NULL AND medium != '' THEN medium END) as current_medium,
                           MAX(CASE WHEN location IS NOT NULL AND location != '' THEN location END) as current_location,
                           JULIANDAY('now') - JULIANDAY(MIN(date)) as culture_days,
                           MAX(CASE WHEN passage IS NOT NULL THEN passage END) as current_passage
                    FROM logs 
                    WHERE thaw_id IS NOT NULL AND thaw_id != ''
                    GROUP BY thaw_id
                ) v ON l.thaw_id = v.thaw_id
                WHERE l.next_action_date BETWEEN ? AND ?
                ORDER BY l.next_action_date, l.assigned_to, l.cell_line
            """, (start_date, end_date))
        
        rows = cur.fetchall()
    return [dict(r) for r in rows]


def get_weekend_task_summary(conn: sqlite3.Connection, assigned_to: str, weekend_date: str) -> Dict[str, Any]:
    """Get a comprehensive summary of weekend tasks for a specific person."""
    # Calculate weekend dates (Saturday and Sunday)
    from datetime import datetime, timedelta
    
    try:
        base_date = datetime.fromisoformat(weekend_date)
        # Find the Saturday of that week
        days_ahead = 5 - base_date.weekday()  # Saturday is weekday 5
        if days_ahead < 0:
            days_ahead += 7
        saturday = base_date + timedelta(days_ahead)
        sunday = saturday + timedelta(1)
        
        saturday_str = saturday.strftime('%Y-%m-%d')
        sunday_str = sunday.strftime('%Y-%m-%d')
        
    except:
        # Fallback - assume weekend_date is already Saturday
        saturday_str = weekend_date
        sunday_date = datetime.fromisoformat(weekend_date) + timedelta(1)
        sunday_str = sunday_date.strftime('%Y-%m-%d')
    
    # Get tasks for the weekend
    weekend_tasks = get_weekend_tasks(conn, saturday_str, sunday_str, assigned_to)
    
    # Group tasks by day and type
    saturday_tasks = [t for t in weekend_tasks if t['next_action_date'] == saturday_str]
    sunday_tasks = [t for t in weekend_tasks if t['next_action_date'] == sunday_str]
    
    # Group by task type
    task_summary = {
        'assigned_to': assigned_to,
        'weekend_start': saturday_str,
        'weekend_end': sunday_str,
        'total_tasks': len(weekend_tasks),
        'saturday_tasks': len(saturday_tasks),
        'sunday_tasks': len(sunday_tasks),
        'saturday_events': saturday_tasks,
        'sunday_events': sunday_tasks,
        'task_types': {},
        'media_needed': set(),
        'locations': set(),
        'cell_lines': set()
    }
    
    # Analyze task types and requirements
    for task in weekend_tasks:
        event_type = task.get('event_type', 'Unknown')
        if event_type not in task_summary['task_types']:
            task_summary['task_types'][event_type] = 0
        task_summary['task_types'][event_type] += 1
        
        # Collect required resources
        if task.get('current_medium'):
            task_summary['media_needed'].add(task['current_medium'])
        if task.get('current_location'):
            task_summary['locations'].add(task['current_location'])
        if task.get('cell_line'):
            task_summary['cell_lines'].add(task['cell_line'])
    
    # Convert sets to lists for JSON serialization
    task_summary['media_needed'] = list(task_summary['media_needed'])
    task_summary['locations'] = list(task_summary['locations'])
    task_summary['cell_lines'] = list(task_summary['cell_lines'])
    
    return task_summary


def create_weekend_checklist(conn: sqlite3.Connection, assigned_to: str, weekend_date: str) -> List[Dict[str, Any]]:
    """Create a detailed checklist for weekend tasks."""
    summary = get_weekend_task_summary(conn, assigned_to, weekend_date)
    checklist = []
    
    # Preparation checklist
    checklist.append({
        'category': 'Preparation',
        'priority': 'high',
        'task': 'Review all assigned tasks',
        'details': f"Total: {summary['total_tasks']} tasks ({summary['saturday_tasks']} Saturday, {summary['sunday_tasks']} Sunday)",
        'completed': False
    })
    
    # Media preparation
    if summary['media_needed']:
        checklist.append({
            'category': 'Preparation',
            'priority': 'high',
            'task': 'Prepare culture media',
            'details': f"Media needed: {', '.join(summary['media_needed'])}",
            'completed': False
        })
    
    # Equipment check
    checklist.append({
        'category': 'Preparation',
        'priority': 'medium',
        'task': 'Check equipment availability',
        'details': f"Locations: {', '.join(summary['locations'])}",
        'completed': False
    })
    
    # Cell line specific tasks
    for cell_line in summary['cell_lines']:
        line_tasks = [t for t in summary['saturday_events'] + summary['sunday_events'] if t['cell_line'] == cell_line]
        for task in line_tasks:
            checklist.append({
                'category': f'Cell Line: {cell_line}',
                'priority': 'high',
                'task': f"{task['event_type']} - {task['next_action_date']}",
                'details': f"Vessel: {task.get('current_vessel', 'N/A')}, Medium: {task.get('current_medium', 'N/A')}, Location: {task.get('current_location', 'N/A')}, Passage: P{task.get('current_passage', 'N/A')}",
                'notes': task.get('notes', ''),
                'thaw_id': task.get('thaw_id', ''),
                'log_id': task.get('id'),
                'completed': False
            })
    
    return checklist


def mark_weekend_task_completed(conn: sqlite3.Connection, log_id: int, completion_notes: str = None) -> bool:
    """Mark a weekend task as completed and optionally add completion notes."""
    try:
        with closing(conn.cursor()) as cur:
            # Update the task to mark it as completed
            update_time = datetime.utcnow().isoformat()
            
            if completion_notes:
                # Append completion notes to existing notes
                cur.execute("SELECT notes FROM logs WHERE id = ?", (log_id,))
                existing_notes = cur.fetchone()
                if existing_notes and existing_notes[0]:
                    new_notes = f"{existing_notes[0]}\n\n[COMPLETED {update_time[:16]}]: {completion_notes}"
                else:
                    new_notes = f"[COMPLETED {update_time[:16]}]: {completion_notes}"
                
                cur.execute("""
                    UPDATE logs 
                    SET notes = ?, next_action_date = NULL
                    WHERE id = ?
                """, (new_notes, log_id))
            else:
                cur.execute("""
                    UPDATE logs 
                    SET next_action_date = NULL
                    WHERE id = ?
                """, (log_id,))
            
            conn.commit()
            return True
    except Exception:
        return False


def get_weekend_task_instructions(task_type: str, current_passage: int = None) -> Dict[str, str]:
    """Get detailed instructions for common weekend tasks."""
    instructions = {
        'Media Change': {
            'summary': 'Replace culture medium with fresh medium',
            'steps': [
                '1. Warm medium to 37°C in water bath',
                '2. Aspirate old medium carefully',
                '3. Add fresh medium slowly to avoid disturbing cells',
                '4. Return to incubator immediately',
                '5. Update log with volume used and observations'
            ],
            'time_estimate': '5-10 minutes per plate',
            'critical_notes': 'Work in sterile conditions, check for contamination'
        },
        'Split': {
            'summary': f'Passage cells (current passage: P{current_passage or "?"})',
            'steps': [
                '1. Warm medium and dissociation reagent',
                '2. Aspirate medium and wash with PBS',
                '3. Add dissociation reagent and incubate',
                '4. Neutralize and collect cells',
                '5. Count cells and seed at appropriate density',
                '6. Update passage number in log'
            ],
            'time_estimate': '20-30 minutes per plate',
            'critical_notes': 'Monitor dissociation time carefully, avoid over-dissociation'
        },
        'Observation': {
            'summary': 'Check cell morphology and confluence',
            'steps': [
                '1. Examine under microscope',
                '2. Check for contamination',
                '3. Assess confluence percentage',
                '4. Note cell morphology',
                '5. Take photos if needed',
                '6. Record observations in log'
            ],
            'time_estimate': '5 minutes per plate',
            'critical_notes': 'Look for signs of differentiation or stress'
        },
        'Thawing': {
            'summary': 'Thaw cryopreserved cells',
            'steps': [
                '1. Warm medium in 37°C water bath',
                '2. Rapidly thaw vial in 37°C water bath',
                '3. Transfer to tube with warm medium',
                '4. Centrifuge and resuspend pellet',
                '5. Seed in culture vessel',
                '6. Record thaw ID and initial observations'
            ],
            'time_estimate': '15-20 minutes',
            'critical_notes': 'Work quickly to minimize cell death, first 24h critical'
        }
    }
    
    return instructions.get(task_type, {
        'summary': f'Perform {task_type} as scheduled',
        'steps': ['Follow standard protocol for this task type'],
        'time_estimate': 'Variable',
        'critical_notes': 'Refer to SOPs for detailed instructions'
    })


def update_log_field(conn: sqlite3.Connection, log_id: int, field_name: str, field_value: Any) -> bool:
    """
    Update a specific field in a log entry.
    
    Args:
        conn: Database connection
        log_id: ID of the log entry to update
        field_name: Name of the field to update
        field_value: New value for the field
    
    Returns:
        bool: True if update was successful, False otherwise
    """
    try:
        # Validate field name to prevent SQL injection
        valid_fields = [
            'cell_line', 'event_type', 'passage', 'vessel', 'location', 'medium',
            'cell_type', 'volume', 'notes', 'operator', 'thaw_id', 'cryo_vial_position',
            'assigned_to', 'next_action_date', 'experimental_conditions', 'protocol_reference',
            'success_metrics', 'experiment_type', 'experiment_stage', 'outcome_status'
        ]
        
        if field_name not in valid_fields:
            print(f"Warning: Field '{field_name}' not in valid fields list")
            return False
        
        with closing(conn.cursor()) as cursor:
            cursor.execute(f"UPDATE logs SET {field_name} = ? WHERE id = ?", (field_value, log_id))
            conn.commit()
            return cursor.rowcount > 0
            
    except sqlite3.Error as e:
        print(f"Database error updating field {field_name} for log {log_id}: {e}")
        return False
    except Exception as e:
        print(f"Error updating field {field_name} for log {log_id}: {e}")
        return False


# Weekend Planning Database Functions

def save_weekend_schedule(conn: sqlite3.Connection, weekend_date: str, assignee: str, created_by: str) -> bool:
    """Save a weekend assignment to the database"""
    try:
        with closing(conn.cursor()) as cur:
            cur.execute(
                """
                INSERT OR REPLACE INTO weekend_schedules 
                (weekend_date, assignee, created_by, created_at) 
                VALUES (?, ?, ?, ?)
                """,
                (weekend_date, assignee, created_by, datetime.utcnow().isoformat())
            )
            conn.commit()
            return True
    except Exception as e:
        print(f"Error saving weekend schedule: {e}")
        return False


def delete_weekend_schedule(conn: sqlite3.Connection, weekend_date: str) -> bool:
    """Delete a weekend assignment from the database"""
    try:
        with closing(conn.cursor()) as cur:
            cur.execute(
                "DELETE FROM weekend_schedules WHERE weekend_date = ?",
                (weekend_date,)
            )
            conn.commit()
            return True
    except Exception as e:
        print(f"Error deleting weekend schedule: {e}")
        return False


def get_weekend_schedules(conn: sqlite3.Connection) -> List[Dict[str, Any]]:
    """Get all weekend schedule assignments"""
    try:
        with closing(conn.cursor()) as cur:
            cur.execute(
                """
                SELECT weekend_date, assignee, created_by, created_at 
                FROM weekend_schedules 
                ORDER BY weekend_date
                """
            )
            rows = cur.fetchall()
            return [
                {
                    'weekend_date': row[0],
                    'assignee': row[1],
                    'created_by': row[2],
                    'created_at': row[3]
                }
                for row in rows
            ]
    except Exception as e:
        print(f"Error getting weekend schedules: {e}")
        return []


def get_weekend_assignee(conn: sqlite3.Connection, weekend_date: str) -> Optional[str]:
    """Get the assignee for a specific weekend date"""
    try:
        with closing(conn.cursor()) as cur:
            cur.execute(
                "SELECT assignee FROM weekend_schedules WHERE weekend_date = ?",
                (weekend_date,)
            )
            result = cur.fetchone()
            return result[0] if result else None
    except Exception as e:
        print(f"Error getting weekend assignee: {e}")
        return None


def save_user_caliber(conn: sqlite3.Connection, username: str, caliber_level: str, updated_by: str) -> bool:
    """Save a user's caliber level"""
    try:
        with closing(conn.cursor()) as cur:
            cur.execute(
                """
                INSERT OR REPLACE INTO user_calibers 
                (username, caliber_level, updated_by, updated_at) 
                VALUES (?, ?, ?, ?)
                """,
                (username, caliber_level, updated_by, datetime.utcnow().isoformat())
            )
            conn.commit()
            return True
    except Exception as e:
        print(f"Error saving user caliber: {e}")
        return False


def get_user_calibers(conn: sqlite3.Connection) -> Dict[str, str]:
    """Get all user caliber levels"""
    try:
        with closing(conn.cursor()) as cur:
            cur.execute("SELECT username, caliber_level FROM user_calibers")
            rows = cur.fetchall()
            return {row[0]: row[1] for row in rows}
    except Exception as e:
        print(f"Error getting user calibers: {e}")
        return {}


def save_custom_weekend_work(conn: sqlite3.Connection, work_data: Dict[str, Any], created_by: str) -> bool:
    """Save custom weekend work to the database"""
    try:
        with closing(conn.cursor()) as cur:
            cur.execute(
                """
                INSERT INTO custom_weekend_work 
                (work_type, description, hours, assignee, work_date, priority, created_by, created_at) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    work_data['type'],
                    work_data['description'],
                    work_data['hours'],
                    work_data['assignee'],
                    work_data['date'],
                    work_data['priority'],
                    created_by,
                    datetime.utcnow().isoformat()
                )
            )
            conn.commit()
            return True
    except Exception as e:
        print(f"Error saving custom weekend work: {e}")
        return False


def get_custom_weekend_work(conn: sqlite3.Connection, start_date: str = None, end_date: str = None) -> List[Dict[str, Any]]:
    """Get custom weekend work entries, optionally filtered by date range"""
    try:
        with closing(conn.cursor()) as cur:
            if start_date and end_date:
                cur.execute(
                    """
                    SELECT id, work_type, description, hours, assignee, work_date, priority, created_by, created_at 
                    FROM custom_weekend_work 
                    WHERE work_date BETWEEN ? AND ?
                    ORDER BY work_date DESC
                    """,
                    (start_date, end_date)
                )
            else:
                cur.execute(
                    """
                    SELECT id, work_type, description, hours, assignee, work_date, priority, created_by, created_at 
                    FROM custom_weekend_work 
                    ORDER BY work_date DESC
                    """
                )
            
            rows = cur.fetchall()
            return [
                {
                    'id': row[0],
                    'type': row[1],
                    'description': row[2],
                    'hours': row[3],
                    'assignee': row[4],
                    'date': row[5],
                    'priority': row[6],
                    'created_by': row[7],
                    'created_at': row[8]
                }
                for row in rows
            ]
    except Exception as e:
        print(f"Error getting custom weekend work: {e}")
        return []


def delete_custom_weekend_work(conn: sqlite3.Connection, work_id: int) -> bool:
    """Delete a custom weekend work entry"""
    try:
        with closing(conn.cursor()) as cur:
            cur.execute("DELETE FROM custom_weekend_work WHERE id = ?", (work_id,))
            conn.commit()
            return True
    except Exception as e:
        print(f"Error deleting custom weekend work: {e}")
        return False


def export_to_excel(conn: sqlite3.Connection, filename: str = None) -> str:
    """Export all database data to Excel file with multiple sheets"""
    import pandas as pd
    from datetime import datetime
    import os
    
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ipsc_tracker_export_{timestamp}.xlsx"
    
    # Ensure we have the full path
    if not os.path.isabs(filename):
        data_root = os.environ.get('DATA_ROOT', os.path.dirname(os.path.abspath(__file__)))
        filename = os.path.join(data_root, "exports", filename)
        os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    try:
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            
            # Export main logs table (this should always exist and be visible)
            logs_df = pd.read_sql_query("""
                SELECT id, thaw_id, cell_line, event_type, passage, vessel, medium, 
                       location, operator, date as log_date, notes, image_path, created_at,
                       linked_thaw_id, experiment_type, experiment_stage, 
                       experimental_conditions, protocol_reference, outcome_status, 
                       success_metrics
                FROM logs 
                ORDER BY created_at DESC
            """, conn)
            
            # Ensure we have at least an empty logs sheet if no data
            if logs_df.empty:
                logs_df = pd.DataFrame({
                    'id': [], 'thaw_id': [], 'cell_line': [], 'event_type': [], 
                    'passage': [], 'vessel': [], 'medium': [], 'location': [], 
                    'operator': [], 'log_date': [], 'notes': [], 'image_path': [],
                    'created_at': [], 'linked_thaw_id': [], 'experiment_type': [],
                    'experiment_stage': [], 'experimental_conditions': [],
                    'protocol_reference': [], 'outcome_status': [], 'success_metrics': []
                })
            
            logs_df.to_excel(writer, sheet_name='Culture_Logs', index=False)
            
            # Export metadata sheet
            metadata_df = pd.DataFrame({
                'Export_Info': [
                    f'Export Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
                    f'Total Records: {len(logs_df)}',
                    f'Database File: iPSC Tracker',
                    f'Export Type: Full Database Export'
                ]
            })
            metadata_df.to_excel(writer, sheet_name='Export_Info', index=False)
            
            # Export reference tables (optional)
            ref_tables = [
                ('cell_lines', 'Cell_Lines'),
                ('event_types', 'Event_Types'), 
                ('vessels', 'Vessels'),
                ('locations', 'Locations'),
                ('cell_types', 'Cell_Types'),
                ('culture_media', 'Culture_Media'),
                ('users', 'Users')
            ]
            
            for table_name, sheet_name in ref_tables:
                try:
                    df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
                    if not df.empty:
                        df.to_excel(writer, sheet_name=sheet_name, index=False)
                except Exception as e:
                    print(f"Warning: Could not export {table_name}: {e}")
                    # Continue with other tables even if one fails
                    continue
        
        print(f"✅ Excel export completed: {filename}")
        return filename
        
    except Exception as e:
        print(f"Error exporting to Excel: {e}")
        raise


def export_filtered_logs_to_excel(conn: sqlite3.Connection, filters: dict, filename: str = None) -> str:
    """Export filtered logs to Excel file"""
    import pandas as pd
    from datetime import datetime
    import os
    
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ipsc_filtered_export_{timestamp}.xlsx"
    
    # Ensure we have the full path
    if not os.path.isabs(filename):
        data_root = os.environ.get('DATA_ROOT', os.path.dirname(os.path.abspath(__file__)))
        filename = os.path.join(data_root, "exports", filename)
        os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    try:
        # Build SQL query with filters
        where_conditions = []
        params = []
        
        if filters.get('cell_line'):
            where_conditions.append("cell_line = ?")
            params.append(filters['cell_line'])
        
        if filters.get('event_type'):
            where_conditions.append("event_type = ?")
            params.append(filters['event_type'])
        
        if filters.get('operator'):
            where_conditions.append("operator = ?")
            params.append(filters['operator'])
        
        if filters.get('date_from'):
            where_conditions.append("log_date >= ?")
            params.append(filters['date_from'])
        
        if filters.get('date_to'):
            where_conditions.append("log_date <= ?")
            params.append(filters['date_to'])
        
        if filters.get('thaw_id'):
            where_conditions.append("thaw_id = ?")
            params.append(filters['thaw_id'])
        
        where_clause = ""
        if where_conditions:
            where_clause = "WHERE " + " AND ".join(where_conditions)
        
        query = f"""
            SELECT id, thaw_id, cell_line, event_type, passage, vessel, medium, 
                   location, operator, log_date, notes, image_path, created_at,
                   linked_thaw_id, experiment_type, experiment_stage, 
                   experimental_conditions, protocol_reference, outcome_status, 
                   success_metrics
            FROM logs 
            {where_clause}
            ORDER BY created_at DESC
        """
        
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            logs_df = pd.read_sql_query(query, conn, params=params)
            logs_df.to_excel(writer, sheet_name='Filtered_Logs', index=False)
            
            # Add summary sheet with filter information
            summary_data = {
                'Filter': list(filters.keys()),
                'Value': list(filters.values())
            }
            summary_df = pd.DataFrame(summary_data)
            summary_df.to_excel(writer, sheet_name='Filter_Summary', index=False)
        
        return filename
        
    except Exception as e:
        print(f"Error exporting filtered data to Excel: {e}")
        raise


def import_from_excel(conn: sqlite3.Connection, filename: str) -> dict:
    """Import data from Excel file back to database (with conflict handling)"""
    import pandas as pd
    
    results = {
        'imported': 0,
        'skipped': 0,
        'errors': 0,
        'messages': []
    }
    
    try:
        # Read the main logs sheet
        logs_df = pd.read_excel(filename, sheet_name='Culture_Logs')
        
        with closing(conn.cursor()) as cur:
            for _, row in logs_df.iterrows():
                try:
                    # Check if entry already exists (by ID or unique combination)
                    cur.execute("SELECT id FROM logs WHERE id = ?", (row['id'],))
                    if cur.fetchone():
                        results['skipped'] += 1
                        continue
                    
                    # Insert new entry
                    cur.execute("""
                        INSERT INTO logs (
                            thaw_id, cell_line, event_type, passage, vessel, medium,
                            location, operator, log_date, notes, image_path, created_at,
                            linked_thaw_id, experiment_type, experiment_stage,
                            experimental_conditions, protocol_reference, outcome_status,
                            success_metrics
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        row.get('thaw_id'), row.get('cell_line'), row.get('event_type'),
                        row.get('passage'), row.get('vessel'), row.get('medium'),
                        row.get('location'), row.get('operator'), row.get('log_date'),
                        row.get('notes'), row.get('image_path'), row.get('created_at'),
                        row.get('linked_thaw_id'), row.get('experiment_type'),
                        row.get('experiment_stage'), row.get('experimental_conditions'),
                        row.get('protocol_reference'), row.get('outcome_status'),
                        row.get('success_metrics')
                    ))
                    results['imported'] += 1
                    
                except Exception as e:
                    results['errors'] += 1
                    results['messages'].append(f"Error importing row {row.get('id', 'unknown')}: {str(e)}")
            
            conn.commit()
            results['messages'].append(f"Import completed: {results['imported']} imported, {results['skipped']} skipped, {results['errors']} errors")
        
    except Exception as e:
        results['messages'].append(f"Error reading Excel file: {str(e)}")
        results['errors'] += 1
    
    return results
