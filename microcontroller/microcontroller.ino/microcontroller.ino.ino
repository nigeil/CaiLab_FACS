
// Microcontroller code for cell sorting.
// Works alongside the main (python/kivy) application.
// Designed for Teensy 3.6: https://www.pjrc.com/store/teensy36.html 





// ----- Included libraries ----- //

// fast, configurable ADC using https://github.com/pedvide/ADC
#include <ADC_Module.h>
#include <RingBufferDMA.h>
#include <ADC.h>
#include <RingBuffer.h>

// limits library, to calculate max values of various types
#include <limits>






// ----- Definitions ----- //

// analog pins for reading fluorescent voltage signals
#define REDPIN    A0
#define GREENPIN  A1
#define BLUEPIN   A2
#define YELLOWPIN A3

// digital pin for triggering electrode (droplet selection)
#define ELECTRODEPIN 2
#define ELECTRODE_ON_TIME 100 // in us

// digital pin for LED status light (HIGH if runstate == 1, running)
#define LEDSTATUSPIN 0

// analog settings
#define AREF ADC_REFERENCE::REF_3V3                        // reference voltage setting, 1.2V for low voltages
#define AREF_VAL 3.3                                       // for calculations, set to voltage of above
#define ASAMPSPEED ADC_SAMPLING_SPEED::VERY_HIGH_SPEED     // sampling speed; can set it high for low-impedence signals
#define ACONVSPEED ADC_CONVERSION_SPEED::VERY_HIGH_SPEED     // conversion speed; upclocks the ADC freq at accuracy cost
#define ARES adc->getMaxValue(ADC_0)                       // analog resolution, set to be the same for both ADCs0&1

// Division factor for converting integer voltages to floats
// i.e. INPUT: [0, max(int)] -> OUTPUT: [0/float_div_factor, max(int)/float_div_factor]
#define VOLTAGE_DIV_FACTOR 1000 // gives 3 decimal places


// ----- Helper type definitions ----- //

//for converting short ints (cell counts) to bytes for transmission
struct byteint{
  char b[sizeof(int)];
  u_int i;
};





// ----- Helper functions ----- //


// CONVERSIONS

// Converting from bytes to a 4 byte intger
int bytes_to_int(char* the_bytes){
  return u_int(the_bytes[3] << 24) | (the_bytes[2] << 16) | (the_bytes[1] << 8) | (the_bytes[0]);
};

// Converting from a 4 byte integer to a string of bytes
// Can't return an array, so must pass it as a parameter and modify in-function
void int_to_bytes(int the_int, char* byte_buffer){
  for (u_int i = 0; i < sizeof(int); i++) {
    byte_buffer[3 - i] = char(the_int >> (i * 8));
    //byte_buffer[i] = char(the_int >> (i * 8));
  }
};

// Reverses a byte array in-place, size given by count
void reverse(char* arr, int count)
{
   int temp;
   for (int i = 0; i < count/2; ++i)
   {
      temp = arr[i];
      arr[i] = arr[count-i-1];
      arr[count-i-1] = temp;
   }
}


// SETTERS

// call when new threshold values have been recieved (as bytes) from the computer
void set_threshold_voltages(byteint* thresh_voltages, byteint* new_thresh_voltages){
  for(int i=0; i<4; i++){
    new_thresh_voltages[i].i = bytes_to_int(new_thresh_voltages[i].b);
    thresh_voltages[i].i = new_thresh_voltages[i].i;
    for(u_int j=0; j<sizeof(int); j++){
      thresh_voltages[i].b[j] = new_thresh_voltages[i].b[j];
    }
  }
  return;
}


// call when new cell counts have been recieved (as bytes) from the computer
void set_cell_selection_counts(byteint* max_cell_counts, byteint* new_cell_max_counts){
  for(u_int i=0; i<4; i++){
    new_cell_max_counts[i].i = bytes_to_int(new_cell_max_counts[i].b);
    max_cell_counts[i].i = new_cell_max_counts[i].i;
    for(u_int j=0; j<sizeof(int); j++){
      max_cell_counts[i].b[j] = new_cell_max_counts[i].b[j];
    }
  }
  return;
}


// call when new PMT logic states have been recieved (as bytes) from the computer
void set_logic_states(byteint* logic_states, byteint* new_logic_states){
  for (u_int i=0; i<4; i++){
    new_logic_states[i].i = bytes_to_int(new_logic_states[i].b);
    logic_states[i].i = new_logic_states[i].i;
    for (u_int j=0; j<sizeof(int); j++){
      logic_states[i].b[j] = new_logic_states[i].b[j];
    }
  }
  return;
}

// MEASUREMENT

// read from 4 analog pins and convert to voltages
void measure_voltages(ADC* adc, byteint* voltages){
  voltages[0].i = (adc->analogRead(REDPIN))    * (AREF_VAL / ARES) * VOLTAGE_DIV_FACTOR;
  voltages[1].i = (adc->analogRead(GREENPIN))  * (AREF_VAL / ARES) * VOLTAGE_DIV_FACTOR;
  voltages[2].i = (adc->analogRead(BLUEPIN))   * (AREF_VAL / ARES) * VOLTAGE_DIV_FACTOR;
  voltages[3].i = (adc->analogRead(YELLOWPIN)) * (AREF_VAL / ARES) * VOLTAGE_DIV_FACTOR;
  //voltages[0].i = 0;
  //voltages[2].i = 0;
  //voltages[3].i = 0;
  return;
}


// SENDERS

// send the measured voltages back to the computer
void send_voltages(byteint* voltages){
  u_char send_buffer[1 + 4 * sizeof(int)];
  
  // send data ID to computer
  send_buffer[0] = 1;

  // send voltages as 4-byte ints
  u_int index = 1;
  for(int i=0; i<4; i++){
    int_to_bytes(voltages[i].i, voltages[i].b);
    for(u_int j=0; j<sizeof(int); j++){
      send_buffer[index] = voltages[i].b[j];
      //send_buffer[index] = char(1);
      index = index + 1;
    }
  }
  
  Serial.write(send_buffer, 1 + 4*sizeof(int));  
  return;
}


void send_min_thresh_voltages(byteint* voltages){
  u_char send_buffer[1 + 4 * sizeof(int)];
  
  // send data ID to computer
  send_buffer[0] = 4;

  // send voltages as 4-byte ints
  u_int index = 1;
  for(int i=0; i<4; i++){
    int_to_bytes(voltages[i].i, voltages[i].b);
    for(u_int j=0; j<sizeof(int); j++){
      send_buffer[index] = voltages[i].b[j];
      //send_buffer[index] = char(1);
      index = index + 1;
    }
  }
  
  Serial.write(send_buffer, 1 + 4*sizeof(int));  
  return;
}

void send_max_thresh_voltages(byteint* voltages){
  u_char send_buffer[1 + 4 * sizeof(int)];
  
  // send data ID to computer
  send_buffer[0] = 6;

  // send voltages as 4-byte ints
  u_int index = 1;
  for(int i=0; i<4; i++){
    int_to_bytes(voltages[i].i, voltages[i].b);
    for(u_int j=0; j<sizeof(int); j++){
      send_buffer[index] = voltages[i].b[j];
      //send_buffer[index] = char(1);
      index = index + 1;
    }
  }
  
  Serial.write(send_buffer, 1 + 4*sizeof(int));  
  return;
}

// send the number of sorted cells back to the computer
void send_cell_counts(byteint* cell_counts){
  byte send_buffer[1 + (4 * sizeof(int))];
    
  // send data ID to computer
  send_buffer[0] = 2; //identifier byte

  // send cell counts as 4-byte ints
  u_int index = 1;
  for(u_int i=0; i<4; i++){    
    int_to_bytes(cell_counts[i].i, cell_counts[i].b);
    for(u_int j=0; j<sizeof(int); j++){
      send_buffer[index] = cell_counts[i].b[j];
      //send_buffer[index] = char(1);
      index = index + 1;
    }
  }
  
  Serial.write(send_buffer, 1 + (4 * sizeof(int)));
  return;
}

// send the number of sorted cells back to the computer
void send_max_cell_counts(byteint* cell_counts){
  byte send_buffer[1 + (4 * sizeof(int))];
    
  // send data ID to computer
  send_buffer[0] = 5; //identifier byte

  // send cell counts as 4-byte ints
  u_int index = 1;
  for(u_int i=0; i<4; i++){    
    int_to_bytes(cell_counts[i].i, cell_counts[i].b);
    for(u_int j=0; j<sizeof(int); j++){
      send_buffer[index] = cell_counts[i].b[j];
      //send_buffer[index] = char(1);
      index = index + 1;
    }
  }
  
  Serial.write(send_buffer, 1 + (4 * sizeof(int)));
  return;
}


// send time to complete last loop
void send_loop_time(byteint loop_time){
  byte send_buffer[1 + (4 * sizeof(int))];
    
  // send data ID to computer
  send_buffer[0] = 3; //identifier byte

  // send cell counts as 4-byte ints
  u_int index = 1;
  for(u_int j=0; j<sizeof(int); j++){
    send_buffer[index] = loop_time.b[j];
    index = index + 1;
  }
  
  Serial.write(send_buffer, 1 + (1 * sizeof(int)));
  return;
}


// send the current PMT logic states back to the computer
void send_logic_states(byteint* logic_states){
  byte send_buffer[1 + (4 * sizeof(int))];
    
  // send data ID to computer
  send_buffer[0] = 7; //identifier byte

  // send logic states as 4-byte ints
  u_int index = 1;
  for(u_int i=0; i<4; i++){    
    int_to_bytes(logic_states[i].i, logic_states[i].b);
    for(u_int j=0; j<sizeof(int); j++){
      send_buffer[index] = logic_states[i].b[j];
      index = index + 1;
    }
  }
  
  Serial.write(send_buffer, 1 + (4 * sizeof(int)));
  return;
}




// ----- Global variables ----- //
u_int pins[4] = {REDPIN,GREENPIN,BLUEPIN,YELLOWPIN};   // analog reading pins

byteint current_voltage[4];                            // {r,g,b,y}
byteint min_threshold_voltage[4];                      // {r,g,b,y}; select cell if max_threshold_voltage[i] >= current_voltage[i] >= min_threshold_voltage[i].
byteint max_threshold_voltage[4];                      // {r,g,b,y}
byteint logic_states[4];                               // {r,g,b,y}; 0->ignore PMT, 1->logical inclusive OR, 2->logical AND, 3->logical NOT

u_int time_in_state[4] = {0,0,0,0};                    // time that current_voltage[i] > threshold_voltage[i] 
u_int time_out_of_state[4] = {0,0,0,0};                // time that current_voltage[i] < threshold_voltage[i] AFTER it entered the state 
const u_int required_time = 10;                        // (10) us, time that time_in_state[i] must be greater than for selection 
const u_int allowance_time = 10;                       // (10) us, time that current_voltage[i] can be < threshold_voltage[i] 
                                                       // before resetting timer TODO: maybe remove this logic, we have signal averaging now
                                                     
byteint current_cell_count[4];                         // {r,g,b,y} in range [0, 65536]
byteint max_cell_count[4];                             // as above, but current_cell_count[i] <= max_cell_count[i];
                                                       // stop selecting cells of this color after maximum number are selected.
                                                     
ADC* adc;                                              // pointer to what will be the analog-to-digital converter object

byteint time0;                                          // start time
byteint time1;                                          // total time taken for 1 loop

u_int measurement_time;                                 // time taken to measure voltages; used in determining whether or not to select cell

byteint run_state;                                      // 0 if not running, 1 if running, 2 if paused (no reset when restarting)

byteint id;                                             // id for incoming serial communications; used to determine what's on the way




// ----- Setup the microcontroller ----- //
void setup() {
  // serial communication with computer
  Serial.begin(9600); // USB is always 12 Mbit/sec for Teensy, baud setting is required but ignored
  Serial.setTimeout(10);
  
  // analog to digital (ADC) setup
  adc = new ADC();
  adc->setReference(AREF, ADC_0);
  adc->setReference(AREF, ADC_1);
  adc->setSamplingSpeed(ASAMPSPEED);
  adc->setConversionSpeed(ACONVSPEED);
  adc->setAveraging(8
  );   // set number of averages
  adc->setResolution(16); // set bits of resolution

  //set electrode (digital) pin to output, analogs to input
  pinMode(ELECTRODEPIN, OUTPUT);
  pinMode(LEDSTATUSPIN, OUTPUT);
  pinMode(REDPIN, INPUT);
  pinMode(GREENPIN, INPUT);
  pinMode(BLUEPIN, INPUT);
  pinMode(YELLOWPIN, INPUT);

  for(u_int i=0; i<4; i++){
    current_voltage[i].i = 0;
    min_threshold_voltage[i].i = 3300;
    max_threshold_voltage[i].i = 3300;
    current_cell_count[i].i = 0;
    max_cell_count[i].i = std::numeric_limits<unsigned int>::max();
    logic_states[i].i = 0;
  }
  run_state.i = 0; // DEBUG: turn it on
}





// ----- Start the main loop ----- //
void loop() {
  time0.i = micros();
  id.i = 1000; // maps to nothing in the defined communication protocol
  
  // ---- Computer -> Microcontroller serial communications ---- //
  
  // if there is something at the serial line grab it, otherwise continue with cell selection
  if(Serial.available() > 0) {
      // check id code and act accordingly
      Serial.readBytes(id.b, sizeof(int));
      reverse(id.b, sizeof(int));
      id.i = bytes_to_int(id.b);


      // id == 0: incoming run state
      if (id.i == 0) {
        byteint old_run_state; 
        old_run_state.i = run_state.i;
        Serial.readBytes(run_state.b, sizeof(int));
        reverse(run_state.b, sizeof(int));
        run_state.i = bytes_to_int(run_state.b);

        // check for valid run states, set to safe value if not:
        // 0 -> off; 1 -> on; 2 -> paused (off, but don't reset when turned back on)
        if (!(run_state.i == 0 || run_state.i == 1 || run_state.i == 2)) {
          run_state.i = 0;
        }
        
        if (run_state.i == 1){
          digitalWrite(LEDSTATUSPIN, HIGH);
        } 
        else {
          digitalWrite(LEDSTATUSPIN, LOW);
        }
        
        // first time starting the microcontroller - zero everything out and start again (reset)
        if (old_run_state.i == 0 && run_state.i == 1){
          for(u_int i=0; i<4; i++){
            current_voltage[i].i = 0;
            min_threshold_voltage[i].i = 3300;
            max_threshold_voltage[i].i = 3300;
            current_cell_count[i].i = 0;
            max_cell_count[i].i = std::numeric_limits<unsigned int>::max();
          }
        }
      }

      
      // id == 1: incoming minimum threshold voltage settings
      else if(id.i == 1) {
        byteint new_threshold_voltage_buffer[4];
        for(int i=0; i<4; i++) {
          Serial.readBytes(new_threshold_voltage_buffer[i].b, sizeof(int));
          reverse(new_threshold_voltage_buffer[i].b, sizeof(int));
        }
        set_threshold_voltages(min_threshold_voltage, new_threshold_voltage_buffer);
      }


      // id == 2: incoming cell selection maxima
      else if(id.i == 2){
        byteint new_cell_count_maxima[4];
        for(u_int i=0; i<4; i++){
          Serial.readBytes(new_cell_count_maxima[i].b, sizeof(int));
          reverse(new_cell_count_maxima[i].b, sizeof(int));
        }
        set_cell_selection_counts(max_cell_count, new_cell_count_maxima);
      }

      // id == 3: incoming maximum threshold voltage settings
      else if(id.i == 3) {
        byteint new_threshold_voltage_buffer[4];
        for(int i=0; i<4; i++) {
          Serial.readBytes(new_threshold_voltage_buffer[i].b, sizeof(int));
          reverse(new_threshold_voltage_buffer[i].b, sizeof(int));
        }
        set_threshold_voltages(max_threshold_voltage, new_threshold_voltage_buffer);
      }

      // id.i == 4: incoming PMT logic states
      else if (id.i == 4){
        byteint new_logic_states[4];
        for(u_int i=0; i<4; i++){
          Serial.readBytes(new_logic_states[i].b, sizeof(int));
          reverse(new_logic_states[i].b, sizeof(int));
        }
        set_logic_states(logic_states, new_logic_states);
      }

      // id == 10: request for current voltages
      else if(id.i == 10) {
        // --- Send current voltages over serial to the host computer --- //
        send_voltages(current_voltage);
      }

      // id == 20: request for cell counts
      else if (id.i == 20) {
        // --- Send current cell counts over serial to the host computer --- //
        send_cell_counts(current_cell_count);
      }

      // id==30: request time of loop
      else if (id.i == 30){
        int_to_bytes(time1.i, time1.b);
        send_loop_time(time1);
      }

      // id==40: request current minimum threshold voltages
      else if (id.i == 40){
        send_min_thresh_voltages(min_threshold_voltage);
      }

      // id==50: request for current max cell counts
      else if (id.i == 50){
        send_max_cell_counts(max_cell_count);
      }
      
      // id==60: request current maximum threshold voltages
      else if (id.i == 60){
        send_max_thresh_voltages(max_threshold_voltage);
      }

      // id==70: request for current logic states
      else if (id.i == 70){
        send_logic_states(logic_states);
      }
  }


  // ---- Check run state ---- //
  // run_state == 0 means off, so go back to top of loop (return) and wait to turn on
  // run_state == 2 means PAUSED, so go back to top of loop and wait, but don't reset anything
  if (run_state.i == 0 || run_state.i == 2){
    return;
  }


  // ---- Cell selection ---- //
  
  // --- Detecting fluoresence on all 4 color channels --- //
  measure_voltages(adc, current_voltage);
  measurement_time = micros() - time0.i;

  // --- Calculating logical condition --- //
  bool should_we_capture_cell = false; // default to FALSE, possibly set to true after looking at all channels
  
  u_int n_nots = 0;
  u_int n_ors  = 0;
  u_int n_ands = 0;                   // number of each TRUE condition, across all channels

  bool stop_checking_ands = false;    // if one AND channel has no signal, don't check others
  
  bool positive_signals[4] = {false,false,false,false};  // stores which channels were positive for cell_count logging only
  for (u_int i=0; i<4; i++){
    positive_signals[i] = (current_voltage[i].i > min_threshold_voltage[i].i) && (current_voltage[i].i < max_threshold_voltage[i].i);
  }
  
  for (u_int i=0; i<4; i++){
    bool is_positive_signal = (positive_signals[i]);
    
    switch(logic_states[i].i) {
      
      // check for NOT conditions first
      case 3: {
        if(is_positive_signal){
          n_nots += 1;
          break;
        }
      }
      
      // check for OR (inclusive) conditions second:
      case 1: {
        if(is_positive_signal){
          n_ors += 1;
          break;
        }
      }

      // check for AND conditions last:
      case 2: {
        if (stop_checking_ands){
          break;
        }
        
        if(is_positive_signal){
          n_ands += 1;
        } 
        else {
          n_ands = 0;
          stop_checking_ands = true;
        }
      }
    }
  }

  if (n_nots == 0 && (n_ors > 0 || n_ands > 1)) { // need minimum of 2 TRUE conditions for AND to make sense
    should_we_capture_cell = true;
  }
  else {
    return; // no conditions met, don't select a cell, start over from the top of the main loop immediately
  }

  // --- Checking that we haven't hit ANY of the max cell counts on channels with positive signals --- //
  for (u_int i=0; i<4; i++){
    if (positive_signals[i] == true){
      if(current_cell_count[i].i >= max_cell_count[i].i){
         should_we_capture_cell = false; // positive signal on channel we are full of - don't pick cell
      }
    }
  }

  // --- Sending signal to to trigger selection electrode if required --- //
  if (should_we_capture_cell){
    digitalWrite(ELECTRODEPIN, HIGH);
    delayMicroseconds(ELECTRODE_ON_TIME);
    digitalWrite(ELECTRODEPIN, LOW);
    for (u_int i=0; i<4; i++){
      if(positive_signals[i] == true){
        current_cell_count[i].i += 1;
      }
    }
  }



/*  
  // --- Comparing voltages to thresholds and times in state (above min threshold voltage, below max) --- //
  for(u_int i=0; i<4; i++){
    if((current_voltage[i].i > min_threshold_voltage[i].i) && (current_voltage[i].i < max_threshold_voltage[i].i)){
      time_in_state[i] += measurement_time;
      time_out_of_state[i] = 0;
    } 
    else{
      time_out_of_state[i] += measurement_time;
      if(time_out_of_state[i] > allowance_time){
        time_in_state[i] = 0;
        time_out_of_state[i] = 0;
      }
    }
  }


  // --- Select cells based on time spent in state (above threshold voltage) --- // 
  // --- and number of cells to select of that color --- //
  for(u_int i=0; i<4; i++){
    if(time_in_state[i] > required_time){
      if(current_cell_count[i].i < max_cell_count[i].i){
        digitalWrite(ELECTRODEPIN, HIGH);
        delayMicroseconds(ELECTRODE_ON_TIME);
        digitalWrite(ELECTRODEPIN, LOW);
        current_cell_count[i].i += 1;
        // selected cell, so reset time-in-state counters
        for(u_int j=0; j<4; j++){
          time_in_state[j] = 0;
          time_out_of_state[j] = 0;
        }
      }
    }
  }
*/
  Serial.flush();
  time1.i = (micros() - time0.i);








  // debugging - timing of the main loop needs to be < ~25us for reliable detection
  // set if(false) for off, if(true) for on (WILL SLOW DOWN LOOP)
 
  if(false) {
  Serial.write(255);
  Serial.print(" ID");
  Serial.print(id.i);
  Serial.print(" TIME: ");
  Serial.print(time1.i);
  Serial.print(" RUNSTATE: ");
  Serial.print(run_state.i);
  Serial.print(" CURR_VOLTAGES: ");
  for(u_int i=0; i<4; i++){
    Serial.print(current_voltage[i].i);
    Serial.print(" ");
  }
  Serial.print(" THRESH_VOLTAGES: ");
  for(u_int i=0; i<4; i++){
    Serial.print(min_threshold_voltage[i].i);
    Serial.print(" ");
  }
  Serial.print(" CURR_CELL_COUNTS: ");
  for(u_int i=0; i<4; i++){
    Serial.print(current_cell_count[i].i);
    Serial.print(" ");
  }
  Serial.print(" MAX_CELL_COUNTS: ");
  for(u_int i=0; i<4; i++){
    Serial.print(max_cell_count[i].i);
    Serial.print(" ");
  } 
  Serial.print(" LOGIC_STATES: ");
  for(u_int i=0; i<4; i++){
    Serial.print(logic_states[i].i);
    Serial.print(" ");
  }
  Serial.print("\n"); 
  }

}
