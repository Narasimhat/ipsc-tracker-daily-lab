"""
Migration script: SQLite → Supabase (PostgreSQL)
Converts existing iPSC Tracker database to cloud-based PostgreSQL
"""

import sqlite3
import psycopg2
from psycopg2.extras import execute_batch
import os
from datetime import datetime

# ============================================================================
# STEP 1: Set your Supabase credentials here (after creating project)
# ============================================================================
SUPABASE_HOST = "your-project.supabase.co"  # Replace with your Supabase host
SUPABASE_DB = "postgres"
SUPABASE_USER = "postgres"
SUPABASE_PASSWORD = "your-password"  # Replace with your Supabase password
SUPABASE_PORT = 5432

# Local SQLite database
SQLITE_DB = "data/ipsc_tracker.db"

# ============================================================================
# PostgreSQL Schema Creation
# ============================================================================

CREATE_TABLES_SQL = """
-- Cell lines table
CREATE TABLE IF NOT EXISTS cell_lines (
    id SERIAL PRIMARY KEY,
    line_name VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    source VARCHAR(255),
    date_established DATE,
    passage_number INTEGER,
    mycoplasma_status VARCHAR(50),
    karyotype_status VARCHAR(50),
    storage_location VARCHAR(255),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Passages table
CREATE TABLE IF NOT EXISTS passages (
    id SERIAL PRIMARY KEY,
    line_name VARCHAR(255) REFERENCES cell_lines(line_name) ON DELETE CASCADE,
    passage_number INTEGER,
    passage_date DATE,
    split_ratio VARCHAR(50),
    medium_used VARCHAR(255),
    confluence VARCHAR(50),
    notes TEXT,
    performed_by VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Thaws table
CREATE TABLE IF NOT EXISTS thaws (
    id SERIAL PRIMARY KEY,
    line_name VARCHAR(255) REFERENCES cell_lines(line_name) ON DELETE CASCADE,
    thaw_date DATE,
    vial_id VARCHAR(255),
    passage_at_thaw INTEGER,
    viability VARCHAR(50),
    seeding_density VARCHAR(255),
    medium_used VARCHAR(255),
    notes TEXT,
    performed_by VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Freezes table
CREATE TABLE IF NOT EXISTS freezes (
    id SERIAL PRIMARY KEY,
    line_name VARCHAR(255) REFERENCES cell_lines(line_name) ON DELETE CASCADE,
    freeze_date DATE,
    passage_number INTEGER,
    vial_count INTEGER,
    vial_ids TEXT,
    cell_count VARCHAR(255),
    freezing_medium VARCHAR(255),
    storage_location VARCHAR(255),
    notes TEXT,
    performed_by VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Quality control table
CREATE TABLE IF NOT EXISTS quality_control (
    id SERIAL PRIMARY KEY,
    line_name VARCHAR(255) REFERENCES cell_lines(line_name) ON DELETE CASCADE,
    qc_date DATE,
    qc_type VARCHAR(255),
    result VARCHAR(50),
    passage_number INTEGER,
    notes TEXT,
    image_path VARCHAR(500),
    performed_by VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Experiments table
CREATE TABLE IF NOT EXISTS experiments (
    id SERIAL PRIMARY KEY,
    experiment_name VARCHAR(255) UNIQUE NOT NULL,
    line_name VARCHAR(255) REFERENCES cell_lines(line_name) ON DELETE SET NULL,
    start_date DATE,
    end_date DATE,
    experiment_type VARCHAR(255),
    description TEXT,
    status VARCHAR(50),
    performed_by VARCHAR(255),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_passages_line_name ON passages(line_name);
CREATE INDEX IF NOT EXISTS idx_thaws_line_name ON thaws(line_name);
CREATE INDEX IF NOT EXISTS idx_freezes_line_name ON freezes(line_name);
CREATE INDEX IF NOT EXISTS idx_qc_line_name ON quality_control(line_name);
CREATE INDEX IF NOT EXISTS idx_experiments_line_name ON experiments(line_name);
"""

# ============================================================================
# Migration Functions
# ============================================================================

def connect_sqlite():
    """Connect to local SQLite database"""
    if not os.path.exists(SQLITE_DB):
        print(f"❌ SQLite database not found: {SQLITE_DB}")
        return None
    return sqlite3.connect(SQLITE_DB)

def connect_postgres():
    """Connect to Supabase PostgreSQL database"""
    try:
        conn = psycopg2.connect(
            host=SUPABASE_HOST,
            database=SUPABASE_DB,
            user=SUPABASE_USER,
            password=SUPABASE_PASSWORD,
            port=SUPABASE_PORT
        )
        print("✅ Connected to Supabase PostgreSQL")
        return conn
    except Exception as e:
        print(f"❌ Failed to connect to Supabase: {e}")
        return None

def create_postgres_schema(pg_conn):
    """Create PostgreSQL tables"""
    try:
        cursor = pg_conn.cursor()
        cursor.execute(CREATE_TABLES_SQL)
        pg_conn.commit()
        print("✅ PostgreSQL schema created")
        return True
    except Exception as e:
        print(f"❌ Failed to create schema: {e}")
        return False

def migrate_table(sqlite_conn, pg_conn, table_name):
    """Migrate data from SQLite table to PostgreSQL"""
    try:
        # Get data from SQLite
        sqlite_cursor = sqlite_conn.cursor()
        sqlite_cursor.execute(f"SELECT * FROM {table_name}")
        rows = sqlite_cursor.fetchall()
        
        if not rows:
            print(f"⚠️  Table '{table_name}' is empty, skipping...")
            return True
        
        # Get column names
        column_names = [description[0] for description in sqlite_cursor.description]
        
        # Prepare INSERT statement for PostgreSQL (skip 'id' as it's auto-generated)
        columns_without_id = [col for col in column_names if col != 'id']
        placeholders = ', '.join(['%s'] * len(columns_without_id))
        insert_sql = f"INSERT INTO {table_name} ({', '.join(columns_without_id)}) VALUES ({placeholders})"
        
        # Prepare data (skip 'id' column)
        id_index = column_names.index('id') if 'id' in column_names else -1
        data = []
        for row in rows:
            row_list = list(row)
            if id_index >= 0:
                row_list.pop(id_index)
            data.append(tuple(row_list))
        
        # Insert into PostgreSQL
        pg_cursor = pg_conn.cursor()
        execute_batch(pg_cursor, insert_sql, data)
        pg_conn.commit()
        
        print(f"✅ Migrated {len(rows)} rows from '{table_name}'")
        return True
        
    except Exception as e:
        print(f"❌ Failed to migrate '{table_name}': {e}")
        pg_conn.rollback()
        return False

def migrate_all_data():
    """Main migration function"""
    print("\n" + "="*70)
    print("🚀 iPSC Tracker: SQLite → Supabase Migration")
    print("="*70 + "\n")
    
    # Connect to databases
    sqlite_conn = connect_sqlite()
    if not sqlite_conn:
        return False
    
    pg_conn = connect_postgres()
    if not pg_conn:
        sqlite_conn.close()
        return False
    
    # Create schema
    if not create_postgres_schema(pg_conn):
        sqlite_conn.close()
        pg_conn.close()
        return False
    
    # Migrate tables in order (respecting foreign keys)
    tables = [
        'cell_lines',
        'passages',
        'thaws',
        'freezes',
        'quality_control',
        'experiments'
    ]
    
    print("\n📦 Migrating data...\n")
    
    for table in tables:
        migrate_table(sqlite_conn, pg_conn, table)
    
    # Close connections
    sqlite_conn.close()
    pg_conn.close()
    
    print("\n" + "="*70)
    print("✅ Migration completed successfully!")
    print("="*70)
    print("\n💡 Next steps:")
    print("   1. Verify data in Supabase dashboard")
    print("   2. Update app to use PostgreSQL (db.py)")
    print("   3. Deploy to Streamlit Cloud")
    print("\n")
    
    return True

# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    print("\n⚠️  BEFORE RUNNING THIS SCRIPT:")
    print("   1. Create a Supabase project at https://supabase.com")
    print("   2. Get your connection details from project settings")
    print("   3. Update SUPABASE_* variables at the top of this file")
    print("   4. Make sure your local SQLite database exists\n")
    
    response = input("Have you completed the above steps? (yes/no): ")
    
    if response.lower() in ['yes', 'y']:
        migrate_all_data()
    else:
        print("\n❌ Migration cancelled. Complete the setup steps first.")
