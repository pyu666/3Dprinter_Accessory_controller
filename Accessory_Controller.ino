// including servo
#include <Servo.h>
Servo myservo;

void setup() {
  // put your setup code here, to run once:
  // setup serial and servo
  Serial.begin(9600);
  myservo.attach(9);
  //setup LED port
  pinMode(8,OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  String data = Serial.readStringUntil("\n");
  if (data.equals("f")) {
    ledOff();
  } else if (data.equals("n")) {
    ledOn();
  } else if (data.equals("m")) {
    servo();
  }else {
    
  }
}
void ledOff() {
  digitalWrite(8,LOW);
}
void ledOn() {
  digitalWrite(8,HIGH);
}
void servo() {
  myservo.write(30);
  delay(500);
}
