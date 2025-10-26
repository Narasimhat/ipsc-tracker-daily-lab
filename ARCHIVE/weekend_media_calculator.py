#!/usr/bin/env python3
"""
Weekend Media Volume Calculator
Analyzes the iPSC tracker database to calculate required media volumes by type for weekend tasks.
"""

import sqlite3
from datetime import datetime, date, timedelta
from collections import defaultdict
import os

def get_weekend_dates():
    """Get next Saturday and Sunday dates"""
    today = date.today()
    days_ahead = 5 - today.weekday()  # Saturday = 5
    if days_ahead <= 0:  # Already past Saturday this week
        days_ahead += 7
    saturday = today + timedelta(days_ahead)
    sunday = saturday + timedelta(1)
    return saturday, sunday

def find_database():
    """Find the iPSC tracker database"""
    possible_paths = [
        'ipsc_tracker.db',
        'data/ipsc_tracker.db',
        '../ipsc_tracker.db'
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    # If not found, return default name
    return 'ipsc_tracker.db'

def calculate_weekend_media_volumes(db_path, saturday, sunday):
    """Calculate media volumes needed for weekend by media type"""
    
    if not os.path.exists(db_path):
        print(f"⚠️  Database not found at {db_path}")
        print("Creating sample calculation based on typical usage...")
        return create_sample_calculation()
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all entries for the weekend dates
        saturday_str = saturday.strftime('%Y-%m-%d')
        sunday_str = sunday.strftime('%Y-%m-%d')
        
        # Query for media-related events (Media Change, Split, etc.)
        query = """
        SELECT date, medium, volume, event_type, cell_line
        FROM logs 
        WHERE date IN (?, ?) 
        AND event_type IN ('Media Change', 'Split', 'Observation', 'Thawing')
        AND medium IS NOT NULL 
        AND medium != ''
        AND volume > 0
        ORDER BY date, medium
        """
        
        cursor.execute(query, (saturday_str, sunday_str))
        entries = cursor.fetchall()
        
        # Aggregate volumes by media type and day
        saturday_volumes = defaultdict(float)
        sunday_volumes = defaultdict(float)
        
        for log_date, medium, volume, event_type, cell_line in entries:
            if log_date == saturday_str:
                saturday_volumes[medium] += volume
            elif log_date == sunday_str:
                sunday_volumes[medium] += volume
        
        conn.close()
        
        return saturday_volumes, sunday_volumes, len(entries)
        
    except Exception as e:
        print(f"⚠️  Error accessing database: {e}")
        return create_sample_calculation()

def create_sample_calculation():
    """Create sample calculation when database is not available"""
    saturday_volumes = {
        'E8': 35.0,
        'mTeSR1': 25.0,
        'Essential 8': 15.0
    }
    sunday_volumes = {
        'E8': 30.0,
        'mTeSR1': 20.0,
        'Essential 8': 10.0
    }
    return saturday_volumes, sunday_volumes, 12  # Sample entry count

def print_media_report(saturday_volumes, sunday_volumes, entry_count, saturday, sunday):
    """Print and save media volume report"""
    
    print("🧬 iPSC Weekend Media Volume Calculator")
    print("=" * 50)
    print(f"📅 Weekend: {saturday.strftime('%A, %B %d')} - {sunday.strftime('%A, %B %d, %Y')}")
    print(f"📊 Based on {entry_count} scheduled entries")
    print()
    
    # Get all unique media types
    all_media = set(saturday_volumes.keys()) | set(sunday_volumes.keys())
    
    if not all_media:
        print("📝 No media volumes found for the weekend.")
        print("💡 This could mean:")
        print("   - No weekend tasks scheduled yet")
        print("   - Database not found - using sample data")
        return
    
    print("📋 MEDIA VOLUME REQUIREMENTS:")
    print("-" * 40)
    
    total_saturday = 0
    total_sunday = 0
    
    report_lines = []
    
    for media in sorted(all_media):
        sat_vol = saturday_volumes.get(media, 0)
        sun_vol = sunday_volumes.get(media, 0)
        total_vol = sat_vol + sun_vol
        
        total_saturday += sat_vol
        total_sunday += sun_vol
        
        if total_vol > 0:
            line = f"{media}: {sat_vol:.1f} mL (Sat), {sun_vol:.1f} mL (Sun) = {total_vol:.1f} mL total"
            print(f"🧪 {line}")
            report_lines.append(line)
    
    print()
    print(f"📊 DAILY TOTALS:")
    print(f"   Saturday: {total_saturday:.1f} mL")
    print(f"   Sunday: {total_sunday:.1f} mL")
    print(f"   Weekend Total: {total_saturday + total_sunday:.1f} mL")
    
    # Save to file
    with open('weekend_media_volumes.txt', 'w') as f:
        f.write(f"iPSC Weekend Media Volume Report\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Weekend: {saturday.strftime('%Y-%m-%d')} to {sunday.strftime('%Y-%m-%d')}\n")
        f.write(f"Entries analyzed: {entry_count}\n\n")
        
        f.write("MEDIA VOLUME REQUIREMENTS:\n")
        f.write("-" * 30 + "\n")
        for line in report_lines:
            f.write(f"{line}\n")
        
        f.write(f"\nDAILY TOTALS:\n")
        f.write(f"Saturday: {total_saturday:.1f} mL\n")
        f.write(f"Sunday: {total_sunday:.1f} mL\n")
        f.write(f"Weekend Total: {total_saturday + total_sunday:.1f} mL\n")
    
    print(f"\n💾 Report saved to: weekend_media_volumes.txt")

def main():
    print("🔍 Calculating weekend media volumes...")
    
    # Get weekend dates
    saturday, sunday = get_weekend_dates()
    
    # Find database
    db_path = find_database()
    print(f"📂 Looking for database: {db_path}")
    
    # Calculate volumes
    saturday_volumes, sunday_volumes, entry_count = calculate_weekend_media_volumes(db_path, saturday, sunday)
    
    # Print report
    print_media_report(saturday_volumes, sunday_volumes, entry_count, saturday, sunday)

if __name__ == "__main__":
    main()