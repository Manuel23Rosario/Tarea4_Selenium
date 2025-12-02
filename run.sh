#!/usr/bin/env bash
set -e
# Levantar la app en background y ejecutar tests
python3 app/app.py &
APP_PID=$!
echo "App PID: $APP_PID"
sleep 2
pytest --html=reports/latest_report.html --self-contained-html -q || true
kill $APP_PID
