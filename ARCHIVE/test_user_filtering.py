#!/usr/bin/env python3
"""
Test script for the enhanced user filtering functionality
"""

import sys
import os
from contextlib import closing

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from db import get_conn
    
    def test_operator_query():
        """Test the operator dropdown query"""
        try:
            conn = get_conn()
            with closing(conn.cursor()) as cursor:
                cursor.execute("SELECT DISTINCT operator FROM logs WHERE operator IS NOT NULL AND operator != '' ORDER BY operator")
                operators = [row[0] for row in cursor.fetchall()]
                
                print(f"✅ Successfully retrieved {len(operators)} operators from database:")
                for op in operators:
                    print(f"   - {op}")
                    
                return True
        except Exception as e:
            print(f"❌ Error retrieving operators: {e}")
            return False
        finally:
            if 'conn' in locals():
                conn.close()
    
    def test_database_connection():
        """Test basic database connection"""
        try:
            conn = get_conn()
            with closing(conn.cursor()) as cursor:
                cursor.execute("SELECT COUNT(*) FROM logs")
                count = cursor.fetchone()[0]
                print(f"✅ Database connection successful. Total entries: {count}")
                return True
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            return False
        finally:
            if 'conn' in locals():
                conn.close()
    
    if __name__ == "__main__":
        print("🧪 Testing Enhanced User Filtering Components")
        print("=" * 50)
        
        # Test database connection
        if test_database_connection():
            # Test operator query
            test_operator_query()
        else:
            print("Cannot proceed with operator testing due to database connection failure")
        
        print("\n✨ User filtering test completed!")

except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please ensure all required modules are available")
except Exception as e:
    print(f"❌ Unexpected error: {e}")