# Intelligent Log Noise Reduction System 📊

A robust, web-based application powered by **Machine Learning** to accept system logs, cluster similar entries, and significantly reduce noise for better observability and analysis.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://intelligent-log-noise-reduction-system-9gvder8p6bnjtzhitbxbnx.streamlit.app/)

---

## 🚀 Features

### 👤 Public User Interface
- **Public Access**: Accessible by anyone via a web link.
- **Login system**: Simple email-based login for users.
- **Welcome Dashboard**: Personalized landing page for general users.

### 🛡️ Admin Dashboard (Enterprise Grade)
- **Health Dashboard**: Visual analytics with **Interactive Plotly Charts** showing cluster distributions and noise reduction KPIs.
- **Log Processing**: Upload raw CSV log files for analysis.
- **ML Clustering**: Uses **TF-IDF Vectorization** and **K-Means Clustering** to group similar logs.
- **Delta Comparison (Regression)**: Compare "Baseline" vs "Current" logs to automatically detect **New Issue Patterns**.
- **Professional Reporting**: Generate and download **Multi-Sheet Excel Reports (.xlsx)** with summary metrics and raw data.
- **Data Export**: Download results as CSV or Enterprise Excel files.
- **User Management**: View a history of all user logins.

---

## 📂 Project Structure

```bash
├── app.py                 # 📱 Main Streamlit application entry point (Frontend & Controller)
├── ml_engine.py           # 🧠 Machine Learning logic (Cleaning, TF-IDF, K-Means)
├── db_handler.py          # 🗄️ Database operations (SQLite for user login tracking)
├── requirements.txt       # 📦 Python dependencies
├── packages.txt           # 📦 Application dependencies (if needed for deployment)
├── Dockerfile             # 🐳 Docker configuration (Optional for containerization)
└── README.md              # 📖 Project documentation
```

### Key Modules:
- **`app.py`**: Handles the UI layout, session state management (User/Admin), and interactions.
- **`ml_engine.py`**:
    - `clean_log()`: Prepares raw text by removing timestamps, IPs, and dynamic numbers.
    - `cluster_logs()`: Groups logs into 'K' clusters.
    - `identify_noise()`: Finds frequent patterns within clusters.
- **`db_handler.py`**: Manages the `log_noise_system.db` SQLite database.

---

## 🛠️ Technology Stack

- **Language**: Python 3.9+
- **Frontend**: Streamlit
- **ML/DS Libraries**: Scikit-Learn, Pandas, NumPy
- **Database**: SQLite3
- **Visualization**: Matplotlib / Built-in Streamlit charts

---

## 💻 How to Run Locally

Follow these steps to set up the project on your local machine.

### Prerequisites
- Python installed (version 3.8 or higher).

### 1. Clone the Repository
```bash
git clone https://github.com/JayabharathiMK/intelligent-log-noise-reduction-system.git
cd intelligent-log-noise-reduction-system
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
streamlit run app.py
```

### Access the App
Open your browser and navigate to: http://localhost:8501

---

## ☁️ Deployment (Cloud Access 24/7)

This project is deployed on **Streamlit Community Cloud**.

**🔗 Live Link:** [https://intelligent-log-noise-reduction-system-9gvder8p6bnjtzhitbxbnx.streamlit.app/](https://intelligent-log-noise-reduction-system-9gvder8p6bnjtzhitbxbnx.streamlit.app/)

*(Note: Since it is on a free tier, it may take a few seconds to "wake up" if it hasn't been used recently.)*

---

## 🔐 Credentials (Demo)

Use the following credentials to test the generic flows:

| Role | Email | Password | Access |
| :--- | :--- | :--- | :--- |
| **User** | `user@test.com` | *No Password* | View Welcome Dashboard |
| **Admin** | `admin@example.com` | `admin` | Full ML Dashboard & Reports |

---

## 📊 Sample Data Format

If you want to upload your own logs, use a **CSV file** with a column named `Log Message`.

**Example `test_logs.csv`**:
```csv
Log Message
2024-01-01 10:00:01 Error: Connection timeout at 192.168.1.5
2024-01-01 10:00:05 Error: Connection timeout at 192.168.1.6
2024-01-01 10:01:00 Info: User Login Successful
2024-01-01 10:02:00 Warning: High Memory Usage
```

---

## 🤝 Contribution

1. Fork the repo.
2. Create standard branch (`git checkout -b feature-name`).
3. Commit changes (`git commit -m 'Add new feature'`).
4. Push to branch (`git push origin feature-name`).
5. Open a Pull Request.

---

**Developed with ❤️ using Python & Streamlit**
