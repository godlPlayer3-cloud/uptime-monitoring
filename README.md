
PL Monitor V3

1. Create venv
2. pip install -r requirements.txt
3. playwright install chromium

Start collector:

python agent/scheduler.py

Start dashboard:

streamlit run dashboard/app.py

Data stored in:
data/monitor.db

Screenshots stored in:
screenshots/
