import wave
import numpy as np
import os

# === Configuraciones ===
base_dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(base_dir, "aiaiai im ur little butterfly.wav")  # Archivo de entrada (WAV)
output_header = os.path.join(base_dir, "audio_data.h")  # Archivo de salida (header C)
array_name = "audioData"                # Nombre del array en el .h
target_rate = 8000                      # Hz
target_width = 1                        # bytes (1 byte = 8 bits unsigned)
target_channels = 1                     # Mono

# === Abrir archivo WAV ===
with wave.open(input_file, 'rb') as wav:
    assert wav.getframerate() == target_rate, "La frecuencia debe ser 8000 Hz"
    assert wav.getsampwidth() == target_width, "El audio debe ser 8 bits (unsigned)"
    assert wav.getnchannels() == target_channels, "El audio debe ser mono"
    
    frames = wav.readframes(wav.getnframes())
    samples = np.frombuffer(frames, dtype=np.uint8)

# === Escribir archivo .h con array C ===
with open(output_header, 'w') as f:
    f.write(f"// Audio convertido a unsigned 8-bit, 8kHz, mono\n")
    f.write(f"const uint8_t {array_name}[] = {{\n    ")

    for i, sample in enumerate(samples):
        f.write(f"{sample}, ")
        if (i + 1) % 20 == 0:
            f.write("\n    ")

    f.write("\n};\n")
    f.write(f"const size_t {array_name}_len = {len(samples)};\n")

print(f"Generado: {output_header} ({len(samples)} muestras)")
