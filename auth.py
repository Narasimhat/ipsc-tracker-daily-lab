"""
Simple Authentication System for iPSC Tracker
Bypasses streamlit-authenticator complexity for reliable demo
"""

import streamlit as st

def require_authentication():
    """
    Simple authentication that definitely works
    """
    
    # Check if user is already logged in
    if st.session_state.get("authenticated"):
        return True
    
    # Show login form
    st.title("🔐 iPSC Tracker Login")
    st.write("Professional Laboratory Information Management System")
    
    # Login form
    with st.form("login_form"):
        st.write("### Please log in to continue")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_button = st.form_submit_button("🚀 Login")
        
        if login_button:
            # Check credentials
            if username in ["admin", "demo"] and password == "demo123":
                # Set session state
                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.name = "Admin User" if username == "admin" else "Demo User"
                st.session_state.user_role = "admin"
                st.session_state.user_email = f"{username}@lab.org"
                st.session_state.user_team = "Management" if username == "admin" else "General"
                
                st.success("✅ Login successful!")
                st.balloons()
                st.rerun()
            else:
                st.error("❌ Invalid username or password")
                st.info("💡 Demo credentials: admin/demo123 or demo/demo123")
    
    # Show demo credentials
    st.info("🔑 **Demo Credentials:**")
    col1, col2 = st.columns(2)
    with col1:
        st.code("Username: admin\nPassword: demo123")
    with col2:
        st.code("Username: demo\nPassword: demo123")
    
    st.warning("⚠️ Please enter your credentials above to continue")
    st.stop()

def get_current_user():
    return st.session_state.get("username", None)

def get_current_user_display_name():
    return st.session_state.get("name", "Unknown User")

def get_current_user_role():
    return st.session_state.get("user_role", "member")

def is_admin():
    return st.session_state.get("user_role") == "admin"

def is_pro_user():
    role = st.session_state.get("user_role", "member")
    return role in ["admin", "pro"]

def require_admin():
    if not st.session_state.get("authenticated"):
        st.error("❌ Authentication required")
        st.stop()
    
    if not is_admin():
        st.error("❌ Admin access required")
        st.stop()

def require_pro():
    if not st.session_state.get("authenticated"):
        st.error("❌ Authentication required")
        st.stop()
    
    if not is_pro_user():
        st.error("❌ Pro features required")
        st.stop()

# Add logout functionality to sidebar
def show_user_info():
    """Show user info and logout in sidebar"""
    if st.session_state.get("authenticated"):
        with st.sidebar:
            st.success(f"👋 Hi, {get_current_user_display_name()}")
            st.caption(f"Role: {get_current_user_role().title()}")
            if st.session_state.get('user_team'):
                st.caption(f"Team: {st.session_state.user_team}")
            
            st.markdown("---")
            if st.button("🚪 Logout"):
                # Clear session state
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()

# For compatibility with existing imports
def get_user_team(username):
    if username == st.session_state.get("username"):
        return st.session_state.get("user_team")
    return None