// -----------------------------------------
//  TEMPERATURE CONTROL LOOP
// -----------------------------------------
//
// GND ---- power supply ---- arduino pin ---- relay in ---- heat sink --- TMP36
// D2   (arduino) -->-- IN1 (relay)
// 5V   (arduino) -->-- VCC (relay in)
// A0   (arduino) -->-- signal pin (TMP36)
// 3.3V (arduino) -->-- VCC (TMP36)
// J1-1 (relay)   -->-- VCC (heat sink)
// J1-3 (relay)   -->-- VCC  (power supply)
//
// -----------------------------------------
// Average readings from a TMP36 thermistor and actuate a peltier coil.
// Bang-bang control with hysteresis.

#include <stdio.h>

#define TEMP_FORMAT_WIDTH 5 // temperature format specifier width
#define TEMP_FORMAT_PREC 2 // temperature format specifier precision

// file struct for printf redirection
static FILE uart = {0};

const int sensorPin = 14; // A0 = 14
const int peltierOut = 2; // D2 = 2

// Set aside some memory for averaging samples
const int N_SAMPLES = 100;
int sum;
float temperature;

// Controlling TIME
const int SAMPLE_FREQUENCY = 10; // ms
const int LOOP_DELAY = 500; // ms

// We want the algae to stay at a certain temperature
const float setpoint = 10.0; // °C

// variable to store temperature tolerance for implementing hysteresis
float setpoint_hysteresis = 0.5; // °C

// variable to track duration of peltier on and off-time
uint32_t peltier_duration = 0; // ms

static int uart_putchar (char c, FILE *stream)
{
    Serial.write(c) ;
    return 0 ;
}

void setup() {
  pinMode(peltierOut, OUTPUT);
  pinMode(sensorPin, INPUT);
  
  Serial.begin(9600);
  
  // set up stdout to uart for printf
  fdev_setup_stream(&uart, uart_putchar, NULL, _FDEV_SETUP_WRITE);
  stdout = &uart;
}

float readingToCelsius(float analogReading) {
  // Convert reading to mV -> 5000 millivolts / 1024 units = 4.882 per unit
  float millivolts = analogReading * 4.882;
  
  // The TMP36 reads 500 mV at 0°C and has an output scale factor of 10 mV/°C.
  // so [reading in mV - 500 / 10] = [reading in V * 100 - 50] = °C
  return (millivolts - 500) / 10.0;
}

void loop() {
  // Average many samples
  sum = 0;
  for (int n = 0; n < N_SAMPLES; n++) {
    sum += analogRead(sensorPin);
    delay(SAMPLE_FREQUENCY);
    peltier_duration += SAMPLE_FREQUENCY;
  }
  
  temperature = readingToCelsius((sum / N_SAMPLES));

  char temp_string[6];
  dtostrf(temperature, TEMP_FORMAT_WIDTH, TEMP_FORMAT_PREC, temp_string); // alternative function to properly format temperature strings

  printf("%s\n", temp_string);

  if (temperature > (setpoint + setpoint_hysteresis)) {
    if (digitalRead(peltierOut) == HIGH) {
      digitalWrite(peltierOut, LOW);
      printf("Peltiers ON: off for %d milliseconds\n", peltier_duration);
      peltier_duration = 0;
    }
  }
  else if (temperature < (setpoint - setpoint_hysteresis)) {
    if (digitalRead(peltierOut) == LOW) {
      digitalWrite(peltierOut, HIGH);
      printf("Peltiers OFF: on for %d milliseconds\n", peltier_duration);
      peltier_duration = 0;
    }
  }
  
  delay(LOOP_DELAY);
  peltier_duration += LOOP_DELAY;
}

