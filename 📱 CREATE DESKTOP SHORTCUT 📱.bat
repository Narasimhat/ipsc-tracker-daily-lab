@echo off
color 0B
title Create iPSC Tracker Desktop Shortcut

cls
echo.
echo    ═══════════════════════════════════════════════════════════════
echo                    🧬 iPSC Tracker Shortcut Creator 🧬
echo    ═══════════════════════════════════════════════════════════════
echo.
echo    This will create a desktop shortcut for easy access to iPSC Tracker
echo.
echo    📍 Target: iPSC Tracker - Lab Management System
echo    🏠 Location: Your Desktop
echo    🎯 Purpose: Quick access for team members
echo.
echo    ═══════════════════════════════════════════════════════════════
echo.

pause

echo    🔧 Creating desktop shortcut...
powershell -ExecutionPolicy Bypass -File "create_desktop_shortcuts.ps1"

echo.
echo    ═══════════════════════════════════════════════════════════════
echo    ✅ Shortcut creation process complete!
echo    
echo    Look for this icon on your desktop:
echo    🧬 iPSC Tracker - Lab Management
echo    
echo    Double-click it to start the application anytime!
echo    ═══════════════════════════════════════════════════════════════
echo.
pause