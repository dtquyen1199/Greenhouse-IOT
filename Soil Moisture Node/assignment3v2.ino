
int echoPin = 4;
int trigPin = 2;
int redLightPin= 11;
int greenLightPin = 9;
int blueLightPin = 10;
int moistureTrigerPoint = 200;
int waterPin = 3;
bool automatic = true;
bool needWatering = false;
int pumpState = 0;

int red = 0;
int blue = 0;
int green = 0;

unsigned long measuringInterval = 5000; 
unsigned long previousTime = 0;
unsigned long currentTime = 0;

float duration, distanceCm;
String string1;

void setup() {
  Serial.begin(9600);
  pinMode(trigPin,OUTPUT);
  pinMode(echoPin,INPUT);
  pinMode(redLightPin, OUTPUT);
  pinMode(greenLightPin, OUTPUT);
  pinMode(blueLightPin, OUTPUT);
  pinMode(waterPin,OUTPUT);
  RGB_color(255, 0, 0);
  digitalWrite(waterPin,HIGH);  
}

void loop() {
  currentTime = millis();
  RGB_color(red,green,blue);
  if ((currentTime - previousTime) >= measuringInterval) {
    readSensors();
    previousTime = currentTime;
  }

  if (digitalRead(waterPin) == HIGH){
  }
  
  if (Serial.available()>0)
   {
      int value = Serial.read();
      switch (value){
        case '1': //Red light
          red = 255;
          blue = 0;
          green = 0;
          break;
        case '2': //Yellow light
          red = 255;
          blue = 0;
          green  = 255;
          break;
        case '3': // Green light 
          red = 0;
          blue = 0;
          green = 255;
          break;
        case '4':
          moistureTrigerPoint = 200;
          break;
        case '5':
          moistureTrigerPoint = 400;
          break;
        case '6':
          moistureTrigerPoint = 600;
          break;
        case '7':
          automatic = !automatic;
          if (pumpState == 0){
            digitalWrite(waterPin, HIGH);
          }
          else if (pumpState == 1){
            digitalWrite(waterPin,LOW);
          }
          break; 
      }          
   }

   if (automatic == true && needWatering == true){
      digitalWrite(waterPin,HIGH);
   }
   else if(automatic == true && needWatering == false) {
      digitalWrite(waterPin,LOW);
   }
}


void readSensors(){
  int moistureSensorVal = analogRead(A0);
  if (moistureSensorVal < moistureTrigerPoint){
    needWatering = true;
  }
  
  if (moistureSensorVal >= moistureTrigerPoint){
    needWatering = false;
  }
  
  pumpState = digitalRead(waterPin);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin,LOW);
  
  duration = pulseIn(echoPin, HIGH);
  distanceCm = 0.017 * duration;
  string1 = String(moistureSensorVal)+"," + String(distanceCm)+"," + pumpState;
  Serial.println(string1);
}

void RGB_color(int redLightValue, int greenLightValue, int blueLightValue)
 {
  analogWrite(redLightPin, redLightValue);
  analogWrite(greenLightPin, greenLightValue);
  analogWrite(blueLightPin, blueLightValue);
}
