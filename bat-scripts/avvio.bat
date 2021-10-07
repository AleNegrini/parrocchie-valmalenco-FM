@echo off
echo Se attivo, arresto il programma di gestione delle messe...
taskkill /f /im "pythonw.exe"

echo Avvio il programma di gestione delle messe...
rem cd D:\Data\max\lavoro\chiese-caspoggio\VALMALENCO-PARROCCHIE\parrocchie-valmalenco-FM\src
cd C:\Users\salar\Desktop\VALMALENCO-PARROCCHIE\parrocchie-valmalenco-FM\src
start /B pythonw main.py test

echo Il programma di gestione delle messe e' stato avviato
pause