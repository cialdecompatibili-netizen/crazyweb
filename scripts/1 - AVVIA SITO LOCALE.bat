@echo off
title CrazyWeb - Server Locale
color 0A
cd /d "C:\Users\mirco\Desktop\crazyweb"

echo ============================================
echo   CRAZYWEB - Server di sviluppo locale
echo ============================================
echo.
echo Sto avviando il sito in locale...
echo Il browser si aprira' da solo tra pochi secondi su:
echo.
echo      http://127.0.0.1:4000/crazyweb/
echo.
echo Ogni volta che salvi una modifica a un file,
echo il sito si aggiorna da solo nel browser (2-3 secondi).
echo.
echo NON CHIUDERE QUESTA FINESTRA finche' stai lavorando.
echo Per fermare il server: chiudi questa finestra oppure premi CTRL+C.
echo ============================================
echo.

start "" cmd /c "timeout /t 15 /nobreak >nul && start http://127.0.0.1:4000/crazyweb/"

bundle exec jekyll serve --livereload --incremental

pause
