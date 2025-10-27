"""
Admin Panel for iPSC Tracker
Role-based administrative interface for user and system management
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
from auth import require_admin, get_current_user, is_admin, generate_password_hash
from db import get_conn, get_all_users, query_logs

def show_admin_panel():
    """Display the admin panel interface"""
    require_admin()  # Only admins can access
    
    st.title("🔧 Admin Panel")
    st.write("Administrative interface for iPSC Tracker management")
    
    # Admin tabs
    admin_tab1, admin_tab2, admin_tab3, admin_tab4 = st.tabs([
        "👥 User Management",
        "📊 System Analytics", 
        "🗄️ Data Management",
        "⚙️ System Settings"
    ])
    
    with admin_tab1:
        show_user_management()
    
    with admin_tab2:
        show_system_analytics()
    
    with admin_tab3:
        show_data_management()
    
    with admin_tab4:
        show_system_settings()

def show_user_management():
    """User management interface"""
    st.subheader("👥 User Management")
    
    # User overview
    try:
        users_data = []
        if hasattr(st, 'secrets') and 'users' in st.secrets:
            for username, user_info in st.secrets['users'].items():
                users_data.append({
                    'Username': username,
                    'Name': user_info.get('name', username),
                    'Email': user_info.get('email', ''),
                    'Role': user_info.get('role', 'member'),
                    'Team': user_info.get('team', ''),
                })
        
        if users_data:
            df_users = pd.DataFrame(users_data)
            st.dataframe(df_users, use_container_width=True)
            
            # User statistics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Users", len(users_data))
            with col2:
                admins = len([u for u in users_data if u['Role'] == 'admin'])
                st.metric("Admins", admins)
            with col3:
                members = len([u for u in users_data if u['Role'] == 'member'])
                st.metric("Members", members)
            with col4:
                teams = len(set(u['Team'] for u in users_data if u['Team']))
                st.metric("Teams", teams)
        else:
            st.info("No users configured in secrets.toml")
    
    except Exception as e:
        st.error(f"Error loading user data: {e}")
    
    # Password hash generator
    with st.expander("🔑 Generate Password Hash"):
        st.write("Generate bcrypt hashes for new user passwords")
        
        col1, col2 = st.columns(2)
        with col1:
            new_password = st.text_input("Password", type="password", key="admin_new_password")
        with col2:
            if st.button("Generate Hash") and new_password:
                try:
                    hash_value = generate_password_hash(new_password)
                    st.code(f'hashed_password = "{hash_value}"')
                    st.success("Copy this hash to your secrets.toml file")
                except Exception as e:
                    st.error(f"Error generating hash: {e}")
    
    # User activity
    with st.expander("📈 User Activity"):
        conn = get_conn()
        try:
            # Get activity data
            logs = query_logs(conn, start_date=date.today() - timedelta(days=30))
            if logs:
                df_logs = pd.DataFrame(logs)
                
                # Activity by user
                if 'operator' in df_logs.columns:
                    activity = df_logs.groupby('operator').size().sort_values(ascending=False)
                    st.bar_chart(activity)
                    
                    # Recent activity table
                    recent_activity = df_logs[['date', 'operator', 'event_type', 'cell_line']].tail(10)
                    st.write("Recent Activity (Last 10 entries):")
                    st.dataframe(recent_activity, use_container_width=True)
            else:
                st.info("No activity data available")
        except Exception as e:
            st.error(f"Error loading activity data: {e}")

def show_system_analytics():
    """System analytics and monitoring"""
    st.subheader("📊 System Analytics")
    
    conn = get_conn()
    
    try:
        # Database statistics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Total entries
            logs = query_logs(conn)
            st.metric("Total Log Entries", len(logs))
        
        with col2:
            # Active thaw IDs
            thaw_ids = set()
            for log in logs:
                if log.get('thaw_id'):
                    thaw_ids.add(log['thaw_id'])
            st.metric("Unique Thaw IDs", len(thaw_ids))
        
        with col3:
            # Unique cell lines
            cell_lines = set()
            for log in logs:
                if log.get('cell_line'):
                    cell_lines.add(log['cell_line'])
            st.metric("Unique Cell Lines", len(cell_lines))
        
        # Usage trends
        if logs:
            df_logs = pd.DataFrame(logs)
            df_logs['date'] = pd.to_datetime(df_logs['date'])
            
            # Daily activity chart
            st.subheader("📈 Daily Activity Trend")
            daily_counts = df_logs.groupby(df_logs['date'].dt.date).size()
            st.line_chart(daily_counts)
            
            # Event type distribution
            st.subheader("🔄 Event Type Distribution")
            if 'event_type' in df_logs.columns:
                event_counts = df_logs['event_type'].value_counts()
                st.bar_chart(event_counts)
            
            # Cell line usage
            st.subheader("🧬 Most Active Cell Lines")
            if 'cell_line' in df_logs.columns:
                cell_line_counts = df_logs['cell_line'].value_counts().head(10)
                st.bar_chart(cell_line_counts)
    
    except Exception as e:
        st.error(f"Error loading analytics: {e}")

def show_data_management():
    """Data management and backup interface"""
    st.subheader("🗄️ Data Management")
    
    # Database backup
    with st.expander("💾 Database Backup"):
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Create Backup"):
                try:
                    from db import backup_now
                    backup_path = backup_now()
                    st.success(f"Backup created: {backup_path}")
                except Exception as e:
                    st.error(f"Backup failed: {e}")
        
        with col2:
            st.info("Regular backups are recommended weekly")
    
    # Data export
    with st.expander("📤 Data Export"):
        export_format = st.selectbox("Export Format", ["Excel", "CSV", "JSON"])
        date_range = st.date_input("Date Range", value=[date.today() - timedelta(days=30), date.today()])
        
        if st.button("Export Data"):
            try:
                conn = get_conn()
                if len(date_range) == 2:
                    logs = query_logs(conn, start_date=date_range[0], end_date=date_range[1])
                else:
                    logs = query_logs(conn)
                
                if logs:
                    df = pd.DataFrame(logs)
                    
                    if export_format == "Excel":
                        # Create Excel export
                        from io import BytesIO
                        buffer = BytesIO()
                        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                            df.to_excel(writer, sheet_name='iPSC_Tracker_Data', index=False)
                        
                        st.download_button(
                            label="Download Excel File",
                            data=buffer.getvalue(),
                            file_name=f"ipsc_tracker_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                    
                    elif export_format == "CSV":
                        csv = df.to_csv(index=False)
                        st.download_button(
                            label="Download CSV File",
                            data=csv,
                            file_name=f"ipsc_tracker_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv"
                        )
                    
                    elif export_format == "JSON":
                        json_data = df.to_json(orient='records', indent=2)
                        st.download_button(
                            label="Download JSON File",
                            data=json_data,
                            file_name=f"ipsc_tracker_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                            mime="application/json"
                        )
                else:
                    st.warning("No data to export")
            
            except Exception as e:
                st.error(f"Export failed: {e}")
    
    # Data cleanup
    with st.expander("🧹 Data Cleanup"):
        st.warning("⚠️ Data cleanup operations cannot be undone")
        
        # Old entries cleanup
        cleanup_days = st.number_input("Delete entries older than (days)", min_value=30, value=365)
        
        if st.button("Preview Cleanup", key="preview_cleanup"):
            try:
                conn = get_conn()
                cutoff_date = date.today() - timedelta(days=cleanup_days)
                logs = query_logs(conn, end_date=cutoff_date)
                st.info(f"Would delete {len(logs)} entries older than {cutoff_date}")
            except Exception as e:
                st.error(f"Preview failed: {e}")

def show_system_settings():
    """System settings and configuration"""
    st.subheader("⚙️ System Settings")
    
    # Authentication settings
    with st.expander("🔐 Authentication Settings"):
        st.write("Current authentication configuration:")
        
        try:
            if hasattr(st, 'secrets') and 'cookie' in st.secrets:
                cookie_config = st.secrets['cookie']
                st.write(f"**Cookie Name:** {cookie_config.get('name', 'Not set')}")
                st.write(f"**Expiry Days:** {cookie_config.get('expiry_days', 'Not set')}")
                
                # Cookie key status (don't show the actual key)
                key = cookie_config.get('key', '')
                if key and key != "REPLACE_WITH_A_RANDOM_32_CHAR_SECRET_KEY_HERE":
                    st.success("✅ Cookie key is configured")
                else:
                    st.error("❌ Cookie key needs to be set")
            else:
                st.error("Authentication configuration not found")
        except Exception as e:
            st.error(f"Error reading auth config: {e}")
    
    # Database settings
    with st.expander("🗄️ Database Settings"):
        try:
            import os
            from db import DB_PATH, DATA_ROOT, IMAGES_DIR
            
            st.write(f"**Data Root:** {DATA_ROOT}")
            st.write(f"**Database Path:** {DB_PATH}")
            st.write(f"**Images Directory:** {IMAGES_DIR}")
            
            # Database size
            if os.path.exists(DB_PATH):
                db_size = os.path.getsize(DB_PATH) / (1024 * 1024)  # MB
                st.write(f"**Database Size:** {db_size:.2f} MB")
            
            # Images count
            if os.path.exists(IMAGES_DIR):
                image_files = [f for f in os.listdir(IMAGES_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
                st.write(f"**Stored Images:** {len(image_files)} files")
        
        except Exception as e:
            st.error(f"Error reading database settings: {e}")
    
    # Feature flags
    with st.expander("🚩 Feature Configuration"):
        st.write("Configure optional features:")
        
        # These would typically be stored in a config file or database
        experimental_features = st.checkbox("Enable Experimental Features", value=False)
        advanced_analytics = st.checkbox("Enable Advanced Analytics", value=True)
        team_filtering = st.checkbox("Enable Team-Based Filtering", value=True)
        
        if st.button("Save Feature Settings"):
            st.success("Feature settings saved (Note: Implement persistence)")
    
    # System information
    with st.expander("ℹ️ System Information"):
        st.write("**Application Version:** 2.0 - Professional Auth")
        st.write(f"**Current User:** {get_current_user()}")
        st.write(f"**Session Start:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        try:
            import streamlit as st_version
            st.write(f"**Streamlit Version:** {st_version.__version__}")
        except:
            st.write("**Streamlit Version:** Unknown")

if __name__ == "__main__":
    show_admin_panel()