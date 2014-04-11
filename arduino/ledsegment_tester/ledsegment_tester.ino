#define NOE 9 //pwm
#define LE 8 //latch
#define CLK 10 //clock
#define SDO 11 //serial data
#define LED 13 //indicator led on arduino

byte segments[] = 
  {  
    0b11111100, //0
    0b01100000, //1
    0b11011010, //2
    0b11110010, //3
    0b01100110, //4
    0b10110110, //5
    0b00111110, //6
    0b11100000, //7
    0b11111110, //8
    0b11100110, //9
    0b00000001, //dot
  };
  
int seq_length;

//pwm settings  
int max_pwm = 255;
int min_pwm = 0;
int pwm_step = 10;
int fade_time = 5;



void setup()
{
  seq_length = sizeof(segments);
  Serial.begin(9600);
  Serial.println(seq_length);
  pinMode(LED,OUTPUT);
  pinMode(LE,OUTPUT);
  analogWrite(NOE,min_pwm);
  pinMode(CLK,OUTPUT);
  pinMode(SDO,OUTPUT);

  digitalWrite(LE,false);

}

void loop()
{
  for(int seq = 0; seq < seq_length; seq ++ )
  {
    digitalWrite(LED,true);
    
    //send the current segments
    for(int seg=0; seg< 8; seg ++)
    { 
      digitalWrite(CLK,false);
      delay(1);
      digitalWrite(SDO,segments[seq] & 1 << seg);
      digitalWrite(CLK,true);
      delay(1);
    }
    //fade in
    for(int p=min_pwm; p<max_pwm ; p+=pwm_step)
    {
      delay(fade_time);
      analogWrite(NOE,p);
      Serial.println(p);
    }

    //latch the shift register
    digitalWrite(LE,false);
    digitalWrite(LE,true);
    digitalWrite(LE,false);

    digitalWrite(LED,false);
    
    //wait till next sequence
    delay(100);

    //fade out
    for(int p=max_pwm; p>=min_pwm ; p-=pwm_step)
    {
      delay(fade_time);
      analogWrite(NOE,p);

    }
  }
}

