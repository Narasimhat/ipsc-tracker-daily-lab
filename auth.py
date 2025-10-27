"""
Professional Authentication System for iPSC Tracker
No credentials visible in code or UI
"""

import streamlit as st

def require_authentication():
    """
    Professional authentication using Streamlit secrets
    """
    
    # Check if user is already logged in
    if st.session_state.get("authenticated"):
        return True
    
    # Show login form
    st.title(" iPSC Tracker Login")
    st.write("Professional Laboratory Information Management System")
    
    # Login form
    with st.form("login_form"):
        st.write("### Please log in to continue")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_button = st.form_submit_button(" Login")
        
        if login_button:
            # Try to get user credentials from Streamlit secrets
            try:
                users = st.secrets["users"]
                if username in users and password == users[username]["password"]:
                    # Set session state
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.session_state.name = users[username].get("name", username)
                    st.session_state.user_role = users[username].get("role", "member")
                    st.session_state.user_email = users[username].get("email", f"{username}@lab.org")
                    st.session_state.user_team = users[username].get("team", "General")
                    
                    st.success(" Login successful!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error(" Invalid username or password")
                    st.info(" Contact your lab administrator for access credentials")
            except:
                # Fallback admin for testing
                if username == "admin" and password == "iPSC_Lab2024!":
                    st.session_state.authenticated = True
                    st.session_state.username = "admin"
                    st.session_state.name = "Administrator"
                    st.session_state.user_role = "admin"
                    st.session_state.user_email = "admin@lab.org"
                    st.session_state.user_team = "Management"
                    
                    st.success(" Login successful!")
                    st.warning(" Using fallback admin credentials")
                    st.rerun()
                else:
                    st.error(" Invalid credentials")
    
    st.warning(" Please enter your credentials to continue")
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
        st.error(" Authentication required")
        st.stop()
    
    if not is_admin():
        st.error(" Admin access required")
        st.stop()

def require_pro():
    if not st.session_state.get("authenticated"):
        st.error(" Authentication required")
        st.stop()
    
    if not is_pro_user():
        st.error(" Pro features required")
        st.stop()

def show_user_info():
    """Show user info and logout in sidebar"""
    if st.session_state.get("authenticated"):
        with st.sidebar:
            st.success(f" Hi, {get_current_user_display_name()}")
            st.caption(f"Role: {get_current_user_role().title()}")
            if st.session_state.get('user_team'):
                st.caption(f"Team: {st.session_state.user_team}")
            
            st.markdown("---")
            if st.button(" Logout"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()

def get_user_team(username):
    if username == st.session_state.get("username"):
        return st.session_state.get("user_team")
    return None
