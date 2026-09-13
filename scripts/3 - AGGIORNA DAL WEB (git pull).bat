@echo off
title CrazyWeb - Aggiorna da GitHub
color 0E
cd /d "C:\Users\mirco\Desktop\crazyweb"

echo ============================================
echo   CRAZYWEB - Scarica ultime modifiche
echo ============================================
echo.
echo Questo script scarica sul PC le modifiche fatte
echo online (es. da admin2) o da altri dispositivi,
echo cosi' la copia locale resta allineata.
echo ============================================
echo.

git pull

echo.
echo ============================================
echo   FATTO!
echo ============================================
echo.
pause
