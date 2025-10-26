#!/usr/bin/env python3
"""Test script to verify thaw linking functionality works"""

import sqlite3
from datetime import datetime
from contextlib import closing
import sys
import os

# Add current directory to path to import db functions
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from db import get_conn, insert_log

def test_thaw_linking():
    """Test that we can insert entries with linked_thaw_id"""
    
    print("Testing thaw vial linking functionality...")
    
    # Get database connection
    conn = get_conn()
    
    # Create a test entry with linked_thaw_id
    test_payload = {
        "date": datetime.now().isoformat(),
        "cell_line": "Test Cell Line",
        "event_type": "Media Change", 
        "passage": 5,
        "vessel": "6-well plate",
        "location": "Incubator A",
        "medium": "mTeSR1",
        "cell_type": "iPSC",
        "notes": "Test entry for thaw linking",
        "operator": "Test User",
        "thaw_id": "",
        "cryo_vial_position": None,
        "image_path": None,
        "assigned_to": None,
        "next_action_date": None,
        "volume": None,
        "experiment_type": None,
        "experiment_stage": None,
        "experimental_conditions": None,
        "protocol_reference": None,
        "outcome_status": None,
        "success_metrics": None,
        "linked_thaw_id": "TH-20251025-001",  # Test thaw ID
        "created_by": "Test User",
        "created_at": datetime.now().isoformat(),
    }
    
    try:
        # Insert the test entry
        log_id = insert_log(conn, test_payload)
        print(f"✅ Successfully inserted entry with ID {log_id}")
        
        # Verify the entry was saved with linked_thaw_id
        with closing(conn.cursor()) as cur:
            cur.execute("SELECT linked_thaw_id FROM logs WHERE id = ?", (log_id,))
            result = cur.fetchone()
            
            if result and result[0] == "TH-20251025-001":
                print(f"✅ Linked thaw ID correctly saved: {result[0]}")
                
                # Clean up test entry
                cur.execute("DELETE FROM logs WHERE id = ?", (log_id,))
                conn.commit()
                print("✅ Test entry cleaned up")
                
                return True
            else:
                print(f"❌ Linked thaw ID not saved correctly. Got: {result}")
                return False
                
    except Exception as e:
        print(f"❌ Error testing thaw linking: {e}")
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    success = test_thaw_linking()
    if success:
        print("\n🎉 Thaw linking functionality is working correctly!")
    else:
        print("\n❌ Thaw linking test failed")
    
    sys.exit(0 if success else 1)