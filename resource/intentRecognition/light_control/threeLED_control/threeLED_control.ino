int LED1 = 2;
int LED2 = 3;
int LED3 = 4;

void setup() {
  // put your setup code here, to run once:
  pinMode(LED1, OUTPUT);
  pinMode(LED2, OUTPUT);
  pinMode(LED3, OUTPUT);
  digitalWrite(LED1, LOW);
  digitalWrite(LED2, LOW);
  digitalWrite(LED3, LOW);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  char data;
  if (Serial.available()){
    data = Serial.read();

    if(data == '1') {
      digitalWrite(LED1, LOW);
    }
    else if(data == '2') {
      digitalWrite(LED1, HIGH);
    }
    else if(data == '3') {
      digitalWrite(LED2, LOW);
    }
    else if(data == '4') {
      digitalWrite(LED2, HIGH);
    }
    else if(data == '5') {
      digitalWrite(LED3, LOW);
    }
    else if(data == '6') {
      digitalWrite(LED3, HIGH);
    }
  }
  delay(10);
}
