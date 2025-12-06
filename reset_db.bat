@echo off
echo 🚨 Reseteando base de datos y migraciones...

REM 1. Borrar base de datos SQLite
del db.sqlite3

REM 2. Borrar migraciones (excepto __init__.py)
for /r %%x in (migrations) do (
  del /q %%x\*.py
  del /q %%x\*.pyc
  copy nul %%x\__init__.py >nul
)

REM 3. Crear nuevas migraciones
python manage.py makemigrations

REM 4. Aplicar migraciones
python manage.py migrate

REM 5. Crear superusuario
echo ✅ Base de datos reseteada. Ahora crea tu superusuario:
python manage.py createsuperuser
