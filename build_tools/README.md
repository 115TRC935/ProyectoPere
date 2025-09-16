
# Build Tools y Utilidades de Audio

Aquí se encuentran los scripts y utilidades para preparar los archivos de audio y generar los headers para el firmware.

## Scripts principales
- `wavToTone.py`: Convierte un archivo WAV (8kHz, 8bit, mono) a un array C (`audio_data.h`).
- `audio_optimizer.py`: Optimiza el array generado usando compresión RLE y genera `audioData_optimized.h`.
- `ESP32_Serial_Monitor.spec`: Especificación para PyInstaller.

## Ejemplo de uso
1. Coloca tu archivo WAV en esta carpeta.
2. Ejecuta `wavToTone.py` para generar `audio_data.h`.
3. Ejecuta `audio_optimizer.py` para generar `audioData_optimized.h`.
4. Copia `audioData_optimized.h` a la carpeta `firmware/`.

## Archivos
- `*.wav`: Archivos fuente de audio.
- `audio_data.h`: Array sin optimizar.
- `audioData_optimized.h`: Array optimizado.
