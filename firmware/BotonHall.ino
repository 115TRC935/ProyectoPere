#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include "frames.h"     // tu archivo con frames
#include "audioData_optimized.h" // Array optimizado RLE

// OLED config
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define SDA_PIN 4
#define SCL_PIN 5
#define OLED_ADDR 0x3C


Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

// Pines
const int pinAudio = 7;      // Pin para audio PWM manual (digitalWrite)
const int pinHall = 3;       // Pin analógico para sensor Hall

// Variables animación
int currentFrame = 0;
unsigned long lastFrameTime = 0;
const unsigned long frameInterval = 30;  // ms por frame

// Variables para lectura y print serial
unsigned long lastPrintTime = 0;
const unsigned long printInterval = 500; // ms

// PWM manual variables
const int sampleRate = 34000;
const int sampleDelay = 1000000 / sampleRate;
const int repeatFactor = 4;

// Histeresis control
const int thresholdOn = 2480;
const int thresholdOff = 2410;
bool keyPressed = false;

// Clase para interpretar arrays optimizados con compresión RLE usando uint8_t
class AudioOptimizado {
private:
  const uint8_t* array_data;
  size_t array_length;
  size_t posicion_actual;
  int repeticiones_restantes;
  uint8_t valor_actual;
  
public:
  AudioOptimizado(const uint8_t* data, size_t length) {
    array_data = data;
    array_length = length;
    reset();
  }
  
  void reset() {
    posicion_actual = 0;
    repeticiones_restantes = 0;
    valor_actual = 0;
  }
  
  bool hasNext() {
    return posicion_actual < array_length || repeticiones_restantes > 0;
  }
  
  int getNext() {
    // Si tenemos repeticiones pendientes
    if (repeticiones_restantes > 0) {
      repeticiones_restantes--;
      return valor_actual;
    }
    
    // Si llegamos al final
    if (posicion_actual >= array_length) {
      return -1;
    }
    
    uint8_t elemento = array_data[posicion_actual];
    posicion_actual++;
    
    // Verificar si es marcador de repetición (255)
    if (elemento == 255 && posicion_actual + 1 < array_length) {
      // Es formato comprimido: [255, valor, repeticiones]
      valor_actual = array_data[posicion_actual];
      posicion_actual++;
      int repeticiones = array_data[posicion_actual];
      posicion_actual++;
      
      // Validar que repeticiones esté en rango válido (1-254)
      if (repeticiones == 255 || repeticiones == 0) {
        // Error: repeticiones inválidas, retroceder y tratar como valores individuales
        posicion_actual -= 2;
        return 255; // Tratar el marcador como valor individual
      }
      
      repeticiones_restantes = repeticiones - 1; // -1 porque devolvemos uno ahora
      return valor_actual;
    } else {
      // Es valor individual
      return elemento;
    }
  }
};

void reproducirAudio() {
  // Crear instancia del audio optimizado
  AudioOptimizado audio(audioData_optimized, audioData_optimized_len);
  
  // Reproducir con los mismos parámetros que la función original
  while (audio.hasNext()) {
    int value = audio.getNext();
    if (value == -1) break;
    
    int t_on = map(value, 0, 255, 0, sampleDelay);
    int t_off = sampleDelay - t_on;

    for (int j = 0; j < repeatFactor; j++) {
      digitalWrite(pinAudio, HIGH);
      delayMicroseconds(t_on);
      digitalWrite(pinAudio, LOW);
      delayMicroseconds(t_off);
    }
  }
  digitalWrite(pinAudio, LOW);
}

void setup() {

  Wire.begin(SDA_PIN, SCL_PIN, 400000);
  if (!display.begin(SSD1306_SWITCHCAPVCC, OLED_ADDR)) {
    for (;;);
  }
  display.clearDisplay();
  display.display();

  pinMode(pinAudio, OUTPUT);
  pinMode(pinHall, INPUT);
  reproducirAudio();

  Serial.begin(115200);
  delay(1000);
}

void loop() {
  unsigned long now = millis();

  // --- Animación OLED ---
  if (now - lastFrameTime >= frameInterval) {
    lastFrameTime = now;
    display.clearDisplay();
    display.drawBitmap(25, 0, epd_bitmap_allArray[currentFrame], 77, 64, SSD1306_WHITE);
    display.display();

    currentFrame++;
    if (currentFrame >= epd_bitmap_allArray_LEN) currentFrame = 0;
  }

  // --- Leer pin Hall en cada loop ---
  int hallVal = analogRead(pinHall);

  // Print valor crudo cada 500 ms (opcional, no afecta reacción)
  if (now - lastPrintTime >= printInterval) {
    lastPrintTime = now;
    Serial.print("Hall analog val: ");
    Serial.println(hallVal);
  }

  // Detección rápida con histeresis
  if (!keyPressed && hallVal >= thresholdOn) {
    Serial.println("ENTER_ON");
    keyPressed = true;
  } else if (keyPressed && hallVal <= thresholdOff) {
    Serial.println("ENTER_OFF");
    keyPressed = false;
  }
}
