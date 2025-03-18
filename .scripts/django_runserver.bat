@echo off
cd..
echo Avvio Server in corso...
call .venv\Scripts\activate
python manage.py runserver 127.0.0.1:8282
pause