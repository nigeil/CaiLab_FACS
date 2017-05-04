struct byteint{
  char b[sizeof(int)];
  u_int i;
};

struct bytefloat{
  char b[sizeof(float)];
  float f;
};

int bytes_to_int(char* the_bytes){
  return (the_bytes[3] << 24) | (the_bytes[2] << 16) | (the_bytes[1] << 8) | (the_bytes[0]);
};

void int_to_bytes(int the_int, u_char* byte_buffer){
  for (u_int i = 0; i < sizeof(int); i++) {
    byte_buffer[3 - i] = u_char(the_int >> (i * 8));
  }
};




void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  u_long t1;
  byteint value;
  u_int true_value = 12345678;
  float true_float = 3.574;
  u_char ret_bytes[sizeof(int)];
  
  if(Serial.available() > 0) {
    t1 = micros();
    if (1) {
      Serial.readBytes(value.b, sizeof(int));
      Serial.readBytes(float_val, sizeof(float));
      value.i = bytes_to_int(value.b);
      int_to_bytes(value.i, ret_bytes);
      Serial.write(ret_bytes, sizeof(int));
      Serial.print(value.i);
      Serial.print(" ");
      for(u_int i = 0; i<sizeof(int); i++){
        Serial.print(value.b[i]);
        Serial.print(" ");
      }
      if (value.i == true_value) {
        Serial.println(" Value matches true value.");
        Serial.println(micros() - t1);
      } 
      else {
        Serial.println(" Value does not match true value. Difference: ");
        Serial.print(value.i - true_value);
        Serial.print("Time: ");
        Serial.println(micros() - t1);
      }
    }
  }

}
