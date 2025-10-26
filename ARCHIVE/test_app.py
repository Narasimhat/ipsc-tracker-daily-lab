import contextlib
import streamlit as st

st.title("Test App")
st.write("If you can see this, Streamlit is working!")
st.write("Database test:")

try:
    import db
    conn = db.get_conn()
    st.write("✅ Database connection successful")
    
    # Test a simple query
    with contextlib.closing(conn.cursor()) as cur:
        cur.execute("SELECT COUNT(*) FROM logs")
        count = cur.fetchone()[0]
        st.write(f"✅ Found {count} log entries")
    
    conn.close()
    st.write("✅ Database test completed successfully")
    
except Exception as e:
    st.error(f"❌ Database error: {str(e)}")
    import traceback
    st.code(traceback.format_exc())
