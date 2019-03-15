#include <vexMotor.h> // includes the vexMotor library - uses Servo.h
vexMotor myVexMotor1;  // creates an instance of the vexMotor class
int error  = 0;
float kp = 0.8;
int target;
int power;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(A0,INPUT);
  myVexMotor1.attach(9);
}

void loop() {
  // put your main code here, to run repeatedly:
  while(true){
   target  = 150;
   error = target - analogRead(A0);
   while(abs(error)>30){
    error = target - analogRead(A0);
    Serial.print(analogRead(A0));
    Serial.print(',');
    Serial.print(error);
    power  = error*kp; 
    if(abs(power)>255)
      power = power/abs(power)*255;
    Serial.print(',');
    Serial.println(power);
    myVexMotor1.write(power);
   }
   delay(100);
   target = 250;
   error = target - analogRead(A0);
   while(abs(error)>30){
    error = target - analogRead(A0);
    Serial.print(analogRead(A0));
    Serial.print(',');
    Serial.print(error);
    power  = error*kp; 
    if(abs(power)>255)
      power = power/abs(power)*255;
    Serial.print(',');
    Serial.println(power);
    myVexMotor1.write(power);
   }
   //delay(1500);
  }
}
