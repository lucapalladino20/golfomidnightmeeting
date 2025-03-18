@echo off

cd .. 

REM Imposta la directory di backup (puoi cambiarla)
set backup_folder=.backup

REM Imposta la directory del progetto come directory corrente
set project_folder=%cd%

REM Ottieni la data in formato YYYYMMDD
set date_part=%date:~-4,4%%date:~-7,2%%date:~-10,2%

REM Ottieni l'ora in formato HHMM (rimuovi spazi e due punti)
set time_part=%time: =0%          
REM Aggiungi uno 0 se l'ora è a una cifra
set time_part=%time_part:~0,2%%time_part:~3,2%

REM Crea il nome del file ZIP con data, ora e minuti
set backup_name=backup_progetto_%date_part%_%time_part%.zip

REM Crea il file ZIP nella directory di backup, escludendo la cartella di backup
"C:\Program Files\7-Zip\7z.exe" a -tzip "%backup_folder%\%backup_name%" "%project_folder%\*" -xr!"%backup_folder%\*"

REM Messaggio di conferma
echo Backup completato: %backup_folder%\%backup_name%