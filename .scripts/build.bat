@echo off

cd ..

:: Esci in caso di errore
setlocal enabledelayedexpansion

call .venv\Scripts\activate

:: Aggiorna pip
    python -m pip install --upgrade pip

pause

:: Installa le dipendenze
pip install -r requirements.txt

pause

:: Raccogli i file statici
python manage.py collectstatic --no-input

pause

:: Crea le migrazioni
python manage.py makemigrations

pause

:: Applica le migrazioni
python manage.py migrate

pause

:: Termina lo script
exit /b 0