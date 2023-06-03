// Constants used to set pin numbers.
const int ledPin = 2;     // number of the LED pin
const int transPin = A0;    // number of the phototransistor pin

bool manualMode = false;

int lightRead() {
  int transRead = analogRead(transPin);   // read value of phototransistor
  Serial.println(transRead);              // print value of phototransistor
  delay(1000);
  return transRead;
}

void setup() {
  // put your setup code here, to run once:
  pinMode (transPin, INPUT);    // initialise ldr pin as input
  pinMode (ledPin, OUTPUT);   // initialise led pin as output

  digitalWrite(ledPin, LOW);   // set initial LED state
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  int transRead = lightRead();

  // if the light is being controlled by the sensor's input
  if (!manualMode)
  {
    if (transRead < 6)
    {
      digitalWrite(ledPin, HIGH);
    }
    else
    {
      digitalWrite(ledPin, LOW);
    }
  }

  //Check if there is serial input data available
  if (Serial.available() > 0)
  {
    //Read serial input
    int value = Serial.read();
    if (value == '1')
    {
      manualMode = true;
    }
    else if (value == '2')
    {
      manualMode = false;
    }
    // if the light is being controlled by user input
    if (manualMode)
    {
      if (value == '3')
      {
        digitalWrite(2, HIGH);
      }
      else if (value == '4')
      {
        digitalWrite(2, LOW);
      }
    }
  }
}
