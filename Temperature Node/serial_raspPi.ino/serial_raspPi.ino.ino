#include <dht.h>


dht DHT;

#define DHT11_PIN A0
int greenLed = 2;
int redLed = 4;
#define fan 9
String command;
int fanSpeed;


void greenLightOn(){
  digitalWrite(greenLed, HIGH);
}
void greenLightOff(){
  digitalWrite(greenLed, LOW);
}
void redLightOn(){
  digitalWrite(redLed, HIGH);
}
void redLightOff(){
  digitalWrite(redLed, LOW);
}
void fanOn(){
  digitalWrite(fan, HIGH);
}
void fanOff(){
  digitalWrite(fan, LOW);
}


void setup(){
  Serial.begin(9600);
  pinMode(redLed, OUTPUT);
  pinMode(greenLed, OUTPUT);
  pinMode(fan, OUTPUT);
  pinMode(DHT11_PIN, INPUT);
}

void loop(){
  
  int chk = DHT.read11(DHT11_PIN);
  int t = DHT.temperature;
  int humidity = DHT.humidity;
  
  //Serial.print("Temperature = ");
  //Serial.print(t);
  String temp = String(t) + "," + String(humidity);
  Serial.println(temp);
  //Serial.print("\t");
  //Serial.print("Humidity = ");
  //Serial.print(humidity);
  //Serial.println("\t");
  delay(1000);


  if (Serial.available() > 0) {
    command = Serial.read();
    command.trim();
    
    if (command.equals("one")) {
      greenLightOn(); 
    }
    else if (command.equals("two")) {
      greenLightOff();      
    }
    else if (command.equals("three")) {
      redLightOn();     
    }
    else if (command.equals("four")) {
      redLightOff();      
    }
    else if (command.equals("five")) {
      fanOn();      
    }
    else if (command.equals("six")) {
      fanOff();      
    }
    else if (command.equals("low")) {
      //Fan Speed: 40%
      analogWrite(fan, 102);
    }
    else if (command.equals("medium")) {
      //Fan Speed: 60%
      analogWrite(fan, 153);
    }
    else if (command.equals("high")) {
      //Fan Speed: 100%
      analogWrite(fan, 255);
    }
    
  }    
}
