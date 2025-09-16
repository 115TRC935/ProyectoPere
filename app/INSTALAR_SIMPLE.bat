@echo off
echo Creando entorno virtual...
python -m venv venv
echo Activando entorno virtual...
call venv\Scripts\activate.bat


echo Instalando dependencias...
pip install -r requirements.txt

echo Generando ejecutable (modo onefile)...
pyinstaller --clean --noconfirm --onefile --windowed --icon=icono.ico --add-data "icono.ico;." --add-data "bonzi.gif;." --add-data "bonzi.mp3;." --exclude-module pytest --workpath . --specpath . --distpath . esp32_serial_monitor_tray.py

echo Configurando auto-inicio...
reg add "HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" /v "ESP32_Serial_Monitor" /t REG_SZ /d "%cd%\esp32_serial_monitor_tray.exe" /f

echo Instalacion completada!
echo El programa se ejecutara automaticamente al iniciar Windows.
echo Ejecutable creado: dist\esp32_serial_monitor_tray\esp32_serial_monitor_tray.exe


echo Limpiando archivos temporales...
rmdir /s /q build
rmdir /s /q __pycache__
del /q esp32_serial_monitor_tray.spec
rmdir /s /q venv
rmdir /s /q esp32_serial_monitor_tray

echo Instalacion completada!
echo El programa se ejecutara automaticamente al iniciar Windows.
echo Ejecutable creado: esp32_serial_monitor_tray.exe

pause
