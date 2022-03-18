#define TRIG 6
#define ECHO 5

void setup() {
  Serial.begin(115200);
  pinMode(TRIG, OUTPUT);

  pinMode(ECHO, INPUT);

  pinMode(4, OUTPUT);       // Motor A 방향설정1

  pinMode(8, OUTPUT);       // Motor A 방향설정2
}

float Iterm = 0;
float prev_error;
float error;


void loop() {
  float duration, distance, ref, Pterm, Dterm, Kp, Ki, Kd, derror, error;

  

  digitalWrite(TRIG, LOW);

  delayMicroseconds(2);

  digitalWrite(TRIG, HIGH);

  delayMicroseconds(10);

  digitalWrite(TRIG, LOW);



  duration = pulseIn (ECHO, HIGH); 


  distance = duration * 17 / 1000; 



  Serial.print("\nDIstance : ");

  Serial.println(distance, 5); 

  Serial.println(" Cm");
  ref = 12;
  Kp = 20;
  Ki = 0.000;
  Kd = 0;
  error = ref-distance;
  Pterm = Kp*(error);
  Iterm += Ki*(error);
  derror = error-prev_error;
  prev_error = error;
  Dterm = Kd*derror;

  
  if (distance > ref+0.5) {
    digitalWrite(4, HIGH);     // Motor A 방향설정1

    digitalWrite(8, LOW);      // Motor A 방향설정2
    analogWrite(9, 255);       // Motor A 속도조절 (0~255)
  }

  else if (distance < ref-0.5) {
    digitalWrite(4, LOW);      // Motor A 방향설정1

    digitalWrite(8, HIGH);     // Motor A 방향설정2
    analogWrite(9, 255);       // Motor A 속도조절 (0~255)
  }

  else {
    
    analogWrite(9, abs(Pterm+Iterm+Dterm));       // Motor A 속도조절 (0~255)
  }

}
