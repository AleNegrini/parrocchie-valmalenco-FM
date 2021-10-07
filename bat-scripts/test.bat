@echo off
echo Controllo se il programma di gestione delle messe e' attivo...
tasklist /fi "ImageName eq pythonw.exe" /fo csv 2>NUL | find /I "pythonw.exe">NUL
if "%ERRORLEVEL%"=="0" (
	echo Il programma di gestione delle messe e' in esecuzione
) else (
	echo Il programma di gestione delle messe NON e' in esecuzione !!!!!
)
pause