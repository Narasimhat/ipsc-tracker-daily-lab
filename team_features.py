"""
Team Features for iPSC Tracker
Team-based data filtering and collaboration features
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
from auth import get_current_user, get_user_team, is_admin, is_pro_user
from db import get_conn, query_logs

def apply_team_filter(logs, user_info=None):
    """Apply team-based filtering to logs based on user permissions"""
    if not user_info:
        user_info = get_current_user()
    
    if not user_info:
        return []
    
    # Admins see everything
    if is_admin():
        return logs
    
    # Get user's team - user_info is now a string (username)
    user_team = get_user_team(user_info)
    
    if not user_team:
        # If no team assigned, user only sees their own data
        return [log for log in logs if log.get('operator') == user_info]
    
    # Filter by team members
    team_members = get_team_members(user_team)
    return [log for log in logs if log.get('operator') in team_members]

def get_team_members(team_name):
    """Get list of all members in a team"""
    # This would typically query a teams table in the database
    # For now, we'll use a simple mapping
    team_mappings = {
        'iPSC Team': ['admin', 'researcher1', 'researcher2'],
        'Differentiation Team': ['researcher3', 'researcher4'],
        'Analytics Team': ['analyst1', 'analyst2'],
    }
    
    return team_mappings.get(team_name, [])

def show_team_dashboard():
    """Display team collaboration dashboard"""
    st.title("👥 Team Dashboard")
    
    user_info = get_current_user()
    if not user_info:
        st.error("User not authenticated")
        return
    
    # Fix: get_current_user() returns a string, not a dict
    user_team = get_user_team(user_info)
    
    # Team overview
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Your Team", user_team or "No Team")
    
    with col2:
        if user_team:
            team_members = get_team_members(user_team)
            st.metric("Team Size", len(team_members))
        else:
            st.metric("Team Size", "N/A")
    
    with col3:
        # Team activity (last 7 days)
        conn = get_conn()
        recent_logs = query_logs(conn, start_date=date.today() - timedelta(days=7))
        team_logs = apply_team_filter(recent_logs, user_info)
        st.metric("Team Activity (7d)", len(team_logs))
    
    # Team activity tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Team Activity",
        "🧬 Shared Experiments",
        "📈 Team Performance",
        "💬 Collaboration"
    ])
    
    with tab1:
        show_team_activity(user_info)
    
    with tab2:
        show_shared_experiments(user_info)
    
    with tab3:
        show_team_performance(user_info)
    
    with tab4:
        show_collaboration_features(user_info)

def show_team_activity(user_info):
    """Show team activity overview"""
    st.subheader("📊 Team Activity Overview")
    
    conn = get_conn()
    user_team = get_user_team(user_info)
    
    if not user_team:
        st.warning("You are not assigned to a team. Contact an administrator.")
        return
    
    # Date range selector
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", value=date.today() - timedelta(days=30))
    with col2:
        end_date = st.date_input("End Date", value=date.today())
    
    # Get team data
    logs = query_logs(conn, start_date=start_date, end_date=end_date)
    team_logs = apply_team_filter(logs, user_info)
    
    if not team_logs:
        st.info("No team activity in the selected date range")
        return
    
    df = pd.DataFrame(team_logs)
    df['date'] = pd.to_datetime(df['date'])
    
    # Team member activity breakdown
    st.write("### 👨‍🔬 Team Member Activity")
    
    member_activity = df.groupby('operator').agg({
        'id': 'count',
        'event_type': lambda x: x.value_counts().index[0] if len(x) > 0 else 'N/A',
        'date': ['min', 'max']
    }).round(2)
    
    member_activity.columns = ['Total Entries', 'Most Common Event', 'First Entry', 'Last Entry']
    st.dataframe(member_activity)
    
    # Team activity timeline
    st.write("### 📅 Team Activity Timeline")
    
    daily_activity = df.groupby([df['date'].dt.date, 'operator']).size().unstack(fill_value=0)
    st.line_chart(daily_activity)
    
    # Event type distribution
    st.write("### 🔬 Event Type Distribution")
    
    col1, col2 = st.columns(2)
    
    with col1:
        event_counts = df['event_type'].value_counts()
        st.bar_chart(event_counts)
    
    with col2:
        st.write("**Event Summary:**")
        for event_type, count in event_counts.items():
            percentage = (count / len(df)) * 100
            st.write(f"• {event_type}: {count} ({percentage:.1f}%)")

def show_shared_experiments(user_info):
    """Show shared experiments within the team"""
    st.subheader("🧬 Shared Experiments")
    
    conn = get_conn()
    logs = query_logs(conn)
    team_logs = apply_team_filter(logs, user_info)
    
    # Find experiments with multiple contributors
    df = pd.DataFrame(team_logs)
    
    if 'thaw_id' not in df.columns or df['thaw_id'].isna().all():
        st.info("No shared experiments found")
        return
    
    # Group by thaw_id to find collaborative experiments
    thaw_groups = df.groupby('thaw_id')['operator'].nunique()
    collaborative_thaws = thaw_groups[thaw_groups > 1].index.tolist()
    
    if not collaborative_thaws:
        st.info("No collaborative experiments found in your team")
        return
    
    st.write(f"Found {len(collaborative_thaws)} collaborative experiments")
    
    # Show collaborative experiments
    for thaw_id in collaborative_thaws:
        thaw_data = df[df['thaw_id'] == thaw_id].sort_values('date')
        
        with st.expander(f"🧪 Experiment: {thaw_id}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Cell Line:** {thaw_data['cell_line'].iloc[0]}")
                
                # Fix date handling - convert to datetime if they're strings
                try:
                    if isinstance(thaw_data['date'].iloc[0], str):
                        thaw_data['date'] = pd.to_datetime(thaw_data['date'])
                    duration = (thaw_data['date'].max() - thaw_data['date'].min()).days
                    st.write(f"**Duration:** {duration} days")
                except Exception as e:
                    st.write(f"**Duration:** Unable to calculate")
                
                st.write(f"**Total Events:** {len(thaw_data)}")
                
                contributors = thaw_data['operator'].unique()
                st.write(f"**Contributors:** {', '.join(contributors)}")
            
            with col2:
                # Timeline of events
                timeline = thaw_data[['date', 'operator', 'event_type']].copy()
                timeline['date'] = timeline['date'].dt.strftime('%Y-%m-%d')
                st.write("**Timeline:**")
                
                for _, row in timeline.iterrows():
                    st.write(f"• {row['date']}: {row['event_type']} ({row['operator']})")

def show_team_performance(user_info):
    """Show team performance metrics"""
    st.subheader("📈 Team Performance Metrics")
    
    if not is_pro_user():
        st.warning("Team performance metrics are available for Pro users")
        return
    
    conn = get_conn()
    user_team = get_user_team(user_info)
    
    if not user_team:
        st.warning("No team assigned")
        return
    
    # Get team data for last 90 days
    logs = query_logs(conn, start_date=date.today() - timedelta(days=90))
    team_logs = apply_team_filter(logs, user_info)
    
    if not team_logs:
        st.info("No team data available")
        return
    
    df = pd.DataFrame(team_logs)
    df['date'] = pd.to_datetime(df['date'])
    
    # Performance metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_daily = len(df) / 90
        st.metric("Avg Daily Entries", f"{avg_daily:.1f}")
    
    with col2:
        active_lines = df['cell_line'].nunique()
        st.metric("Active Cell Lines", active_lines)
    
    with col3:
        experiments = df[df['experiment_type'].notna()]['thaw_id'].nunique()
        st.metric("Active Experiments", experiments)
    
    with col4:
        team_members = get_team_members(user_team)
        productivity = len(df) / len(team_members) if team_members else 0
        st.metric("Productivity/Member", f"{productivity:.1f}")
    
    # Team efficiency trends
    st.write("### 📊 Efficiency Trends")
    
    # Weekly productivity
    weekly_data = df.groupby([df['date'].dt.to_period('W'), 'operator']).size().unstack(fill_value=0)
    
    if not weekly_data.empty:
        st.line_chart(weekly_data)
    
    # Individual performance comparison
    st.write("### 👤 Individual Performance (Last 30 Days)")
    
    recent_df = df[df['date'] >= datetime.now() - timedelta(days=30)]
    individual_stats = recent_df.groupby('operator').agg({
        'id': 'count',
        'cell_line': 'nunique',
        'event_type': lambda x: len(set(x))
    })
    individual_stats.columns = ['Total Entries', 'Cell Lines Worked', 'Event Types Used']
    
    st.dataframe(individual_stats)

def show_collaboration_features(user_info):
    """Show collaboration and communication features"""
    st.subheader("💬 Team Collaboration")
    
    user_team = get_user_team(user_info)
    
    if not user_team:
        st.warning("No team assigned for collaboration features")
        return
    
    # Team announcements section
    st.write("### 📢 Team Announcements")
    
    # In a real implementation, this would connect to a database
    announcements = [
        {
            'date': '2024-01-15',
            'author': 'admin',
            'title': 'New Protocol Update',
            'message': 'Updated splitting protocol is now available. Please review before next passage.'
        },
        {
            'date': '2024-01-14',
            'author': 'researcher1',
            'title': 'Equipment Maintenance',
            'message': 'Incubator B will be under maintenance tomorrow 2-4 PM.'
        }
    ]
    
    for announcement in announcements:
        with st.expander(f"{announcement['date']} - {announcement['title']} (by {announcement['author']})"):
            st.write(announcement['message'])
    
    # Add new announcement (for admins and pros)
    if is_admin() or is_pro_user():
        st.write("### ➕ Add Team Announcement")
        
        with st.form("new_announcement"):
            ann_title = st.text_input("Title")
            ann_message = st.text_area("Message")
            
            if st.form_submit_button("Post Announcement"):
                if ann_title and ann_message:
                    # In real implementation, save to database
                    st.success("Announcement posted!")
                else:
                    st.error("Please fill in all fields")
    
    # Recent team activity feed
    st.write("### 🔄 Recent Team Activity")
    
    conn = get_conn()
    recent_logs = query_logs(conn, start_date=date.today() - timedelta(days=7))
    team_logs = apply_team_filter(recent_logs, user_info)
    
    if team_logs:
        # Sort by date descending
        sorted_logs = sorted(team_logs, key=lambda x: x['date'], reverse=True)
        
        for log in sorted_logs[:10]:  # Show last 10 activities
            log_date = pd.to_datetime(log['date']).strftime('%m/%d %H:%M')
            st.write(f"• {log_date} - {log['operator']}: {log['event_type']} on {log['cell_line']}")
    else:
        st.info("No recent team activity")
    
    # Team resources
    st.write("### 📚 Team Resources")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**📋 Shared Protocols:**")
        protocols = [
            "Standard iPSC Maintenance",
            "Differentiation Protocol v2.1",
            "Contamination Response",
            "Weekend Feeding Schedule"
        ]
        
        for protocol in protocols:
            if st.button(f"📄 {protocol}", key=f"protocol_{protocol}"):
                st.info(f"Opening {protocol}... (Feature in development)")
    
    with col2:
        st.write("**🔗 Quick Links:**")
        links = [
            ("Team Calendar", "https://calendar.example.com"),
            ("Shared Drive", "https://drive.example.com"),
            ("Protocol Wiki", "https://wiki.example.com"),
            ("Contact List", "https://contacts.example.com")
        ]
        
        for link_name, link_url in links:
            st.markdown(f"[🔗 {link_name}]({link_url})")

def get_team_filtered_data(table_name, user_info=None):
    """Get team-filtered data for any table"""
    if not user_info:
        user_info = get_current_user()
    
    if not user_info:
        return []
    
    conn = get_conn()
    
    if table_name == 'logs':
        logs = query_logs(conn)
        return apply_team_filter(logs, user_info)
    
    # For other tables, implement similar filtering logic
    return []

def show_team_selector():
    """Show team selector for admins"""
    if not is_admin():
        return None
    
    teams = ['All Teams', 'iPSC Team', 'Differentiation Team', 'Analytics Team']
    selected_team = st.selectbox("Filter by Team", teams)
    
    return selected_team if selected_team != 'All Teams' else None

if __name__ == "__main__":
    show_team_dashboard()