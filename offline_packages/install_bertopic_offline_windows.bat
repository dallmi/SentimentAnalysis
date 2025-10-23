@echo off
REM BERTopic Offline Installation Script for Windows
REM This script installs BERTopic and all dependencies from local wheel files

echo ============================================
echo BERTopic Offline Installation (Windows)
echo ============================================
echo.

cd /d "%~dp0bertopic_windows"

echo Installing BERTopic and dependencies...
pip install --no-index --find-links . bertopic sentence-transformers umap-learn hdbscan

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ============================================
    echo Installation successful!
    echo ============================================
    echo.
    echo You can now use BERTopic offline.
    echo Models are in: offline_packages/models/
    echo.
) else (
    echo.
    echo ============================================
    echo Installation failed!
    echo ============================================
    echo.
    echo Check the error messages above.
    echo.
)

pause
