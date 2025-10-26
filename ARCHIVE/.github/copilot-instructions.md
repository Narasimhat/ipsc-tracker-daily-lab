# iPSC Tracker - AI Coding Agent Instructions

## Project Overview
This is a **Streamlit-based LIMS** (Laboratory Information Management System) for tracking induced Pluripotent Stem Cell (iPSC) culture workflows with **comprehensive experimental protocol tracking**. The app provides a team-ready interface for logging culture events, tracking thaw timelines, managing experimental workflows (genome editing, differentiation, etc.), and exporting data, using SQLite for persistence.

## Architecture & Key Components

### Core Application Structure
- **Frontend**: Single-page Streamlit app with tabbed interface (`app.py`)
- **Database Layer**: SQLite with raw SQL queries and connection management (`db.py`)
- **Storage**: Local file system for uploaded images, configurable via `DATA_ROOT`
- **Deployment**: Render.com ready with persistent disk mounting

### Key Files to Understand
```
├── app.py              # Main Streamlit interface with 5 tabs including experimental tracking
├── db.py               # SQLite operations, schema, experimental workflow functions
├── requirements.txt    # Minimal dependencies: streamlit, pandas, pillow
├── render.yaml         # Deployment config with persistent storage
└── README.md           # Setup and collaboration workflow
```

## Development Patterns

### Database Design
- **SQLite Schema**: Single `logs` table with all event data including experimental workflow fields, separate reference tables for dropdowns
- **Thaw ID System**: Auto-generated format `TH-YYYYMMDD-001` for tracking cell thaw lineages
- **Experimental Workflow Schema**: Dedicated tables for `experiment_types`, `experimental_workflows`, plus fields in `logs` for tracking experimental procedures
- **Reference Management**: Dynamic dropdown values stored in separate tables (cell_lines, event_types, etc.)

### Streamlit App Structure
```python
# Tab-based interface pattern used throughout
tab_add, tab_history, tab_thaw, tab_dashboard, tab_settings = st.tabs([...])

# Enhanced experimental workflow section in Add Entry
st.markdown("### 🧬 Experimental Workflow (Optional)")
experiment_types = get_experiment_types(conn)
experiment_category = st.selectbox("Experiment Category:", exp_categories)
experiment_type = st.selectbox("Experiment Type:", filtered_exp_types)

# Enhanced copy/reuse outside forms for independent interaction
with st.expander("Copy Options"):
    if st.button("Copy Entry"):
        st.session_state.form_values = copied_data
        st.rerun()

# Form patterns for data entry with experimental fields
with st.form("form_name", clear_on_submit=False):
    # Pre-populate from session state including experimental data
    prev = st.session_state.get("form_values", {})
    # Input fields with intelligent defaults
    submitted = st.form_submit_button("Save Entry")
    if submitted:
        # Validation and database insert with experimental workflow data
```

### Experimental Workflow Patterns
- **Experiment Types**: Categorized experimental procedures (Genome Editing, Differentiation, etc.)
- **Workflow Templates**: Predefined experimental protocols with stages and success criteria
- **Journey Tracking**: `get_experimental_journey()` provides complete experimental timeline for vials
- **Progress Analytics**: Track experimental success rates, durations, and outcomes
- **Stage Management**: Track progression through experimental stages (e.g., Transfection → Selection → Validation)

### Vial Tracking Patterns
- **Lifecycle Functions**: Use `get_vial_lifecycle()` for complete vial history
- **Experimental Journey**: `get_experimental_journey()` tracks research protocols alongside culture maintenance
- **Analytics Integration**: `get_vial_analytics()` provides performance metrics
- **Active Monitoring**: `get_active_vials()` and `get_vial_alerts()` for dashboard views
- **Visual Timeline**: Enhanced display with icons, metrics, and experimental progression tracking

### Data Entry Workflow
- **Smart Defaults**: Auto-suggest passage numbers, reuse previous values for same cell line + event
- **Experimental Integration**: Optional experimental workflow fields with category-based filtering
- **Template System**: Save and reuse entry templates with usage tracking, including experimental parameters
- **Pattern Matching**: Find similar entries by vessel, medium, experimental conditions
- **Session State**: Copy/reuse functionality uses session state for form pre-population

## Critical Workflows

### Adding New Culture Events with Experimental Tracking
1. **Tab Navigation**: Use "Add Entry" tab with auto-generated thaw IDs for thawing events
2. **Basic Culture Fields**: Cell line, event type, passage, vessel, medium, location, operator
3. **Experimental Workflow Section**: Optional fields for experiment category, type, stage, conditions, protocol reference, success metrics
4. **Smart Defaults**: System predicts next passage number and suggests likely next events
5. **Enhanced Copy/Reuse**: Multiple methods to copy previous entries, templates, and patterns including experimental data
6. **Image Upload**: Optional colony images stored in `images/` directory with timestamped filenames
7. **Reference Management**: Dropdowns populated from reference tables, managed in Settings tab

### Experimental Journey Tracking
- **Complete Protocol Tracking**: From initial setup through completion with stage progression
- **Multi-Experiment Support**: Track multiple concurrent experiments on the same vial
- **Success Metrics**: Capture quantitative measures of experimental outcomes
- **Protocol References**: Link to DOIs, SOPs, or internal protocol documents
- **Condition Recording**: Detailed experimental conditions (temperature, supplements, timings)
- **Outcome Status**: Track success/failure/optimization needs for each experimental stage

### Vial Lifecycle with Experimental Context
- **Integrated Timeline**: Shows both culture maintenance and experimental events
- **Experimental Phases**: Groups events by experiment type with phase analysis
- **Recommendations Engine**: Suggests next experiments based on passage, culture duration, and history
- **Success Rate Analytics**: Track experimental success rates across vials and protocols

### Database Operations in `db.py`
- **Connection Pattern**: Use `get_conn()` with WAL mode for concurrent access
- **Query Functions**: All database operations abstracted into functions (e.g., `query_logs()`, `insert_log()`)
- **Migration Safe**: Schema changes handled via `init_db()` with `ALTER TABLE` checks
- **Experimental Functions**: `get_experimental_journey()`, `get_experiment_types()`, `get_experiment_recommendations()`
- **Vial Analytics**: Functions for lifecycle tracking, analytics, and alert generation

### Multi-User Collaboration
- **User Management**: Operators managed in Settings tab, stored in `users` table
- **Assignment System**: Tasks can be assigned with next action dates for dashboard view
- **Template Sharing**: Entry templates can be shared across team members including experimental templates
- **Experimental Workflow Management**: Team can define and share experimental protocols
- **Backup/Restore**: Manual backup creates timestamped copies of DB + images

## Key Files & Conventions

### Database Schema (SQLite)
- **Main Table**: `logs` contains all culture events with optional references to thaw timelines and experimental workflow fields
- **Experimental Tables**: `experiment_types`, `experimental_workflows` for protocol management
- **Reference Tables**: `cell_lines`, `event_types`, `vessels`, `locations`, `cell_types`, `culture_media`
- **User Management**: `users` table for operator tracking and task assignment

### Experimental Workflow Fields in Logs Table
- **experiment_type**: Links to experiment_types table
- **experiment_stage**: Current stage in the experimental workflow
- **experimental_conditions**: Detailed conditions specific to the experiment
- **protocol_reference**: DOI, SOP number, or internal reference
- **outcome_status**: Success/failure/in progress status
- **success_metrics**: Quantitative measures of experimental success

### File Organization
- **Database**: `ipsc_tracker.db` (git-ignored, local per deployment)
- **Images**: `images/` directory with format `YYYYMMDD_HHMMSS_microsec_thawId.ext`
- **Backups**: `backups/` directory with timestamped folders

### Streamlit Session State
- **Pending Thaw ID**: `st.session_state["pending_thaw_id"]` for auto-generated thaw tracking
- **User Context**: `st.session_state["my_name"]` for "assigned to me" filters
- **Form Values**: `st.session_state["form_values"]` for copy/reuse functionality including experimental data

## External Dependencies

### Deployment Options
- **Local Development**: Virtual environment with `streamlit run app.py`
- **Team Sharing**: Git-based collaboration with local SQLite databases
- **Cloud Deployment**: Render.com with persistent disk for shared database and images

### Streamlit Framework
- **UI Components**: Forms, tabs, file uploaders, dataframes with built-in filtering
- **Session State**: Used for pending thaw IDs, user context, and experimental data across tab navigation
- **Data Display**: Automatic CSV download generation for filtered log exports

## Development Commands

```bash
# Local setup and run
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py

# Alternative with specific host/port
python -m streamlit run app.py --server.address=localhost --server.port=8501

# Deployment check (mimics Render.com environment)
export DATA_ROOT=/tmp/ipsc_data
streamlit run app.py --server.address 0.0.0.0 --server.port 8080
```

## Code Style & Standards
- **Streamlit Patterns**: Use forms for data entry, session state for persistence across reloads
- **Database Operations**: Always use context managers (`with closing(conn.cursor())`) for safe cleanup
- **File Paths**: Use `os.path.join()` for cross-platform compatibility, respect `DATA_ROOT` environment variable
- **Error Handling**: Graceful degradation when schema migrations fail, display user-friendly messages
- **Experimental Integration**: Optional experimental workflow fields with fallback to basic culture tracking

## Debugging & Monitoring
- **Database Inspection**: Direct SQLite access at `ipsc_tracker.db` for troubleshooting
- **Image Storage**: Check `images/` directory for uploaded files with predictable naming
- **Experimental Data**: Use experimental journey tracking to debug protocol progression
- **Deployment Logs**: Render.com provides log access for production debugging
- **Backup Verification**: Use Settings tab backup feature to verify data integrity

## AI Agent Guidelines
- When adding new features, follow the existing tab-based UI pattern in `app.py`
- Database schema changes must include migration logic in `init_db()` function
- New reference data types require updates to both `db.py` functions and Settings tab management
- File uploads should follow the existing timestamped naming convention in `IMAGES_DIR`
- Experimental workflow features should be optional and not interfere with basic culture tracking
- When implementing experimental features, consider both individual vial tracking and cross-vial analytics
- Always provide fallback functionality for systems without experimental workflow data