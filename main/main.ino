int redPin = 9;    
int greenPin = 10; 
int bluePin = 11;  
int buzzerPin = 3; 
unsigned long buzzerStart = 0;
bool buzzerActive = false;
void setup() {
  Serial.begin(9600);
  pinMode(redPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  pinMode(bluePin, OUTPUT);
  pinMode(buzzerPin, OUTPUT);
}


void loop() {
  if (Serial.available()) {
    String data = Serial.readStringUntil('\n');
    int c1 = data.indexOf(',');
    int c2 = data.lastIndexOf(',');

    if (c1 > 0 && c2 > c1) {
      int R = data.substring(0, c1).toInt();
      int G = data.substring(c1 + 1, c2).toInt();
      int B = data.substring(c2 + 1).toInt();

      analogWrite(redPin, R);
      analogWrite(greenPin, G);
      analogWrite(bluePin, B);

      if (R == 0 && G == 0 && B == 0 && !buzzerActive) {
        tone(buzzerPin, 1000);
        buzzerStart = millis();
        buzzerActive = true;
      }
    }
  }

  // Stop buzzer after 500 ms
  if (buzzerActive && millis() - buzzerStart >= 500) {
    noTone(buzzerPin);
    buzzerActive = false;
  }
}
