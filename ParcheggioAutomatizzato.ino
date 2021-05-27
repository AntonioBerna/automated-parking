#include <LiquidCrystal.h>
#include <Servo.h>

// Corrispondenza pin LCD con i pin digitali di Arduino UNO
#define REGISTER_SELECT 8
#define ENABLE 9
#define DATA_PIN_7 38
#define DATA_PIN_6 36
#define DATA_PIN_5 34
#define DATA_PIN_4 32

// Variabili per il LED Multicolore RGB
#define RED 22
#define GREEN 23

// Variabili per i sensori ad ultrasuoni HC-SR04
#define TRIGGER_PIN_INPUT 10
#define ECHO_PIN_INPUT 11
#define TRIGGER_PIN_OUTPUT 12
#define ECHO_PIN_OUTPUT 13

// Variabili per i servo motori
#define SERVO_IN_PIN 3
#define SERVO_OUT_PIN 6
int pos_in_min;
int pos_in_max;
int pos_out_min;
int pos_out_max;

int current_in_pos;
int current_out_pos;

Servo servo_in;
Servo servo_out;

int seats = 5; // Posti totali del parcheggio
int range_input = 4;
int range_output = 5;
bool old_input = false;
bool old_output = false;

LiquidCrystal lcd(REGISTER_SELECT, ENABLE, DATA_PIN_4, DATA_PIN_5, DATA_PIN_6, DATA_PIN_7);

void setup() {
  pinMode(RED, OUTPUT);
  pinMode(GREEN, OUTPUT);

  pinMode(TRIGGER_PIN_INPUT, OUTPUT);
  pinMode(ECHO_PIN_INPUT, INPUT);
  pinMode(TRIGGER_PIN_OUTPUT, OUTPUT);
  pinMode(ECHO_PIN_OUTPUT, INPUT);

  digitalWrite(TRIGGER_PIN_INPUT, LOW);
  digitalWrite(TRIGGER_PIN_OUTPUT, LOW);

  lcd.begin(16, 2); // Impostazioni display LCD (colonne, righe)
  servo_in.attach(SERVO_IN_PIN);
  servo_out.attach(SERVO_OUT_PIN);

  pos_in_min = servo_in.read() + 90;
  pos_in_max = servo_in.read();
  current_in_pos = pos_in_max;

  pos_out_min = servo_out.read() + 90;
  pos_out_max = servo_out.read();
  current_out_pos = pos_out_max;

  Serial.begin(9600);
}

void loop() {
  digitalWrite(TRIGGER_PIN_INPUT, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIGGER_PIN_INPUT, LOW);

  unsigned long input_time = pulseIn(ECHO_PIN_INPUT, HIGH);
  float input_distance = 0.03438 * input_time / 2;

  digitalWrite(TRIGGER_PIN_OUTPUT, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIGGER_PIN_OUTPUT, LOW);

  unsigned long output_time = pulseIn(ECHO_PIN_OUTPUT, HIGH);
  float output_distance = 0.03438 * output_time / 2;

  // Serial.println("input_distance: " + String(input_distance) + "\n" + "output_distance: " + String(output_distance));

  bool input = input_distance < range_input;
  bool output = output_distance < range_output;

  if (input == true && old_input == false) {
    if (seats > 0) {
      seats--;
      while (current_in_pos < pos_in_min) {
        current_in_pos++;
        servo_in.write(current_in_pos);
        delay(10);
      }
    }
  } else if (input == false && old_input == true) {
    while (current_in_pos > pos_in_max) {
      current_in_pos--;
      servo_in.write(current_in_pos);
      delay(10);
    }
  } else if (output == true && old_output == false) {
    if (seats < 5) {
      seats++;
      while (current_out_pos < pos_out_min) {
        current_out_pos++;
        servo_out.write(current_out_pos);
        delay(10);
      }
    }
  } else if (output == false && old_output == true) {
    while (current_out_pos > pos_out_max) {
      current_out_pos--;
      servo_out.write(current_out_pos);
      delay(10);
    }
  }
  old_input = input;
  old_output = output;

  if (seats > 0) {
    digitalWrite(GREEN, HIGH);
    digitalWrite(RED, LOW);
  } else {
    digitalWrite(GREEN, LOW);
    digitalWrite(RED, HIGH);
  }
  
  Serial.println(seats);
  
  lcd.clear(); // Pulisce lo schermo
  lcd.setCursor(0, 0); // Va in posizione: colonna 1, riga 1
  lcd.print("Posti");
  lcd.setCursor(0, 1); // Va in posizione: colonna 1, riga 2
  lcd.print("Liberi: " + String(seats));

  delay(500);
}
