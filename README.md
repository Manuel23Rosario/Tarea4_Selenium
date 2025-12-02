# Tarea4_Selenium

Contenido del proyecto:
- `app/` : Flask web application (login + CRUD de inmuebles usando SQLite)
- `tests/` : Tests automatizados con pytest + Selenium
- `requirements.txt` : dependencias
- `run.sh` : script para levantar la app y ejecutar pruebas localmente (Linux/macOS)
- `run_windows.bat` : script equivalente para Windows (PowerShell/Batch)
- `reports/` y `screenshots/` : carpetas donde se guardarán artefactos al ejecutar tests

## Requisitos
- Python 3.10+
- Google Chrome instalado (o ajustar a otro navegador)

## Instalar dependencias
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Ejecutar la aplicación (puerta 5000)
```bash
# En una terminal
python -m app.app

## Ejecutar pruebas (en otra terminal)
pytest --html=reports/report.html --self-contained-html -q
```

## Notas importantes
- Con webdriver-manager las pruebas intentan descargar el driver correcto para Chrome automáticamente.
- Conftest incluye hooks para capturas automáticas (`screenshots/`) y genera `reports/latest_report.html`.
- Antes de grabar el video: ejecuta las pruebas y abre `reports/latest_report.html`, muestra el tablero en Azure/Jira y da acceso a los correos requeridos.
