//-----L298N-----
#define enA 11
#define in1 8
#define in2 9
#define in3 12
#define in4 13
#define enB 10
#define en1A 3
#define in1_1 2
#define in1_2 4
bool flag = false;

unsigned long forwardDurationStartTime = 0;
bool lastForward = false;
char lastCommand = '0';

void DongCo() {
  analogWrite(en1A, 50);
  digitalWrite(in1_1, HIGH);
  digitalWrite(in1_2, LOW);
}

void Forward() {
  analogWrite(enA, 90);
  analogWrite(enB, 90);
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW);
}
void Back() {
  analogWrite(enA, 90);
  analogWrite(enB, 90);
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);
}

void Left() {
  analogWrite(enA, 240);
  analogWrite(enB, 240);
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW);
}

void Right() {
  analogWrite(enA, 240);
  analogWrite(enB, 240);
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);
}

void Stop() {
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);
}

void setup() {
  Serial.begin(9600);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
  pinMode(enA, OUTPUT);
  pinMode(enB, OUTPUT);
  pinMode(en1A, OUTPUT);
  pinMode(in1_1, OUTPUT);
  pinMode(in1_2, OUTPUT);
  DongCo();
  countTime = millis();
}

void loop()
{  
  unsigned long currentMillis = millis();
  if (Serial.available() > 0) // 
  {         
    char receivedChar = Serial.read();  
    Serial.println(receivedChar);
    if(receivedChar == 'A') 
    {
      flag = false;
    }
    else if(receivedChar == 'M') 
    {
      flag = true;
    }
    if(!flag) //
    {
      if(receivedChar == '1' || receivedChar == '2' ) 
      {
        if(lastForward) 
        {
          if (currentMillis - forwardDurationStartTime >= 800 || forwardDurationStartTime == 0) // 
          {
            forwardDurationStartTime = millis();
            Forward();
            lastForward = false;
          }
        } 
        else
        {
          forwardDurationStartTime = millis();
          Left();
        }
      } 
      else if (receivedChar == '4' || receivedChar == '3' || receivedChar == '5') // 
      {
        Forward();
        lastForward = true;
      } 
      else if (receivedChar == '6' || receivedChar == '7'|| receivedChar == '0') // KT điều kiện rẻ phải
      {
        if (lastForward) 
        {
          if (currentMillis - forwardDurationStartTime >= 800 || forwardDurationStartTime == 0) 
          {
            forwardDurationStartTime = millis();
            Forward();
            lastForward = false;
          }
        }
        else // 
        {
          forwardDurationStartTime = millis();
          Right();
        }
      }
    }

    else if(flag) 
    {
      if(receivedChar == 'F') 
      {
        Forward();
      }
      else if(receivedChar == 'L') 
      {
        Left();
      }
      else if(receivedChar == 'B') 
      {
        Back();
      }
      else if(receivedChar == 'R') 
      {
        Right();
      }
      else if(receivedChar == 'S')
      {
        Stop();
      }
    }
  }
}
