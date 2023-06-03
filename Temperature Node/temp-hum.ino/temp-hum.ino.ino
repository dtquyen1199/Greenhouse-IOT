#include <dht.h>


dht DHT;

//Define analog and digital pins
#define DHT11_PIN A0
int greenLed = 2;
int redLed = 4;
int fan = 9;
String command;

//Set methods to control pin status. 
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
  //Set baud rate to at 9600 to set serial communication
  Serial.begin(9600);
  //Initialize pins mode
  pinMode(redLed, OUTPUT);
  pinMode(greenLed, OUTPUT);
  pinMode(fan, OUTPUT);
  pinMode(DHT11_PIN, INPUT);
}

void loop(){
  //Read temperature and Humidity values from DHT library
  int chk = DHT.read11(DHT11_PIN);
  int temperature = DHT.temperature;
  int humidity = DHT.humidity;

  //print temperature and humidity to the terminal
 //erial.print("Temperature ");
  Serial.print(temperature);
  //tab key to separate data printed
  Serial.print("\t");
 //erial.print("Humidity ");
  Serial.print(humidity);
  Serial.println("\t");
  delay(1000);

  //set 1st threshold between 20C - 22C green LED on
  if(temperature >= 20 && temperature <= 22 ){
    greenLightOn();
    redLightOff();
    fanOn(); 
  }
  //set 2st threshold between 22C - 24C green LED off - Red LED on
  else if(temperature > 22 && temperature <= 24){
    greenLightOff();
    fanOff();    
    redLightOn();    
  }
  //set 3st threshold greater than 24C green LED off - Red LED on - Fan on
  else if(temperature > 24){
    redLightOn();
    fanOn();    
    greenLightOff();   
    
  }
  //Temperatura levels normal
  else{
    greenLightOff(); 
    redLightOff();
    fanOff();   
  }

  
}
