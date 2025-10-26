import streamlit as st
import sys
import os

st.title("🧪 iPSC Tracker Diagnostic Test")

try:
    st.write("✅ Streamlit imported successfully")
    
    # Test basic database import
    sys.path.append(os.path.dirname(__file__))
    import db
    st.write("✅ Database module imported successfully")
    
    # Test database connection
    conn = db.get_conn()
    st.write("✅ Database connection established")
    
    # Test a simple query
    import contextlib
    with contextlib.closing(conn.cursor()) as cur:
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cur.fetchall()
        st.write(f"✅ Found {len(tables)} database tables")
        for table in tables:
            st.write(f"  - {table[0]}")
    
    conn.close()
    st.write("✅ Database connection closed")
    
    st.success("🎉 All basic tests passed! iPSC Tracker should work.")
    
except Exception as e:
    st.error(f"❌ Error: {str(e)}")
    import traceback
    st.code(traceback.format_exc())