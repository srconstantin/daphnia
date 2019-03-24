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
const int sensorPin = 14; // A0 = 14
const int peltierOut = 2; // D2 = 2

// Set aside some memory for averaging samples
const int N_SAMPLES = 100;
float sum;
float temperature;

// Controlling TIME
const int SAMPLE_FREQUENCY = 10; // ms
const int LOOP_DELAY = 500; // ms

// We want the algae to stay at a certain temperature
const float setpoint = 10.0; // °C

void setup() {
  pinMode(peltierOut, OUTPUT);
  pinMode(sensorPin, INPUT);
  Serial.begin(9600);
}

float readingToCelcius(float analogReading) {
  // Convert reading to V -> 5 volts / 1024 units = 0.0049 volts (4.9 mV) per unit
  float volts = analogReading * 0.0049;
  
  // The TMP36 reads 0.5 V at 0°C and has an output scale factor of 10 mV/°C.
  // so [reading in mV - 500 / 10] = [reading in V * 100 - 50] = °C
  return volts * 100 - 50;
}

void loop() {
  // Average many samples
  sum = 0;
  for (int n = 0; n < N_SAMPLES; n++) {
    sum += readingToCelcius(analogRead(sensorPin));
    delay(SAMPLE_FREQUENCY);
  }
  temperature = sum / N_SAMPLES;

  Serial.print(temperature);
  Serial.print("\n");

  if (temperature > setpoint) {
    digitalWrite(peltierOut, LOW);
    Serial.print("turn on the peltiers\n");
  }
  else {
    digitalWrite(peltierOut, HIGH);
    Serial.print("turn off the peltiers\n");
  }
  delay(LOOP_DELAY);
}

