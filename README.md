# Intelligent Log Noise Reduction System

This is a web-based application built with **Streamlit** and **Python** that uses Machine Learning to analyze log files, cluster similar entries, and reduce noise.

## Features
- **Public Login**: Simple email-based login for users.
- **Admin Dashboard**: Secure area effectively (role-based) to process logs.
- **Machine Learning**: Uses TF-IDF and KMeans to cluster logs.
- **Noise Reduction**: Identifies frequent noisy logs and reduces them to unique patterns.
- **Reporting**: Downloadable CSV reports of the analysis.

## Setup & Run

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the Application**:
    ```bash
    streamlit run app.py
    ```

3.  **Access the App**:
    Open your browser and navigate to `http://localhost:8501`.

## Credentials (Demo)
- **User Role**: Enter any email (e.g., `user@test.com`)
- **Admin Role**:
    - Email: `admin@example.com`
    - Password: `admin`

## Project Structure
- `app.py`: Main application file.
- `ml_engine.py`: Contains the machine learning logic (TF-IDF, KMeans).
- `db_handler.py`: Handles SQLite database operations for user logins.
- `requirements.txt`: Python dependencies.
