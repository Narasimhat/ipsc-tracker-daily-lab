import os
import io
import contextlib
from datetime import date, datetime
import pandas as pd
import streamlit as st
from PIL import Image

from db import *

# Lab Book Formatting Functions
def generate_detailed_lab_format(df, include_options):
    """Generate detailed lab book format with full entry descriptions"""
    if df.empty:
        return "No entries to format."
    
    output = []
    output.append("=" * 60)
    output.append("iPSC CULTURE LOG ENTRIES")
    output.append("=" * 60)
    output.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    output.append(f"Total Entries: {len(df)}")
    output.append("")
    
    for idx, row in df.iterrows():
        output.append("-" * 40)
        output.append(f"ENTRY #{row.get('ID', 'N/A')}")
        output.append("-" * 40)
        
        # Date and basic info
        output.append(f"Date: {row.get('Date', 'N/A')}")
        output.append(f"Cell Line: {row.get('Cell Line', 'N/A')}")
        output.append(f"Event: {row.get('Event Type', 'N/A')}")
        
        # Conditional includes
        if "📊 Passage numbers" in include_options and row.get('Passage'):
            output.append(f"Passage: P{row.get('Passage', 'N/A')}")
        
        if "🧪 Vessels" in include_options and row.get('Vessel'):
            output.append(f"Vessel: {row.get('Vessel', 'N/A')}")
        
        if "📍 Locations" in include_options and row.get('Location'):
            output.append(f"Location: {row.get('Location', 'N/A')}")
        
        if row.get('Medium'):
            output.append(f"Medium: {row.get('Medium', 'N/A')}")
        
        if "👤 Operators" in include_options and row.get('Operator'):
            output.append(f"Operator: {row.get('Operator', 'N/A')}")
        
        if "🕒 Time stamps" in include_options and row.get('Created'):
            output.append(f"Time: {row.get('Created', 'N/A')}")
        
        # Notes section
        if "📝 Notes" in include_options and row.get('Notes'):
            output.append(f"Notes: {row.get('Notes', 'None')}")
        
        output.append("")
    
    return "\n".join(output)

def generate_compact_format(df, include_options):
    """Generate compact summary format for quick lab book entries"""
    if df.empty:
        return "No entries to format."
    
    output = []
    output.append(f"iPSC Culture Summary - {datetime.now().strftime('%Y-%m-%d')}")
    output.append("=" * 50)
    output.append("")
    
    for idx, row in df.iterrows():
        line_parts = []
        
        # Basic info
        line_parts.append(f"{row.get('Date', 'N/A')}")
        line_parts.append(f"{row.get('Cell Line', 'N/A')}")
        line_parts.append(f"{row.get('Event Type', 'N/A')}")
        
        # Conditional info
        if "📊 Passage numbers" in include_options and row.get('Passage'):
            line_parts.append(f"P{row.get('Passage')}")
        
        if "🧪 Vessels" in include_options and row.get('Vessel'):
            line_parts.append(f"[{row.get('Vessel')}]")
        
        if "📍 Locations" in include_options and row.get('Location'):
            line_parts.append(f"@{row.get('Location')}")
        
        if "👤 Operators" in include_options and row.get('Operator'):
            line_parts.append(f"by {row.get('Operator')}")
        
        # Join with separators
        entry_line = " | ".join(line_parts)
        output.append(f"• {entry_line}")
        
        # Add notes on next line if included
        if "📝 Notes" in include_options and row.get('Notes'):
            output.append(f"  └─ {row.get('Notes')}")
        
        output.append("")
    
    return "\n".join(output)

def generate_table_format(df, include_options):
    """Generate table format for structured lab book entries"""
    if df.empty:
        return "No entries to format."
    
    output = []
    output.append(f"iPSC Culture Log Table - {datetime.now().strftime('%Y-%m-%d')}")
    output.append("=" * 80)
    output.append("")
    
    # Create header
    headers = ["Date", "Cell Line", "Event"]
    if "📊 Passage numbers" in include_options:
        headers.append("Pass.")
    if "🧪 Vessels" in include_options:
        headers.append("Vessel")
    if "📍 Locations" in include_options:
        headers.append("Location")
    if "👤 Operators" in include_options:
        headers.append("Operator")
    
    # Calculate column widths
    col_widths = [max(12, len(h)) for h in headers]
    
    # Add header row
    header_row = " | ".join(h.ljust(w) for h, w in zip(headers, col_widths))
    output.append(header_row)
    output.append("-" * len(header_row))
    
    # Add data rows
    for idx, row in df.iterrows():
        row_data = [
            str(row.get('Date', 'N/A'))[:col_widths[0]],
            str(row.get('Cell Line', 'N/A'))[:col_widths[1]],
            str(row.get('Event Type', 'N/A'))[:col_widths[2]]
        ]
        
        col_idx = 3
        if "📊 Passage numbers" in include_options:
            row_data.append(f"P{row.get('Passage', 'N/A')}"[:col_widths[col_idx]])
            col_idx += 1
        if "🧪 Vessels" in include_options:
            row_data.append(str(row.get('Vessel', 'N/A'))[:col_widths[col_idx]])
            col_idx += 1
        if "📍 Locations" in include_options:
            row_data.append(str(row.get('Location', 'N/A'))[:col_widths[col_idx]])
            col_idx += 1
        if "👤 Operators" in include_options:
            row_data.append(str(row.get('Operator', 'N/A'))[:col_widths[col_idx]])
            col_idx += 1
        
        data_row = " | ".join(d.ljust(w) for d, w in zip(row_data, col_widths))
        output.append(data_row)
        
        # Add notes as separate row if included
        if "📝 Notes" in include_options and row.get('Notes'):
            notes_line = f"  Notes: {row.get('Notes')}"
            output.append(notes_line)
            output.append("")
    
    return "\n".join(output)

def generate_simple_list_format(df, include_options):
    """Generate simple bullet-point list format"""
    if df.empty:
        return "No entries to format."
    
    output = []
    output.append(f"iPSC Culture Activities - {datetime.now().strftime('%Y-%m-%d')}")
    output.append("")
    
    for idx, row in df.iterrows():
        # Basic entry
        entry = f"• {row.get('Date', 'N/A')}: {row.get('Event Type', 'N/A')} - {row.get('Cell Line', 'N/A')}"
        
        # Add additional details
        details = []
        if "📊 Passage numbers" in include_options and row.get('Passage'):
            details.append(f"P{row.get('Passage')}")
        if "🧪 Vessels" in include_options and row.get('Vessel'):
            details.append(row.get('Vessel'))
        if "📍 Locations" in include_options and row.get('Location'):
            details.append(row.get('Location'))
        if "👤 Operators" in include_options and row.get('Operator'):
            details.append(f"({row.get('Operator')})")
        
        if details:
            entry += f" [{', '.join(details)}]"
        
        output.append(entry)
        
        # Add notes if included
        if "📝 Notes" in include_options and row.get('Notes'):
            output.append(f"  └ {row.get('Notes')}")
    
    output.append("")
    output.append(f"Total entries: {len(df)}")
    
    return "\n".join(output)
    list_distinct_thaw_ids,
    get_active_thaw_options,
    get_thaw_latest_info,
    list_distinct_values,
    get_last_log_for_cell_line,
    predict_next_passage,
    top_values,
    suggest_next_event,
    get_ref_values,
    add_ref_value,
    delete_ref_value,
    rename_ref_value,
    backup_now,
    get_last_log_for_line_event,
    get_recent_logs_for_cell_line,
    save_weekend_schedule,
    get_weekend_schedules,
    delete_weekend_schedule,
    get_weekend_assignee,
    save_user_caliber,
    get_user_calibers,
    save_custom_weekend_work,
    get_custom_weekend_work,
    delete_custom_weekend_work,
    get_or_create_user,
    get_all_users,
    delete_user,
    delete_log,
    update_log,
    update_log_field,
    get_log_by_id,
    get_template_entries,
    get_recent_entries_by_operator,
    get_entries_by_pattern,
    save_entry_template,
    get_entry_templates,
    increment_template_usage,
    delete_entry_template,
    get_vial_lifecycle,
    get_vial_analytics,
    get_active_vials,
    get_vial_alerts,
    get_experiment_types,
    get_experimental_journey,
    get_experiment_recommendations,
    get_weekend_tasks,
    get_weekend_task_summary,
    create_weekend_checklist,
    mark_weekend_task_completed,
    get_weekend_task_instructions,
    export_to_excel,
    export_filtered_logs_to_excel,
    import_from_excel,
    IMAGES_DIR

st.set_page_config(page_title="iPSC Culture Tracker", layout="wide")

st.title("🧬 iPSC Culture Tracker")
st.write("LIMS-style multi-user cell culture tracker with thaw-linked histories.")

# Initialize database and storage
conn = get_conn()
init_db(conn)
ensure_dirs()

# Current user context (for 'Assigned to me' filters)
try:
    _rows_users = conn.execute("SELECT username FROM users ORDER BY username").fetchall()
    _usernames_all = [r[0] for r in _rows_users]
except Exception:
    _usernames_all = []
my_name = st.selectbox("My name", options=["(none)"] + _usernames_all if _usernames_all else ["(none)"], index=0, help="Used for 'Assigned to me' filters")
st.session_state["my_name"] = None if my_name == "(none)" else my_name

# Initialize session state
if "pending_thaw_id" not in st.session_state:
    st.session_state["pending_thaw_id"] = ""

tab_add, tab_history, tab_thaw, tab_weekend, tab_dashboard, tab_settings = st.tabs([
    "Add Entry",
    "History",
    "Thaw Timeline",
    "Weekend Tasks",
    "Dashboard",
    "Settings",
])

# ----------------------- Add Entry Tab -----------------------
with tab_add:
    st.subheader("📋 Add New Log Entry")
    
    # Critical Alert Banner - Check for vials with excessive splits
    try:
        active_vials = get_active_vials(conn, days_threshold=30)
        critical_vials = []
        for vial in active_vials:
            alerts = get_vial_alerts(conn, vial['thaw_id'])
            critical_alerts = [a for a in alerts if a['type'] == 'critical']
            if critical_alerts:
                critical_vials.append((vial, critical_alerts[0]))
        
        if critical_vials:
            st.error("🚨 **CRITICAL ALERTS** - Immediate attention required:")
            for vial, alert in critical_vials[:3]:  # Show max 3 critical alerts
                with st.expander(f"🚨 {vial['thaw_id']} - {vial.get('cell_line', 'Unknown')}", expanded=True):
                    st.error(alert['message'])
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button(f"📝 Add Thawing Entry", key=f"thaw_{vial['thaw_id']}"):
                            st.session_state.form_values = {
                                'cell_line': vial.get('cell_line', ''),
                                'event_type': 'Thawing',
                                'passage': 1,
                                'notes': f"Fresh vial - replacing {vial['thaw_id']} due to excessive splits"
                            }
                            st.success("✅ Form pre-filled for new thawing entry")
                            st.rerun()
                    with col2:
                        if st.button(f"🧬 Karyotype Check", key=f"karyo_{vial['thaw_id']}"):
                            st.session_state.form_values = {
                                'cell_line': vial.get('cell_line', ''),
                                'event_type': 'Other',
                                'passage': vial.get('current_passage', 1),
                                'thaw_id': vial['thaw_id'],
                                'notes': 'Karyotype analysis - checking genetic stability after prolonged culture'
                            }
                            st.success("✅ Form pre-filled for karyotype entry")
                            st.rerun()
                    with col3:
                        if st.button(f"❄️ Cryopreserve", key=f"cryo_{vial['thaw_id']}"):
                            st.session_state.form_values = {
                                'cell_line': vial.get('cell_line', ''),
                                'event_type': 'Cryopreservation',
                                'passage': vial.get('current_passage', 1),
                                'thaw_id': vial['thaw_id'],
                                'notes': 'Cryopreservation - preserving before genetic drift'
                            }
                            st.success("✅ Form pre-filled for cryopreservation")
                            st.rerun()
            st.markdown("---")
    except Exception as e:
        # Don't let alert checking break the app
        pass

    # Enhanced Copy/Reuse Section (OUTSIDE the form so it can work independently)
    st.markdown("### 🔄 Copy & Reuse Options")
    
    # Initialize session state for form values if not exists
    if "form_values" not in st.session_state:
        st.session_state.form_values = {}
    
    # Create tabs for different copy methods
    copy_tab1, copy_tab2, copy_tab3, copy_tab4 = st.columns(4)
    
    with copy_tab1:
        enable_recent_copy = st.checkbox("📋 Copy Recent Entry", value=False, help="Copy from recent entries for this cell line")
    
    with copy_tab2:
        enable_template_copy = st.checkbox("⭐ Use Template", value=False, help="Use saved templates or common patterns")
    
    with copy_tab3:
        enable_pattern_copy = st.checkbox("🔍 Pattern Match", value=False, help="Copy from entries with similar conditions")
    
    with copy_tab4:
        enable_my_entries = st.checkbox("👤 My Entries", value=False, help="Copy from your recent entries")

    # Cell Line selection (needed for copy functionality)
    cl_values = get_ref_values(conn, "cell_line")
    cell_line = st.selectbox("Select Cell Line for Copy/Reuse", options=[""] + cl_values if cl_values else [""], help="Select a cell line to see copy options")

    # Copy functionality sections
    copied_data = None
    
    # Recent Entry Copy
    if enable_recent_copy and cell_line:
        with st.expander("📋 Recent Entries for " + cell_line, expanded=True):
            recent = get_recent_logs_for_cell_line(conn, cell_line, limit=15)
            if recent:
                recent_options = []
                for i, r in enumerate(recent):
                    date_str = r.get('date', '')[:10]
                    event_str = r.get('event_type', '')
                    passage_str = f"P{r.get('passage', '')}" if r.get('passage') else ""
                    vessel_str = r.get('vessel', '')
                    medium_str = r.get('medium', '')
                    notes_preview = (r.get('notes', '') or '')[:30] + "..." if len(r.get('notes', '') or '') > 30 else r.get('notes', '')
                    display_text = f"{date_str} | {event_str} | {passage_str} | {vessel_str} | {medium_str}"
                    if notes_preview:
                        display_text += f" | {notes_preview}"
                    recent_options.append(display_text)
                
                selected_recent = st.selectbox(
                    "Choose an entry to copy:",
                    options=list(range(len(recent_options))),
                    format_func=lambda i: recent_options[i],
                    key="recent_copy_select"
                )
                
                if st.button("📋 Copy This Entry", key="copy_recent_btn"):
                    copied_data = recent[selected_recent]
                    st.session_state.form_values = copied_data.copy()
                    st.success(f"✅ Copied entry from {recent[selected_recent].get('date', '')}")
                    st.rerun()
            else:
                st.info("No previous entries for this cell line yet.")
    
    # Template Copy
    if enable_template_copy:
        with st.expander("⭐ Templates & Common Patterns", expanded=True):
            template_type = st.radio(
                "Template Type:",
                ["Saved Templates", "Common Patterns", "Cell Line Patterns"],
                horizontal=True,
                key="template_type_radio"
            )
            
            if template_type == "Saved Templates":
                current_user = st.session_state.get("my_name", "Unknown")
                templates = get_entry_templates(conn, created_by=current_user)
                
                if templates:
                    template_names = [t['name'] for t in templates]
                    selected_template_idx = st.selectbox(
                        "Choose a saved template:",
                        options=list(range(len(template_names))),
                        format_func=lambda i: f"{template_names[i]} (used {templates[i]['usage_count']} times)",
                        key="saved_template_select"
                    )
                    
                    if st.button("⭐ Use Template", key="use_template_btn"):
                        copied_data = templates[selected_template_idx]['template_data']
                        st.session_state.form_values = copied_data.copy()
                        increment_template_usage(conn, templates[selected_template_idx]['name'])
                        st.success(f"✅ Loaded template: {templates[selected_template_idx]['name']}")
                        st.rerun()
                else:
                    st.info("No saved templates yet. Create one by saving an entry as a template below.")
            
            elif template_type == "Common Patterns":
                common_patterns = get_template_entries(conn, limit=10)
                if common_patterns:
                    pattern_options = []
                    for p in common_patterns:
                        pattern_text = f"{p.get('event_type', '')} | {p.get('vessel', '')} | {p.get('medium', '')} | {p.get('cell_type', '')} (used {p.get('usage_count', 1)} times)"
                        pattern_options.append(pattern_text)
                    
                    selected_pattern = st.selectbox(
                        "Common combinations:",
                        options=list(range(len(pattern_options))),
                        format_func=lambda i: pattern_options[i],
                        key="common_pattern_select"
                    )
                    
                    if st.button("🔄 Use Pattern", key="use_pattern_btn"):
                        copied_data = common_patterns[selected_pattern]
                        st.session_state.form_values = copied_data.copy()
                        st.success("✅ Loaded common pattern")
                        st.rerun()
                else:
                    st.info("No common patterns found yet.")
            
            elif template_type == "Cell Line Patterns":
                if cell_line:
                    line_patterns = get_template_entries(conn, cell_line=cell_line, limit=8)
                    if line_patterns:
                        line_pattern_options = []
                        for p in line_patterns:
                            pattern_text = f"{p.get('event_type', '')} | {p.get('vessel', '')} | {p.get('medium', '')} (used {p.get('usage_count', 1)} times)"
                            line_pattern_options.append(pattern_text)
                        
                        selected_line_pattern = st.selectbox(
                            f"Patterns for {cell_line}:",
                            options=list(range(len(line_pattern_options))),
                            format_func=lambda i: line_pattern_options[i],
                            key="line_pattern_select"
                        )
                        
                        if st.button("📊 Use Cell Line Pattern", key="use_line_pattern_btn"):
                            copied_data = line_patterns[selected_line_pattern]
                            st.session_state.form_values = copied_data.copy()
                            st.success(f"✅ Loaded pattern for {cell_line}")
                            st.rerun()
                    else:
                        st.info(f"No patterns found for {cell_line} yet.")
                else:
                    st.info("Select a cell line first to see its patterns.")
    
    # Pattern Matching Copy
    if enable_pattern_copy:
        with st.expander("🔍 Find Similar Entries", expanded=True):
            st.write("Find entries matching specific criteria:")
            
            pcol1, pcol2 = st.columns(2)
            with pcol1:
                pattern_vessel = st.text_input("Vessel type:", placeholder="e.g., T25, 6-well", key="pattern_vessel")
                pattern_medium = st.text_input("Medium:", placeholder="e.g., StemFlex", key="pattern_medium")
            
            with pcol2:
                evt_values = get_ref_values(conn, "event_type")
                pattern_event = st.selectbox("Event type:", [""] + (evt_values or ["Observation", "Media Change", "Split", "Thawing", "Cryopreservation", "Other"]), key="pattern_event")
                pattern_cell_type = st.text_input("Cell type:", placeholder="e.g., iPSC", key="pattern_cell_type")
            
            if st.button("🔍 Find Matching Entries", key="find_pattern_btn"):
                pattern_filters = {}
                if pattern_vessel: pattern_filters['vessel'] = pattern_vessel
                if pattern_medium: pattern_filters['medium'] = pattern_medium
                if pattern_event: pattern_filters['event_type'] = pattern_event
                if pattern_cell_type: pattern_filters['cell_type'] = pattern_cell_type
                
                if pattern_filters:
                    matching_entries = get_entries_by_pattern(conn, **pattern_filters)
                    if matching_entries:
                        st.session_state['pattern_matches'] = matching_entries
                        st.success(f"Found {len(matching_entries)} matching entries")
                    else:
                        st.info("No matching entries found")
                else:
                    st.warning("Enter at least one search criteria")
            
            if 'pattern_matches' in st.session_state and st.session_state['pattern_matches']:
                matches = st.session_state['pattern_matches']
                match_options = []
                for m in matches:
                    match_text = f"{m.get('date', '')[:10]} | {m.get('cell_line', '')} | {m.get('event_type', '')} | {m.get('vessel', '')} | {m.get('medium', '')}"
                    match_options.append(match_text)
                
                selected_match = st.selectbox(
                    "Matching entries:",
                    options=list(range(len(match_options))),
                    format_func=lambda i: match_options[i],
                    key="pattern_match_select"
                )
                
                if st.button("📋 Copy Match", key="copy_match_btn"):
                    copied_data = matches[selected_match]
                    st.session_state.form_values = copied_data.copy()
                    st.success("✅ Copied matching entry")
                    st.rerun()
    
    # My Entries Copy
    if enable_my_entries and st.session_state.get("my_name"):
        with st.expander("👤 My Recent Entries", expanded=True):
            my_entries = get_recent_entries_by_operator(conn, st.session_state["my_name"], limit=15)
            if my_entries:
                my_options = []
                for m in my_entries:
                    my_text = f"{m.get('date', '')[:10]} | {m.get('cell_line', '')} | {m.get('event_type', '')} | {m.get('vessel', '')} | {m.get('medium', '')}"
                    my_options.append(my_text)
                
                selected_my_entry = st.selectbox(
                    "Your recent entries:",
                    options=list(range(len(my_options))),
                    format_func=lambda i: my_options[i],
                    key="my_entry_select"
                )
                
                if st.button("👤 Copy My Entry", key="copy_my_btn"):
                    copied_data = my_entries[selected_my_entry]
                    st.session_state.form_values = copied_data.copy()
                    st.success("✅ Copied your entry")
                    st.rerun()
            else:
                st.info("No entries found for you yet.")
    elif enable_my_entries and not st.session_state.get("my_name"):
        st.info("Set 'My name' at the top to see your entries.")

    # Clear copied data button
    if st.session_state.form_values:
        if st.button("🗑️ Clear Copied Data", key="clear_copied_btn"):
            st.session_state.form_values = {}
            st.success("✅ Cleared copied data")
            st.rerun()

    st.markdown("---")
    
    # Pre-form thaw selection for auto-fill (outside the form to work properly)
    selected_thaw_id = None
    
    # First, get cell line from previous form values or None for initial state
    previous_cell_line = st.session_state.form_values.get('cell_line') if st.session_state.form_values else None
    
    # Quick cell line selection for thaw filtering (outside form)
    conn = get_conn()
    cell_lines = get_ref_values(conn, "cell_line")
    
    # Get the cell line for thaw filtering - either from previous selection or first available
    filter_cell_line = previous_cell_line if previous_cell_line in cell_lines else (cell_lines[0] if cell_lines else "")
    
    # Show thaw selection outside form for auto-fill functionality
    st.markdown("### 🔗 Quick Thaw Selection (Auto-fill)")
    st.caption("Select a thaw vial to auto-fill the form with its latest information")
    
    thaw_options = get_active_thaw_options(conn, filter_cell_line)
    # If no thaw options for the chosen filter cell line, fall back to showing all recent thaws
    fallback_all_thaws = False
    if not thaw_options:
        thaw_options = get_active_thaw_options(conn, "")
        fallback_all_thaws = True

    if thaw_options:
        # Add refresh button
        refresh_col1, refresh_col2 = st.columns([3, 1])
        
        with refresh_col2:
            if st.button("🔄 Refresh", help="Refresh thaw options"):
                st.rerun()
        
        with refresh_col1:
            thaw_display_options = ["(none) - Manual entry"]
            thaw_id_mapping = {"(none) - Manual entry": "(none)"}
            
            for opt in thaw_options:
                status_emoji = {
                    "Active": "🟢",
                    "Aged": "🟡", 
                    "Old": "🟠",
                    "Cryopreserved": "❄️"
                }.get(opt['status'], "⚪")
                
                display_text = f"{status_emoji} {opt['thaw_id']} (P{opt['current_passage']}) - {opt['cell_line']}"
                thaw_display_options.append(display_text)
                thaw_id_mapping[display_text] = opt['thaw_id']
            
            selected_thaw_display = st.selectbox(
                "Choose thaw vial to auto-fill form:",
                options=thaw_display_options,
                index=0,
                help="🟢=Active, 🟡=Aged, 🟠=Old, ❄️=Cryopreserved",
                key="pre_form_thaw_selection"
            )
            # If we had to fallback to all thaws, show a hint so user knows we are showing all cell lines
            if fallback_all_thaws:
                st.caption("Showing recent thaw vials across all cell lines (no thaws found for current filter)")
        
        selected_thaw_id = thaw_id_mapping.get(selected_thaw_display, "(none)")
        
        # Auto-fill when thaw is selected
        if selected_thaw_id != "(none)":
            # Always show current thaw selection status
            thaw_info = get_thaw_latest_info(conn, selected_thaw_id)
            
            # Show current thaw info
            with st.expander(f"📋 Current Thaw Info: {selected_thaw_id}", expanded=False):
                info_col1, info_col2 = st.columns(2)
                with info_col1:
                    st.write(f"**Cell Line:** {thaw_info['cell_line']}")
                    st.write(f"**Passage:** {thaw_info['passage']}")
                    st.write(f"**Vessel:** {thaw_info['vessel']}")
                    st.write(f"**Location:** {thaw_info['location']}")
                with info_col2:
                    st.write(f"**Medium:** {thaw_info['medium']}")
                    st.write(f"**Cell Type:** {thaw_info['cell_type']}")
                    st.write(f"**Volume:** {thaw_info['volume']} mL")
                    st.write(f"**Operator:** {thaw_info['operator']}")
            
            # Check if this is a new thaw selection or force refresh
            current_form_thaw = st.session_state.get("current_form_thaw_id")
            if current_form_thaw != selected_thaw_id:
                # Store auto-filled values in session state
                st.session_state.form_values = {
                    'cell_line': thaw_info['cell_line'],
                    'passage': thaw_info['passage'],
                    'vessel': thaw_info['vessel'], 
                    'location': thaw_info['location'],
                    'medium': thaw_info['medium'],
                    'cell_type': thaw_info['cell_type'],
                    'volume': thaw_info['volume'],
                    'operator': thaw_info['operator'],
                    'experimental_conditions': thaw_info['experimental_conditions'],
                    'protocol_reference': thaw_info['protocol_reference'],
                    'success_metrics': thaw_info['success_metrics'],
                    'experiment_type': thaw_info['experiment_type'],
                    'experiment_stage': thaw_info['experiment_stage'],
                    'outcome_status': thaw_info['outcome_status'],
                    'linked_thaw_id': selected_thaw_id
                }
                
                # Store the current thaw ID
                st.session_state["current_form_thaw_id"] = selected_thaw_id
                
                # Show success message and rerun to refresh form
                st.success(f"✅ Form auto-filled with data from {selected_thaw_id}")
                st.rerun()  # Force refresh to show auto-filled values
            else:
                # Already loaded - show status
                st.info(f"📋 Form is populated with data from {selected_thaw_id}")
        else:
            # Clear form values when no thaw selected
            if st.session_state.get("current_form_thaw_id"):
                st.session_state.form_values = None
                st.session_state["current_form_thaw_id"] = None

    st.markdown("---")

    # Weekend Context Banner
    weekend_assignee = st.session_state.get("selected_weekend_assignee")
    if weekend_assignee:
        from datetime import date, timedelta
        today = date.today()
        is_weekend = today.weekday() >= 5  # Saturday=5, Sunday=6
        
        if is_weekend:
            st.info(f"🎯 **Weekend Mode**: Entries will auto-assign to **{weekend_assignee}** | [Change in Weekend Planning →]()")
        else:
            st.success(f"📋 **Weekend Planning Active**: Next entries will auto-assign to **{weekend_assignee}** | [Modify →]()")

    # Main Entry Form with improved UX
    with st.form("add_entry_form", clear_on_submit=False):
        from datetime import date, timedelta  # Import needed for weekend date calculations
        
        # Get copied values from session state
        prev = st.session_state.form_values if st.session_state.form_values else None
        
        # Initialize linked_thaw_id properly from session state
        linked_thaw_id = prev.get("linked_thaw_id", "(none)") if prev else "(none)"
        
        # Show auto-fill status if values are present
        if prev and prev.get("linked_thaw_id"):
            with st.expander("📋 Auto-fill Status", expanded=False):
                st.caption(f"**Form populated from:** {prev.get('linked_thaw_id')}")
                filled_fields = [k for k, v in prev.items() if v and k != 'linked_thaw_id']
                st.caption(f"**Auto-filled fields:** {', '.join(filled_fields)}")
        
        # Essential Information Section (always visible)
        st.markdown("### ✏️ Essential Information")
        
        # Row 1: Cell Line, Event Type, and Thaw Link (most important fields)
        ess_col1, ess_col2, ess_col3 = st.columns([1, 1, 1])
        
        with ess_col1:
            cl_values = get_ref_values(conn, "cell_line")
            if cl_values:
                default_cell_line = ""
                if prev and prev.get("cell_line") in cl_values:
                    default_cell_line = prev.get("cell_line")
                elif cell_line in cl_values:
                    default_cell_line = cell_line
                
                cl_options = ["+ Add new cell line"] + cl_values
                selected_cl_idx = cl_values.index(default_cell_line) + 1 if default_cell_line in cl_values else 0
                
                cell_line_selection = st.selectbox("Cell Line ID *", options=cl_options, index=selected_cl_idx)
                
                if cell_line_selection == "+ Add new cell line":
                    cell_line_final = st.text_input("Enter new Cell Line ID *", 
                                                  value="",
                                                  placeholder="e.g., BIHi005-A-24",
                                                  key="new_cell_line_manual")
                    if cell_line_final and cell_line_final not in cl_values:
                        st.caption(f"💡 Will add: {cell_line_final}")
                else:
                    cell_line_final = cell_line_selection
            else:
                cell_line_final = st.text_input("Cell Line ID *", 
                                              value=prev.get("cell_line", "") if prev else "",
                                              placeholder="e.g., BIHi005-A-24")
        
        with ess_col2:
            evt_values = get_ref_values(conn, "event_type")
            if evt_values:
                default_event_idx = 0
                if prev and prev.get("event_type") in evt_values:
                    default_event_idx = evt_values.index(prev.get("event_type"))
                
                event_options = ["+ Add new event type"] + evt_values
                event_selection = st.selectbox("Event Type *", options=event_options, index=default_event_idx + 1 if default_event_idx >= 0 else 0)
                
                if event_selection == "+ Add new event type":
                    event_type = st.text_input("Enter new Event Type *", 
                                             placeholder="e.g., Cell Sorting, Transfection",
                                             key="new_event_type_manual")
                    if event_type and event_type not in evt_values:
                        st.caption(f"💡 Will add: {event_type}")
                else:
                    event_type = event_selection
            else:
                default_options = ["Observation", "Media Change", "Split", "Thawing", "Cryopreservation", "Other"]
                default_event_idx = 0
                if prev and prev.get("event_type") in default_options:
                    default_event_idx = default_options.index(prev.get("event_type"))
                event_type = st.selectbox("Event Type *", options=default_options, index=default_event_idx)

        with ess_col3:
            # Show linked thaw ID from pre-form selection
            if event_type != "Thawing":
                st.markdown("**🔗 Linked Thaw**")
                if prev and prev.get("linked_thaw_id"):
                    st.success(f"🔗 {prev.get('linked_thaw_id')}")
                    linked_thaw_id = prev.get('linked_thaw_id')
                    
                    # Show auto-fill status
                    if st.session_state.get("auto_filled_from_thaw"):
                        auto_fill_info = st.session_state.get("auto_fill_source", linked_thaw_id)
                        st.caption(f"✅ Auto-filled from {auto_fill_info}")
                    
                    # Show split counter for linked thaw vial
                    try:
                        lifecycle = get_vial_lifecycle(conn, linked_thaw_id)
                        if lifecycle and lifecycle.get('events'):
                            split_count = sum(1 for e in lifecycle['events'] if e.get('event_type') == 'Split')
                            if split_count > 10:
                                st.error(f"🚨 {split_count} splits - CRITICAL!")
                            elif split_count > 8:
                                st.warning(f"⚠️ {split_count} splits - approaching limit")
                            elif split_count > 5:
                                st.info(f"📊 {split_count} splits performed")
                            else:
                                st.success(f"📊 {split_count} splits performed")
                    except Exception:
                        pass
                else:
                    st.info("� Use thaw selection above to link")
                    linked_thaw_id = "(none)"
            else:
                # For thawing events, show placeholder
                st.markdown("**🧪 New Thaw**")
                st.selectbox("Creating new thaw vial", options=["(auto-generated)"], index=0, disabled=True, key="thawing_placeholder")
                st.caption("💡 Thaw ID will be auto-generated")
                linked_thaw_id = ""

        # Row 2: Basic culture details in compact layout
        basic_col1, basic_col2, basic_col3, basic_col4 = st.columns(4)
        
        with basic_col1:
            # Smart passage prediction based on event type
            default_passage = 1
            if cell_line_final:
                last_for_line = get_last_log_for_cell_line(conn, cell_line_final)
                if last_for_line and last_for_line.get("passage"):
                    try:
                        current_passage = int(last_for_line.get("passage"))
                        # Only increment passage for Split events
                        if event_type == "Split":
                            default_passage = current_passage + 1
                        else:
                            # For all other events (Media Change, Observation, etc.), keep same passage
                            default_passage = current_passage
                    except Exception:
                        default_passage = 1
                else:
                    # No previous entry, start with passage 1
                    default_passage = 1
            
            # If auto-filled from thaw selection, use that passage number (may be overridden by event type logic above)
            if prev and prev.get("passage"):
                try:
                    auto_fill_passage = int(prev.get("passage"))
                    # Apply same logic to auto-filled values
                    if event_type == "Split":
                        default_passage = auto_fill_passage + 1
                    else:
                        default_passage = auto_fill_passage
                except Exception:
                    pass
            
            passage_no = st.number_input("Passage", min_value=1, step=1, value=default_passage)
            
            # Show helpful hint about passage numbering
            if event_type == "Split":
                st.caption("🔢 Passage will increment for split")
            else:
                st.caption("🔢 Passage stays same for this event")
        
        with basic_col2:
            vessel_refs = get_ref_values(conn, "vessel")
            if vessel_refs:
                v_index = 0
                if prev and prev.get("vessel") in vessel_refs:
                    v_index = vessel_refs.index(prev.get("vessel"))
                
                vessel_options = ["+ Add new"] + vessel_refs
                vessel_selection = st.selectbox("Vessel", options=vessel_options, index=v_index + 1 if v_index >= 0 else 0)
                
                if vessel_selection == "+ Add new":
                    vessel = st.text_input("New Vessel", 
                                         placeholder="T25, 6-well",
                                         key="new_vessel_manual")
                    if vessel and vessel not in vessel_refs:
                        st.caption(f"💡 Will add: {vessel}")
                else:
                    vessel = vessel_selection
            else:
                vessel_default = prev.get("vessel") if prev and prev.get("vessel") else ""
                vessel = st.text_input("Vessel", placeholder="T25, 6-well", value=vessel_default)
        
        with basic_col3:
            cm_refs = get_ref_values(conn, "culture_medium")
            if cm_refs:
                m_index = 0
                if prev and prev.get("medium") in cm_refs:
                    m_index = cm_refs.index(prev.get("medium"))
                
                medium_options = ["+ Add new"] + cm_refs
                medium_selection = st.selectbox("Medium", options=medium_options, index=m_index + 1 if m_index >= 0 else 0)
                
                if medium_selection == "+ Add new":
                    medium = st.text_input("New Medium", 
                                         placeholder="StemFlex",
                                         key="new_medium_manual")
                    if medium and medium not in cm_refs:
                        st.caption(f"💡 Will add: {medium}")
                else:
                    medium = medium_selection
            else:
                med_default = prev.get("medium") if prev and prev.get("medium") else ""
                medium = st.text_input("Medium", placeholder="StemFlex", value=med_default)
        
        with basic_col4:
            default_volume = 0.0
            if prev and prev.get("volume") is not None:
                try:
                    default_volume = float(prev.get("volume"))
                except Exception:
                    default_volume = 0.0
            volume = st.number_input("Volume (mL)", min_value=0.0, step=0.5, value=default_volume)

        # Suggestions row (compact)
        if cell_line_final:
            _med_sugs = top_values(conn, "medium", cell_line=cell_line_final)
            _ct_sugs = top_values(conn, "cell_type", cell_line=cell_line_final)
            hint_event = suggest_next_event(conn, cell_line_final)
            
            suggestions = []
            if hint_event:
                suggestions.append(f"Next: {hint_event}")
            if _med_sugs:
                suggestions.append(f"Medium: {', '.join(str(x) for x in _med_sugs[:2])}")
            if _ct_sugs:
                suggestions.append(f"Type: {', '.join(str(x) for x in _ct_sugs[:2])}")
            
            if suggestions:
                st.caption("💡 " + " | ".join(suggestions))

        # Auto-fill notice and controls
        if st.session_state.get("auto_filled_from_thaw", False):
            autofill_col1, autofill_col2 = st.columns([3, 1])
            with autofill_col1:
                auto_fill_info = st.session_state.get("auto_fill_source", "unknown thaw")
                st.info(f"🎯 Form auto-filled from {auto_fill_info}. You can modify any field below, then change the Event Type to Split, Media Change, etc.")
            with autofill_col2:
                if st.button("🗑️ Clear Auto-fill", help="Clear auto-filled values and start fresh"):
                    st.session_state.form_values = {}
                    st.session_state["last_selected_thaw_id"] = None
                    st.session_state["auto_filled_from_thaw"] = False
                    st.session_state["auto_fill_source"] = None
                    st.rerun()
        
        # Debug info (temporary - remove after testing)
        if st.checkbox("🔧 Show Debug Info", help="Temporary debug information"):
            st.write("**Session State Debug:**")
            st.write(f"- auto_filled_from_thaw: {st.session_state.get('auto_filled_from_thaw', False)}")
            st.write(f"- last_selected_thaw_id: {st.session_state.get('last_selected_thaw_id', 'None')}")
            st.write(f"- auto_fill_source: {st.session_state.get('auto_fill_source', 'None')}")
            if st.session_state.get('form_values'):
                st.write(f"- form_values keys: {list(st.session_state.get('form_values', {}).keys())}")
                st.write(f"- cell_line from form_values: {st.session_state.get('form_values', {}).get('cell_line', 'None')}")
                st.write(f"- passage from form_values: {st.session_state.get('form_values', {}).get('passage', 'None')}")
            else:
                st.write("- form_values: Empty")

        # More Thaw Options (expandable when needed)
        if st.session_state.get("show_all_thaw_options", False) and event_type != "Thawing":
            with st.expander("🔗 More Thaw Options", expanded=True):
                st.markdown("**All Available Thawed Vials**")
                
                # Get all thaw options for this cell line
                all_thaw_options = get_active_thaw_options(conn, cell_line_final if cell_line_final else "")
                
                if all_thaw_options:
                    # Create detailed display options
                    detailed_thaw_options = ["(none) - New independent culture"]
                    detailed_thaw_mapping = {"(none) - New independent culture": "(none)"}
                    
                    for opt in all_thaw_options:
                        status_emoji = {
                            "Active": "🟢",
                            "Aged": "🟡", 
                            "Old": "🟠",
                            "Cryopreserved": "❄️"
                        }.get(opt['status'], "⚪")
                        
                        # Detailed display text
                        display_text = f"{status_emoji} {opt['thaw_id']} | {opt['cell_line']} | P{opt['current_passage']} | {opt['last_event']} | {opt['days_since_thaw']}d ago"
                        if opt['vessel']:
                            display_text += f" | {opt['vessel']}"
                        
                        detailed_thaw_options.append(display_text)
                        detailed_thaw_mapping[display_text] = opt['thaw_id']
                    
                    # Set default selection based on pre-form Quick Thaw Selection
                    default_detailed_index = 0
                    if linked_thaw_id and linked_thaw_id != "(none)":
                        # Find the index of the pre-selected thaw
                        for i, option in enumerate(detailed_thaw_options):
                            if detailed_thaw_mapping.get(option) == linked_thaw_id:
                                default_detailed_index = i
                                break
                    
                    selected_detailed_thaw = st.selectbox(
                        "Select thawed vial:",
                        options=detailed_thaw_options,
                        index=default_detailed_index,
                        help="🟢=Active, 🟡=Aged, 🟠=Old, ❄️=Cryopreserved",
                        key="detailed_thaw_select"
                    )
                    
                    # Only override if user explicitly changed selection
                    new_linked_thaw_id = detailed_thaw_mapping.get(selected_detailed_thaw, "(none)")
                    if new_linked_thaw_id != linked_thaw_id:
                        linked_thaw_id = new_linked_thaw_id
                    
                    # Auto-fill form with detailed thaw vial information
                    if linked_thaw_id != "(none)":
                        # Check if this is a new thaw selection (different from previous)
                        if st.session_state.get("last_selected_thaw_id") != linked_thaw_id:
                            # Get latest info for this thaw and auto-fill
                            thaw_info = get_thaw_latest_info(conn, linked_thaw_id)
                            
                            # Store auto-filled values in session state
                            st.session_state.form_values = {
                                'cell_line': thaw_info['cell_line'],
                                'passage': thaw_info['passage'],
                                'vessel': thaw_info['vessel'], 
                                'location': thaw_info['location'],
                                'medium': thaw_info['medium'],
                                'cell_type': thaw_info['cell_type'],
                                'volume': thaw_info['volume'],
                                'operator': thaw_info['operator'],
                                'experimental_conditions': thaw_info['experimental_conditions'],
                                'protocol_reference': thaw_info['protocol_reference'],
                                'success_metrics': thaw_info['success_metrics'],
                                'experiment_type': thaw_info['experiment_type'],
                                'experiment_stage': thaw_info['experiment_stage'],
                                'outcome_status': thaw_info['outcome_status']
                            }
                            
                            # Remember this selection to avoid re-filling on form refresh
                            st.session_state["last_selected_thaw_id"] = linked_thaw_id
                            st.session_state["auto_filled_from_thaw"] = True
                            st.session_state["auto_fill_source"] = f"{linked_thaw_id} (P{thaw_info['passage']}, {thaw_info['last_event']})"
                            
                            # Force a rerun to update the form with auto-filled values
                            st.rerun()
                        elif st.session_state.get("auto_filled_from_thaw"):
                            # Show the auto-fill status if already filled
                            auto_fill_info = st.session_state.get("auto_fill_source", linked_thaw_id)
                            st.success(f"✅ Auto-filled from {auto_fill_info}")
                        
                        # Show additional info for selected thaw
                        selected_opt = next((opt for opt in all_thaw_options if opt['thaw_id'] == linked_thaw_id), None)
                        if selected_opt:
                            info_col1, info_col2 = st.columns(2)
                            with info_col1:
                                st.caption(f"📅 Thawed: {selected_opt['thaw_date']}")
                                st.caption(f"🧪 Current passage: {selected_opt['current_passage']}")
                            with info_col2:
                                st.caption(f"📍 Location: {selected_opt['location'] or 'Not specified'}")
                                st.caption(f"🔬 Last event: {selected_opt['last_event']}")
                    else:
                        # Clear auto-fill when "(none)" selected
                        if st.session_state.get("last_selected_thaw_id"):
                            st.session_state["last_selected_thaw_id"] = None
                            st.session_state["auto_filled_from_thaw"] = False
                            st.session_state["auto_fill_source"] = None
                            st.session_state.form_values = {}  # Clear form values
                else:
                    st.info("No thawed vials found for the selected cell line.")
                    # Don't override linked_thaw_id if it was set from Quick Thaw Selection
                    if not (linked_thaw_id and linked_thaw_id != "(none)"):
                        linked_thaw_id = "(none)"

        
        # Additional Details (collapsible)
        with st.expander("📍 Location & Cell Type", expanded=False):
            detail_col1, detail_col2 = st.columns(2)
            
            with detail_col1:
                location_refs = get_ref_values(conn, "location")
                if location_refs:
                    l_index = 0
                    if prev and prev.get("location") in location_refs:
                        l_index = location_refs.index(prev.get("location"))
                    
                    location_options = ["+ Add new"] + location_refs
                    location_selection = st.selectbox("Location", options=location_options, index=l_index + 1 if l_index >= 0 else 0, key="location_detail")
                    
                    if location_selection == "+ Add new":
                        location = st.text_input("New Location", 
                                               placeholder="Incubator A, Shelf 2",
                                               key="new_location_manual")
                        if location and location not in location_refs:
                            st.caption(f"💡 Will add: {location}")
                    else:
                        location = location_selection
                else:
                    loc_default = prev.get("location") if prev and prev.get("location") else ""
                    location = st.text_input("Location", placeholder="Incubator A, Shelf 2", value=loc_default)
            
            with detail_col2:
                ct_refs = get_ref_values(conn, "cell_type")
                if ct_refs:
                    ct_index = 0
                    if prev and prev.get("cell_type") in ct_refs:
                        ct_index = ct_refs.index(prev.get("cell_type"))
                    
                    cell_type_options = ["+ Add new"] + ct_refs
                    cell_type_selection = st.selectbox("Cell Type", options=cell_type_options, index=ct_index + 1 if ct_index >= 0 else 0, key="cell_type_detail")
                    
                    if cell_type_selection == "+ Add new":
                        cell_type = st.text_input("New Cell Type", 
                                                placeholder="iPSC, Fibroblast",
                                                key="new_cell_type_manual")
                        if cell_type and cell_type not in ct_refs:
                            st.caption(f"💡 Will add: {cell_type}")
                    else:
                        cell_type = cell_type_selection
                else:
                    ct_default = prev.get("cell_type") if prev and prev.get("cell_type") else ""
                    cell_type = st.text_input("Cell Type", placeholder="iPSC, NPC, cardiomyocyte", value=ct_default)

        # Operator and Date (compact row)
        op_date_col1, op_date_col2 = st.columns(2)
        
        with op_date_col1:
            user_rows = conn.execute("SELECT username FROM users ORDER BY username").fetchall()
            usernames = [r[0] for r in user_rows]
            if usernames:
                # Default to "My name" if set, otherwise first user
                default_operator_idx = 0
                my_name_value = st.session_state.get("my_name")
                weekend_assignee = st.session_state.get("selected_weekend_assignee")
                
                # Priority order: Weekend assignee > My name > Previous entry operator
                if weekend_assignee and weekend_assignee in usernames:
                    default_operator_idx = usernames.index(weekend_assignee)
                elif my_name_value and my_name_value in usernames:
                    default_operator_idx = usernames.index(my_name_value)
                elif prev and prev.get("operator") in usernames:
                    # Fall back to copied/previous operator if neither weekend nor My name set
                    default_operator_idx = usernames.index(prev.get("operator"))
                
                operator = st.selectbox("Operator *", options=usernames, index=default_operator_idx)
                
                # Show helpful info when auto-populated
                if weekend_assignee and operator == weekend_assignee:
                    st.caption("🎯 Auto-filled from Weekend Planning assignee")
                elif my_name_value and operator == my_name_value and not weekend_assignee:
                    st.caption("✅ Auto-filled from 'My name' selection")
            else:
                st.info("💡 Add operators in Settings tab")
                # Default to My name if no operators in database yet
                default_name = st.session_state.get("my_name", "")
                operator = st.text_input("Operator *", placeholder="Your name", value=default_name)
        
        with op_date_col2:
            # Smart date suggestion based on weekend planning
            default_date = date.today()
            
            # If weekend planning is active, suggest next weekend dates
            weekend_assignee = st.session_state.get("selected_weekend_assignee")
            if weekend_assignee:
                today = date.today()
                current_weekday = today.weekday()  # Monday=0, Sunday=6
                
                if current_weekday < 5:  # Monday to Friday
                    # Suggest next Saturday
                    days_to_saturday = 5 - current_weekday
                    default_date = today + timedelta(days=days_to_saturday)
                elif current_weekday == 5:  # Saturday
                    # If it's Saturday, suggest today or tomorrow (Sunday)
                    default_date = today
                else:  # Sunday
                    # If it's Sunday, suggest today
                    default_date = today
            
            log_date = st.date_input("Date *", value=default_date)
            
            # Show helpful weekend planning hint and quick weekend selector
            if weekend_assignee:
                today = date.today()
                current_weekday = today.weekday()
                
                # Calculate this weekend's Saturday and Sunday
                if current_weekday < 5:  # Monday to Friday
                    days_to_saturday = 5 - current_weekday
                    this_saturday = today + timedelta(days=days_to_saturday)
                    this_sunday = this_saturday + timedelta(days=1)
                elif current_weekday == 5:  # Saturday
                    this_saturday = today
                    this_sunday = today + timedelta(days=1)
                else:  # Sunday
                    this_saturday = today - timedelta(days=1)
                    this_sunday = today
                
                # Quick weekend date selector
                weekend_options = [
                    f"📅 Saturday ({this_saturday.strftime('%m/%d')})",
                    f"📅 Sunday ({this_sunday.strftime('%m/%d')})",
                    "📅 Custom date (use picker above)"
                ]
                
                selected_weekend = st.radio(
                    "Quick weekend date:",
                    weekend_options,
                    index=2,  # Default to custom
                    horizontal=True,
                    key="weekend_date_selector"
                )
                
                # Override date based on selection
                if "Saturday" in selected_weekend:
                    log_date = this_saturday
                elif "Sunday" in selected_weekend:
                    log_date = this_sunday
                # If "Custom" is selected, use the date_input value above
                
                if log_date.weekday() == 5:  # Saturday
                    st.caption("📅 Selected: Saturday (weekend planning active)")
                elif log_date.weekday() == 6:  # Sunday  
                    st.caption("📅 Selected: Sunday (weekend planning active)")
                else:
                    st.caption("📅 Weekend planning active")

        # Notes (always visible but compact)
        notes = st.text_area("Notes / Observations", height=60, placeholder="Any additional observations or notes...")

        # Experimental Workflow (collapsible)
        with st.expander("🧬 Experimental Workflow", expanded=False):
            st.caption("Track experimental procedures beyond basic culture maintenance")
            
            exp_col1, exp_col2 = st.columns(2)
            
            with exp_col1:
                try:
                    from db import get_experiment_types
                    experiment_types = get_experiment_types(conn)
                    exp_categories = sorted(list(set([exp['category'] for exp in experiment_types])))
                    
                    experiment_category = st.selectbox(
                        "Category:",
                        options=[""] + exp_categories,
                        help="General experiment category"
                    )
                    
                    filtered_exp_types = []
                    if experiment_category:
                        filtered_exp_types = [exp['name'] for exp in experiment_types if exp['category'] == experiment_category]
                    
                    experiment_type = st.selectbox(
                        "Type:",
                        options=[""] + filtered_exp_types,
                        help="Specific experimental protocol"
                    )
                    
                    experiment_stage = st.text_input(
                        "Stage:",
                        placeholder="e.g., Day 3, Transfection",
                        value=prev.get("experiment_stage", "") if prev else ""
                    )
                    
                    outcome_status = st.selectbox(
                        "Status:",
                        options=["", "In Progress", "Successful", "Failed", "Partial Success", "Needs Optimization"]
                    )
                    
                except ImportError:
                    experiment_type = st.text_input("Type:", placeholder="CRISPR Editing, Differentiation")
                    experiment_stage = st.text_input("Stage:", placeholder="Day 3, Selection")
                    outcome_status = st.selectbox("Status:", options=["", "In Progress", "Successful", "Failed"])
            
            with exp_col2:
                experimental_conditions = st.text_area(
                    "Conditions:",
                    placeholder="Temperature, supplements, concentrations...",
                    height=80,
                    value=prev.get("experimental_conditions", "") if prev else ""
                )
                
                protocol_reference = st.text_input(
                    "Protocol:",
                    placeholder="DOI, SOP number",
                    value=prev.get("protocol_reference", "") if prev else ""
                )
                
                success_metrics = st.text_input(
                    "Metrics:",
                    placeholder="Efficiency %, viability...",
                    value=prev.get("success_metrics", "") if prev else ""
                )

        # Task Assignment & Special Features (collapsible)
        with st.expander("📋 Assignment & Special Features", expanded=False):
            st.markdown("**Task Assignment**")
            assign_col1, assign_col2 = st.columns(2)
            
            with assign_col1:
                # Default assignment options with smart defaults
                assignment_options = ["(unassigned)"] + usernames if usernames else ["(unassigned)"]
                default_assign_idx = 0
                
                # Default to "My name" if set and user wants to assign to themselves
                my_name_value = st.session_state.get("my_name")
                if my_name_value and my_name_value in usernames:
                    # Offer "My name" as default but allow changing
                    default_assign_idx = assignment_options.index(my_name_value) if my_name_value in assignment_options else 0
                elif prev and prev.get("assigned_to") in assignment_options:
                    # Fall back to copied/previous assignment
                    default_assign_idx = assignment_options.index(prev.get("assigned_to"))
                
                assigned_to = st.selectbox("Assigned To", options=assignment_options, index=default_assign_idx)
                
                # Show helpful info when auto-populated
                if my_name_value and assigned_to == my_name_value and not prev:
                    st.caption("✅ Auto-assigned to you")
            
            with assign_col2:
                next_action_date = st.date_input("Next Action Date", value=None, key="next_action_main")

            st.markdown("**Weekend Quick Setup**")
            weekend_setup = st.checkbox("🗓️ Schedule as weekend task", value=False, help="Quick weekend scheduling")
            
            weekend_assignee_quick = None
            weekend_day = None
            
            if weekend_setup:
                weekend_col1, weekend_col2 = st.columns(2)
                
                with weekend_col1:
                    from datetime import datetime, timedelta
                    today = datetime.now()
                    days_to_saturday = (5 - today.weekday()) % 7
                    if days_to_saturday == 0 and today.weekday() == 5:
                        days_to_saturday = 7
                    
                    saturday = today + timedelta(days=days_to_saturday)
                    sunday = saturday + timedelta(days=1)
                    
                    weekend_day = st.selectbox("Weekend Day:", [
                        f"Saturday ({saturday.strftime('%m-%d')})",
                        f"Sunday ({sunday.strftime('%m-%d')})"
                    ])
                    
                with weekend_col2:
                    if usernames:
                        # Default weekend assignee to "My name"
                        weekend_default_idx = 0
                        my_name_value = st.session_state.get("my_name")
                        if my_name_value and my_name_value in usernames:
                            weekend_default_idx = usernames.index(my_name_value)
                        
                        weekend_assignee_quick = st.selectbox("Weekend Assignee:", usernames, index=weekend_default_idx)

            # Thawing/Linking section
            if event_type == "Thawing":
                st.markdown("**Thawing Details**")
                
                # Generate enhanced thaw ID based on current form values
                enhanced_thaw_id = generate_enhanced_thaw_id(conn, log_date, operator, cell_type)
                
                # Update session state if values changed
                if not st.session_state.get("pending_thaw_id") or st.session_state.get("last_thaw_params") != (operator, cell_type, log_date):
                    st.session_state["pending_thaw_id"] = enhanced_thaw_id
                    st.session_state["last_thaw_params"] = (operator, cell_type, log_date)
                
                thaw_col1, thaw_col2 = st.columns(2)
                with thaw_col1:
                    st.text_input("Thaw ID (auto)", value=st.session_state["pending_thaw_id"], disabled=True, key="thaw_display")
                with thaw_col2:
                    cryo_vial_position = st.text_input("Cryo Vial Position", placeholder="Box A2, Row 3 Col 5")
                
                # Show thaw ID format explanation
                if operator and cell_type:
                    st.caption(f"💡 Format: TH-Date-{operator.split()[0][0] if operator.split() else 'X'}{operator.split()[-1][0] if len(operator.split()) > 1 else operator[1:2] if len(operator) > 1 else 'X'}-{cell_type[:5].upper()}-###")
                elif operator:
                    st.caption(f"💡 Format: TH-Date-{operator.split()[0][0] if operator.split() else 'X'}{operator.split()[-1][0] if len(operator.split()) > 1 else operator[1:2] if len(operator) > 1 else 'X'}-###")
                elif cell_type:
                    st.caption(f"💡 Format: TH-Date-{cell_type[:5].upper()}-###")
                else:
                    st.caption("💡 Add Operator and Cell Type for enhanced Thaw ID format")
                
                cryo_vial_position = ""
            else:
                # For non-thawing events, linked_thaw_id is set in essential section above
                # Just need to set cryo_vial_position for consistency
                cryo_vial_position = ""
                
                # Smart recommendations based on event type and linked thaw
                if linked_thaw_id != "(none)" and event_type:
                    if event_type in ["Split", "Media Change", "Observation"]:
                        st.success(f"✅ Perfect! Linking {event_type.lower()} to {linked_thaw_id} will maintain the vial lineage.")
                    elif event_type == "Cryopreservation":
                        st.info(f"❄️ This will mark {linked_thaw_id} as cryopreserved, ending its active culture.")
                
                # Suggest linking if no thaw selected but cell line matches
                if linked_thaw_id == "(none)" and cell_line_final and event_type in ["Split", "Media Change", "Observation"]:
                    if cell_line_final:  # Basic suggestion without complex logic
                        st.warning(f"💡 Consider linking to an active {cell_line_final} vial above to track lineage for this {event_type.lower()}.")

            # Image upload
            st.markdown("**Colony Image**")
            uploaded_img = st.file_uploader("Add image (optional)", type=["png", "jpg", "jpeg"], help="Upload colony or culture image")

            # Template saving
            st.markdown("**Save as Template**")
            template_col1, template_col2 = st.columns([1, 2])
            with template_col1:
                save_template = st.checkbox("Save template", value=False)
            with template_col2:
                template_name = ""
                if save_template:
                    template_name = st.text_input("Template name:", placeholder="e.g., 'T25 Split'", key="template_name_input")

        # Apply weekend assignment override
        if weekend_setup and weekend_day and weekend_assignee_quick:
            from datetime import datetime, timedelta
            today = datetime.now()
            days_to_saturday = (5 - today.weekday()) % 7
            if days_to_saturday == 0 and today.weekday() == 5:
                days_to_saturday = 7
            
            saturday = today + timedelta(days=days_to_saturday)
            sunday = saturday + timedelta(days=1)
            
            if "Saturday" in weekend_day:
                calculated_date = saturday.date()
            else:
                calculated_date = sunday.date()
            
            st.info(f"✅ Weekend: **{weekend_assignee_quick}** on **{calculated_date.strftime('%A, %b %d')}**")
            assigned_to = weekend_assignee_quick
            next_action_date = calculated_date

        # Form submission buttons
        st.markdown("---")
        submit_col1, submit_col2, submit_col3 = st.columns([2, 1, 1])
        
        with submit_col1:
            submitted = st.form_submit_button("💾 **Save Entry**", type="primary", use_container_width=True)
        
        with submit_col2:
            if save_template and template_name:
                save_template_only = st.form_submit_button("⭐ Template Only", use_container_width=True)
            else:
                save_template_only = False
        
        with submit_col3:
            if st.form_submit_button("🔄 Clear Form", use_container_width=True):
                st.session_state.form_values = {}
                st.rerun()
        if submitted:
            if not operator:
                st.error("Please provide an Operator.")
                st.stop()
            img_bytes = uploaded_img.getvalue() if uploaded_img else None
            thaw_id_val = ""
            if event_type == "Thawing":
                # Use enhanced thaw ID with final operator and cell_type values
                thaw_id_val = st.session_state["pending_thaw_id"] or generate_enhanced_thaw_id(conn, log_date, operator, cell_type)
                st.session_state["pending_thaw_id"] = ""
                st.session_state["last_thaw_params"] = None
            else:
                thaw_id_val = linked_thaw_id if linked_thaw_id and linked_thaw_id != "(none)" else ""

            image_path = None
            if img_bytes:
                ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                ext = os.path.splitext(uploaded_img.name)[1] if uploaded_img and uploaded_img.name else ".jpg"
                fname = f"{ts}_{(thaw_id_val or 'noThaw').replace('-', '')}{ext}"
                fpath = os.path.join(IMAGES_DIR, fname)
                with open(fpath, "wb") as f:
                    f.write(img_bytes)
                image_path = fpath

            payload = {
                "date": log_date.isoformat(),
                "cell_line": cell_line_final,
                "event_type": event_type,
                "passage": int(passage_no) if passage_no else None,
                "vessel": vessel,
                "location": location,
                "medium": medium,
                "cell_type": cell_type,
                "volume": float(volume) if volume is not None else None,
                "notes": notes,
                "operator": operator,
                "thaw_id": thaw_id_val,
                "cryo_vial_position": cryo_vial_position,
                "image_path": image_path,
                "assigned_to": None if assigned_to in (None, "(unassigned)") else assigned_to,
                "next_action_date": next_action_date.isoformat() if next_action_date else None,
                "created_by": operator,
                "created_at": datetime.now().isoformat(),
                # Experimental workflow fields
                "experiment_type": experiment_type if experiment_type else None,
                "experiment_stage": experiment_stage if experiment_stage else None,
                "experimental_conditions": experimental_conditions if experimental_conditions else None,
                "protocol_reference": protocol_reference if protocol_reference else None,
                "outcome_status": outcome_status if outcome_status else None,
                "success_metrics": success_metrics if success_metrics else None,
                "linked_thaw_id": linked_thaw_id if linked_thaw_id and linked_thaw_id != "(none)" else None,
            }
            
            # Auto-add new values to reference lists
            try:
                # Add new cell line if it doesn't exist
                if cell_line_final:
                    existing_cell_lines = get_ref_values(conn, "cell_line")
                    if cell_line_final not in existing_cell_lines:
                        add_ref_value(conn, "cell_line", cell_line_final)
                        st.success(f"✅ Added new cell line: {cell_line_final}")
                
                # Add new event type if it doesn't exist
                if event_type:
                    existing_event_types = get_ref_values(conn, "event_type")
                    if event_type not in existing_event_types:
                        add_ref_value(conn, "event_type", event_type)
                        st.success(f"✅ Added new event type: {event_type}")
                
                # Add new vessel if it doesn't exist
                if vessel:
                    existing_vessels = get_ref_values(conn, "vessel")
                    if vessel not in existing_vessels:
                        add_ref_value(conn, "vessel", vessel)
                        st.success(f"✅ Added new vessel: {vessel}")
                
                # Add new location if it doesn't exist
                if location:
                    existing_locations = get_ref_values(conn, "location")
                    if location not in existing_locations:
                        add_ref_value(conn, "location", location)
                        st.success(f"✅ Added new location: {location}")
                
                # Add new medium if it doesn't exist
                if medium:
                    existing_media = get_ref_values(conn, "culture_medium")
                    if medium not in existing_media:
                        add_ref_value(conn, "culture_medium", medium)
                        st.success(f"✅ Added new medium: {medium}")
                
                # Add new cell type if it doesn't exist
                if cell_type:
                    existing_cell_types = get_ref_values(conn, "cell_type")
                    if cell_type not in existing_cell_types:
                        add_ref_value(conn, "cell_type", cell_type)
                        st.success(f"✅ Added new cell type: {cell_type}")
            except Exception as e:
                st.warning(f"⚠️ Note: Could not auto-add some values to reference lists: {str(e)}")
            
            insert_log(conn, payload)
            
            # Save as template if requested
            if save_template and template_name and template_name.strip():
                template_data = {
                    "cell_line": cell_line_final,
                    "event_type": event_type,
                    "vessel": vessel,
                    "location": location,
                    "medium": medium,
                    "cell_type": cell_type,
                    "volume": float(volume) if volume is not None else None,
                    "notes": notes,
                    # Don't save passage, date, or IDs in templates
                }
                try:
                    save_entry_template(conn, template_name.strip(), template_data, operator)
                    st.success(f"✅ Log entry saved and template '{template_name}' created!")
                except Exception as e:
                    st.success("✅ Log entry saved to database!")
                    st.warning(f"⚠️ Template save failed: {str(e)}")
            else:
                st.success("✅ Log entry saved to database!")
        
        # Handle template-only saving
        if save_template_only and template_name and template_name.strip():
            if not operator:
                st.error("Please provide an Operator to save template.")
            else:
                template_data = {
                    "cell_line": cell_line_final,
                    "event_type": event_type,
                    "vessel": vessel,
                    "location": location,
                    "medium": medium,
                    "cell_type": cell_type,
                    "volume": float(volume) if volume is not None else None,
                    "notes": notes,
                }
                try:
                    save_entry_template(conn, template_name.strip(), template_data, operator)
                    st.success(f"⭐ Template '{template_name}' saved successfully!")
                except Exception as e:
                    st.error(f"❌ Template save failed: {str(e)}")

with tab_history:
    st.subheader("📜 Culture History")
    
    # Enhanced Filter & Sort Controls
    with st.expander("🔍 Advanced Filters & Sorting", expanded=True):
        st.markdown("**Filter your entries:** Use these controls to find specific entries in your database")
        
        # Row 1: Basic filters
        fcol1, fcol2, fcol3, fcol4 = st.columns([2, 2, 2, 1])
        with fcol1:
            f_cell = st.text_input("🧬 Cell line contains", "", help="Find entries containing this cell line name")
        with fcol2:
            # Get dynamic event types from database
            event_types = get_ref_values(conn, "event_type")
            event_options = ["(any)"] + event_types if event_types else ["(any)", "Observation", "Media Change", "Split", "Thawing", "Cryopreservation", "Other"]
            f_event = st.selectbox("📋 Event Type", event_options, help="Filter by specific type of lab activity")
        with fcol3:
            # Get operators/users from database
            try:
                with closing(conn.cursor()) as cur:
                    cur.execute("SELECT DISTINCT operator FROM logs WHERE operator IS NOT NULL AND operator != '' ORDER BY operator")
                    operators = [row[0] for row in cur.fetchall()]
                operator_options = ["(any)"] + operators if operators else ["(any)"]
            except:
                operator_options = ["(any)"]
            f_operator = st.selectbox("👤 Operator", operator_options, help="Select specific person who performed the work")
        with fcol4:
            only_mine = st.checkbox("📌 Only mine", value=False, help="Show only entries where you are the operator (set your name at the top first)")
        
        # Row 1.5: Additional assignment filter
        if f_operator == "(any)":
            assign_col1, assign_col2, assign_col3, assign_col4 = st.columns(4)
            with assign_col1:
                f_assigned = st.text_input("👥 Assigned To contains", "", help="Filter by assignment field (different from operator)")
            with assign_col2:
                st.empty()  # Placeholder
            with assign_col3:
                st.empty()  # Placeholder  
            with assign_col4:
                st.empty()  # Placeholder
        else:
            f_assigned = ""  # Clear assigned filter when specific operator is selected
        
        # Row 2: Culture-specific filters
        cult_col1, cult_col2, cult_col3, cult_col4 = st.columns(4)
        with cult_col1:
            # Get dynamic culture media options
            media_options = get_ref_values(conn, "culture_medium")
            media_filter_options = ["(any)"] + media_options if media_options else ["(any)"]
            f_medium = st.selectbox("🧪 Culture Medium", media_filter_options)
        with cult_col2:
            # Get dynamic location options
            location_options = get_ref_values(conn, "location")
            location_filter_options = ["(any)"] + location_options if location_options else ["(any)"]
            f_location = st.selectbox("📍 Location", location_filter_options)
        with cult_col3:
            # Get dynamic vessel options
            vessel_options = get_ref_values(conn, "vessel")
            vessel_filter_options = ["(any)"] + vessel_options if vessel_options else ["(any)"]
            f_vessel = st.selectbox("🥼 Vessel", vessel_filter_options)
        with cult_col4:
            # Passage range filter
            f_passage_min = st.number_input("🔢 Min Passage", min_value=0, value=0, step=1)
            f_passage_max = st.number_input("🔢 Max Passage", min_value=0, value=100, step=1)
        
        # Row 3: Date filters and sorting
        date_col1, date_col2, sort_col1, sort_col2 = st.columns(4)
        with date_col1:
            f_start_date = st.date_input("📅 From Date", value=None)
        with date_col2:
            f_end_date = st.date_input("📅 To Date", value=None)
        with sort_col1:
            sort_options = [
                "Date (newest first)", "Date (oldest first)",
                "Cell Line (A-Z)", "Cell Line (Z-A)",
                "Event Type (A-Z)", "Event Type (Z-A)",
                "Culture Medium (A-Z)", "Culture Medium (Z-A)",
                "Location (A-Z)", "Location (Z-A)",
                "Passage (low to high)", "Passage (high to low)",
                "Operator (A-Z)", "Operator (Z-A)"
            ]
            sort_by = st.selectbox("📊 Sort by", sort_options, index=0)
        with sort_col2:
            # Quick filter presets
            quick_filters = [
                "All entries",
                "Today's entries", 
                "This week",
                "My entries only",
                "Weekend entries",
                "Split events only",
                "Media changes only",
                "Active cultures only"
            ]
            quick_filter = st.selectbox("⚡ Quick Filter", quick_filters, index=0, help="Quick presets for common filter combinations")
    
    # Apply quick filter logic
    start_date_filter = None
    end_date_filter = None
    event_filter = f_event if f_event != "(any)" else None
    
    if quick_filter == "Today's entries":
        from datetime import datetime, date
        today = date.today()
        start_date_filter = today
        end_date_filter = today
    elif quick_filter == "This week":
        from datetime import datetime, date, timedelta
        today = date.today()
        start_of_week = today - timedelta(days=today.weekday())
        start_date_filter = start_of_week
        end_date_filter = today
    elif quick_filter == "Weekend entries":
        from datetime import datetime, date, timedelta
        today = date.today()
        # Get last Saturday and Sunday
        days_since_monday = today.weekday()
        last_saturday = today - timedelta(days=days_since_monday + 2)
        last_sunday = today - timedelta(days=days_since_monday + 1)
        # For current weekend if it's weekend now
        if today.weekday() >= 5:  # Saturday=5, Sunday=6
            start_date_filter = today if today.weekday() == 5 else today - timedelta(days=1)
            end_date_filter = today if today.weekday() == 6 else today + timedelta(days=1)
        else:
            start_date_filter = last_saturday
            end_date_filter = last_sunday
    elif quick_filter == "My entries only":
        # Filter by current user's name - this will be applied after data retrieval
        pass  # Logic handled in the operator filter section below
    elif quick_filter == "Split events only":
        event_filter = "Split"
    elif quick_filter == "Media changes only":
        event_filter = "Media Change"
    elif quick_filter == "Active cultures only":
        # Show only non-cryopreserved cultures from last 30 days
        from datetime import datetime, date, timedelta
        start_date_filter = date.today() - timedelta(days=30)
        event_filter = None  # Will filter out cryopreservation in query
    
    # Override with manual date selection if provided
    if f_start_date:
        start_date_filter = f_start_date
    if f_end_date:
        end_date_filter = f_end_date

    # Query logs with enhanced filters
    logs = query_logs(
        conn,
        user=None,
        event_type=event_filter,
        thaw_id=None,
        start_date=start_date_filter,
        end_date=end_date_filter,
        cell_line_contains=f_cell or None,
    )

    if logs:
        df = pd.DataFrame(logs)
        
        # Apply additional filters
        # Quick filter: "My entries only" takes priority
        if quick_filter == "My entries only":
            if st.session_state.get("my_name"):
                df = df[df.get("operator", "").astype(str) == st.session_state["my_name"]]
            else:
                st.warning("💡 Set 'My name' at the top of the page to use 'My entries only' filter.")
        
        # Operator filter (primary filter for who performed the work)
        elif f_operator != "(any)":
            df = df[df.get("operator", "").astype(str) == f_operator]
        
        # Assignment filter (secondary filter for who work is assigned to)
        if f_assigned:
            df = df[df.get("assigned_to", "").astype(str).str.contains(f_assigned, case=False, na=False)]
        
        # "Only mine" filter - filters by operator field matching user's name
        if only_mine and st.session_state.get("my_name"):
            df = df[df.get("operator", "").astype(str) == st.session_state["my_name"]]
        elif only_mine and not st.session_state.get("my_name"):
            st.info("💡 Set 'My name' at the top to enable 'Only mine' filter. This will show entries where you are the operator.")
        
        # Culture-specific filters
        if f_medium != "(any)":
            df = df[df.get("medium", "").astype(str) == f_medium]
        if f_location != "(any)":
            df = df[df.get("location", "").astype(str) == f_location]
        if f_vessel != "(any)":
            df = df[df.get("vessel", "").astype(str) == f_vessel]
        
        # Passage range filter
        if f_passage_min > 0 or f_passage_max < 100:
            df["passage_num"] = pd.to_numeric(df.get("passage", 0), errors='coerce').fillna(0)
            df = df[(df["passage_num"] >= f_passage_min) & (df["passage_num"] <= f_passage_max)]
        
        # Special filters for quick filter options
        if quick_filter == "Active cultures only":
            # Exclude cryopreservation events
            df = df[df.get("event_type", "") != "Cryopreservation"]
        
        # Apply sorting
        if "Date (newest first)" in sort_by:
            df = df.sort_values("date", ascending=False)
        elif "Date (oldest first)" in sort_by:
            df = df.sort_values("date", ascending=True)
        elif "Cell Line (A-Z)" in sort_by:
            df = df.sort_values("cell_line", ascending=True)
        elif "Cell Line (Z-A)" in sort_by:
            df = df.sort_values("cell_line", ascending=False)
        elif "Event Type (A-Z)" in sort_by:
            df = df.sort_values("event_type", ascending=True)
        elif "Event Type (Z-A)" in sort_by:
            df = df.sort_values("event_type", ascending=False)
        elif "Culture Medium (A-Z)" in sort_by:
            df = df.sort_values("medium", ascending=True)
        elif "Culture Medium (Z-A)" in sort_by:
            df = df.sort_values("medium", ascending=False)
        elif "Location (A-Z)" in sort_by:
            df = df.sort_values("location", ascending=True)
        elif "Location (Z-A)" in sort_by:
            df = df.sort_values("location", ascending=False)
        elif "Passage (low to high)" in sort_by:
            df["passage_num"] = pd.to_numeric(df.get("passage", 0), errors='coerce').fillna(0)
            df = df.sort_values("passage_num", ascending=True)
        elif "Passage (high to low)" in sort_by:
            df["passage_num"] = pd.to_numeric(df.get("passage", 0), errors='coerce').fillna(0)
            df = df.sort_values("passage_num", ascending=False)
        elif "Operator (A-Z)" in sort_by:
            df = df.sort_values("operator", ascending=True)
        elif "Operator (Z-A)" in sort_by:
            df = df.sort_values("operator", ascending=False)
        
        # Display summary statistics
        if len(df) > 0:
            stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)
            with stats_col1:
                st.metric("📊 Total Entries", len(df))
            with stats_col2:
                unique_cell_lines = df["cell_line"].nunique()
                st.metric("🧬 Cell Lines", unique_cell_lines)
            with stats_col3:
                unique_operators = df["operator"].nunique()
                st.metric("👥 Operators", unique_operators)
            with stats_col4:
                date_range = f"{df['date'].min()} to {df['date'].max()}"
                st.metric("📅 Date Range", f"{(pd.to_datetime(df['date'].max()) - pd.to_datetime(df['date'].min())).days + 1} days")
        
        # Add ID column and action columns for editing/deleting
        df_with_actions = df.copy()
        display_cols = [
            "id", "date", "cell_line", "event_type", "passage", "vessel", "location", "medium", "cell_type", "volume", "notes", "operator", "thaw_id", "cryo_vial_position", "assigned_to", "next_action_date", "created_by"
        ]
        for c in display_cols:
            if c not in df_with_actions.columns:
                df_with_actions[c] = ""
        
        pretty = df_with_actions[display_cols].rename(columns={
            "id": "ID",
            "date": "Date",
            "cell_line": "Cell Line",
            "event_type": "Event Type",
            "passage": "Passage",
            "vessel": "Vessel",
            "location": "Location",
            "medium": "Culture Medium",
            "cell_type": "Cell Type",
            "volume": "Volume (mL)",
            "notes": "Notes",
            "operator": "Operator",
            "thaw_id": "Thaw ID",
            "cryo_vial_position": "Cryo Vial Position",
            "assigned_to": "Assigned To",
            "next_action_date": "Next Action Date",
            "created_by": "Created By",
        })
        
        # Display the dataframe
        st.dataframe(pretty, width='stretch')
        
        # Action buttons section
        st.markdown("---")
        st.subheader("📝 Individual Entry Actions")
        
        action_col1, action_col2 = st.columns(2)
        
        with action_col1:
            st.markdown("**Edit Entry**")
            edit_id = st.number_input("Enter ID to edit", min_value=1, step=1, value=1)
            if st.button("� Edit Entry"):
                st.session_state["editing_log_id"] = edit_id
                st.rerun()
        
        with action_col2:
            st.markdown("**Delete Entry**")
            delete_id = st.number_input("Enter ID to delete", min_value=1, step=1, value=1)
            confirm_delete = st.checkbox("I confirm I want to delete this entry")
            if st.button("🗑️ Delete Entry") and confirm_delete:
                if delete_log(conn, delete_id):
                    st.success(f"✅ Entry {delete_id} deleted successfully!")
                    st.rerun()
                else:
                    st.error(f"❌ Entry {delete_id} not found or could not be deleted.")

        
        # Edit form (appears when editing)
        if "editing_log_id" in st.session_state:
            edit_log_id = st.session_state["editing_log_id"]
            existing_log = get_log_by_id(conn, edit_log_id)
            
            if existing_log:
                st.markdown("---")
                st.subheader(f"✏️ Editing Entry ID: {edit_log_id}")
                
                with st.form(f"edit_form_{edit_log_id}"):
                    # Pre-fill form with existing values
                    edit_cell_line = st.text_input("Cell Line ID", value=existing_log.get("cell_line", ""))
                    edit_event_type = st.selectbox("Event Type", 
                        options=["Observation", "Media Change", "Split", "Thawing", "Cryopreservation", "Other"],
                        index=["Observation", "Media Change", "Split", "Thawing", "Cryopreservation", "Other"].index(existing_log.get("event_type", "Observation")) 
                        if existing_log.get("event_type") in ["Observation", "Media Change", "Split", "Thawing", "Cryopreservation", "Other"] else 0
                    )
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        edit_passage = st.number_input("Passage No.", min_value=1, step=1, 
                                                     value=int(existing_log.get("passage", 1)) if existing_log.get("passage") else 1)
                    with col2:
                        edit_vessel = st.text_input("Vessel", value=existing_log.get("vessel", ""))
                    with col3:
                        edit_location = st.text_input("Location", value=existing_log.get("location", ""))
                    
                    edit_medium = st.text_input("Culture Medium", value=existing_log.get("medium", ""))
                    edit_cell_type = st.text_input("Cell Type", value=existing_log.get("cell_type", ""))
                    edit_volume = st.number_input("Volume (mL)", min_value=0.0, step=0.5, 
                                                value=float(existing_log.get("volume", 0.0)) if existing_log.get("volume") else 0.0)
                    edit_notes = st.text_area("Notes / Observations", value=existing_log.get("notes", ""))
                    
                    # User and date fields
                    user_rows = conn.execute("SELECT username FROM users ORDER BY username").fetchall()
                    usernames = [r[0] for r in user_rows]
                    current_operator = existing_log.get("operator", "")
                    if usernames and current_operator in usernames:
                        op_index = usernames.index(current_operator)
                    else:
                        op_index = 0
                    edit_operator = st.selectbox("Operator", options=usernames if usernames else [current_operator], 
                                               index=op_index if usernames else 0)
                    
                    # Parse existing date
                    try:
                        existing_date = datetime.fromisoformat(existing_log.get("date", "")).date()
                    except:
                        existing_date = date.today()
                    edit_date = st.date_input("Date", value=existing_date)
                    
                    # Assignment fields
                    all_users = get_all_users(conn)
                    current_assigned = existing_log.get("assigned_to", "")
                    assigned_options = ["(unassigned)"] + all_users
                    assigned_index = 0
                    if current_assigned and current_assigned in all_users:
                        assigned_index = assigned_options.index(current_assigned)
                    
                    edit_assigned_to = st.selectbox("Assigned To", options=assigned_options, index=assigned_index)
                    
                    # Parse existing next action date
                    existing_next_date = None
                    if existing_log.get("next_action_date"):
                        try:
                            existing_next_date = datetime.fromisoformat(existing_log.get("next_action_date")).date()
                        except:
                            pass
                    edit_next_action_date = st.date_input("Next Action Date", value=existing_next_date)
                    
                    # Form buttons
                    col_save, col_cancel = st.columns(2)
                    with col_save:
                        save_changes = st.form_submit_button("💾 Save Changes")
                    with col_cancel:
                        cancel_edit = st.form_submit_button("❌ Cancel")
                    
                    if save_changes:
                        # Prepare update payload
                        update_payload = {
                            "date": edit_date.isoformat(),
                            "cell_line": edit_cell_line,
                            "event_type": edit_event_type,
                            "passage": int(edit_passage) if edit_passage else None,
                            "vessel": edit_vessel,
                            "location": edit_location,
                            "medium": edit_medium,
                            "cell_type": edit_cell_type,
                            "volume": float(edit_volume) if edit_volume is not None else None,
                            "notes": edit_notes,
                            "operator": edit_operator,
                            "assigned_to": None if edit_assigned_to == "(unassigned)" else edit_assigned_to,
                            "next_action_date": edit_next_action_date.isoformat() if edit_next_action_date else None,
                        }
                        
                        if update_log(conn, edit_log_id, update_payload):
                            st.success(f"✅ Entry {edit_log_id} updated successfully!")
                            del st.session_state["editing_log_id"]
                            st.rerun()
                        else:
                            st.error(f"❌ Failed to update entry {edit_log_id}")
                    
                    if cancel_edit:
                        del st.session_state["editing_log_id"]
                        st.rerun()
            else:
                st.error(f"❌ Entry {edit_log_id} not found!")
                del st.session_state["editing_log_id"]
        
        # Export options
        export_col1, export_col2, export_col3 = st.columns(3)
        
        with export_col1:
            # CSV download
            csv = pretty.to_csv(index=False).encode('utf-8')
            st.download_button("📂 Download CSV", data=csv, file_name="ipsc_culture_log.csv", mime="text/csv")
        
        with export_col2:
            # Excel download
            if st.button("📊 Export to Excel"):
                try:
                    # Create filters from current UI state
                    filters = {}
                    if f_cell:
                        # Use contains logic for cell line
                        # For exact match export, we'll pass the filter as-is
                        pass  # We'll export all filtered data from current view
                    
                    # For Excel export, we'll export the current filtered dataframe
                    # Convert the displayed dataframe to Excel
                    excel_buffer = io.BytesIO()
                    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                        pretty.to_excel(writer, sheet_name='iPSC_Logs', index=False)
                        
                        # Add filter summary sheet
                        filter_summary = pd.DataFrame({
                            'Applied_Filters': [
                                f'Cell Line: {f_cell if f_cell else "All"}',
                                f'Event Type: {f_event}',
                                f'Operator: {f_operator}',
                                f'Assigned To: {f_assigned if f_assigned else "All"}',
                                f'Only Mine: {"Yes" if only_mine else "No"}',
                                f'Medium: {f_medium}',
                                f'Location: {f_location}',
                                f'Vessel: {f_vessel}',
                                f'Passage Range: {f_passage_min}-{f_passage_max}',
                                f'Date From: {f_start_date if f_start_date else "All"}',
                                f'Date To: {f_end_date if f_end_date else "All"}',
                                f'Sort By: {sort_by}',
                                f'Export Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
                            ]
                        })
                        filter_summary.to_excel(writer, sheet_name='Filter_Summary', index=False)
                    
                    excel_buffer.seek(0)
                    
                    st.download_button(
                        label="⬇️ Download Excel File",
                        data=excel_buffer.getvalue(),
                        file_name=f"ipsc_filtered_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key="history_excel_download"
                    )
                    st.success("✅ Excel file ready for download!")
                except Exception as e:
                    st.error(f"❌ Excel export failed: {str(e)}")
        
        with export_col3:
            # Lab Book Copy-Paste functionality
            if st.button("📋 Lab Book Format"):
                st.session_state["show_lab_format"] = True
                st.rerun()
        
        # Lab Book Format Display (appears when button is clicked)
        if st.session_state.get("show_lab_format", False):
            st.markdown("---")
            st.markdown("### 📋 Lab Book Copy-Paste Formats")
            
            format_col1, format_col2 = st.columns(2)
            
            with format_col1:
                format_type = st.selectbox(
                    "Choose Format Style:",
                    ["🔬 Detailed Lab Format", "📝 Compact Summary", "📊 Table Format", "📋 Simple List"]
                )
            
            with format_col2:
                include_options = st.multiselect(
                    "Include Additional Info:",
                    ["🕒 Time stamps", "📍 Locations", "🧪 Vessels", "📊 Passage numbers", "👤 Operators", "📝 Notes"],
                    default=["📍 Locations", "🧪 Vessels", "📊 Passage numbers"]
                )
            
            # Generate formatted text based on selection
            if format_type == "🔬 Detailed Lab Format":
                formatted_text = generate_detailed_lab_format(pretty, include_options)
            elif format_type == "📝 Compact Summary":
                formatted_text = generate_compact_format(pretty, include_options)
            elif format_type == "📊 Table Format":
                formatted_text = generate_table_format(pretty, include_options)
            else:  # Simple List
                formatted_text = generate_simple_list_format(pretty, include_options)
            
            # Display formatted text with copy button
            st.markdown("#### 📄 Formatted Output:")
            st.text_area(
                "Copy this text to your lab book:",
                value=formatted_text,
                height=300,
                help="Select all text (Ctrl+A) and copy (Ctrl+C) to paste into your lab book"
            )
            
            # Backup copy instructions
            st.caption("💡 **Manual Copy Instructions:** If the copy button doesn't work, select all text in the box above (Ctrl+A or Cmd+A), then copy (Ctrl+C or Cmd+C) and paste into your lab book.")
            
            # Quick action buttons
            copy_col1, copy_col2, copy_col3 = st.columns(3)
            with copy_col1:
                # Simple and reliable copy approach
                st.markdown("**📋 Copy Options:**")
                
                # Option 1: Try pyperclip for direct copying (works locally, not in Docker)
                clipboard_available = False
                try:
                    import pyperclip
                    # Test if clipboard actually works
                    pyperclip.copy("")
                    clipboard_available = True
                except (ImportError, FileNotFoundError, Exception):
                    # Clipboard not available (Docker, headless environments, etc.)
                    clipboard_available = False
                
                if clipboard_available:
                    if st.button("📋 Copy to Clipboard", help="Direct copy using pyperclip", type="primary"):
                        try:
                            pyperclip.copy(formatted_text)
                            st.success("✅ **Copied to clipboard!** You can now paste (Ctrl+V) in your lab book.")
                            st.balloons()
                        except Exception:
                            st.warning("⚠️ Clipboard copy failed. Please use manual copy (Ctrl+A, Ctrl+C)")
                else:
                    # Option 2: Show instructions prominently (fallback for Docker/restricted environments)
                    if st.button("📋 Copy to Clipboard", help="Click to get copy instructions", type="primary"):
                        st.success("✅ **How to Copy:**")
                        st.info("1. **Select All**: Click in the text area above and press `Ctrl+A` (or `Cmd+A` on Mac)\n"
                               "2. **Copy**: Press `Ctrl+C` (or `Cmd+C` on Mac)\n"
                               "3. **Paste**: Go to your lab book and press `Ctrl+V` (or `Cmd+V` on Mac)")
                        st.balloons()
                
                # Option 3: Auto-select text area (works better in some browsers)
                auto_select_html = f"""
                <div style="margin: 5px 0;">
                    <button onclick="selectAllText()" 
                            style="background-color: #0066cc; 
                                   border: none; 
                                   color: white; 
                                   padding: 6px 12px; 
                                   font-size: 12px; 
                                   border-radius: 3px; 
                                   cursor: pointer;">
                        🎯 Select All Text
                    </button>
                    <span id="select-status" style="margin-left: 10px; color: blue; font-size: 12px;"></span>
                </div>
                
                <script>
                function selectAllText() {{
                    // Find the text area containing the formatted text
                    const textareas = document.querySelectorAll('textarea');
                    let targetTextarea = null;
                    
                    // Look for the textarea with our content
                    for (let i = 0; i < textareas.length; i++) {{
                        if (textareas[i].value && textareas[i].value.length > 100) {{
                            targetTextarea = textareas[i];
                            break;
                        }}
                    }}
                    
                    if (targetTextarea) {{
                        targetTextarea.focus();
                        targetTextarea.select();
                        targetTextarea.setSelectionRange(0, targetTextarea.value.length);
                        document.getElementById('select-status').innerHTML = '✅ Text selected! Press Ctrl+C to copy';
                        
                        setTimeout(() => {{
                            document.getElementById('select-status').innerHTML = '';
                        }}, 4000);
                    }} else {{
                        document.getElementById('select-status').innerHTML = '⚠️ Please select manually';
                        setTimeout(() => {{
                            document.getElementById('select-status').innerHTML = '';
                        }}, 3000);
                    }}
                }}
                </script>
                """
                
                st.markdown(auto_select_html, unsafe_allow_html=True)
            
            with copy_col2:
                # Save as text file
                st.download_button(
                    label="💾 Download as Text",
                    data=formatted_text.encode('utf-8'),
                    file_name=f"lab_book_entries_{datetime.now().strftime('%Y%m%d')}.txt",
                    mime="text/plain"
                )
            
            with copy_col3:
                if st.button("❌ Close Format"):
                    st.session_state["show_lab_format"] = False
                    st.rerun()
    else:
        st.info("No entries yet — add your first log in Add Entry tab.")

with tab_thaw:
    st.subheader("🧊 Vial Lifecycle Tracking")
    
    # Tab selection for different tracking views
    tracking_tab1, tracking_tab2, tracking_tab3, tracking_tab4 = st.tabs(["📊 Vial Timeline", "🧬 Experimental Journey", "📈 Active Vials", "🔍 Vial Analytics"])
    
    with tracking_tab1:
        st.markdown("### Individual Vial Timeline")
        thaw_ids_list = list_distinct_thaw_ids(conn)
        
        if thaw_ids_list:
            selected_tid = st.selectbox("Select Thaw ID", options=["(choose)"] + thaw_ids_list)
            
            if selected_tid != "(choose)":
                # Get comprehensive lifecycle data
                lifecycle = get_vial_lifecycle(conn, selected_tid)
                
                if lifecycle:
                    # Vial Summary Cards
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Culture Days", lifecycle.get('culture_days', 0))
                    with col2:
                        st.metric("Current Passage", f"P{lifecycle.get('current_passage', 'N/A')}")
                    with col3:
                        st.metric("Total Events", lifecycle.get('total_events', 0))
                    with col4:
                        splits = len([e for e in lifecycle.get('events', []) if e.get('event_type') == 'Split'])
                        st.metric("Total Splits", splits)
                    
                    # Current Status
                    st.markdown("### 📋 Current Status")
                    status_col1, status_col2 = st.columns(2)
                    
                    with status_col1:
                        st.info(f"""
                        **Current Vessel:** {lifecycle.get('current_vessel', 'N/A')}  
                        **Current Medium:** {lifecycle.get('current_medium', 'N/A')}  
                        **Current Location:** {lifecycle.get('current_location', 'N/A')}
                        """)
                    
                    with status_col2:
                        # Alerts and recommendations
                        alerts = get_vial_alerts(conn, selected_tid)
                        if alerts:
                            st.markdown("**🚨 Alerts & Recommendations:**")
                            for alert in alerts:
                                if alert['type'] == 'critical':
                                    st.error(f"🚨 {alert['message']}")
                                elif alert['type'] == 'warning':
                                    st.warning(alert['message'])
                                else:
                                    st.info(alert['message'])
                        else:
                            st.success("✅ No alerts for this vial")
                    
                    # Passage Progression Visualization
                    if lifecycle.get('passage_progression'):
                        st.markdown("### 📈 Passage Progression")
                        
                        progression_data = []
                        for p in lifecycle['passage_progression']:
                            progression_data.append({
                                'Date': p['date'][:10],
                                'Passage': f"P{p['passage']}",
                                'Event': p['event_type'],
                                'Vessel': p['vessel'],
                                'Medium': p['medium']
                            })
                        
                        if progression_data:
                            prog_df = pd.DataFrame(progression_data)
                            st.dataframe(prog_df, width='stretch')
                            
                            # Simple passage number chart
                            try:
                                import matplotlib.pyplot as plt
                                fig, ax = plt.subplots(figsize=(10, 4))
                                dates = [p['date'][:10] for p in lifecycle['passage_progression']]
                                passages = [p['passage'] for p in lifecycle['passage_progression']]
                                ax.plot(range(len(dates)), passages, marker='o', linewidth=2)
                                ax.set_xticks(range(len(dates)))
                                ax.set_xticklabels(dates, rotation=45)
                                ax.set_ylabel('Passage Number')
                                ax.set_title(f'Passage Progression for {selected_tid}')
                                ax.grid(True, alpha=0.3)
                                plt.tight_layout()
                                st.pyplot(fig)
                            except ImportError:
                                # Fallback if matplotlib not available
                                st.info("Install matplotlib for passage progression charts")
                    
                    # Detailed Event Timeline
                    st.markdown("### 📅 Detailed Event Timeline")
                    
                    # Create enhanced timeline display
                    events = lifecycle.get('events', [])
                    if events:
                        timeline_data = []
                        for i, event in enumerate(events):
                            # Add visual indicators
                            event_icon = {
                                'Thawing': '🧊',
                                'Split': '🔄',
                                'Observation': '👁️',
                                'Media Change': '🧪',
                                'Cryopreservation': '❄️'
                            }.get(event.get('event_type', ''), '📝')
                            
                            timeline_data.append({
                                'Day': i + 1,
                                'Date': event.get('date', '')[:10],
                                'Event': f"{event_icon} {event.get('event_type', '')}",
                                'Passage': f"P{event.get('passage', '')}" if event.get('passage') else "",
                                'Vessel': event.get('vessel', ''),
                                'Location': event.get('location', ''),
                                'Medium': event.get('medium', ''),
                                'Cell Type': event.get('cell_type', ''),
                                'Volume (mL)': event.get('volume', ''),
                                'Notes': (event.get('notes', '') or '')[:50] + "..." if len(event.get('notes', '') or '') > 50 else event.get('notes', ''),
                                'Operator': event.get('operator', ''),
                                'Cryo Position': event.get('cryo_vial_position', '')
                            })
                        
                        timeline_df = pd.DataFrame(timeline_data)
                        st.dataframe(timeline_df, width='stretch')
                        
                        # CSV download for this vial
                        csv_data = timeline_df.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            f"📂 Download {selected_tid} Timeline CSV",
                            data=csv_data,
                            file_name=f"{selected_tid}_timeline.csv",
                            mime="text/csv"
                        )
                    else:
                        st.info("No events found for this thaw ID")
                else:
                    st.error("No data found for this thaw ID")
        else:
            st.info("No thaw IDs found. Add some thawing events first.")
    
    with tracking_tab2:
        st.markdown("### 🧬 Experimental Journey Tracking")
        
        thaw_ids_list = list_distinct_thaw_ids(conn)
        if thaw_ids_list:
            journey_tid = st.selectbox("Select Thaw ID for Experimental Journey", options=["(choose)"] + thaw_ids_list, key="journey_thaw_select")
            
            if journey_tid != "(choose)":
                try:
                    from db import get_experimental_journey, get_experiment_recommendations
                    
                    # Get experimental journey data
                    journey = get_experimental_journey(conn, journey_tid)
                    
                    if journey:
                        # Journey Summary
                        st.markdown("### 🎯 Experimental Journey Summary")
                        
                        journey_col1, journey_col2, journey_col3, journey_col4 = st.columns(4)
                        
                        with journey_col1:
                            st.metric("Experimental Phases", journey.get('total_experimental_phases', 0))
                        with journey_col2:
                            st.metric("Active Experiments", len(journey.get('active_experiments', [])))
                        with journey_col3:
                            maintenance_count = len(journey.get('maintenance_events', []))
                            st.metric("Maintenance Events", maintenance_count)
                        with journey_col4:
                            total_exp_events = sum([data['total_events'] for data in journey.get('experimental_phases', {}).values()])
                            st.metric("Total Exp. Events", total_exp_events)
                        
                        # Active Experiments
                        active_experiments = journey.get('active_experiments', [])
                        if active_experiments:
                            st.markdown("### 🔬 Currently Active Experiments")
                            for exp in active_experiments:
                                exp_data = journey['experimental_phases'][exp]
                                st.info(f"""
                                **{exp}**  
                                📅 Started: {exp_data['start_date'][:10]}  
                                ⏱️ Duration: {exp_data['duration_days']} days  
                                📊 Events: {exp_data['total_events']}  
                                🎯 Stages: {', '.join(exp_data['stages']) if exp_data['stages'] else 'None recorded'}
                                """)
                        
                        # Experimental Phases Details
                        experimental_phases = journey.get('experimental_phases', {})
                        if experimental_phases:
                            st.markdown("### 🧪 Experimental Phases Breakdown")
                            
                            for exp_type, exp_data in experimental_phases.items():
                                with st.expander(f"🔬 {exp_type} ({exp_data['total_events']} events)", expanded=exp_type in active_experiments):
                                    
                                    # Phase summary
                                    phase_col1, phase_col2, phase_col3 = st.columns(3)
                                    
                                    with phase_col1:
                                        st.markdown(f"""
                                        **📅 Timeline:**  
                                        Start: {exp_data['start_date'][:10]}  
                                        End: {exp_data['end_date'][:10]}  
                                        Duration: {exp_data['duration_days']} days
                                        """)
                                    
                                    with phase_col2:
                                        completion_status = "✅ Completed" if exp_data['is_completed'] else "🔄 In Progress"
                                        st.markdown(f"""
                                        **📊 Progress:**  
                                        Status: {completion_status}  
                                        Events: {exp_data['total_events']}  
                                        Stages: {len(exp_data['stages'])}
                                        """)
                                    
                                    with phase_col3:
                                        st.markdown(f"""
                                        **🎯 Stages Covered:**  
                                        {', '.join(exp_data['stages']) if exp_data['stages'] else 'None recorded'}
                                        """)
                                    
                                    # Success metrics
                                    if exp_data['success_metrics']:
                                        st.markdown("**📈 Success Metrics:**")
                                        for metric in exp_data['success_metrics']:
                                            if metric:
                                                st.write(f"• {metric}")
                                    
                                    # Detailed events for this experiment
                                    st.markdown("**📝 Experimental Events:**")
                                    exp_events_data = []
                                    for event in exp_data['events']:
                                        exp_events_data.append({
                                            'Date': event.get('date', '')[:10],
                                            'Stage': event.get('experiment_stage', ''),
                                            'Event Type': event.get('event_type', ''),
                                            'Conditions': event.get('experimental_conditions', ''),
                                            'Protocol Ref': event.get('protocol_reference', ''),
                                            'Outcome': event.get('outcome_status', ''),
                                            'Success Metrics': event.get('success_metrics', ''),
                                            'Notes': (event.get('notes', '') or '')[:50] + "..." if len(event.get('notes', '') or '') > 50 else event.get('notes', ''),
                                            'Operator': event.get('operator', '')
                                        })
                                    
                                    if exp_events_data:
                                        exp_events_df = pd.DataFrame(exp_events_data)
                                        st.dataframe(exp_events_df, width='stretch')
                        
                        # Experiment Recommendations
                        st.markdown("### 💡 Experiment Recommendations")
                        try:
                            recommendations = get_experiment_recommendations(conn, journey_tid)
                            if recommendations:
                                for rec in recommendations:
                                    if rec['type'] == 'warning':
                                        st.warning(f"**{rec['category']}:** {rec['message']}")
                                    elif rec['type'] == 'suggestion':
                                        st.info(f"**{rec['category']}:** {rec['message']}")
                                    else:
                                        st.write(f"**{rec['category']}:** {rec['message']}")
                            else:
                                st.success("✅ No specific recommendations at this time")
                        except Exception as e:
                            st.info("Recommendations feature unavailable")
                        
                        # Maintenance Events Summary
                        maintenance_events = journey.get('maintenance_events', [])
                        if maintenance_events:
                            with st.expander(f"🧪 Culture Maintenance Events ({len(maintenance_events)})", expanded=False):
                                maintenance_data = []
                                for event in maintenance_events:
                                    maintenance_data.append({
                                        'Date': event.get('date', '')[:10],
                                        'Event Type': event.get('event_type', ''),
                                        'Passage': f"P{event.get('passage', '')}" if event.get('passage') else "",
                                        'Vessel': event.get('vessel', ''),
                                        'Medium': event.get('medium', ''),
                                        'Notes': (event.get('notes', '') or '')[:40] + "..." if len(event.get('notes', '') or '') > 40 else event.get('notes', ''),
                                        'Operator': event.get('operator', '')
                                    })
                                
                                if maintenance_data:
                                    maintenance_df = pd.DataFrame(maintenance_data)
                                    st.dataframe(maintenance_df, width='stretch')
                    
                    else:
                        st.info("No experimental journey data found for this vial. Only maintenance events recorded.")
                        
                        # Show basic lifecycle as fallback
                        lifecycle = get_vial_lifecycle(conn, journey_tid)
                        if lifecycle:
                            st.markdown("### 🧪 Basic Culture Timeline")
                            events = lifecycle.get('events', [])
                            basic_data = []
                            for event in events:
                                basic_data.append({
                                    'Date': event.get('date', '')[:10],
                                    'Event Type': event.get('event_type', ''),
                                    'Passage': f"P{event.get('passage', '')}" if event.get('passage') else "",
                                    'Notes': (event.get('notes', '') or '')[:50] + "..." if len(event.get('notes', '') or '') > 50 else event.get('notes', '')
                                })
                            
                            if basic_data:
                                basic_df = pd.DataFrame(basic_data)
                                st.dataframe(basic_df, width='stretch')
                        
                except ImportError:
                    st.error("Experimental journey tracking functions not available. Please update the database functions.")
            
        else:
            st.info("No thaw IDs found. Add some thawing events first to track experimental journeys.")
    
    with tracking_tab3:
        st.markdown("### 🔬 Active Vials Dashboard")
        
        # Controls
        col_days, col_refresh = st.columns([3, 1])
        with col_days:
            days_threshold = st.slider("Consider vials active if last event within (days):", 1, 90, 30)
        with col_refresh:
            if st.button("🔄 Refresh", key="refresh_active"):
                st.rerun()
        
        # Get active vials
        active_vials = get_active_vials(conn, days_threshold)
        
        if active_vials:
            st.success(f"Found {len(active_vials)} active vials")
            
            # Summary cards for all active vials
            active_summary = []
            for vial in active_vials:
                thaw_event = vial.get('thaw_event', {})
                latest_event = vial.get('latest_event', {})
                
                # Get analytics for alerts
                alerts = get_vial_alerts(conn, vial['thaw_id'])
                alert_count = len([a for a in alerts if a['type'] == 'warning'])
                
                active_summary.append({
                    'Thaw ID': vial['thaw_id'],
                    'Cell Line': thaw_event.get('cell_line', ''),
                    'Days Active': vial.get('culture_days', 0),
                    'Current Passage': f"P{vial.get('current_passage', 'N/A')}",
                    'Current Vessel': vial.get('current_vessel', ''),
                    'Current Medium': vial.get('current_medium', ''),
                    'Current Location': vial.get('current_location', ''),
                    'Total Events': vial.get('total_events', 0),
                    'Last Event': latest_event.get('date', '')[:10] if latest_event.get('date') else '',
                    'Last Event Type': latest_event.get('event_type', ''),
                    'Alerts': '⚠️' if alert_count > 0 else '✅'
                })
            
            # Display active vials table
            active_df = pd.DataFrame(active_summary)
            st.dataframe(active_df, width='stretch')
            
            # Quick actions section
            st.markdown("### ⚡ Quick Actions")
            
            if active_vials:
                quick_col1, quick_col2 = st.columns(2)
                
                with quick_col1:
                    st.markdown("**🚨 High Priority Vials:**")
                    high_priority = [v for v in active_vials if len(get_vial_alerts(conn, v['thaw_id'])) > 0]
                    
                    if high_priority:
                        # Sort vials by alert severity (critical first)
                        def get_max_alert_priority(vial):
                            alerts = get_vial_alerts(conn, vial['thaw_id'])
                            if any(a['type'] == 'critical' for a in alerts):
                                return 3
                            elif any(a['type'] == 'warning' for a in alerts):
                                return 2
                            else:
                                return 1
                        
                        high_priority.sort(key=get_max_alert_priority, reverse=True)
                        
                        for vial in high_priority[:3]:  # Show top 3
                            alerts = get_vial_alerts(conn, vial['thaw_id'])
                            critical_alerts = [a for a in alerts if a['type'] == 'critical']
                            warning_alerts = [a for a in alerts if a['type'] == 'warning']
                            
                            if critical_alerts:
                                st.error(f"**🚨 {vial['thaw_id']}**: {critical_alerts[0]['message']}")
                            elif warning_alerts:
                                st.warning(f"**⚠️ {vial['thaw_id']}**: {warning_alerts[0]['message']}")
                    else:
                        st.success("No high priority vials!")
                
                with quick_col2:
                    st.markdown("**📊 Quick Stats:**")
                    total_passages = sum([v.get('current_passage', 0) or 0 for v in active_vials])
                    avg_days = sum([v.get('culture_days', 0) for v in active_vials]) / len(active_vials)
                    
                    st.info(f"""
                    **Total Active Vials:** {len(active_vials)}  
                    **Average Culture Days:** {avg_days:.1f}  
                    **Highest Passage:** P{max([v.get('current_passage', 0) or 0 for v in active_vials])}  
                    **Total Culture Events:** {sum([v.get('total_events', 0) for v in active_vials])}
                    """)
        else:
            st.info(f"No active vials found within the last {days_threshold} days.")
    
    with tracking_tab3:
        st.markdown("### 📊 Vial Analytics & Insights")
        
        # Select vial for analytics
        thaw_ids_list = list_distinct_thaw_ids(conn)
        if thaw_ids_list:
            analytics_tid = st.selectbox("Select Thaw ID for Analytics", options=["(choose)"] + thaw_ids_list, key="analytics_thaw_select")
            
            if analytics_tid != "(choose)":
                analytics = get_vial_analytics(conn, analytics_tid)
                
                if analytics:
                    # Analytics Summary
                    st.markdown("### 📈 Culture Performance Metrics")
                    
                    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
                    
                    with metric_col1:
                        st.metric("Average Split Interval", f"{analytics.get('avg_passage_interval', 0):.1f} days")
                    with metric_col2:
                        st.metric("Total Splits", analytics.get('total_splits', 0))
                    with metric_col3:
                        st.metric("Media Changes", analytics.get('media_changes', 0))
                    with metric_col4:
                        st.metric("Observations", analytics.get('total_observations', 0))
                    
                    # Culture Conditions Analysis
                    st.markdown("### 🧪 Culture Conditions Used")
                    
                    cond_col1, cond_col2, cond_col3 = st.columns(3)
                    
                    with cond_col1:
                        st.markdown("**Media Used:**")
                        for medium in analytics.get('media_used', []):
                            st.write(f"• {medium}")
                    
                    with cond_col2:
                        st.markdown("**Vessels Used:**")
                        for vessel in analytics.get('vessels_used', []):
                            st.write(f"• {vessel}")
                    
                    with cond_col3:
                        st.markdown("**Locations Used:**")
                        for location in analytics.get('locations_used', []):
                            st.write(f"• {location}")
                    
                    # Event Frequency Analysis
                    st.markdown("### 📊 Event Frequency Analysis")
                    
                    event_freq = analytics.get('event_frequency', {})
                    if event_freq:
                        freq_data = []
                        for event_type, count in event_freq.items():
                            freq_data.append({'Event Type': event_type, 'Count': count})
                        
                        freq_df = pd.DataFrame(freq_data)
                        st.dataframe(freq_df, width='stretch')
                        
                        # Simple bar chart if possible
                        try:
                            import matplotlib.pyplot as plt
                            fig, ax = plt.subplots(figsize=(10, 6))
                            events = list(event_freq.keys())
                            counts = list(event_freq.values())
                            ax.bar(events, counts)
                            ax.set_title(f'Event Frequency for {analytics_tid}')
                            ax.set_ylabel('Number of Events')
                            plt.xticks(rotation=45)
                            plt.tight_layout()
                            st.pyplot(fig)
                        except ImportError:
                            st.info("Install matplotlib for event frequency charts")
                    
                    # Passage Interval Analysis
                    intervals = analytics.get('passage_intervals', [])
                    if intervals:
                        st.markdown("### ⏱️ Passage Interval Analysis")
                        
                        interval_col1, interval_col2 = st.columns(2)
                        
                        with interval_col1:
                            st.metric("Average Interval", f"{analytics.get('avg_passage_interval', 0):.1f} days")
                            st.metric("Shortest Interval", f"{min(intervals)} days" if intervals else "N/A")
                            st.metric("Longest Interval", f"{max(intervals)} days" if intervals else "N/A")
                        
                        with interval_col2:
                            if len(intervals) > 1:
                                import statistics
                                st.metric("Median Interval", f"{statistics.median(intervals):.1f} days")
                                if len(intervals) > 2:
                                    st.metric("Std Deviation", f"{statistics.stdev(intervals):.1f} days")
                                
                                # Recommendations
                                if analytics.get('avg_passage_interval', 0) > 7:
                                    st.warning("⚠️ Long passage intervals detected. Consider more frequent splitting.")
                                elif analytics.get('avg_passage_interval', 0) < 3:
                                    st.info("ℹ️ Frequent splitting detected. Monitor cell health.")
                else:
                    st.info("No analytics data available for this vial.")
        else:
            st.info("No vials available for analytics.")

with tab_weekend:
    st.subheader("🗓️ Weekend Task Management & Multi-Weekend Scheduling")
    st.caption("Advanced weekend planning with caliber tracking, multi-weekend scheduling, and extra work calculation")
    
    # Weekend task tabs
    weekend_tab1, weekend_tab2, weekend_tab3, weekend_tab4, weekend_tab5 = st.tabs([
        "🎯 Multi-Weekend Planning", 
        "📊 Weekend Analytics", 
        "⚡ Quick Actions",
        "🏆 Caliber & Extra Work",
        "📅 Yearly Calendar"
    ])
    
    with weekend_tab1:
        st.markdown("### 📅 Multi-Weekend Planning System")
        st.caption("Schedule different users for different weekends and track custom work")
        
        # Multi-weekend scheduling
        with st.expander("🗓️ Weekend Schedule Manager", expanded=True):
            st.markdown("**Schedule Weekend Assignments:**")
            
            schedule_col1, schedule_col2 = st.columns([2, 1])
            
            with schedule_col1:
                # Get next 4 weekends
                from datetime import datetime, timedelta
                today = datetime.now()
                weekends = []
                
                for week_offset in range(4):  # Next 4 weekends
                    # Calculate Saturday for this week
                    days_to_saturday = (5 - today.weekday()) % 7
                    if days_to_saturday == 0 and today.weekday() == 5:  # If today is Saturday
                        days_to_saturday = 7
                    
                    saturday = today + timedelta(days=days_to_saturday + (week_offset * 7))
                    sunday = saturday + timedelta(days=1)
                    
                    weekends.append({
                        'saturday': saturday,
                        'sunday': sunday,
                        'week_num': week_offset + 1
                    })
                
                st.markdown("**Weekend Assignments:**")
                
                # Load existing weekend schedules from database
                existing_schedules = get_weekend_schedules(conn)
                schedule_dict = {s['weekend_date']: s['assignee'] for s in existing_schedules}
                
                all_users = get_all_users(conn)
                current_user = st.session_state.get("my_name", "Unknown")
                
                for weekend in weekends:
                    saturday_str = weekend['saturday'].strftime('%Y-%m-%d')
                    sunday_str = weekend['sunday'].strftime('%Y-%m-%d')
                    weekend_key = saturday_str
                    
                    weekend_col1, weekend_col2, weekend_col3 = st.columns([2, 2, 1])
                    
                    with weekend_col1:
                        st.write(f"**Week {weekend['week_num']}:** {weekend['saturday'].strftime('%b %d')} - {weekend['sunday'].strftime('%b %d')}")
                    
                    with weekend_col2:
                        if all_users:
                            assignee_options = ["(unassigned)"] + all_users
                            # Get current assignee from database
                            current_assignee = schedule_dict.get(weekend_key, "(unassigned)")
                            
                            selected_assignee = st.selectbox(
                                "Assignee:",
                                options=assignee_options,
                                index=assignee_options.index(current_assignee) if current_assignee in assignee_options else 0,
                                key=f"weekend_assignee_{weekend_key}"
                            )
                            
                            # Save to database when selection changes
                            if selected_assignee != current_assignee and selected_assignee != "(unassigned)":
                                if save_weekend_schedule(conn, weekend_key, selected_assignee, current_user):
                                    st.success(f"✅ Saved {selected_assignee} for {weekend['saturday'].strftime('%b %d')}")
                                    st.rerun()  # Refresh to show updated assignment
                        else:
                            st.write("No users available")
                    
                    with weekend_col3:
                        if st.button("📝 Plan", key=f"plan_{weekend_key}"):
                            # Get the saved assignee from database
                            saved_assignee = get_weekend_assignee(conn, weekend_key)
                            if saved_assignee:
                                st.session_state['selected_weekend_assignee'] = saved_assignee
                                st.session_state['selected_weekend_saturday'] = saturday_str
                                st.session_state['selected_weekend_sunday'] = sunday_str
                                st.success(f"✅ Planning mode set for {saved_assignee}")
                            else:
                                st.warning("Please assign someone first")
            
            with schedule_col2:
                st.markdown("**Current Week:**")
                # Show current active weekend assignment
                active_assignee = st.session_state.get('selected_weekend_assignee')
                active_saturday = st.session_state.get('selected_weekend_saturday')
                
                if active_assignee and active_saturday:
                    st.info(f"""
                    **Active Planning:**  
                    👤 **{active_assignee}**  
                    📅 **{active_saturday}**
                    """)
                    st.caption("This assignee will auto-fill in Add Entry tab")
                    
                    # Clear weekend planning button
                    if st.button("🔄 Clear Weekend Planning", key="clear_weekend_planning"):
                        st.session_state['selected_weekend_assignee'] = None
                        st.session_state['selected_weekend_saturday'] = None
                        st.session_state['selected_weekend_sunday'] = None
                        st.success("✅ Weekend planning cleared")
                        st.rerun()
                else:
                    st.info("No active weekend planning set")
        
        # Custom work tracker
        with st.expander("📋 Custom Work Tracker", expanded=False):
            st.markdown("**Add Custom Weekend Work:**")
            st.caption("Track extra tasks beyond regular culture maintenance")
            
            custom_col1, custom_col2 = st.columns(2)
            
            with custom_col1:
                custom_task_type = st.selectbox(
                    "Task Type:",
                    ["Equipment Maintenance", "Lab Cleanup", "Inventory Count", "Training", "Documentation", "Protocol Development", "Other"],
                    key="custom_task_type"
                )
                
                if custom_task_type == "Other":
                    custom_task_type = st.text_input("Specify task type:", key="custom_task_other")
                
                custom_description = st.text_area("Task Description:", height=80, key="custom_task_desc")
                custom_hours = st.number_input("Estimated Hours:", min_value=0.5, max_value=8.0, step=0.5, key="custom_task_hours")
            
            with custom_col2:
                custom_assignee = st.selectbox("Assigned To:", options=all_users if all_users else ["No users"], key="custom_task_assignee")
                custom_date = st.date_input("Date:", key="custom_task_date")
                custom_priority = st.selectbox("Priority:", ["Low", "Medium", "High", "Critical"], key="custom_task_priority")
                
                if st.button("➕ Add Custom Work", key="add_custom_work"):
                    if custom_task_type and custom_description and custom_assignee != "No users":
                        # Store custom work in database
                        current_user = st.session_state.get("my_name", "Unknown")
                        
                        custom_work = {
                            "type": custom_task_type,
                            "description": custom_description,
                            "hours": custom_hours,
                            "assignee": custom_assignee,
                            "date": custom_date.isoformat(),
                            "priority": custom_priority
                        }
                        
                        if save_custom_weekend_work(conn, custom_work, current_user):
                            st.success(f"✅ Added custom work: {custom_task_type} for {custom_assignee}")
                            st.rerun()  # Refresh to show updated custom work
                        else:
                            st.error("Failed to save custom work")
                    else:
                        st.error("Please fill in all required fields")
        
        # Quick Friday setup
        with st.expander("🚀 Quick Friday Setup", expanded=True):
            st.markdown("**Fast track for creating weekend entries on Friday:**")
            
            quick_col1, quick_col2, quick_col3 = st.columns(3)
            
            with quick_col1:
                # Get upcoming weekend dates
                from datetime import datetime, timedelta
                today = datetime.now()
                days_to_saturday = (5 - today.weekday()) % 7
                if days_to_saturday == 0 and today.weekday() == 5:  # If today is Saturday
                    days_to_saturday = 7
                
                saturday = today + timedelta(days=days_to_saturday)
                sunday = saturday + timedelta(days=1)
                
                st.info(f"""
                **This Weekend:**  
                📅 Saturday: {saturday.strftime('%Y-%m-%d')} ({saturday.strftime('%B %d')})  
                📅 Sunday: {sunday.strftime('%Y-%m-%d')} ({sunday.strftime('%B %d')})
                """)
            
            with quick_col2:
                st.markdown("**Weekend Assignees:**")
                all_users = get_all_users(conn)
                
                if all_users:
                    weekend_assignee = st.selectbox("Who's working this weekend?", options=all_users, key="weekend_assignee")
                    # Auto-set the session state when assignee is selected
                    if weekend_assignee:
                        st.session_state['selected_weekend_assignee'] = weekend_assignee
                        st.session_state['selected_weekend_saturday'] = saturday.strftime('%Y-%m-%d')
                        st.session_state['selected_weekend_sunday'] = sunday.strftime('%Y-%m-%d')
                        st.success(f"✅ Weekend assignee set: {weekend_assignee}")
                        st.info("💡 This assignee will auto-fill in Add Entry tab for faster logging!")
                else:
                    weekend_assignee = st.text_input("Weekend assignee:", key="weekend_assignee_manual")
                    # Auto-set the session state when assignee is entered
                    if weekend_assignee:
                        st.session_state['selected_weekend_assignee'] = weekend_assignee
                        st.session_state['selected_weekend_saturday'] = saturday.strftime('%Y-%m-%d')
                        st.session_state['selected_weekend_sunday'] = sunday.strftime('%Y-%m-%d')
            
            with quick_col3:
                st.markdown("**Quick Actions:**")
                
                if st.button("📋 View Current Tasks", key="view_current_weekend"):
                    st.session_state['show_current_weekend'] = True
                    st.rerun()
        
        # Display current weekend tasks if requested
        if st.session_state.get('show_current_weekend'):
            st.markdown("---")
            st.markdown("### 📋 Current Weekend Tasks")
            
            weekend_tasks = get_weekend_tasks(conn, saturday.strftime('%Y-%m-%d'), sunday.strftime('%Y-%m-%d'))
            
            if weekend_tasks:
                # Group by assignee
                assignees = {}
                for task in weekend_tasks:
                    assignee = task.get('assigned_to', 'Unassigned')
                    if assignee not in assignees:
                        assignees[assignee] = []
                    assignees[assignee].append(task)
                
                for assignee, tasks in assignees.items():
                    with st.expander(f"👤 {assignee} ({len(tasks)} tasks)", expanded=True):
                        task_data = []
                        for task in tasks:
                            task_data.append({
                                'Date': task['next_action_date'],
                                'Cell Line': task['cell_line'],
                                'Task': task['event_type'],
                                'Current Vessel': task.get('current_vessel', 'N/A'),
                                'Current Medium': task.get('current_medium', 'N/A'),
                                'Current Passage': f"P{task.get('current_passage', 'N/A')}",
                                'Location': task.get('current_location', 'N/A'),
                                'Notes': (task.get('notes', '') or '')[:50] + "..." if len(task.get('notes', '') or '') > 50 else task.get('notes', '')
                            })
                        
                        if task_data:
                            task_df = pd.DataFrame(task_data)
                            st.dataframe(task_df, width='stretch')
            else:
                st.info("No weekend tasks scheduled yet. Use the Add Entry tab to schedule tasks.")

        # Media Volume Calculator
        st.markdown("---")
        with st.expander("🧪 Weekend Media Volume Calculator", expanded=False):
            st.markdown("**Calculate total media volumes needed for weekend culture maintenance**")
            
            calc_col1, calc_col2 = st.columns(2)
            
            with calc_col1:
                st.markdown("**📅 Weekend Date Range:**")
                calc_start_date = st.date_input("Start Date (Saturday):", value=saturday.date(), key="media_calc_start")
                calc_end_date = st.date_input("End Date (Sunday):", value=sunday.date(), key="media_calc_end")
                
                st.markdown("**🧬 Filter Options:**")
                calc_cell_lines = st.text_input("Cell lines (comma-separated, leave empty for all):", key="calc_cell_lines")
                calc_locations = st.text_input("Locations (comma-separated, leave empty for all):", key="calc_locations")
            
            with calc_col2:
                st.markdown("**⚗️ Media Types to Calculate:**")
                
                # Get all culture media from database
                media_options = get_ref_values(conn, "culture_medium")
                if not media_options:
                    media_options = ["E8", "mTeSR1", "TeSR-E8", "DMEM/F12", "Custom"]
                
                selected_media = st.multiselect("Select media types:", media_options, default=media_options[:3], key="calc_media")
                
                st.markdown("**📊 Safety Margins:**")
                safety_margin = st.slider("Safety margin (%)", min_value=0, max_value=50, value=20, key="calc_margin")
                extra_days = st.number_input("Extra prep days", min_value=0, max_value=3, value=1, key="calc_extra")
            
            if st.button("🧮 Calculate Media Volumes", key="calc_volumes"):
                try:
                    # Query active cultures and upcoming weekend tasks
                    weekend_calc_query = """
                    SELECT DISTINCT 
                        l.cell_line,
                        l.medium,
                        l.volume,
                        l.location,
                        l.vessel,
                        l.event_type,
                        l.assigned_to,
                        l.next_action_date
                    FROM logs l
                    WHERE (
                        (l.next_action_date BETWEEN ? AND ?) OR
                        (l.event_type IN ('Media Change', 'Split', 'Observation') AND 
                         l.date >= date('now', '-7 days'))
                    )
                    AND l.medium IS NOT NULL 
                    AND l.volume > 0
                    ORDER BY l.cell_line, l.medium
                    """
                    
                    results = conn.execute(weekend_calc_query, (calc_start_date.isoformat(), calc_end_date.isoformat())).fetchall()
                    
                    if results:
                        # Filter by cell lines if specified
                        if calc_cell_lines.strip():
                            filter_cell_lines = [cl.strip() for cl in calc_cell_lines.split(',')]
                            results = [r for r in results if any(fcl in r[0] for fcl in filter_cell_lines)]
                        
                        # Filter by locations if specified
                        if calc_locations.strip():
                            filter_locations = [loc.strip() for loc in calc_locations.split(',')]
                            results = [r for r in results if any(floc in r[3] for floc in filter_locations)]
                        
                        # Calculate volumes by media type
                        media_volumes = {}
                        culture_details = []
                        
                        for row in results:
                            cell_line, medium, volume, location, vessel, event_type, assigned_to, next_action = row
                            
                            if medium in selected_media:
                                # Estimate daily volume needs based on event type
                                daily_volume = volume
                                if event_type == 'Media Change':
                                    daily_volume = volume * 1.0  # Full media change
                                elif event_type == 'Split':
                                    daily_volume = volume * 1.5  # Additional volume for splitting
                                else:
                                    daily_volume = volume * 0.5  # Partial change for observation
                                
                                # Calculate weekend needs (2 days + extra days)
                                weekend_volume = daily_volume * (2 + extra_days)
                                
                                if medium not in media_volumes:
                                    media_volumes[medium] = 0
                                media_volumes[medium] += weekend_volume
                                
                                culture_details.append({
                                    'Cell Line': cell_line,
                                    'Medium': medium,
                                    'Location': location,
                                    'Current Volume': f"{volume} mL",
                                    'Est. Weekend Need': f"{weekend_volume:.1f} mL",
                                    'Next Action': next_action or 'TBD',
                                    'Assigned To': assigned_to or 'Unassigned'
                                })
                        
                        if media_volumes:
                            st.markdown("### 📊 Weekend Media Volume Summary")
                            
                            # Display summary metrics
                            summary_col1, summary_col2, summary_col3 = st.columns(3)
                            
                            total_volume = sum(media_volumes.values())
                            total_with_margin = total_volume * (1 + safety_margin/100)
                            
                            with summary_col1:
                                st.metric("Total Base Volume", f"{total_volume:.1f} mL")
                            with summary_col2:
                                st.metric("With Safety Margin", f"{total_with_margin:.1f} mL")
                            with summary_col3:
                                st.metric("Media Types", len(media_volumes))
                            
                            # Volume breakdown by media type
                            st.markdown("### 🧪 Volume Breakdown by Media Type")
                            
                            media_summary = []
                            for medium, base_vol in media_volumes.items():
                                vol_with_margin = base_vol * (1 + safety_margin/100)
                                media_summary.append({
                                    'Media Type': medium,
                                    'Base Volume (mL)': f"{base_vol:.1f}",
                                    f'With {safety_margin}% Margin (mL)': f"{vol_with_margin:.1f}",
                                    'Recommended Prep (mL)': f"{int(vol_with_margin/50)*50 + 50}"  # Round up to nearest 50mL
                                })
                            
                            media_df = pd.DataFrame(media_summary)
                            st.dataframe(media_df, width='stretch')
                            
                            # Detailed culture breakdown
                            st.markdown("### 📋 Detailed Culture Requirements")
                            if culture_details:
                                culture_df = pd.DataFrame(culture_details)
                                st.dataframe(culture_df, width='stretch')
                            
                            # Preparation checklist
                            st.markdown("### ✅ Preparation Checklist")
                            st.markdown("**Friday Media Preparation:**")
                            for medium, base_vol in media_volumes.items():
                                vol_with_margin = base_vol * (1 + safety_margin/100)
                                prep_vol = int(vol_with_margin/50)*50 + 50
                                st.markdown(f"- [ ] **{medium}**: Prepare {prep_vol} mL (includes {safety_margin}% safety margin)")
                            
                            st.markdown("**Additional Reminders:**")
                            st.markdown("- [ ] Check media expiration dates")
                            st.markdown("- [ ] Ensure adequate incubator space")
                            st.markdown("- [ ] Prepare sterile plasticware")
                            st.markdown("- [ ] Warm media to 37°C before use")
                            
                        else:
                            st.warning("No cultures found requiring the selected media types for the specified weekend.")
                    else:
                        st.info("No cultures found for the specified weekend period. Add some weekend tasks first!")
                        
                except Exception as e:
                    st.error(f"Error calculating media volumes: {str(e)}")

    with weekend_tab2:
        st.markdown("### ✅ Execute Weekend Tasks")
        st.caption("Mark tasks as completed and add notes")
        
        # Select date and assignee for task execution
        exec_col1, exec_col2 = st.columns(2)
        
        with exec_col1:
            exec_date = st.date_input("Select Date:", value=date.today(), key="exec_date")
        
        with exec_col2:
            all_users = get_all_users(conn)
            
            if all_users:
                exec_assignee = st.selectbox("Assignee:", options=["All"] + all_users, key="exec_assignee")
            else:
                exec_assignee = st.text_input("Assignee:", key="exec_assignee_manual")
        
        # Get tasks for the selected date
        if exec_assignee and exec_assignee != "All":
            tasks = get_weekend_tasks(conn, exec_date.isoformat(), exec_date.isoformat(), exec_assignee)
        else:
            tasks = get_weekend_tasks(conn, exec_date.isoformat(), exec_date.isoformat())
        
        if tasks:
            st.markdown(f"### 📋 Tasks for {exec_date.strftime('%A, %B %d, %Y')}")
            
            for i, task in enumerate(tasks):
                with st.expander(f"🧬 {task['cell_line']} - {task['event_type']} (P{task.get('current_passage', 'N/A')})", expanded=True):
                    # Task details
                    detail_col1, detail_col2 = st.columns(2)
                    
                    with detail_col1:
                        st.markdown(f"""
                        **Assignee:** {task.get('assigned_to', 'N/A')}  
                        **Current Vessel:** {task.get('current_vessel', 'N/A')}  
                        **Current Medium:** {task.get('current_medium', 'N/A')}  
                        **Location:** {task.get('current_location', 'N/A')}
                        """)
                    
                    with detail_col2:
                        st.markdown(f"""
                        **Thaw ID:** {task.get('thaw_id', 'N/A')}  
                        **Culture Days:** {task.get('culture_days', 'N/A')}  
                        **Original Notes:** {task.get('notes', 'None')}
                        """)
                    
                    # Task instructions
                    instructions = get_weekend_task_instructions(task['event_type'], task.get('current_passage'))
                    
                    inst_col1, inst_col2 = st.columns(2)
                    
                    with inst_col1:
                        st.markdown("**📋 Instructions:**")
                        st.info(f"**Summary:** {instructions['summary']}")
                        st.caption(f"**Time:** {instructions['time_estimate']}")
                        
                        with st.expander("📝 Detailed Steps", expanded=False):
                            for step in instructions['steps']:
                                st.write(step)
                            
                            if instructions.get('critical_notes'):
                                st.warning(f"⚠️ {instructions['critical_notes']}")
                    
                    with inst_col2:
                        st.markdown("**✅ Mark as Completed:**")
                        
                        completion_notes = st.text_area(
                            "Completion Notes:",
                            placeholder="Add observations, issues, or modifications made...",
                            key=f"completion_notes_{task['id']}"
                        )
                        
                        if st.button(f"Mark Completed ✅", key=f"complete_{task['id']}"):
                            if mark_weekend_task_completed(conn, task['id'], completion_notes):
                                st.success("✅ Task marked as completed!")
                                st.rerun()
                            else:
                                st.error("❌ Failed to mark task as completed")
        else:
            if exec_assignee:
                st.info(f"No tasks found for {exec_assignee} on {exec_date.strftime('%A, %B %d, %Y')}")
            else:
                st.info("Select an assignee to view their tasks")
    
    with weekend_tab3:
        st.markdown("### 📊 Weekend Summary & Analytics")
        
        # Summary date range
        summary_col1, summary_col2 = st.columns(2)
        
        with summary_col1:
            summary_start = st.date_input("From Date:", value=date.today() - timedelta(days=7), key="summary_start")
        
        with summary_col2:
            summary_end = st.date_input("To Date:", value=date.today(), key="summary_end")
        
        # Get weekend tasks in range
        all_weekend_tasks = get_weekend_tasks(conn, summary_start.isoformat(), summary_end.isoformat())
        
        if all_weekend_tasks:
            # Summary metrics
            total_tasks = len(all_weekend_tasks)
            completed_tasks = len([t for t in all_weekend_tasks if not t.get('next_action_date')])
            pending_tasks = total_tasks - completed_tasks
            
            metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
            
            with metric_col1:
                st.metric("Total Tasks", total_tasks)
            with metric_col2:
                st.metric("Completed", completed_tasks)
            with metric_col3:
                st.metric("Pending", pending_tasks)
            with metric_col4:
                completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
                st.metric("Completion Rate", f"{completion_rate:.1f}%")
            
            # Task breakdown by assignee
            st.markdown("### 👥 Tasks by Assignee")
            
            assignee_stats = {}
            for task in all_weekend_tasks:
                assignee = task.get('assigned_to', 'Unassigned')
                if assignee not in assignee_stats:
                    assignee_stats[assignee] = {'total': 0, 'completed': 0}
                assignee_stats[assignee]['total'] += 1
                if not task.get('next_action_date'):
                    assignee_stats[assignee]['completed'] += 1
            
            assignee_data = []
            for assignee, stats in assignee_stats.items():
                completion_rate = (stats['completed'] / stats['total'] * 100) if stats['total'] > 0 else 0
                assignee_data.append({
                    'Assignee': assignee,
                    'Total Tasks': stats['total'],
                    'Completed': stats['completed'],
                    'Pending': stats['total'] - stats['completed'],
                    'Completion Rate': f"{completion_rate:.1f}%"
                })
            
            if assignee_data:
                assignee_df = pd.DataFrame(assignee_data)
                st.dataframe(assignee_df, width='stretch')
            
            # Task type breakdown
            st.markdown("### 📋 Tasks by Type")
            
            task_types = {}
            for task in all_weekend_tasks:
                task_type = task.get('event_type', 'Unknown')
                if task_type not in task_types:
                    task_types[task_type] = 0
                task_types[task_type] += 1
            
            if task_types:
                type_data = [{'Task Type': k, 'Count': v} for k, v in task_types.items()]
                type_df = pd.DataFrame(type_data)
                st.dataframe(type_df, width='stretch')
            
            # Recent weekend activity
            st.markdown("### 📅 Recent Weekend Activity")
            
            # Group by date
            activity_by_date = {}
            for task in all_weekend_tasks:
                task_date = task.get('next_action_date', 'Unknown')
                if task_date not in activity_by_date:
                    activity_by_date[task_date] = []
                activity_by_date[task_date].append(task)
            
            for task_date in sorted(activity_by_date.keys(), reverse=True)[:5]:  # Show last 5 dates
                tasks_on_date = activity_by_date[task_date]
                completed_on_date = len([t for t in tasks_on_date if not t.get('next_action_date')])
                
                with st.expander(f"📅 {task_date} ({len(tasks_on_date)} tasks, {completed_on_date} completed)", expanded=False):
                    date_data = []
                    for task in tasks_on_date:
                        status = "✅ Completed" if not task.get('next_action_date') else "⏳ Pending"
                        date_data.append({
                            'Status': status,
                            'Assignee': task.get('assigned_to', 'N/A'),
                            'Cell Line': task['cell_line'],
                            'Task': task['event_type'],
                            'Vessel': task.get('current_vessel', 'N/A'),
                            'Notes': (task.get('notes', '') or '')[:50] + "..." if len(task.get('notes', '') or '') > 50 else task.get('notes', '')
                        })
                    
                    if date_data:
                        date_df = pd.DataFrame(date_data)
                        st.dataframe(date_df, width='stretch')
        else:
            st.info("No weekend tasks found in the selected date range.")
    
    with weekend_tab4:
        st.markdown("### 🏆 Caliber System & Extra Work Tracking")
        st.caption("Track user performance, extra work hours, and calculate weekend contributions")
        
        # Caliber tracking section
        with st.expander("📊 User Caliber & Performance", expanded=True):
            st.markdown("**Weekend Performance Tracking:**")
            
            caliber_col1, caliber_col2 = st.columns(2)
            
            with caliber_col1:
                # User caliber settings
                st.markdown("**Set User Caliber Levels:**")
                all_users = get_all_users(conn)
                current_user = st.session_state.get("my_name", "Unknown")
                
                # Load existing calibers from database
                existing_calibers = get_user_calibers(conn)
                
                for user in all_users:
                    current_caliber = existing_calibers.get(user, "Standard")
                    caliber_levels = ["Trainee", "Standard", "Advanced", "Expert", "Lead"]
                    
                    user_caliber = st.selectbox(
                        f"Caliber for {user}:",
                        options=caliber_levels,
                        index=caliber_levels.index(current_caliber),
                        key=f"caliber_{user}"
                    )
                    
                    # Save to database when caliber changes
                    if user_caliber != current_caliber:
                        if save_user_caliber(conn, user, user_caliber, current_user):
                            st.success(f"✅ Updated caliber for {user}: {user_caliber}")
                            st.rerun()  # Refresh to show updated caliber
            
            with caliber_col2:
                # Performance metrics
                st.markdown("**Performance Metrics:**")
                selected_user = st.selectbox("Select user for metrics:", options=all_users if all_users else ["No users"])
                
                if selected_user and selected_user != "No users":
                    # Get caliber from database
                    user_calibers_db = get_user_calibers(conn)
                    user_caliber = user_calibers_db.get(selected_user, "Standard")
                    st.info(f"**{selected_user}** - Caliber: **{user_caliber}**")
                    
                    # Calculate user's weekend work (last 4 weeks)
                    four_weeks_ago = date.today() - timedelta(days=28)
                    user_tasks = get_weekend_tasks(conn, four_weeks_ago.isoformat(), date.today().isoformat())
                    user_weekend_tasks = [t for t in user_tasks if t.get('assigned_to') == selected_user]
                    
                    performance_col1, performance_col2 = st.columns(2)
                    
                    with performance_col1:
                        st.metric("Weekend Tasks (4 weeks)", len(user_weekend_tasks))
                        completed_user_tasks = [t for t in user_weekend_tasks if not t.get('next_action_date')]
                        completion_rate = (len(completed_user_tasks) / len(user_weekend_tasks) * 100) if user_weekend_tasks else 0
                        st.metric("Completion Rate", f"{completion_rate:.1f}%")
                    
                    with performance_col2:
                        # Calculate estimated hours based on caliber
                        caliber_multipliers = {"Trainee": 1.5, "Standard": 1.0, "Advanced": 0.8, "Expert": 0.6, "Lead": 0.5}
                        base_hours_per_task = 0.5  # Base estimate
                        multiplier = caliber_multipliers.get(user_caliber, 1.0)
                        estimated_hours = len(user_weekend_tasks) * base_hours_per_task * multiplier
                        st.metric("Estimated Hours", f"{estimated_hours:.1f}h")
                        
                        # Add custom work hours from database
                        four_weeks_ago_str = four_weeks_ago.isoformat()
                        today_str = date.today().isoformat()
                        user_custom_work = get_custom_weekend_work(conn, four_weeks_ago_str, today_str)
                        user_custom_hours = sum([w["hours"] for w in user_custom_work if w.get("assignee") == selected_user])
                        st.metric("Custom Work Hours", f"{user_custom_hours:.1f}h")
        
        # Extra work calculation
        with st.expander("📈 Extra Work & Overtime Calculation", expanded=True):
            st.markdown("**Weekend Work Summary:**")
            
            calc_col1, calc_col2 = st.columns(2)
            
            with calc_col1:
                # Date range for calculation
                calc_start = st.date_input("Calculate from:", value=date.today() - timedelta(days=30), key="calc_start")
                calc_end = st.date_input("Calculate to:", value=date.today(), key="calc_end")
                
                if st.button("🧮 Calculate Extra Work"):
                    # Get all weekend tasks in range
                    range_tasks = get_weekend_tasks(conn, calc_start.isoformat(), calc_end.isoformat())
                    
                    # Get custom work from database in date range
                    custom_work = get_custom_weekend_work(conn, calc_start.isoformat(), calc_end.isoformat())
                    
                    # Get user calibers from database
                    user_calibers_db = get_user_calibers(conn)
                    
                    # Calculate by user
                    user_summaries = {}
                    
                    # Regular weekend tasks
                    for task in range_tasks:
                        assignee = task.get('assigned_to', 'Unassigned')
                        if assignee not in user_summaries:
                            user_summaries[assignee] = {
                                'regular_tasks': 0,
                                'custom_hours': 0,
                                'estimated_hours': 0,
                                'caliber': user_calibers_db.get(assignee, "Standard")
                            }
                        user_summaries[assignee]['regular_tasks'] += 1
                    
                    # Custom work hours
                    for work in custom_work:
                        assignee = work.get('assignee', 'Unassigned')
                        if assignee not in user_summaries:
                            user_summaries[assignee] = {
                                'regular_tasks': 0,
                                'custom_hours': 0,
                                'estimated_hours': 0,
                                'caliber': user_calibers_db.get(assignee, "Standard")
                            }
                        user_summaries[assignee]['custom_hours'] += work.get('hours', 0)
                    
                    # Calculate estimated hours
                    caliber_multipliers = {"Trainee": 1.5, "Standard": 1.0, "Advanced": 0.8, "Expert": 0.6, "Lead": 0.5}
                    base_hours_per_task = 0.5
                    
                    for user, summary in user_summaries.items():
                        multiplier = caliber_multipliers.get(summary['caliber'], 1.0)
                        summary['estimated_hours'] = summary['regular_tasks'] * base_hours_per_task * multiplier
                    
                    # Store results
                    st.session_state["work_calculation_results"] = user_summaries
                    st.session_state["calculation_period"] = f"{calc_start} to {calc_end}"
            
            with calc_col2:
                # Display results
                if "work_calculation_results" in st.session_state:
                    st.markdown(f"**Results for {st.session_state['calculation_period']}:**")
                    
                    results_data = []
                    total_hours = 0
                    
                    for user, summary in st.session_state["work_calculation_results"].items():
                        total_user_hours = summary['estimated_hours'] + summary['custom_hours']
                        total_hours += total_user_hours
                        
                        results_data.append({
                            'User': user,
                            'Caliber': summary['caliber'],
                            'Tasks': summary['regular_tasks'],
                            'Task Hours': f"{summary['estimated_hours']:.1f}",
                            'Custom Hours': f"{summary['custom_hours']:.1f}",
                            'Total Hours': f"{total_user_hours:.1f}"
                        })
                    
                    if results_data:
                        results_df = pd.DataFrame(results_data)
                        st.dataframe(results_df, width='stretch')
                        
                        st.success(f"**Total Weekend Work: {total_hours:.1f} hours**")
                        
                        # Export option
                        if st.button("📊 Export Results"):
                            csv = results_df.to_csv(index=False)
                            st.download_button(
                                label="💾 Download CSV",
                                data=csv,
                                file_name=f"weekend_work_summary_{calc_start}_{calc_end}.csv",
                                mime="text/csv"
                            )
                else:
                    st.info("Click 'Calculate Extra Work' to see results")
        
        # Custom work display
        with st.expander("📋 Custom Work Log", expanded=False):
            # Get custom work from database
            custom_work = get_custom_weekend_work(conn)
            
            if custom_work:
                st.markdown("**Logged Custom Work:**")
                
                custom_data = []
                for work in custom_work:
                    custom_data.append({
                        'Date': work['date'],
                        'Type': work['type'],
                        'Description': work['description'][:50] + "..." if len(work['description']) > 50 else work['description'],
                        'Hours': work['hours'],
                        'Assignee': work['assignee'],
                        'Priority': work['priority'],
                        'Created By': work['created_by']
                    })
                
                custom_df = pd.DataFrame(custom_data)
                st.dataframe(custom_df, width='stretch')
                
                # Delete specific work items
                if custom_work:
                    delete_col1, delete_col2 = st.columns(2)
                    
                    with delete_col1:
                        work_to_delete = st.selectbox(
                            "Select work to delete:",
                            options=[f"{w['date']} - {w['type']} ({w['assignee']})" for w in custom_work],
                            key="delete_custom_work_select"
                        )
                    
                    with delete_col2:
                        if st.button("🗑️ Delete Selected", key="delete_custom_work"):
                            # Find the work ID to delete
                            work_index = [f"{w['date']} - {w['type']} ({w['assignee']})" for w in custom_work].index(work_to_delete)
                            work_id = custom_work[work_index]['id']
                            
                            if delete_custom_weekend_work(conn, work_id):
                                st.success("✅ Custom work deleted")
                                st.rerun()
                            else:
                                st.error("Failed to delete custom work")
            else:
                st.info("No custom work logged yet. Use the Multi-Weekend Planning tab to add custom work.")
    
    with weekend_tab5:
        st.markdown("### 📅 Yearly Weekend Calendar")
        st.caption("Plan and manage weekend assignments for the entire year")
        
        # Year selection
        current_year = date.today().year
        selected_year = st.selectbox("Select Year:", options=[current_year, current_year + 1], index=0, key="calendar_year")
        
        # Calendar view controls
        cal_col1, cal_col2 = st.columns([3, 1])
        
        with cal_col1:
            st.markdown(f"**Weekend Schedule for {selected_year}:**")
        
        with cal_col2:
            if st.button("🔄 Refresh Calendar", key="refresh_calendar"):
                st.rerun()
        
        # Create yearly calendar grid
        import calendar
        from datetime import datetime, timedelta
        
        # Get all weekend schedules for the year
        year_start = f"{selected_year}-01-01"
        year_end = f"{selected_year}-12-31"
        all_schedules = get_weekend_schedules(conn)
        schedule_dict = {s['weekend_date']: s['assignee'] for s in all_schedules}
        
        all_users = get_all_users(conn)
        current_user = st.session_state.get("my_name", "Unknown")
        
        # Create monthly calendar grids
        for month in range(1, 13):
            month_name = calendar.month_name[month]
            
            with st.expander(f"📅 {month_name} {selected_year}", expanded=month == date.today().month if selected_year == current_year else False):
                st.markdown(f"**Weekend Assignments for {month_name}:**")
                
                # Get all Saturdays in the month
                cal = calendar.Calendar(firstweekday=calendar.MONDAY)
                month_days = list(cal.itermonthdates(selected_year, month))
                saturdays = [d for d in month_days if d.weekday() == 5 and d.month == month]
                
                if saturdays:
                    # Create a grid for the month's weekends
                    weekend_cols = st.columns(min(len(saturdays), 4))  # Max 4 columns
                    
                    for i, saturday in enumerate(saturdays):
                        col_index = i % 4
                        
                        with weekend_cols[col_index]:
                            saturday_str = saturday.strftime('%Y-%m-%d')
                            sunday = saturday + timedelta(days=1)
                            
                            # Weekend date display
                            st.write(f"**{saturday.strftime('%b %d')} - {sunday.strftime('%b %d')}**")
                            st.caption(f"Week {saturday.isocalendar()[1]}")
                            
                            # Current assignee
                            current_assignee = schedule_dict.get(saturday_str, "(unassigned)")
                            
                            # Assignment selector
                            if all_users:
                                assignee_options = ["(unassigned)"] + all_users
                                
                                selected_assignee = st.selectbox(
                                    "Assignee:",
                                    options=assignee_options,
                                    index=assignee_options.index(current_assignee) if current_assignee in assignee_options else 0,
                                    key=f"cal_assignee_{saturday_str}"
                                )
                                
                                # Save to database when selection changes
                                if selected_assignee != current_assignee:
                                    if selected_assignee != "(unassigned)":
                                        # Assigning someone new or changing assignment
                                        if save_weekend_schedule(conn, saturday_str, selected_assignee, current_user):
                                            st.success(f"✅ Assigned {selected_assignee} to {saturday_str}")
                                            # Update the schedule dict for immediate UI feedback
                                            schedule_dict[saturday_str] = selected_assignee
                                            st.rerun()
                                    else:
                                        # Removing assignment - implement deletion
                                        from db import delete_weekend_schedule
                                        try:
                                            if delete_weekend_schedule(conn, saturday_str):
                                                st.success(f"✅ Removed assignment for {saturday_str}")
                                                # Update the schedule dict for immediate UI feedback
                                                if saturday_str in schedule_dict:
                                                    del schedule_dict[saturday_str]
                                                st.rerun()
                                        except:
                                            st.info("Assignment removal not yet implemented")
                            else:
                                st.write("No users available")
                            
                            # Quick planning button
                            if st.button("📝 Set Active", key=f"cal_plan_{saturday_str}"):
                                if current_assignee != "(unassigned)":
                                    st.session_state['selected_weekend_assignee'] = current_assignee
                                    st.session_state['selected_weekend_saturday'] = saturday_str
                                    st.session_state['selected_weekend_sunday'] = sunday.strftime('%Y-%m-%d')
                                    st.success(f"✅ Set {current_assignee} as active weekend assignee")
                                else:
                                    st.warning("Please assign someone first")
                else:
                    st.info("No weekends in this month")
        
        # Summary section
        st.markdown("### 📊 Year Summary")
        
        # Count assignments by user
        year_assignments = {}
        year_schedules = [s for s in all_schedules if s['weekend_date'].startswith(str(selected_year))]
        
        for schedule in year_schedules:
            assignee = schedule['assignee']
            if assignee not in year_assignments:
                year_assignments[assignee] = 0
            year_assignments[assignee] += 1
        
        if year_assignments:
            summary_data = []
            for assignee, count in year_assignments.items():
                summary_data.append({
                    'User': assignee,
                    'Weekend Assignments': count,
                    'Percentage': f"{count/len(year_schedules)*100:.1f}%" if year_schedules else "0%"
                })
            
            summary_df = pd.DataFrame(summary_data)
            st.dataframe(summary_df, width='stretch')
            
            # Export option
            if st.button("📊 Export Year Schedule"):
                csv = summary_df.to_csv(index=False)
                st.download_button(
                    label="💾 Download Year Summary CSV",
                    data=csv,
                    file_name=f"weekend_schedule_{selected_year}.csv",
                    mime="text/csv"
                )
        else:
            st.info(f"No weekend assignments scheduled for {selected_year}")

with tab_dashboard:
    st.subheader("� Culture Dashboard")
    
    # Dashboard tabs
    dash_tab1, dash_tab2, dash_tab3 = st.tabs(["📅 Tasks & Schedule", "🗓️ Weekend Preparation", "🧪 Active Vials Overview"])
    
    with dash_tab1:
        st.markdown("### Upcoming & Overdue Tasks")
        dash_only_mine = st.checkbox("Show only items assigned to me", value=False)
        
        # Basic upcoming/overdue view using Next Action Date
        all_logs = query_logs(conn)
        df_all = pd.DataFrame(all_logs) if all_logs else pd.DataFrame([])
        if not df_all.empty and "next_action_date" in df_all.columns:
            today = pd.to_datetime(date.today())
            df_all["_nad"] = pd.to_datetime(df_all["next_action_date"], errors="coerce")
            if dash_only_mine and st.session_state.get("my_name"):
                df_all = df_all[df_all.get("assigned_to", "").astype(str) == st.session_state["my_name"]]
            elif dash_only_mine and not st.session_state.get("my_name"):
                st.info("Set 'My name' at the top to filter to your items.")
            df_overdue = df_all[(~df_all["_nad"].isna()) & (df_all["_nad"] < today)]
            df_upcoming = df_all[(~df_all["_nad"].isna()) & (df_all["_nad"] >= today)].sort_values("_nad").head(50)
            
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**Overdue**")
                if df_overdue.empty:
                    st.info("No overdue items.")
                else:
                    st.dataframe(df_overdue[["cell_line","event_type","assigned_to","next_action_date","notes"]].rename(columns={
                        "cell_line":"Cell Line","event_type":"Event Type","assigned_to":"Assigned To","next_action_date":"Next Action Date","notes":"Notes"
                    }), width='stretch')
            with c2:
                st.markdown("**Upcoming**")
                if df_upcoming.empty:
                    st.info("No upcoming items.")
                else:
                    st.dataframe(df_upcoming[["cell_line","event_type","assigned_to","next_action_date","notes"]].rename(columns={
                        "cell_line":"Cell Line","event_type":"Event Type","assigned_to":"Assigned To","next_action_date":"Next Action Date","notes":"Notes"
                    }), width='stretch')
        else:
            st.info("No Next Action Dates yet.")
    
    with dash_tab2:
        st.markdown("### 🗓️ Weekend Preparation Dashboard")
        st.caption("Quick overview for Friday planning")
        
        # Weekend date calculation
        from datetime import datetime, timedelta
        today = datetime.now()
        days_to_saturday = (5 - today.weekday()) % 7
        if days_to_saturday == 0 and today.weekday() == 5:  # If today is Saturday
            days_to_saturday = 7
        
        saturday = today + timedelta(days=days_to_saturday)
        sunday = saturday + timedelta(days=1)
        
        # Weekend overview
        weekend_overview_col1, weekend_overview_col2 = st.columns(2)
        
        with weekend_overview_col1:
            st.info(f"""
            🗓️ **This Weekend:**  
            📅 Saturday: {saturday.strftime('%B %d, %Y')}  
            📅 Sunday: {sunday.strftime('%B %d, %Y')}  
            ⏰ Days until weekend: {days_to_saturday} days
            """)
        
        with weekend_overview_col2:
            # Quick weekend task statistics
            weekend_tasks = get_weekend_tasks(conn, saturday.strftime('%Y-%m-%d'), sunday.strftime('%Y-%m-%d'))
            
            total_weekend_tasks = len(weekend_tasks)
            saturday_tasks = len([t for t in weekend_tasks if t['next_action_date'] == saturday.strftime('%Y-%m-%d')])
            sunday_tasks = len([t for t in weekend_tasks if t['next_action_date'] == sunday.strftime('%Y-%m-%d')])
            
            st.metric("Total Weekend Tasks", total_weekend_tasks)
            if total_weekend_tasks > 0:
                st.write(f"📅 Saturday: {saturday_tasks} tasks")
                st.write(f"📅 Sunday: {sunday_tasks} tasks")
        
        # Weekend assignments
        if weekend_tasks:
            st.markdown("### 👥 Weekend Assignments")
            
            # Group by assignee
            assignee_groups = {}
            for task in weekend_tasks:
                assignee = task.get('assigned_to', 'Unassigned')
                if assignee not in assignee_groups:
                    assignee_groups[assignee] = {'saturday': [], 'sunday': []}
                
                if task['next_action_date'] == saturday.strftime('%Y-%m-%d'):
                    assignee_groups[assignee]['saturday'].append(task)
                else:
                    assignee_groups[assignee]['sunday'].append(task)
            
            for assignee, tasks in assignee_groups.items():
                saturday_count = len(tasks['saturday'])
                sunday_count = len(tasks['sunday'])
                
                with st.expander(f"👤 {assignee} ({saturday_count + sunday_count} tasks)", expanded=True):
                    assign_col1, assign_col2 = st.columns(2)
                    
                    with assign_col1:
                        st.markdown(f"**📅 Saturday Tasks ({saturday_count}):**")
                        for task in tasks['saturday']:
                            st.write(f"• {task['cell_line']} - {task['event_type']}")
                    
                    with assign_col2:
                        st.markdown(f"**📅 Sunday Tasks ({sunday_count}):**")
                        for task in tasks['sunday']:
                            st.write(f"• {task['cell_line']} - {task['event_type']}")
                    
                    # Quick checklist button
                    if st.button(f"📋 Generate Checklist for {assignee}", key=f"checklist_{assignee}"):
                        st.session_state['selected_weekend_assignee'] = assignee
                        st.session_state['selected_weekend_saturday'] = saturday.strftime('%Y-%m-%d')
                        st.session_state['selected_weekend_sunday'] = sunday.strftime('%Y-%m-%d')
                        st.success(f"✅ Checklist ready! Go to Weekend Tasks tab to view.")
            
            # Resource summary for weekend
            st.markdown("### 🧪 Weekend Resource Requirements")
            
            media_needed = set()
            locations_needed = set()
            cell_lines = set()
            
            for task in weekend_tasks:
                if task.get('current_medium'):
                    media_needed.add(task['current_medium'])
                if task.get('current_location'):
                    locations_needed.add(task['current_location'])
                if task.get('cell_line'):
                    cell_lines.add(task['cell_line'])
            
            resource_col1, resource_col2, resource_col3 = st.columns(3)
            
            with resource_col1:
                st.markdown("**📱 Media to Prepare:**")
                for medium in sorted(media_needed):
                    st.write(f"• {medium}")
            
            with resource_col2:
                st.markdown("**📍 Locations in Use:**")
                for location in sorted(locations_needed):
                    st.write(f"• {location}")
            
            with resource_col3:
                st.markdown("**🧬 Cell Lines Involved:**")
                for cell_line in sorted(cell_lines):
                    st.write(f"• {cell_line}")
        
        else:
            st.info("No weekend tasks scheduled yet.")
            
            # Quick weekend setup
            st.markdown("### 🚀 Quick Weekend Setup")
            st.caption("Quickly schedule weekend tasks from active vials")
            
            # Get active vials that might need weekend attention
            active_vials = get_active_vials(conn, days_threshold=7)
            
            if active_vials:
                st.markdown("**🧪 Active Vials Needing Attention:**")
                
                for vial in active_vials[:5]:  # Show top 5
                    thaw_event = vial.get('thaw_event', {})
                    latest_event = vial.get('latest_event', {})
                    
                    vial_col1, vial_col2 = st.columns([3, 1])
                    
                    with vial_col1:
                        st.write(f"**{vial['thaw_id']}** - {thaw_event.get('cell_line', 'Unknown')} (P{vial.get('current_passage', 'N/A')}, {vial.get('culture_days', 0)} days)")
                        st.caption(f"Current: {vial.get('current_vessel', 'N/A')} in {vial.get('current_location', 'N/A')}")
                    
                    with vial_col2:
                        if st.button("📝 Schedule", key=f"schedule_{vial['thaw_id']}"):
                            st.info("💡 Go to Add Entry tab to schedule weekend tasks for this vial")
            
            else:
                st.info("No active vials found that need weekend attention.")
    
    with dash_tab3:
        st.markdown("### 🧪 Active Vials Summary")
        
        # Get active vials
        active_vials = get_active_vials(conn, days_threshold=30)
        
        if active_vials:
            # Summary metrics
            total_vials = len(active_vials)
            avg_culture_days = sum([v.get('culture_days', 0) for v in active_vials]) / total_vials
            high_passage_vials = len([v for v in active_vials if (v.get('current_passage') or 0) > 8])
            vials_with_alerts = len([v for v in active_vials if len(get_vial_alerts(conn, v['thaw_id'])) > 0])
            
            # Metrics row
            metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
            
            with metric_col1:
                st.metric("Active Vials", total_vials)
            with metric_col2:
                st.metric("Avg Culture Days", f"{avg_culture_days:.1f}")
            with metric_col3:
                st.metric("High Passage (>P8)", high_passage_vials, delta=f"{high_passage_vials/total_vials*100:.0f}%" if total_vials > 0 else "0%")
            with metric_col4:
                st.metric("Vials with Alerts", vials_with_alerts, delta=f"{vials_with_alerts/total_vials*100:.0f}%" if total_vials > 0 else "0%")
            
            # Priority alerts
            if vials_with_alerts > 0:
                st.markdown("### 🚨 Priority Alerts")
                alert_count = 0
                
                # Sort vials by alert severity (critical first, then warnings)
                vials_by_priority = []
                for vial in active_vials:
                    alerts = get_vial_alerts(conn, vial['thaw_id'])
                    if alerts:
                        critical_alerts = [a for a in alerts if a['type'] == 'critical']
                        warning_alerts = [a for a in alerts if a['type'] == 'warning']
                        if critical_alerts:
                            vials_by_priority.append((vial, critical_alerts[0], 'critical'))
                        elif warning_alerts:
                            vials_by_priority.append((vial, warning_alerts[0], 'warning'))
                
                # Sort by priority (critical first)
                vials_by_priority.sort(key=lambda x: 0 if x[2] == 'critical' else 1)
                
                for vial, alert, alert_type in vials_by_priority[:5]:  # Show max 5 alerts
                    thaw_event = vial.get('thaw_event', {})
                    if alert_type == 'critical':
                        st.error(f"**🚨 {vial['thaw_id']}** ({thaw_event.get('cell_line', 'Unknown')}): {alert['message']}")
                    else:
                        st.warning(f"**⚠️ {vial['thaw_id']}** ({thaw_event.get('cell_line', 'Unknown')}): {alert['message']}")
                    alert_count += 1
            
            # Quick overview table
            st.markdown("### 📋 Quick Overview")
            overview_data = []
            for vial in active_vials[:10]:  # Show top 10
                thaw_event = vial.get('thaw_event', {})
                latest_event = vial.get('latest_event', {})
                
                # Status indicator with critical alerts prioritized
                alerts = get_vial_alerts(conn, vial['thaw_id'])
                if any(a['type'] == 'critical' for a in alerts):
                    status = "🚨"
                elif any(a['type'] == 'warning' for a in alerts):
                    status = "⚠️"
                else:
                    status = "✅"
                
                overview_data.append({
                    'Status': status,
                    'Thaw ID': vial['thaw_id'],
                    'Cell Line': thaw_event.get('cell_line', ''),
                    'Days': vial.get('culture_days', 0),
                    'Passage': f"P{vial.get('current_passage', 'N/A')}",
                    'Vessel': vial.get('current_vessel', ''),
                    'Last Event': latest_event.get('event_type', ''),
                    'Last Date': latest_event.get('date', '')[:10] if latest_event.get('date') else ''
                })
            
            if overview_data:
                overview_df = pd.DataFrame(overview_data)
                st.dataframe(overview_df, width='stretch')
            
            # Action suggestions
            st.markdown("### 💡 Suggested Actions")
            suggestions = []
            
            # Long culture vials
            long_culture = [v for v in active_vials if v.get('culture_days', 0) > 21]
            if long_culture:
                suggestions.append(f"📅 {len(long_culture)} vials have been in culture >21 days - consider cryopreservation or differentiation")
            
            # High passage vials
            if high_passage_vials > 0:
                suggestions.append(f"🔬 {high_passage_vials} vials are at high passage (>P8) - plan experimental use or cryopreservation")
            
            # Vials needing observation
            recent_obs_needed = []
            for vial in active_vials:
                events = vial.get('events', [])
                recent_events = events[-3:] if len(events) >= 3 else events
                has_recent_obs = any(e.get('event_type') == 'Observation' for e in recent_events)
                if not has_recent_obs and len(events) > 2:
                    recent_obs_needed.append(vial)
            
            if recent_obs_needed:
                suggestions.append(f"👁️ {len(recent_obs_needed)} vials need recent observation updates")
            
            if suggestions:
                for suggestion in suggestions:
                    st.info(suggestion)
            else:
                st.success("🎉 All vials are being well maintained!")
            
            # Quick links
            st.markdown("### 🔗 Quick Links")
            link_col1, link_col2, link_col3 = st.columns(3)
            
            with link_col1:
                if st.button("📊 View All Active Vials", key="view_all_active"):
                    st.info("💡 Go to 'Vial Lifecycle Tracking' → 'Active Vials' tab for detailed view")
            
            with link_col2:
                if st.button("➕ Add New Entry", key="add_entry_quick"):
                    st.info("💡 Go to 'Add Entry' tab to log new culture events")
            
            with link_col3:
                if st.button("📈 View Analytics", key="view_analytics_quick"):
                    st.info("💡 Go to 'Vial Lifecycle Tracking' → 'Vial Analytics' tab for insights")
        
        else:
            st.info("No active vials found. Add some thawing events to start tracking!")
            
            # Show recent activity instead
            st.markdown("### 📈 Recent Activity")
            recent_logs = query_logs(conn)
            if recent_logs:
                recent_df = pd.DataFrame(recent_logs[-10:])  # Last 10 entries
                recent_display = recent_df[['date', 'cell_line', 'event_type', 'operator']].rename(columns={
                    'date': 'Date',
                    'cell_line': 'Cell Line',
                    'event_type': 'Event Type',
                    'operator': 'Operator'
                })
                st.dataframe(recent_display, width='stretch')
            else:
                st.info("No activity yet - start by adding your first entry!")

with tab_settings:
    st.subheader("⚙️ Settings (Reference Lists)")
    st.caption("Manage dropdown values and backups.")
    
    # Settings sub-tabs
    settings_tab1, settings_tab2, settings_tab3, settings_tab4 = st.tabs(["📋 Reference Lists", "👥 Operators", "🧬 Experimental Workflows", "💾 Backup"])
    
    with settings_tab1:
        manage_kind_label = st.selectbox("Manage list", options=["Cell Lines","Event Types","Vessels","Locations","Cell Types","Culture Media"], index=0)
        _kind_map = {
            "Cell Lines": "cell_line",
            "Event Types": "event_type",
            "Vessels": "vessel",
            "Locations": "location",
            "Cell Types": "cell_type",
            "Culture Media": "culture_medium",
        }
        manage_kind = _kind_map.get(manage_kind_label)

        existing_vals = get_ref_values(conn, manage_kind)
        st.write(f"Current {manage_kind_label} ({len(existing_vals)}):")
        if existing_vals:
            st.dataframe(pd.DataFrame({"Name": existing_vals}), width='stretch')
        else:
            st.info("No values yet.")

        st.markdown("---")
        st.markdown("### Add New")
        new_val = st.text_input("New name", key=f"new_{manage_kind_label}")
        if st.button("Add", key=f"btn_add_{manage_kind_label}"):
            if not new_val or not new_val.strip():
                st.warning("Enter a name to add.")
            else:
                add_ref_value(conn, manage_kind, new_val.strip())
                st.success("Added.")
                st.rerun()

        st.markdown("### Rename")
        existing_vals = get_ref_values(conn, manage_kind)
        if existing_vals:
            old_val = st.selectbox("Select existing", options=existing_vals, key=f"rename_src_{manage_kind_label}")
            new_name = st.text_input("New name", key=f"rename_dst_{manage_kind_label}")
            if st.button("Rename", key=f"btn_rename_{manage_kind_label}"):
                if not new_name or not new_name.strip():
                    st.warning("Enter a new name.")
                else:
                    rename_ref_value(conn, manage_kind, old_val, new_name)
                    st.success("Renamed.")
                    st.rerun()
        else:
            st.info("Nothing to rename.")

        st.markdown("### Delete")
        existing_vals = get_ref_values(conn, manage_kind)
        if existing_vals:
            del_val = st.selectbox("Select to delete", options=existing_vals, key=f"del_{manage_kind_label}")
            confirm = st.checkbox("I understand this will remove the value", key=f"confirm_del_{manage_kind_label}")
            if st.button("Delete", key=f"btn_del_{manage_kind_label}"):
                if confirm:
                    delete_ref_value(conn, manage_kind, del_val)
                    st.success("Deleted.")
                    st.rerun()
                else:
                    st.warning("Please confirm before deleting.")
        else:
            st.info("Nothing to delete.")
    
    with settings_tab2:
        # Operators management
        try:
            _urows = conn.execute("SELECT username, COALESCE(display_name, username) FROM users ORDER BY username").fetchall()
            ops = [(r[0], r[1]) for r in _urows]
        except Exception:
            ops = []
        st.write(f"Current Operators ({len(ops)}):")
        if ops:
            st.dataframe(pd.DataFrame(ops, columns=["Username","Display Name"]), width='stretch')
        else:
            st.info("No operators yet.")

        st.markdown("---")
        st.markdown("### Add Operator")
        new_username = st.text_input("Username", key="new_operator_username")
        new_display = st.text_input("Display name (optional)", key="new_operator_display")
        if st.button("Add Operator", key="btn_add_operator"):
            if not new_username or not new_username.strip():
                st.warning("Enter a username.")
            else:
                get_or_create_user(conn, new_username.strip(), new_display.strip() if new_display else None)
                st.success("Operator added.")
                st.rerun()

        st.markdown("### Delete Operator")
        try:
            _urows2 = conn.execute("SELECT username FROM users ORDER BY username").fetchall()
            ops2 = [r[0] for r in _urows2]
        except Exception:
            ops2 = []
        if ops2:
            del_op = st.selectbox("Select operator to delete", options=ops2, key="del_operator")
            confirm_op = st.checkbox("I understand this will remove the operator", key="confirm_del_operator")
            if st.button("Delete Operator", key="btn_del_operator"):
                if confirm_op:
                    delete_user(conn, del_op)
                    st.success("Operator deleted.")
                    st.rerun()
                else:
                    st.warning("Please confirm before deleting.")
        else:
            st.info("No operators to delete.")
    
    with settings_tab3:
        st.markdown("### 🧬 Experimental Workflow Management")
        st.caption("Manage experiment types and workflow templates for research tracking")
        
        workflow_subtab1, workflow_subtab2 = st.tabs(["🔬 Experiment Types", "📋 Workflow Templates"])
        
        with workflow_subtab1:
            st.markdown("#### Available Experiment Types")
            
            try:
                experiment_types = get_experiment_types(conn)
                if experiment_types:
                    # Group by category for display
                    exp_categories = {}
                    for exp in experiment_types:
                        category = exp['category']
                        if category not in exp_categories:
                            exp_categories[category] = []
                        exp_categories[category].append(exp)
                    
                    # Display experiment types by category
                    for category, exps in exp_categories.items():
                        with st.expander(f"📂 {category} ({len(exps)} types)", expanded=True):
                            exp_data = []
                            for exp in exps:
                                exp_data.append({
                                    'Name': exp['name'],
                                    'Description': exp['description'],
                                    'Typical Duration': f"{exp['typical_duration_days']} days" if exp['typical_duration_days'] else "Variable",
                                    'Success Criteria': exp['success_criteria'][:50] + "..." if len(exp['success_criteria']) > 50 else exp['success_criteria']
                                })
                            
                            if exp_data:
                                exp_df = pd.DataFrame(exp_data)
                                st.dataframe(exp_df, width='stretch')
                else:
                    st.info("No experiment types configured yet.")
                
                # Add new experiment type
                st.markdown("---")
                st.markdown("#### ➕ Add New Experiment Type")
                
                with st.form("add_experiment_type"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        exp_name = st.text_input("Experiment Name *", placeholder="e.g., CRISPR Gene Editing")
                        exp_category = st.selectbox("Category *", options=[
                            "Genome Editing", "Differentiation", "Cell Line Engineering", 
                            "Drug Screening", "Functional Analysis", "Quality Control", "Other"
                        ])
                        exp_duration = st.number_input("Typical Duration (days)", min_value=1, value=7, step=1)
                    
                    with col2:
                        exp_description = st.text_area("Description", placeholder="Brief description of the experimental procedure...")
                        exp_success_criteria = st.text_area("Success Criteria", placeholder="How to measure success of this experiment...")
                    
                    submit_exp_type = st.form_submit_button("Add Experiment Type")
                    
                    if submit_exp_type:
                        if exp_name and exp_category:
                            try:
                                # Add to database
                                with contextlib.closing(conn.cursor()) as cur:
                                    cur.execute("""
                                        INSERT INTO experiment_types (name, category, description, typical_duration_days, success_criteria)
                                        VALUES (?, ?, ?, ?, ?)
                                    """, (exp_name, exp_category, exp_description, exp_duration, exp_success_criteria))
                                    conn.commit()
                                st.success(f"✅ Added experiment type: {exp_name}")
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ Error adding experiment type: {str(e)}")
                        else:
                            st.error("Name and Category are required!")
                
            except Exception as e:
                st.error(f"Error loading experiment types: {str(e)}")
        
        with workflow_subtab2:
            st.markdown("#### 📋 Workflow Templates")
            st.caption("Predefined experimental workflows with stages and protocols")
            
            try:
                from db import get_experimental_workflows, add_experimental_workflow
                
                workflows = get_experimental_workflows(conn)
                if workflows:
                    st.markdown("**Available Workflow Templates:**")
                    
                    workflow_data = []
                    for wf in workflows:
                        workflow_data.append({
                            'Workflow Name': wf['workflow_name'],
                            'Description': wf['description'][:60] + "..." if len(wf['description']) > 60 else wf['description'],
                            'Typical Stages': wf['typical_stages'][:50] + "..." if len(wf['typical_stages']) > 50 else wf['typical_stages'],
                            'Expected Duration': f"{wf['expected_duration_days']} days" if wf['expected_duration_days'] else "Variable",
                            'Success Criteria': wf['success_criteria'][:40] + "..." if len(wf['success_criteria']) > 40 else wf['success_criteria']
                        })
                    
                    workflow_df = pd.DataFrame(workflow_data)
                    st.dataframe(workflow_df, width='stretch')
                else:
                    st.info("No workflow templates defined yet.")
                
                # Add new workflow template
                st.markdown("---")
                st.markdown("#### ➕ Add New Workflow Template")
                
                with st.form("add_workflow_template"):
                    wf_name = st.text_input("Workflow Name *", placeholder="e.g., Standard CRISPR Editing Protocol")
                    wf_description = st.text_area("Description *", placeholder="Detailed description of the complete workflow...")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        wf_stages = st.text_area("Typical Stages", placeholder="Stage 1: Transfection\nStage 2: Selection\nStage 3: Validation")
                        wf_duration = st.number_input("Expected Duration (days)", min_value=1, value=14, step=1)
                    
                    with col2:
                        wf_criteria = st.text_area("Success Criteria", placeholder="Criteria for determining successful completion...")
                    
                    submit_workflow = st.form_submit_button("Add Workflow Template")
                    
                    if submit_workflow:
                        if wf_name and wf_description:
                            try:
                                add_experimental_workflow(conn, wf_name, wf_description, wf_stages, wf_duration, wf_criteria)
                                st.success(f"✅ Added workflow template: {wf_name}")
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ Error adding workflow template: {str(e)}")
                        else:
                            st.error("Workflow Name and Description are required!")
                
            except ImportError:
                st.error("Workflow template functions not available. Please update the database functions.")
            except Exception as e:
                st.error(f"Error loading workflow templates: {str(e)}")
    
    with settings_tab4:
        st.markdown("### 📁 Backup & Data Management")
        
        # Entry templates section
        st.markdown("#### 🎯 Entry Templates")
        st.caption("Manage your saved entry templates for quick data entry.")
        
        # Get current user's templates
        current_user = st.session_state.get("my_name", None)
        if current_user:
            user_templates = get_entry_templates(conn, created_by=current_user)
            
            if user_templates:
                st.write(f"Your saved templates ({len(user_templates)}):")
                
                # Display templates in a nice format
                template_data = []
                for t in user_templates:
                    template_info = {
                        "Name": t['name'],
                        "Event Type": t['template_data'].get('event_type', ''),
                        "Vessel": t['template_data'].get('vessel', ''),
                        "Medium": t['template_data'].get('medium', ''),
                        "Cell Type": t['template_data'].get('cell_type', ''),
                        "Usage Count": t['usage_count'],
                        "Created": t['created_at'][:10]
                    }
                    template_data.append(template_info)
                
                st.dataframe(pd.DataFrame(template_data), width='stretch')
                
                # Delete template option
                st.markdown("**Delete Template**")
                template_names = [t['name'] for t in user_templates]
                del_template = st.selectbox("Select template to delete:", options=template_names, key="del_template_select")
                confirm_template_del = st.checkbox("I confirm I want to delete this template", key="confirm_template_del")
                
                if st.button("🗑️ Delete Template", key="btn_del_template"):
                    if confirm_template_del:
                        if delete_entry_template(conn, del_template, current_user):
                            st.success(f"✅ Template '{del_template}' deleted!")
                            st.rerun()
                        else:
                            st.error("❌ Failed to delete template.")
                    else:
                        st.warning("Please confirm before deleting.")
            else:
                st.info("No templates saved yet. Create templates when adding entries by checking 'Save as template'.")
            
            # Show all templates (read-only view)
            st.markdown("**All Templates** (view only)")
            all_templates = get_entry_templates(conn)
            if all_templates:
                all_template_data = []
                for t in all_templates:
                    all_info = {
                        "Name": t['name'],
                        "Event Type": t['template_data'].get('event_type', ''),
                        "Vessel": t['template_data'].get('vessel', ''),
                        "Medium": t['template_data'].get('medium', ''),
                        "Created By": t['created_by'],
                        "Usage Count": t['usage_count']
                    }
                    all_template_data.append(all_info)
                
                st.dataframe(pd.DataFrame(all_template_data), width='stretch')
            else:
                st.info("No templates in the system yet.")
        else:
            st.info("Set 'My name' at the top to manage your templates.")

        st.markdown("---")
        st.markdown("#### 📁 Database Backup")
        
        backup_col1, backup_col2 = st.columns(2)
        
        with backup_col1:
            st.markdown("**Traditional Backup**")
            if st.button("Backup database and images"):
                out_dir = backup_now()
                st.success(f"Backup created: {out_dir}")
        
        with backup_col2:
            st.markdown("**Excel Export**")
            if st.button("📊 Export All Data to Excel"):
                try:
                    filename = export_to_excel(conn)
                    st.success(f"✅ Excel export created: {filename}")
                    
                    # Provide download link
                    with open(filename, 'rb') as f:
                        excel_data = f.read()
                    
                    st.download_button(
                        label="⬇️ Download Excel File",
                        data=excel_data,
                        file_name=os.path.basename(filename),
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                except Exception as e:
                    st.error(f"❌ Export failed: {str(e)}")
        
        st.markdown("---")
        st.markdown("#### 📊 Excel Export & Import")
        st.caption("Export your data to Excel for backup, analysis, or offline work. Import data back if needed.")
        
        # Filtered export section
        st.markdown("**📋 Filtered Export**")
        
        export_col1, export_col2 = st.columns(2)
        
        with export_col1:
            # Filter options
            export_cell_line = st.selectbox("Cell Line (optional):", ["All"] + list_distinct_values(conn, "cell_line"), key="export_cell_line")
            export_event_type = st.selectbox("Event Type (optional):", ["All"] + list_distinct_values(conn, "event_type"), key="export_event_type")
            export_operator = st.selectbox("Operator (optional):", ["All"] + list_distinct_values(conn, "operator"), key="export_operator")
        
        with export_col2:
            export_date_from = st.date_input("From Date (optional):", value=None, key="export_date_from")
            export_date_to = st.date_input("To Date (optional):", value=None, key="export_date_to")
            export_thaw_id = st.text_input("Thaw ID (optional):", key="export_thaw_id")
        
        if st.button("📊 Export Filtered Data to Excel"):
            try:
                filters = {}
                if export_cell_line != "All":
                    filters['cell_line'] = export_cell_line
                if export_event_type != "All":
                    filters['event_type'] = export_event_type
                if export_operator != "All":
                    filters['operator'] = export_operator
                if export_date_from:
                    filters['date_from'] = export_date_from.strftime('%Y-%m-%d')
                if export_date_to:
                    filters['date_to'] = export_date_to.strftime('%Y-%m-%d')
                if export_thaw_id.strip():
                    filters['thaw_id'] = export_thaw_id.strip()
                
                filename = export_filtered_logs_to_excel(conn, filters)
                st.success(f"✅ Filtered export created: {filename}")
                
                # Provide download link
                with open(filename, 'rb') as f:
                    excel_data = f.read()
                
                st.download_button(
                    label="⬇️ Download Filtered Excel File",
                    data=excel_data,
                    file_name=os.path.basename(filename),
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            except Exception as e:
                st.error(f"❌ Filtered export failed: {str(e)}")
        
        # Import section
        st.markdown("**📥 Excel Import**")
        st.caption("⚠️ Use with caution: This will import data back into the database. Existing entries with the same ID will be skipped.")
        
        uploaded_file = st.file_uploader("Upload Excel file to import:", type=['xlsx'], key="excel_import")
        
        if uploaded_file is not None:
            if st.button("📥 Import from Excel", type="secondary"):
                try:
                    # Save uploaded file temporarily
                    import tempfile
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        temp_filename = tmp_file.name
                    
                    # Import data
                    results = import_from_excel(conn, temp_filename)
                    
                    # Clean up temp file
                    os.unlink(temp_filename)
                    
                    # Show results
                    if results['imported'] > 0:
                        st.success(f"✅ Import completed: {results['imported']} entries imported, {results['skipped']} skipped")
                    else:
                        st.info("No new entries were imported.")
                    
                    if results['errors'] > 0:
                        st.error(f"❌ {results['errors']} errors occurred during import")
                        for msg in results['messages']:
                            st.caption(msg)
                    
                    if results['imported'] > 0:
                        st.rerun()
                        
                except Exception as e:
                    st.error(f"❌ Import failed: {str(e)}")
        
        st.markdown("---")
        st.markdown("#### 📋 Excel Export Features")
        st.info("""
        **What gets exported:**
        - 🧪 **Culture Logs**: All your iPSC tracking entries
        - 📋 **Reference Lists**: Cell lines, event types, vessels, etc.
        - 👥 **User Data**: Operators and their caliber levels
        - 📅 **Weekend Planning**: Schedule assignments and custom work
        - 🎯 **Templates**: Your saved entry templates
        
        **Multiple sheets** for easy analysis in Excel/Google Sheets
        
        **Use cases:**
        - 📊 Data analysis and charts in Excel
        - 📁 Offline backup for lab records
        - 📋 Sharing data with collaborators
        - 🔄 Data migration between systems
        - 📈 Custom reporting and visualization
        """)
