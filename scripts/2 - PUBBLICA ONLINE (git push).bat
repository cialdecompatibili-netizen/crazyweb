@echo off
title CrazyWeb - Pubblica online
color 0B
cd /d "C:\Users\mirco\Desktop\crazyweb"

echo ============================================
echo   CRAZYWEB - Pubblica le modifiche online
echo ============================================
echo.
echo Questo script carica su GitHub tutte le modifiche
echo che hai fatto in locale. Il sito online si
echo aggiornera' automaticamente in 2-3 minuti.
echo.
echo ============================================
echo.

git add -A

set /p MSG="Scrivi una breve descrizione della modifica (poi premi INVIO): "

if "%MSG%"=="" set MSG=Aggiornamento sito

git commit -m "%MSG%"
git push

echo.
echo ============================================
echo   FATTO! Controlla GitHub Actions tra poco
echo   per vedere il deploy completarsi.
echo ============================================
echo.
pause
