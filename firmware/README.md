
# Firmware (Arduino/ESP32)

Aquí se encuentra el firmware principal para el microcontrolador.

## Archivos principales
- `pico.ino`: Código fuente principal para Arduino/ESP32.
- `frames.h`: Datos de animaciones o visualizaciones.
- `audioData_optimized.h`: Array de audio optimizado generado por los scripts de build_tools.

## Instrucciones
1. Copia `audioData_optimized.h` desde `build_tools/` tras optimizar el audio.
2. Compila y sube el firmware usando Arduino IDE o PlatformIO.
