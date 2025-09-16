#!/usr/bin/env python3
"""
Optimizador específico para arrays de audio de Arduino
Lee audio_data.h y genera versión optimizada con uint8_t
"""


import re
import os

def optimizar_array_uint8(array_original, min_repeticiones=10):
    """
    Optimiza un array usando uint8_t con marcadores de repetición
    Formato: [255, valor, repeticiones] para secuencias comprimidas
    255 actúa como marcador especial
    repeticiones está limitado a 1-254 (255 está reservado como marcador)
    """
    if not array_original:
        return [], {"original": 0, "optimizado": 0, "ahorro": 0}
    
    resultado = []
    i = 0
    
    while i < len(array_original):
        valor_actual = array_original[i]
        contador = 1
        
        # Contar valores consecutivos iguales
        while (i + contador < len(array_original) and 
               array_original[i + contador] == valor_actual):
            contador += 1
        
        # Si hay suficientes repeticiones Y no es el valor marcador (255), comprimir
        if contador >= min_repeticiones and valor_actual != 255:
            # Dividir en bloques de máximo 254 repeticiones (255 reservado para marcador)
            contador_restante = contador
            while contador_restante > 0:
                reps_bloque = min(contador_restante, 254)
                resultado.extend([255, valor_actual, reps_bloque])
                print(f"Comprimido: {reps_bloque} repeticiones de {valor_actual} → [255, {valor_actual}, {reps_bloque}]")
                contador_restante -= reps_bloque
        else:
            # Agregar valores individuales
            for _ in range(contador):
                # Si el valor es 255 (marcador), necesitamos escaparlo
                if valor_actual == 255:
                    resultado.extend([255, 255, 1])  # 255 escapado como repetición de 1
                else:
                    resultado.append(valor_actual)
        
        # SIEMPRE avanzar por 'contador' elementos procesados
        i += contador
    
    # Estadísticas
    tamaño_original = len(array_original)
    tamaño_optimizado = len(resultado)
    ahorro_porcentaje = ((tamaño_original - tamaño_optimizado) / tamaño_original * 100) if tamaño_original > 0 else 0
    
    # Contar compresiones (cada grupo de 3 elementos que empiece con 255)
    compresiones = 0
    j = 0
    while j < len(resultado) - 2:
        if resultado[j] == 255 and j + 2 < len(resultado) and resultado[j+2] != 255:
            compresiones += 1
            j += 3
        else:
            j += 1
    
    estadisticas = {
        "original": tamaño_original,
        "optimizado": tamaño_optimizado,
        "ahorro": round(ahorro_porcentaje, 2),
        "elementos_comprimidos": compresiones
    }
    
    return resultado, estadisticas

def generar_header_arduino_uint8(array_optimizado, nombre_variable="audioData_optimized"):
    """
    Genera archivo .h para Arduino con array uint8_t optimizado
    """
    header_content = f"""// Array optimizado con compresión RLE usando uint8_t
// Generado automáticamente por audio_optimizer.py
// Formato: [255, valor, repeticiones] para secuencias comprimidas
// 255 actúa como marcador de repetición

#ifndef {nombre_variable.upper()}_H
#define {nombre_variable.upper()}_H

const uint8_t {nombre_variable}[] = {{
"""
    
    # Generar elementos del array en líneas de ~20 elementos cada una
    elementos_por_linea = 20
    linea_actual = []
    
    for i, elemento in enumerate(array_optimizado):
        linea_actual.append(str(elemento))
        
        # Si completamos una línea o es el último elemento
        if len(linea_actual) >= elementos_por_linea or i == len(array_optimizado) - 1:
            # Agregar comas excepto en el último elemento del array completo
            elementos_con_comas = []
            for j, elem in enumerate(linea_actual):
                if i == len(array_optimizado) - 1 and j == len(linea_actual) - 1:
                    # Último elemento del array completo - sin coma
                    elementos_con_comas.append(elem)
                else:
                    elementos_con_comas.append(elem + ",")
            
            # Escribir la línea
            header_content += "  " + " ".join(elementos_con_comas) + "\n"
            linea_actual = []
    
    header_content += f"""
}};

const size_t {nombre_variable}_len = {len(array_optimizado)};

#endif
"""
    
    return header_content

def extraer_array_desde_header(archivo_h):
    """
    Extrae array de datos desde archivo .h de Arduino
    """
    try:
        with open(archivo_h, 'r') as f:
            contenido = f.read()
        
        # Buscar el array específico: const uint8_t audioData[] = {
        patron = r'const\s+uint8_t\s+audioData\[\]\s*=\s*\{([^}]+)\}'
        match = re.search(patron, contenido, re.DOTALL)
        
        if not match:
            print(f"❌ No se encontró array 'audioData' en {archivo_h}")
            return None, None
        
        datos_str = match.group(1)
        
        # Extraer números
        numeros = []
        for num in re.findall(r'\d+', datos_str):
            numeros.append(int(num))
        
        print(f"✅ Array 'audioData' extraído: {len(numeros)} elementos")
        return numeros, "audioData"
        
    except FileNotFoundError:
        print(f"❌ Archivo {archivo_h} no encontrado")
        return None, None
    except Exception as e:
        print(f"❌ Error leyendo {archivo_h}: {e}")
        return None, None

def optimizar_audio_data():
    """
    Optimiza el archivo audio_data.h existente
    """
    print("=== OPTIMIZADOR DE AUDIO DATA ===\n")
    
    # Usar ruta robusta relativa al script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    array_original, nombre_original = extraer_array_desde_header(os.path.join(base_dir, "audio_data.h"))
    
    if array_original is None:
        print("❌ No se pudo procesar audio_data.h")
        return False
    
    print(f"Array original: {len(array_original)} elementos")
    print(f"Primeros 20 valores: {array_original[:20]}")
    print()
    
    # Optimizar con umbral de 10 repeticiones
    print("--- Optimizando con umbral: 10 repeticiones ---")
    optimizado, stats = optimizar_array_uint8(array_original, min_repeticiones=10)
    
    print(f"Resultado: {stats['original']} → {stats['optimizado']} elementos")
    print(f"Ahorro: {stats['ahorro']}% ({stats['elementos_comprimidos']} compresiones)")
    print()
    
    # Generar archivo optimizado
    header = generar_header_arduino_uint8(optimizado, f"{nombre_original}_optimized")
    nombre_archivo = os.path.join(base_dir, f"{nombre_original}_optimized.h")
    with open(nombre_archivo, "w") as f:
        f.write(header)
    
    print(f"✅ Archivo '{nombre_archivo}' generado")
    
    # Mostrar algunas compresiones encontradas
    compresiones = []
    j = 0
    while j < len(optimizado) - 2:
        if optimizado[j] == 255 and j + 2 < len(optimizado) and optimizado[j+2] != 255:
            valor = optimizado[j+1]
            reps = optimizado[j+2]
            compresiones.append(f"{reps} repeticiones de {valor}")
            j += 3
        else:
            j += 1
    
    if compresiones:
        print("\n🎯 Compresiones detectadas:")
        for comp in compresiones[:10]:  # Mostrar primeras 10
            print(f"  {comp}")
        if len(compresiones) > 10:
            print(f"  ... y {len(compresiones)-10} más")
    
    return True

if __name__ == "__main__":
    # Optimizar audio_data.h si existe
    if not optimizar_audio_data():
        print("No se pudo procesar el archivo audio_data.h")
        exit(1)
