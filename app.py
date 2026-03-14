import streamlit as st
import pandas as pd
import db_handler
import ml_engine
import io
import plotly.express as px
import plotly.graph_objects as go
import re

# Initialize DB on start
db_handler.init_db()

st.set_page_config(page_title="Intelligent Log Noise Reduction", layout="wide")

# Custom CSS for modern styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
        color: #f8fafc;
    }

    [data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.95) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    div.stButton > button, div.stDownloadButton > button {
        background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%);
        color: #ffffff !important;
        border: 2px solid rgba(255, 255, 255, 0.2);
        padding: 0.8rem 1.5rem;
        border-radius: 14px;
        font-weight: 800;
        font-size: 1.1rem;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 0 20px rgba(0, 210, 255, 0.4);
        width: 100%;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-top: 10px;
    }
    
    div.stButton > button:hover, div.stDownloadButton > button:hover {
        transform: translateY(-5px) scale(1.03);
        box-shadow: 0 0 35px rgba(0, 210, 255, 0.7);
        background: linear-gradient(90deg, #3a7bd5 0%, #00d2ff 100%);
        border: 2px solid #ffffff;
    }

    .title-container {
        padding: 4rem 2rem;
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        margin-bottom: 2.5rem;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
    }

    .title-text {
        font-weight: 800;
        background: linear-gradient(135deg, #6366f1 0%, #ec4899 50%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem;
        margin-bottom: 1rem;
        line-height: 1.2;
    }

    .subtitle-text {
        color: #94a3b8;
        font-size: 1.2rem;
        font-weight: 400;
        max-width: 600px;
        margin: 0 auto;
    }

    .card {
        background: rgba(30, 41, 59, 0.7);
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.05);
        margin-bottom: 1.5rem;
        backdrop-filter: blur(5px);
    }

    h1, h2, h3, p, span, div {
        color: #f1f5f9 !important;
    }

    [data-testid="stHeader"] {
        background: rgba(0,0,0,0);
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 15px;
        background-color: transparent;
        padding: 10px 0;
    }

    .stTabs [data-baseweb="tab"] {
        height: 55px;
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        color: #94a3b8 !important;
        padding: 0 25px;
        transition: all 0.3s ease;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, rgba(99, 102, 241, 0.2) 0%, rgba(139, 92, 246, 0.2) 100%);
        border-bottom: 3px solid #6366f1 !important;
        color: #ffffff !important;
    }

    /* Selectbox styling */
    div[data-baseweb="select"] > div {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        color: white !important;
        border-radius: 12px !important;
    }
    div[data-baseweb="select"] div {
        color: white !important;
    }

    /* Input styling - Black text and light background */
    div[data-baseweb="input"] > div {
        background-color: #f8fafc !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 12px !important;
    }
    div[data-baseweb="input"] input {
        color: #000000 !important;
        font-weight: 500 !important;
    }

    [data-testid="stMarkdownContainer"] p {
        color: #f1f5f9 !important;
    }

    /* Fix dropdown list visibility - Dark background with white text */
    div[data-baseweb="popover"] {
        background-color: #1e293b !important;
    }

    div[data-baseweb="popover"] * {
        background-color: transparent !important;
        color: #ffffff !important;
    }
    
    ul[role="listbox"] {
        background-color: #1e293b !important;
    }

    li[role="option"] {
        background-color: transparent !important;
        color: #ffffff !important;
        padding: 10px !important;
    }

    li[role="option"]:hover {
        background-color: #334155 !important;
        color: #00d2ff !important;
    }

    /* DataFrame styling */
    [data-testid="stDataFrame"] {
        background: rgba(15, 23, 42, 0.5);
        border-radius: 12px;
        padding: 10px;
    }

    /* File Uploader visibility fix - Indigo buttons with white text */
    [data-testid="stFileUploader"] {
        background-color: #1e293b !important;
        border: 2px dashed #334155 !important;
        border-radius: 15px !important;
        padding: 20px !important;
    }

    [data-testid="stFileUploader"] section button {
        background-color: #6366f1 !important;
        color: #ffffff !important;
        border: 2px solid #818cf8 !important;
        border-radius: 10px !important;
        font-weight: bold !important;
        padding: 10px 30px !important;
        cursor: pointer !important;
        display: inline-block !important;
    }

    /* Target the text more specifically */
    [data-testid="stFileUploader"] section button div {
        color: #ffffff !important;
    }

    [data-testid="stFileUploader"] section button:hover {
        background-color: #4f46e5 !important;
        border-color: #ffffff !important;
    }

    [data-testid="stFileUploadDropzone"] {
        background-color: transparent !important;
    }

    [data-testid="stFileUploader"] small {
        color: #94a3b8 !important;
    }
    }
</style>
""", unsafe_allow_html=True)

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'user_role' not in st.session_state:
    st.session_state['user_role'] = None
if 'email' not in st.session_state:
    st.session_state['email'] = ""

def is_valid_email(email):
    """Simple regex to check if string follows email format."""
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None

def login_page():
    st.markdown("""
    <div class='title-container'>
        <h1 class='title-text'>Intelligent Log Noise Reduction System</h1>
        <p class='subtitle-text'>Harnessing AI to clarify your system's observability</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    
    with col2:
        st.subheader("Login")
        role = st.selectbox("Select Role", ["User", "Admin"])
        
        email = st.text_input("Enter Email ID")
        
        # For admin, we might want a password, but instructions said:
        # "Users should be able to log in using only their email ID"
        # "There should be a separate Admin login."
        # I'll add a simple password for Admin for realism, or just email check if strictly following 'no password required' for users.
        # Let's keep it simple: Admin requires a specific email or code, or just a toggle for this demo.
        # The prompt says "After successful login... Users should see a welcome page... Admin should be able to..."
        
        if role == "Admin":
            password = st.text_input("Admin Password", value="admin")
            if st.button("Login"):
                if email.strip() == "admin@example.com" and password.strip() == "admin":
                    st.session_state['logged_in'] = True
                    st.session_state['user_role'] = "Admin"
                    st.session_state['email'] = email
                    st.success("Welcome Admin")
                    st.rerun()
                else:
                    st.error("Invalid Admin Credentials (Try admin@example.com / admin)")
        else:
            if st.button("Login"):
                if email.strip():
                    if is_valid_email(email.strip()):
                        st.session_state['logged_in'] = True
                        st.session_state['user_role'] = "User"
                        st.session_state['email'] = email
                        db_handler.log_user_login(email)
                        st.rerun()
                    else:
                        st.error("Invalid email format. Please use 'user@example.com'.")
                else:
                    st.warning("Please enter an email address")

def user_dashboard():
    st.markdown(f"""
    <div class='title-container'>
        <h2 class='title-text'>User Access & Intelligence Portal</h2>
        <p class='subtitle-text'>Welcome, <b>{st.session_state['email']}</b>. Thank you for authenticating with the system.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='card'>
        <h3>System Purpose & Log Capture</h3>
        <p>This platform serves as a <b>Log Capture Node</b> for the Intelligent Log Noise Reduction System. 
        Your successful login contributes to the <i>User Login History</i>, which is utilized by our 
        Machine Learning engine to identify patterns, cluster access behavior, and reduce operational noise.</p>
        <hr>
        <p><b>Note:</b> For advanced log processing, clustering reports, and system-wide analysis, 
        please consult the Administrative Dashboard.</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Logout"):
        st.session_state.clear()
        st.rerun()

def admin_dashboard():
    st.sidebar.title("Admin Dashboard")
    menu = st.sidebar.radio("Navigation", [
        "Health Dashboard", 
        "Upload & Process Logs", 
        "Comparison Analysis (Delta)",
        "View User Logins"
    ])
    
    if st.button("Logout", key='logout_btn'):
        st.session_state.clear()
        st.rerun()

    if menu == "View User Logins":
        st.header("User Login History")
        df_logins = db_handler.get_all_user_logins()
        st.dataframe(df_logins, use_container_width=True)
        
    elif menu == "Upload & Process Logs":
        st.header("Log Processing")
        
        uploaded_file = st.file_uploader("Upload Log File (CSV)", type=['csv'])
        
        # Sample data generation for demo
        if st.checkbox("Use Sample Data"):
            data = {
                'Log Message': [
                    '2023-01-01 10:00:00 Error: Connection failed',
                    '2023-01-01 10:01:00 Error: Connection failed',
                    '2023-01-01 10:02:00 Info: User logged in',
                    '2023-01-01 10:03:00 Warning: Disk space low',
                    '2023-01-01 10:04:00 Error: Connection failed at 192.168.1.1',
                    '2023-01-01 10:05:00 Error: Connection failed at 192.168.1.2',
                    '2023-01-01 10:06:00 Info: User logged out',
                    '2023-01-01 10:07:00 Warning: Disk space low on /dev/sda1'
                ]
            }
            df = pd.DataFrame(data)
            st.session_state['uploaded_df'] = df
            st.success("Sample data loaded!")
        
        elif uploaded_file:
            try:
                df = pd.read_csv(uploaded_file)
                st.session_state['uploaded_df'] = df
            except Exception as e:
                st.error(f"Error reading file: {e}")
        
        if st.button("Load Real-time Logins from DB"):
            try:
                db_df = db_handler.get_all_user_logins()
                if not db_df.empty:
                    st.session_state['uploaded_df'] = db_df
                    st.success(f"Loaded {len(db_df)} records from live database!")
                else:
                    st.warning("No login records found in database.")
            except Exception as e:
                st.error(f"Error loading from DB: {e}")
        
        if 'uploaded_df' in st.session_state:
            df = st.session_state['uploaded_df']
            st.subheader("Raw Data Preview (First 5 Rows)")
            st.write(f"Total Rows Loaded: {len(df)}")
            st.dataframe(df.head(), use_container_width=True)
            
            # Auto-detect best column or let user select
            available_cols = list(df.columns)
            default_ix = 0
            if 'Log Message' in available_cols: default_ix = available_cols.index('Log Message')
            elif 'email' in available_cols: default_ix = available_cols.index('email')
            
            target_col = st.selectbox("Select column to analyze", available_cols, index=default_ix)
            
            n_clusters = st.slider("Number of Clusters", 2, 10, 3)
            
            if st.button("Apply ML Clustering"):
                    with st.spinner(f"Processing using '{target_col}'..."):
                        clustered_df = ml_engine.cluster_logs(df.copy(), n_clusters, target_col=target_col)
                        noise_reduced_df = ml_engine.identify_noise(clustered_df, target_col=target_col)
                        
                        st.session_state['clustered_df'] = clustered_df
                        st.session_state['noise_reduced_df'] = noise_reduced_df
                        st.success(f"Processing Complete! Processed {len(clustered_df)} logs using '{target_col}'.")

        if 'clustered_df' in st.session_state and 'noise_reduced_df' in st.session_state:
            tab1, tab2 = st.tabs(["Clustered Logs", "Noise Reduced Results"])
            
            with tab1:
                st.subheader("Clustered Logs")
                st.write("Logs grouped by similarity.")
                st.dataframe(st.session_state['clustered_df'], use_container_width=True)
                
                csv_cluster = st.session_state['clustered_df'].to_csv(index=False).encode('utf-8')
                st.download_button("Download Clustered Logs", csv_cluster, "clustered_logs.csv", "text/csv")
                
            with tab2:
                st.subheader("Noise Reduced Results")
                st.write("Unique log patterns identified and their frequency.")
                st.dataframe(st.session_state['noise_reduced_df'], use_container_width=True)
                
                csv_noise = st.session_state['noise_reduced_df'].to_csv(index=False).encode('utf-8')
                st.download_button("Download Noise Report", csv_noise, "noise_report.csv", "text/csv")

        # Professional Excel Export Utility
        if 'clustered_df' in st.session_state:
            st.divider()
            if st.button("Generate Enterprise Excel Report"):
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    # Write summary
                    summary_df = pd.DataFrame({
                        'Metric': ['Total Logs Processed', 'Unique Patterns Found', 'Noise Reduction %'],
                        'Value': [
                            len(st.session_state['clustered_df']),
                            len(st.session_state['noise_reduced_df']),
                            f"{((1 - len(st.session_state['noise_reduced_df'])/len(st.session_state['clustered_df']))*100):.2f}%"
                        ]
                    })
                    summary_df.to_excel(writer, sheet_name='Summary', index=False)
                    st.session_state['clustered_df'].to_excel(writer, sheet_name='Raw Clusters', index=False)
                    st.session_state['noise_reduced_df'].to_excel(writer, sheet_name='Noise Report', index=False)
                
                st.download_button(
                    label="📥 Download Professional Report (.xlsx)",
                    data=output.getvalue(),
                    file_name="enterprise_log_analysis.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

    elif menu == "Comparison Analysis (Delta)":
        st.header("Regression & Delta Analysis")
        st.write("Compare a **Baseline** log set with a **Current** set to identify new issues.")
        
        col1, col2 = st.columns(2)
        with col1:
            baseline_file = st.file_uploader("Upload Baseline Logs (e.g. Previous Week)", type=['csv'], key='baseline')
        with col2:
            current_file = st.file_uploader("Upload Current Logs (e.g. This Week)", type=['csv'], key='current')
            
        if baseline_file and current_file:
            df_b = pd.read_csv(baseline_file)
            df_c = pd.read_csv(current_file)
            
            # Find common columns for comparison
            common_cols = list(set(df_b.columns).intersection(set(df_c.columns)))
            
            if not common_cols:
                st.error("The two files have no identical column names. They must share at least one column (e.g., 'Log Message') to be compared.")
            else:
                default_ix = 0
                if 'Log Message' in common_cols: default_ix = common_cols.index('Log Message')
                elif 'email' in common_cols: default_ix = common_cols.index('email')
                
                target_col = st.selectbox("Select column to compare", common_cols, index=default_ix)
                
                if st.button("Run Delta Comparison"):
                    with st.spinner("Analyzing differences..."):
                        try:
                            delta_df = ml_engine.compare_log_sets(df_b, df_c, target_col=target_col)
                            if not delta_df.empty:
                                st.subheader("⚠️ New Patterns Detected")
                                st.write("These log patterns were NOT present in the baseline set.")
                                st.dataframe(delta_df, use_container_width=True)
                            else:
                                st.success("No new patterns detected. System is stable compared to baseline.")
                        except Exception as e:
                            st.error(f"Analysis Error: {e}")

    elif menu == "Health Dashboard":
        st.header("System Health Analytics")
        if 'clustered_df' not in st.session_state:
            st.info("Please process logs in the 'Upload & Process Logs' section first.")
        else:
            df = st.session_state['clustered_df']
            noise_df = st.session_state['noise_reduced_df']
            
            # KPI Row
            kpi1, kpi2, kpi3 = st.columns(3)
            with kpi1:
                st.metric("Total Logs", len(df))
            with kpi2:
                noise_red = (1 - len(noise_df)/len(df)) * 100
                st.metric("Noise Reduction", f"{noise_red:.1f}%", delta=f"{len(df) - len(noise_df)} removed")
            with kpi3:
                st.metric("Unique Patterns", len(noise_df))
            
            # Charts
            c1, c2 = st.columns(2)
            with c1:
                st.subheader("Cluster Distribution")
                fig = px.pie(noise_df, values='Count', names='Cluster', hole=.3,
                            color_discrete_sequence=px.colors.sequential.RdBu)
                st.plotly_chart(fig, use_container_width=True)
            
            with c2:
                st.subheader("Frequency of Patterns")
                fig = px.bar(noise_df.head(10), x='Count', y='Cleaned Log', 
                            orientation='h', color='Count',
                            labels={'Cleaned Log': 'Pattern Signature'})
                st.plotly_chart(fig, use_container_width=True)

if not st.session_state['logged_in']:
    login_page()
else:
    if st.session_state['user_role'] == "Admin":
        admin_dashboard()
    else:
        user_dashboard()
