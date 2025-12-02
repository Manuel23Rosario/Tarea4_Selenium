@echo off
        REM Levanta la app y ejecuta tests en Windows (PowerShell/Batch)
        start /B python app\app.py
        timeout /t 2 /nobreak
        pytest --html=reports\latest_report.html --self-contained-html -q
