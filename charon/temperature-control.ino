
// IOREF
// RESET
// 3.3V
// 5V
// GND
// GND
// VIN

// A0 = 14
// A1 = 15
// A2 = 16
// A3 = 17
// A4 = 18
// A5 = 19



// SCL = 19
// SDA = 18
// AREF
// GND
// D13 = 13
// D [whatever] = [whatever]


const int sensorRead = 14;
const int peltierOut = 2;
const float upperTempLimit = 10.0;

void setup() {
  pinMode(peltierOut, OUTPUT);
  pinMode(sensorRead, INPUT);
  Serial.begin(9600);
}

void loop() {
  int samples = 100;
  float celsia[samples];
  for (int n = 0; n < samples; n++) {
    int readPin = analogRead(sensorRead);
    float readPinVolts = readPin / 205.0;
    celsia[n] = 100.0 * readPinVolts - 50;
    delay(10);
  }
  float sum = 0;
  for (int n = 0; n < samples; n++) {
    sum = sum + celsia[n];
  }
  float average = sum / samples;  
  Serial.print(average);
  Serial.print("\n");
  if (average > upperTempLimit) {
   digitalWrite(peltierOut, HIGH);
   Serial.print("high");
  }
  else {
    digitalWrite(peltierOut, LOW);
    Serial.print("low");
  }
  
}

