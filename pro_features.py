"""
Pro Features for iPSC Tracker
Advanced analytics, reporting, and experimental tracking for Pro users
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, date, timedelta
from auth import require_pro, get_current_user, is_pro_user
from db import get_conn, query_logs, get_vial_lifecycle, get_experimental_journey, get_experiment_types

def show_pro_features():
    """Display pro features interface"""
    require_pro()  # Only pro users can access
    
    st.title("⭐ Pro Features")
    st.write("Advanced analytics and experimental tracking for professional users")
    
    # Pro feature tabs
    pro_tab1, pro_tab2, pro_tab3, pro_tab4 = st.tabs([
        "📊 Advanced Analytics",
        "🧬 Experimental Tracking",
        "📈 Performance Metrics",
        "📤 Bulk Operations"
    ])
    
    with pro_tab1:
        show_advanced_analytics()
    
    with pro_tab2:
        show_experimental_tracking()
    
    with pro_tab3:
        show_performance_metrics()
    
    with pro_tab4:
        show_bulk_operations()

def show_advanced_analytics():
    """Advanced analytics dashboard"""
    st.subheader("📊 Advanced Analytics Dashboard")
    
    conn = get_conn()
    
    # Time range selector
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", value=date.today() - timedelta(days=90))
    with col2:
        end_date = st.date_input("End Date", value=date.today())
    
    # Get data
    logs = query_logs(conn, start_date=start_date, end_date=end_date)
    
    if not logs:
        st.warning("No data available for the selected date range")
        return
    
    df = pd.DataFrame(logs)
    df['date'] = pd.to_datetime(df['date'])
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_entries = len(df)
        st.metric("Total Entries", total_entries)
    
    with col2:
        unique_cell_lines = df['cell_line'].nunique()
        st.metric("Cell Lines", unique_cell_lines)
    
    with col3:
        unique_operators = df['operator'].nunique()
        st.metric("Active Users", unique_operators)
    
    with col4:
        splits = len(df[df['event_type'] == 'Split'])
        st.metric("Total Splits", splits)
    
    # Advanced visualizations
    st.subheader("📈 Trend Analysis")
    
    # Activity heatmap
    if len(df) > 0:
        # Prepare data for heatmap
        df['week'] = df['date'].dt.isocalendar().week
        df['weekday'] = df['date'].dt.day_name()
        
        # Create pivot table for heatmap
        heatmap_data = df.groupby(['week', 'weekday']).size().unstack(fill_value=0)
        
        # Reorder days
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        heatmap_data = heatmap_data.reindex(columns=day_order, fill_value=0)
        
        # Plot heatmap
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.heatmap(heatmap_data, annot=True, fmt='d', cmap='YlOrRd', ax=ax)
        ax.set_title('Activity Heatmap (Entries per Week/Day)')
        ax.set_xlabel('Day of Week')
        ax.set_ylabel('Week Number')
        st.pyplot(fig)
    
    # Experimental success rates
    st.subheader("🧪 Experimental Success Analysis")
    
    # Get experimental data
    exp_data = df[df['experiment_type'].notna()]
    if len(exp_data) > 0:
        # Success rate by experiment type
        success_analysis = exp_data.groupby('experiment_type')['outcome_status'].apply(
            lambda x: (x == 'Successful').sum() / len(x) * 100 if len(x) > 0 else 0
        ).sort_values(ascending=False)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Success Rates by Experiment Type:**")
            for exp_type, success_rate in success_analysis.items():
                st.write(f"• {exp_type}: {success_rate:.1f}%")
        
        with col2:
            # Experiment type distribution
            exp_counts = exp_data['experiment_type'].value_counts()
            fig, ax = plt.subplots(figsize=(8, 6))
            exp_counts.plot(kind='pie', ax=ax, autopct='%1.1f%%')
            ax.set_title('Experiment Type Distribution')
            st.pyplot(fig)
    
    # Passage analysis
    st.subheader("📊 Passage Analysis")
    
    passage_data = df[df['passage'].notna()]
    if len(passage_data) > 0:
        col1, col2 = st.columns(2)
        
        with col1:
            # Passage distribution
            fig, ax = plt.subplots(figsize=(8, 6))
            passage_data['passage'].hist(bins=20, ax=ax)
            ax.set_title('Passage Number Distribution')
            ax.set_xlabel('Passage Number')
            ax.set_ylabel('Frequency')
            st.pyplot(fig)
        
        with col2:
            # Average passage by cell line
            avg_passage = passage_data.groupby('cell_line')['passage'].mean().sort_values(ascending=False)
            st.write("**Average Passage by Cell Line:**")
            for cell_line, avg_pass in avg_passage.head(10).items():
                st.write(f"• {cell_line}: P{avg_pass:.1f}")

def show_experimental_tracking():
    """Advanced experimental tracking and analysis"""
    st.subheader("🧬 Experimental Tracking Dashboard")
    
    conn = get_conn()
    
    # Experiment type selector
    try:
        experiment_types = get_experiment_types(conn)
        exp_names = [exp['name'] for exp in experiment_types]
        
        selected_exp = st.selectbox("Select Experiment Type", options=["All"] + exp_names)
        
        # Get experimental data
        logs = query_logs(conn)
        exp_logs = [log for log in logs if log.get('experiment_type')]
        
        if selected_exp != "All":
            exp_logs = [log for log in exp_logs if log.get('experiment_type') == selected_exp]
        
        if not exp_logs:
            st.warning("No experimental data found")
            return
        
        # Experimental overview
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_experiments = len(set(log.get('thaw_id') for log in exp_logs if log.get('thaw_id')))
            st.metric("Active Experiments", total_experiments)
        
        with col2:
            successful = len([log for log in exp_logs if log.get('outcome_status') == 'Successful'])
            st.metric("Successful", successful)
        
        with col3:
            failed = len([log for log in exp_logs if log.get('outcome_status') == 'Failed'])
            st.metric("Failed", failed)
        
        with col4:
            in_progress = len([log for log in exp_logs if log.get('outcome_status') == 'In Progress'])
            st.metric("In Progress", in_progress)
        
        # Experimental timeline
        st.subheader("🕒 Experimental Timeline")
        
        df_exp = pd.DataFrame(exp_logs)
        df_exp['date'] = pd.to_datetime(df_exp['date'])
        
        # Timeline chart
        timeline_data = df_exp.groupby(['date', 'experiment_type']).size().unstack(fill_value=0)
        
        fig, ax = plt.subplots(figsize=(12, 6))
        timeline_data.plot(kind='line', ax=ax, marker='o')
        ax.set_title('Experimental Activity Timeline')
        ax.set_xlabel('Date')
        ax.set_ylabel('Number of Experiments')
        ax.legend(title='Experiment Type')
        plt.xticks(rotation=45)
        st.pyplot(fig)
        
        # Detailed experimental journeys
        st.subheader("🗺️ Experimental Journeys")
        
        # Get unique thaw IDs with experiments
        thaw_ids = list(set(log.get('thaw_id') for log in exp_logs if log.get('thaw_id')))
        
        if thaw_ids:
            selected_thaw = st.selectbox("Select Thaw ID for Detailed Journey", thaw_ids)
            
            if selected_thaw:
                journey = get_experimental_journey(conn, selected_thaw)
                
                if journey and journey.get('experimental_phases'):
                    for exp_type, phase_data in journey['experimental_phases'].items():
                        with st.expander(f"🧪 {exp_type} - {phase_data['duration_days']} days"):
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.write(f"**Start Date:** {phase_data['start_date']}")
                                st.write(f"**End Date:** {phase_data['end_date']}")
                                st.write(f"**Duration:** {phase_data['duration_days']} days")
                                st.write(f"**Status:** {'✅ Completed' if phase_data['is_completed'] else '🔄 In Progress'}")
                            
                            with col2:
                                st.write(f"**Stages:** {', '.join(phase_data['stages'])}")
                                st.write(f"**Total Events:** {phase_data['total_events']}")
                                if phase_data['success_metrics']:
                                    st.write(f"**Success Metrics:** {', '.join(phase_data['success_metrics'])}")
    
    except Exception as e:
        st.error(f"Error in experimental tracking: {e}")

def show_performance_metrics():
    """Performance metrics and KPIs"""
    st.subheader("📈 Performance Metrics & KPIs")
    
    conn = get_conn()
    logs = query_logs(conn)
    
    if not logs:
        st.warning("No data available")
        return
    
    df = pd.DataFrame(logs)
    df['date'] = pd.to_datetime(df['date'])
    
    # Performance metrics
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### 🎯 Lab Efficiency Metrics")
        
        # Entries per day
        daily_entries = df.groupby(df['date'].dt.date).size()
        avg_daily = daily_entries.mean()
        st.metric("Avg Daily Entries", f"{avg_daily:.1f}")
        
        # Split frequency
        splits = df[df['event_type'] == 'Split']
        if len(splits) > 0:
            split_intervals = []
            for thaw_id in df['thaw_id'].unique():
                if pd.isna(thaw_id):
                    continue
                thaw_splits = splits[splits['thaw_id'] == thaw_id].sort_values('date')
                if len(thaw_splits) > 1:
                    for i in range(1, len(thaw_splits)):
                        interval = (thaw_splits.iloc[i]['date'] - thaw_splits.iloc[i-1]['date']).days
                        split_intervals.append(interval)
            
            if split_intervals:
                avg_interval = sum(split_intervals) / len(split_intervals)
                st.metric("Avg Split Interval (days)", f"{avg_interval:.1f}")
        
        # User productivity
        user_productivity = df.groupby('operator').size().sort_values(ascending=False)
        st.write("**Top Contributors:**")
        for operator, count in user_productivity.head(5).items():
            st.write(f"• {operator}: {count} entries")
    
    with col2:
        st.write("### 🧬 Culture Success Metrics")
        
        # Contamination rate (approximation)
        contamination_keywords = ['contamination', 'contaminated', 'bacteria', 'fungus']
        contaminated = df[df['notes'].str.contains('|'.join(contamination_keywords), case=False, na=False)]
        contamination_rate = len(contaminated) / len(df) * 100
        st.metric("Contamination Rate", f"{contamination_rate:.2f}%")
        
        # Successful thaws
        thaws = df[df['event_type'] == 'Thawing']
        successful_thaws = 0
        for thaw_id in thaws['thaw_id'].unique():
            if pd.isna(thaw_id):
                continue
            thaw_events = df[df['thaw_id'] == thaw_id]
            # Consider successful if there are follow-up events
            if len(thaw_events) > 1:
                successful_thaws += 1
        
        if len(thaws) > 0:
            success_rate = successful_thaws / len(thaws) * 100
            st.metric("Thaw Success Rate", f"{success_rate:.1f}%")
        
        # Cell line diversity
        unique_lines = df['cell_line'].nunique()
        st.metric("Active Cell Lines", unique_lines)
    
    # Trend analysis
    st.subheader("📊 Trend Analysis")
    
    # Monthly activity trend
    monthly_activity = df.groupby(df['date'].dt.to_period('M')).size()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    monthly_activity.plot(kind='line', ax=ax, marker='o')
    ax.set_title('Monthly Lab Activity Trend')
    ax.set_xlabel('Month')
    ax.set_ylabel('Number of Entries')
    plt.xticks(rotation=45)
    st.pyplot(fig)
    
    # Event type trends
    event_trends = df.groupby([df['date'].dt.to_period('M'), 'event_type']).size().unstack(fill_value=0)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    event_trends.plot(kind='area', ax=ax, alpha=0.7)
    ax.set_title('Event Type Trends Over Time')
    ax.set_xlabel('Month')
    ax.set_ylabel('Number of Events')
    ax.legend(title='Event Type', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xticks(rotation=45)
    st.pyplot(fig)

def show_bulk_operations():
    """Bulk operations for data management"""
    st.subheader("📤 Bulk Operations")
    
    # Bulk export options
    st.write("### 📊 Advanced Export Options")
    
    conn = get_conn()
    
    # Export filters
    col1, col2 = st.columns(2)
    
    with col1:
        # Date range
        export_start = st.date_input("Export Start Date", value=date.today() - timedelta(days=90))
        export_end = st.date_input("Export End Date", value=date.today())
        
        # Cell line filter
        logs = query_logs(conn)
        cell_lines = sorted(set(log.get('cell_line', '') for log in logs if log.get('cell_line')))
        selected_lines = st.multiselect("Filter by Cell Lines", cell_lines)
    
    with col2:
        # Event type filter
        event_types = sorted(set(log.get('event_type', '') for log in logs if log.get('event_type')))
        selected_events = st.multiselect("Filter by Event Types", event_types)
        
        # Format options
        export_format = st.selectbox("Export Format", [
            "Excel (Detailed)",
            "Excel (Summary)",
            "CSV (Raw Data)",
            "JSON (API Format)",
            "PDF (Report)"
        ])
    
    # Generate export
    if st.button("Generate Export"):
        try:
            # Apply filters
            filtered_logs = query_logs(conn, start_date=export_start, end_date=export_end)
            
            if selected_lines:
                filtered_logs = [log for log in filtered_logs if log.get('cell_line') in selected_lines]
            
            if selected_events:
                filtered_logs = [log for log in filtered_logs if log.get('event_type') in selected_events]
            
            if not filtered_logs:
                st.warning("No data matches the selected filters")
                return
            
            df = pd.DataFrame(filtered_logs)
            
            # Generate export based on format
            if export_format == "Excel (Detailed)":
                from io import BytesIO
                buffer = BytesIO()
                
                with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                    # Raw data sheet
                    df.to_excel(writer, sheet_name='Raw_Data', index=False)
                    
                    # Summary sheet
                    summary = {
                        'Total Entries': len(df),
                        'Date Range': f"{export_start} to {export_end}",
                        'Cell Lines': df['cell_line'].nunique(),
                        'Event Types': df['event_type'].nunique(),
                        'Operators': df['operator'].nunique()
                    }
                    summary_df = pd.DataFrame(list(summary.items()), columns=['Metric', 'Value'])
                    summary_df.to_excel(writer, sheet_name='Summary', index=False)
                    
                    # Statistics sheet
                    if 'passage' in df.columns:
                        passage_stats = df.groupby('cell_line')['passage'].agg(['count', 'mean', 'max']).reset_index()
                        passage_stats.to_excel(writer, sheet_name='Passage_Stats', index=False)
                
                st.download_button(
                    label="Download Excel File",
                    data=buffer.getvalue(),
                    file_name=f"ipsc_tracker_detailed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            
            elif export_format == "CSV (Raw Data)":
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV File",
                    data=csv,
                    file_name=f"ipsc_tracker_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            
            elif export_format == "JSON (API Format)":
                json_data = df.to_json(orient='records', indent=2, date_format='iso')
                st.download_button(
                    label="Download JSON File",
                    data=json_data,
                    file_name=f"ipsc_tracker_api_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
            
            st.success(f"Export generated with {len(filtered_logs)} entries")
        
        except Exception as e:
            st.error(f"Export failed: {e}")
    
    # Bulk data operations
    st.write("### 🔧 Bulk Data Operations")
    
    with st.expander("⚠️ Advanced Operations (Use with Caution)"):
        st.warning("These operations can affect multiple records. Use carefully.")
        
        # Bulk update operations
        st.write("**Bulk Update Operations:**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            update_field = st.selectbox("Field to Update", [
                "operator", "location", "medium", "cell_type"
            ])
            old_value = st.text_input("Current Value")
            new_value = st.text_input("New Value")
        
        with col2:
            if st.button("Preview Update"):
                if old_value and new_value:
                    # Count affected records
                    affected = [log for log in logs if log.get(update_field) == old_value]
                    st.info(f"Would update {len(affected)} records")
                    
                    # Show sample records
                    if affected:
                        sample_df = pd.DataFrame(affected[:5])
                        st.write("Sample affected records:")
                        st.dataframe(sample_df[['date', 'cell_line', 'event_type', update_field]])

if __name__ == "__main__":
    show_pro_features()