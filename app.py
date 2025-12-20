import streamlit as st
import pandas as pd
import db_handler
import ml_engine
import io

# Initialize DB on start
db_handler.init_db()

st.set_page_config(page_title="Intelligent Log Noise Reduction", layout="wide")

# Custom CSS for styling
st.markdown("""
<style>
    .main {
        background-color: #f0f2f6;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #4CAF50; 
        color: white;
    }
    .title-text {
        color: #2c3e50;
        text-align: center;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    .sidebar .sidebar-content {
        background-color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'user_role' not in st.session_state:
    st.session_state['user_role'] = None
if 'email' not in st.session_state:
    st.session_state['email'] = ""

def login_page():
    st.markdown("<h1 class='title-text'>Intelligent Log Noise Reduction System</h1>", unsafe_allow_html=True)
    
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
                if email:
                    st.session_state['logged_in'] = True
                    st.session_state['user_role'] = "User"
                    st.session_state['email'] = email
                    db_handler.log_user_login(email)
                    st.rerun()
                else:
                    st.warning("Please enter an email address")

def user_dashboard():
    st.markdown(f"<h2 class='title-text'>Welcome, {st.session_state['email']}</h2>", unsafe_allow_html=True)
    st.info("You have successfully accessed the Intelligent Log System.")
    
    st.markdown("### About the System")
    st.write("This system uses machine learning to analyze log files, cluster similar entries, and reduce noise for better observability.")
    
    if st.button("Logout"):
        st.session_state.clear()
        st.rerun()

def admin_dashboard():
    st.sidebar.title("Admin Dashboard")
    menu = st.sidebar.radio("Navigation", ["Upload & Process Logs", "View User Logins"])
    
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
                    # Synthesize a 'Log Message' column compatible with the ML engine
                    db_df['Log Message'] = db_df['login_time'].astype(str) + " Info: User " + db_df['email'] + " logged in"
                    st.session_state['uploaded_df'] = db_df[['Log Message']] # Keep only relevant column for consistency
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
            
            if 'Log Message' not in df.columns:
                st.warning("Data must have a 'Log Message' column.")
            else:
                n_clusters = st.slider("Number of Clusters", 2, 10, 3)
                
                if st.button("Apply ML Clustering"):
                    with st.spinner("Processing..."):
                        clustered_df = ml_engine.cluster_logs(df.copy(), n_clusters)
                        noise_reduced_df = ml_engine.identify_noise(clustered_df)
                        
                        st.session_state['clustered_df'] = clustered_df
                        st.session_state['noise_reduced_df'] = noise_reduced_df
                        st.success(f"Processing Complete! Processed {len(clustered_df)} logs.")

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

if not st.session_state['logged_in']:
    login_page()
else:
    if st.session_state['user_role'] == "Admin":
        admin_dashboard()
    else:
        user_dashboard()
