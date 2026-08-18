import streamlit as st
from pathlib import Path
from datetime import datetime

st.set_page_config(
    page_title="Kyogre Logs",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern, clean CSS inspired by Pulse Clinic
st.markdown("""
<style>
    /* Base styling */
    * {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', sans-serif;
    }

    html, body {
        background-color: #f8f9fa;
    }

    .stMainBlockContainer {
        background-color: #ffffff;
    }

    .block-container {
        padding-top: 0;
        padding-bottom: 2rem;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e9ecef;
    }

    [data-testid="stSidebar"] [data-testid="stSidebarContent"] {
        padding-top: 1rem;
    }

    .sidebar-title {
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        color: #6c757d;
        padding: 1rem 0 0.5rem 1.5rem;
        margin-top: 1.5rem;
    }

    /* Top nav bar */
    .top-nav {
        background-color: #ffffff;
        border-bottom: 1px solid #e9ecef;
        padding: 1rem 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2rem;
    }

    /* Metric cards */
    .metric-card {
        background: white;
        border: 1px solid #e9ecef;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: all 0.2s ease;
    }

    .metric-card:hover {
        border-color: #dee2e6;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }

    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #212529;
        margin: 0.5rem 0;
    }

    .metric-label {
        font-size: 0.85rem;
        color: #6c757d;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.03em;
        margin-bottom: 0.5rem;
    }

    .metric-desc {
        font-size: 0.8rem;
        color: #adb5bd;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 8px;
        border: 1px solid #e9ecef;
        font-weight: 600;
        height: 42px;
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        border-color: #dee2e6;
        background-color: #f8f9fa;
    }

    /* Status badges */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.35rem 0.75rem;
        border-radius: 16px;
        font-size: 0.8rem;
        font-weight: 500;
    }

    .status-error {
        background-color: #fee;
        color: #dc3545;
    }

    .status-warning {
        background-color: #fef3cd;
        color: #ff9800;
    }

    .status-success {
        background-color: #d4edda;
        color: #28a745;
    }

    .status-info {
        background-color: #d1ecf1;
        color: #0c5460;
    }

    /* Tables */
    [data-testid="stDataFrame"] {
        border-radius: 10px;
        overflow: hidden;
    }

    .dataframe {
        border: 1px solid #e9ecef;
        border-radius: 10px;
    }

    /* Expandable sections */
    .stExpander {
        border: 1px solid #e9ecef;
        border-radius: 10px;
    }

    /* Search and filters */
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 1px solid #e9ecef;
        padding: 0.75rem 1rem;
    }

    .stTextInput > div > div > input:focus {
        border-color: #212529;
        box-shadow: 0 0 0 3px rgba(33, 37, 41, 0.1);
    }

    /* Checkbox styling */
    .stCheckbox {
        margin-bottom: 0.75rem;
    }

    .stCheckbox > label {
        font-weight: 500;
        color: #495057;
    }

    /* Code blocks */
    .stCode {
        border-radius: 8px;
    }

    /* Divider */
    hr {
        border: none;
        border-top: 1px solid #e9ecef;
        margin: 1.5rem 0;
    }

    /* Info boxes */
    .stAlert {
        border-radius: 8px;
        border: 1px solid;
    }
</style>
""", unsafe_allow_html=True)

# Load log files
logs_dir = Path.home() / ".kyogre-logs"

if not logs_dir.exists():
    st.error(f"❌ Logs directory not found: {logs_dir}")
    st.stop()

def load_log_file(file_path):
    try:
        with open(file_path, 'r') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"

def parse_logs(log_content):
    return log_content.split('\n')

def filter_logs(lines, search_query):
    if not search_query:
        return lines
    query_lower = search_query.lower()
    return [line for line in lines if query_lower in line.lower()]

def get_log_stats(lines):
    """Get statistics about log levels"""
    stats = {"error": 0, "warning": 0, "success": 0, "debug": 0, "info": 0, "total": 0}

    for line in lines:
        if not line.strip():
            continue

        stats["total"] += 1
        line_lower = line.lower()

        if any(word in line_lower for word in ["error", "exception", "failed", "fatal"]):
            stats["error"] += 1
        elif any(word in line_lower for word in ["warning", "warn"]):
            stats["warning"] += 1
        elif any(word in line_lower for word in ["success", "completed", "finished"]):
            stats["success"] += 1
        elif any(word in line_lower for word in ["debug", "verbose"]):
            stats["debug"] += 1
        else:
            stats["info"] += 1

    return stats

# ============ SIDEBAR ============
with st.sidebar:
    st.markdown("### 📊 LOGS")

    log_type = st.radio(
        "View",
        ["All Logs", "Normal Only", "Errors Only"],
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown("### 🔍 FILTERS")

    search_query = st.text_input(
        "Search logs",
        placeholder="Find in logs...",
        label_visibility="collapsed"
    )

    auto_refresh = st.checkbox("Auto-refresh (5s)", value=False)

    st.divider()

    st.markdown("### ⚙️ OPTIONS")

    if st.button("🔄 Refresh Now", use_container_width=True):
        st.rerun()

# ============ MAIN CONTENT ============

# Load data
agent_log = load_log_file(logs_dir / "agent.log")
error_log = load_log_file(logs_dir / "agent-error.log")

agent_lines = parse_logs(agent_log)
error_lines = parse_logs(error_log)

# Get stats
agent_stats = get_log_stats(agent_lines)
error_stats = get_log_stats(error_lines)

# Top header
col_header1, col_header2, col_header3 = st.columns([1, 2, 1])
with col_header1:
    st.markdown("#### Agent Logs")
with col_header2:
    st.markdown("**" + datetime.now().strftime('%B %d, %Y') + "** — Real-time log monitoring")
with col_header3:
    st.markdown("")

st.divider()

# KPI Cards
st.markdown("### Overview")
col1, col2, col3, col4 = st.columns(4)

# Determine which logs to show
all_lines = agent_lines + error_lines
all_stats = {"error": agent_stats["error"] + error_stats["error"],
             "warning": agent_stats["warning"] + error_stats["warning"],
             "total": len([l for l in all_lines if l.strip()])}

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">📋 Total Entries</div>
        <div class="metric-value">{agent_stats['total']}</div>
        <div class="metric-desc">Normal logs</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">⚠️ Errors & Warnings</div>
        <div class="metric-value">{all_stats['error'] + all_stats['warning']}</div>
        <div class="metric-desc">Across all logs</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    agent_file_stat = (logs_dir / "agent.log").stat()
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">📄 Agent Log Size</div>
        <div class="metric-value">{agent_file_stat.st_size / 1024:.1f}</div>
        <div class="metric-desc">KB</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    error_file_stat = (logs_dir / "agent-error.log").stat()
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">⚡ Error Log Size</div>
        <div class="metric-value">{error_file_stat.st_size / 1024:.1f}</div>
        <div class="metric-desc">KB</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# Main content area - Two columns
col_logs, col_stats = st.columns([2, 1], gap="large")

# LEFT: Log Display
with col_logs:
    st.markdown("### Log Entries")

    # Determine which logs to display
    if log_type == "All Logs":
        display_lines = agent_lines + error_lines
        is_error = [False] * len(agent_lines) + [True] * len(error_lines)
    elif log_type == "Normal Only":
        display_lines = agent_lines
        is_error = [False] * len(agent_lines)
    else:  # Errors Only
        display_lines = error_lines
        is_error = [True] * len(error_lines)

    # Apply search filter
    if search_query:
        filtered_indices = [i for i, line in enumerate(display_lines)
                          if search_query.lower() in line.lower()]
        display_lines = [display_lines[i] for i in filtered_indices]
        is_error = [is_error[i] for i in filtered_indices]
        st.info(f"✓ Found {len(display_lines)} matching entries")

    # Display logs
    if display_lines:
        # Create log display with better formatting
        for idx, (line, is_err) in enumerate(zip(display_lines, is_error)):
            if not line.strip():
                continue

            line_lower = line.lower()

            # Determine status badge
            if any(word in line_lower for word in ["error", "exception", "failed", "fatal"]):
                status = "🔴 Error"
                status_class = "status-error"
            elif any(word in line_lower for word in ["warning", "warn"]):
                status = "🟠 Warning"
                status_class = "status-warning"
            elif any(word in line_lower for word in ["success", "completed", "finished"]):
                status = "🟢 Success"
                status_class = "status-success"
            else:
                status = "⚪ Info"
                status_class = "status-info"

            # Display with expander
            with st.expander(f"{status} · {line[:70]}{'...' if len(line) > 70 else ''}"):
                st.markdown(f"```\n{line}\n```")
    else:
        st.info("No logs found matching your criteria")

# RIGHT: Status Summary
with col_stats:
    st.markdown("### Summary")

    # Normal logs breakdown
    st.markdown("**📋 Normal Logs**")
    st.markdown(f"• 🔴 Errors: `{agent_stats['error']}`")
    st.markdown(f"• 🟠 Warnings: `{agent_stats['warning']}`")
    st.markdown(f"• 🟢 Success: `{agent_stats['success']}`")
    st.markdown(f"• ⚪ Info: `{agent_stats['info']}`")

    st.divider()

    # Error logs breakdown
    st.markdown("**⚠️ Error Logs**")
    st.markdown(f"• 🔴 Errors: `{error_stats['error']}`")
    st.markdown(f"• 🟠 Warnings: `{error_stats['warning']}`")
    st.markdown(f"• ⚪ Info: `{error_stats['info']}`")

    st.divider()

    # File info
    st.markdown("**📂 Files**")
    agent_mod = datetime.fromtimestamp((logs_dir / "agent.log").stat().st_mtime)
    error_mod = datetime.fromtimestamp((logs_dir / "agent-error.log").stat().st_mtime)

    st.markdown(f"**agent.log**")
    st.markdown(f"```\n{agent_mod.strftime('%H:%M:%S')}\n```", help=agent_mod.strftime('%Y-%m-%d'))

    st.markdown(f"**agent-error.log**")
    st.markdown(f"```\n{error_mod.strftime('%H:%M:%S')}\n```", help=error_mod.strftime('%Y-%m-%d'))

# Auto-refresh
if auto_refresh:
    st.markdown("""
    <script>
        setTimeout(function() {
            window.location.reload();
        }, 5000);
    </script>
    """, unsafe_allow_html=True)

st.divider()
st.caption(f"📂 {logs_dir} · Last updated {datetime.now().strftime('%H:%M:%S')}")
