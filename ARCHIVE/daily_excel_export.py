#!/usr/bin/env python3
"""
Daily Excel Export Automation Script for iPSC Tracker
Exports the complete database to Excel with timestamp
"""

import os
import sys
from datetime import datetime
import sqlite3
from contextlib import closing

# Add the current directory to Python path to import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from db import export_to_excel, get_conn, ensure_dirs

def daily_export():
    """
    Perform daily Excel export with timestamp
    """
    try:
        # Ensure directories exist
        ensure_dirs()
        
        # Get database connection
        conn = get_conn()
        
        # Create exports directory if it doesn't exist
        exports_dir = "daily_exports"
        if not os.path.exists(exports_dir):
            os.makedirs(exports_dir)
        
        # Generate filename with date
        today = datetime.now()
        filename = f"iPSC_Daily_Export_{today.strftime('%Y%m%d_%H%M%S')}.xlsx"
        filepath = os.path.join(exports_dir, filename)
        
        print(f"Starting daily export at {today.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Export file: {filepath}")
        
        # Perform the export
        export_to_excel(conn, filepath)
        
        # Clean up old exports (keep last 30 days)
        cleanup_old_exports(exports_dir, days_to_keep=30)
        
        print(f"✅ Daily export completed successfully!")
        print(f"📁 File saved: {os.path.abspath(filepath)}")
        
        # Log the export to a log file
        log_export(filepath, today)
        
        return True
        
    except Exception as e:
        error_msg = f"❌ Daily export failed: {str(e)}"
        print(error_msg)
        
        # Log the error
        log_error(error_msg, datetime.now())
        
        return False
    
    finally:
        if 'conn' in locals():
            conn.close()

def cleanup_old_exports(exports_dir, days_to_keep=30):
    """
    Remove export files older than specified days
    """
    try:
        import time
        current_time = time.time()
        cutoff_time = current_time - (days_to_keep * 24 * 60 * 60)  # Convert days to seconds
        
        deleted_count = 0
        for filename in os.listdir(exports_dir):
            if filename.startswith("iPSC_Daily_Export_") and filename.endswith(".xlsx"):
                filepath = os.path.join(exports_dir, filename)
                file_time = os.path.getctime(filepath)
                
                if file_time < cutoff_time:
                    os.remove(filepath)
                    deleted_count += 1
                    print(f"🗑️  Deleted old export: {filename}")
        
        if deleted_count > 0:
            print(f"🧹 Cleaned up {deleted_count} old export files")
            
    except Exception as e:
        print(f"⚠️  Warning: Cleanup failed: {str(e)}")

def log_export(filepath, timestamp):
    """
    Log successful export to a log file
    """
    try:
        log_file = "daily_export_log.txt"
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"{timestamp.strftime('%Y-%m-%d %H:%M:%S')} - SUCCESS - {filepath}\n")
    except Exception as e:
        print(f"⚠️  Warning: Failed to write to log: {str(e)}")

def log_error(error_msg, timestamp):
    """
    Log export errors to a log file
    """
    try:
        log_file = "daily_export_log.txt"
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"{timestamp.strftime('%Y-%m-%d %H:%M:%S')} - ERROR - {error_msg}\n")
    except Exception as e:
        print(f"⚠️  Warning: Failed to write error to log: {str(e)}")

def get_database_stats():
    """
    Get basic statistics about the database for the export log
    """
    try:
        conn = get_conn()
        with closing(conn.cursor()) as cursor:
            # Count total logs
            cursor.execute("SELECT COUNT(*) FROM logs")
            total_logs = cursor.fetchone()[0]
            
            # Count logs from last 7 days
            cursor.execute("""
                SELECT COUNT(*) FROM logs 
                WHERE date >= date('now', '-7 days')
            """)
            recent_logs = cursor.fetchone()[0]
            
            # Get date range
            cursor.execute("SELECT MIN(date), MAX(date) FROM logs")
            date_range = cursor.fetchone()
            
        conn.close()
        
        return {
            'total_logs': total_logs,
            'recent_logs': recent_logs,
            'date_range': date_range
        }
    except Exception as e:
        print(f"⚠️  Warning: Failed to get database stats: {str(e)}")
        return None

if __name__ == "__main__":
    print("=" * 50)
    print("    iPSC Tracker - Daily Excel Export")
    print("=" * 50)
    
    # Get database stats
    stats = get_database_stats()
    if stats:
        print(f"📊 Database contains {stats['total_logs']} total entries")
        print(f"📈 {stats['recent_logs']} entries added in last 7 days")
        if stats['date_range'][0] and stats['date_range'][1]:
            print(f"📅 Date range: {stats['date_range'][0]} to {stats['date_range'][1]}")
        print("-" * 50)
    
    # Perform the export
    success = daily_export()
    
    print("=" * 50)
    
    # Exit with appropriate code for Task Scheduler
    sys.exit(0 if success else 1)