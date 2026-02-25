@echo off
cd /d "%~dp0"
start "" /B python -m streamlit run app.py
echo Application started in background!
echo Go to http://localhost:8501
pause
