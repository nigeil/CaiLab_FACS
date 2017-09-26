
// Microcontroller code for cell sorting.
// Works alongside the main (python/kivy) application.
// Designed for Teensy 3.6: https://www.pjrc.com/store/teensy36.html

// ----- Included libraries ----- //

// core arduino includes
#include <Arduino.h>

// fast, configurable ADC using https://github.com/pedvide/ADC
#include <ADC_Module.h>
#include <RingBufferDMA.h>
#include <ADC.h>
#include <RingBuffer.h>

// limits library, to calculate max values of various types
#include <limits>

// boost accumulator library, to calculate rolling mean/variance
//#include <boost/accumulators/accumulators.hpp>
//#include <boost/accumulators/statistics/stats.hpp>
//#include <boost/accumulators/statistics/rolling_mean.hpp>
//#include <boost/accumulators/statistics/rolling_variance.hpp>

// project includes
#include "helper_types.h"
#include "global_defines.h"
#include "helper_functions.h"
#include "communication_functions.h"
#include "setter_functions.h"
#include "measurement_functions.h"


// ----- Global variables ----- //
u_int pins[N_CHANNELS] = {REDPIN,GREENPIN,BLUEPIN,YELLOWPIN};   // analog reading pins

byteint current_voltage[N_CHANNELS];                            // {r,g,b,y}
byteint previous_voltage[N_CHANNELS];                           // from previous loop iteration
byteint max_voltage[N_CHANNELS];                                // after crossing minimum threshold, maximum voltage seen is stored here
//byteint running_mean_voltage[N_CHANNELS];                       // from accumulator
//byteint running_std_dev_voltage[N_CHANNELS];                    // from accumulator

//typedef boost::accumulators::accumulator_set<double,stats<tag::rolling_mean, tag::rolling_variance, tag::rolling_window::window_size = ROLLING_WINDOW_SIZE> > window_acc;
//window_acc data_accumulators[N_CHANNELS];                       // stores the accumulators


byteint min_threshold_voltage[N_CHANNELS];                      // {r,g,b,y}; select cell if max_threshold_voltage[i] >= current_voltage[i] >= min_threshold_voltage[i].
byteint max_threshold_voltage[N_CHANNELS];                      // {r,g,b,y}
byteint logic_states[N_CHANNELS];                               // {r,g,b,y}; 0->ignore PMT, 1->logical inclusive OR, 2->logical AND, 3->logical NOT

u_int time_in_state[N_CHANNELS];                                // time that current_voltage[i] > min_threshold_voltage[i]
bool turned_from_high_state_to_low[N_CHANNELS];

byteint current_cell_count[N_CHANNELS];                         // {r,g,b,y} in range [0, 65536]
byteint max_cell_count[N_CHANNELS];                             // as above, but current_cell_count[i] <= max_cell_count[i];
                                                                // stop selecting cells of this color after maximum number are selected.

ADC* adc;                                                       // pointer to the ADC controller object

byteint time0;                                          // start time
byteint time1;                                          // total time taken for 1 loop
byteint clock_time_before_measurement;                  // stores the clock time (micros()) just before measuring voltages

u_int measurement_time;                                 // time taken to measure voltages; used in determining whether or not to select cell

byteint run_state;                                      // 0 if not running, 1 if running, 2 if paused (no reset when restarting)

byteint id;                                             // id for incoming serial communications; used to determine what's on the way

const bool test_mode = false;                           // TRUE if testing (skip serial comms, print debug info)



// ----- Setup the microcontroller ----- //
void setup() {
  // serial communication with computer
  Serial.begin(9600); // USB is always 12 Mbit/sec for Teensy, baud setting is required but ignored
  Serial.setTimeout(10); //time in ms

  // analog to digital (ADC) setup
  adc = new ADC();
  adc->setReference(AREF, ADC_0);
  adc->setReference(AREF, ADC_1);
  adc->setSamplingSpeed(ASAMPSPEED, ADC_0);
  adc->setSamplingSpeed(ASAMPSPEED, ADC_1);
  adc->setConversionSpeed(ACONVSPEED, ADC_0);
  adc->setConversionSpeed(ACONVSPEED, ADC_1);
  adc->setAveraging(N_AVERAGES, ADC_0);
  adc->setAveraging(N_AVERAGES, ADC_1);
  adc->setResolution(ARES_BITS, ADC_0);
  adc->setResolution(ARES_BITS, ADC_1);

  //set electrode (digital) pin to output, analogs to input
  pinMode(ELECTRODEPIN, OUTPUT);
  pinMode(LEDSTATUSPIN, OUTPUT);
  pinMode(REDPIN, INPUT);
  pinMode(GREENPIN, INPUT);
  pinMode(BLUEPIN, INPUT);
  pinMode(YELLOWPIN, INPUT);

  for(u_int i=0; i<N_CHANNELS; i++){
    current_voltage[i].i = 0;
    previous_voltage[i].i = 0;
    max_voltage[i].i = 0;
    //running_mean_voltage[i].i = 0;
    //running_std_dev_voltage[i].i = 0;
    //data_accumulators[i] = window_acc();
    min_threshold_voltage[i].i = AMAX_VAL;
    max_threshold_voltage[i].i = AMAX_VAL;
    current_cell_count[i].i = 0;
    max_cell_count[i].i = std::numeric_limits<unsigned int>::max();
    logic_states[i].i = 0;
    time_in_state[i] = 0;
    turned_from_high_state_to_low[i] = false;
  }

  run_state.i = 0;
}





// ----- Start the main loop ----- //
void loop() {
  time0.i = micros();
  id.i = 1000; // maps to nothing in the defined communication protocol, reset at top of each loop

  // ---- Computer -> Microcontroller serial communications ---- //
  if(test_mode == false){
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
            for(u_int i=0; i<N_CHANNELS; i++){
              current_voltage[i].i = 0;
              previous_voltage[i].i = 0;
              max_voltage[i].i = 0;
              //running_mean_voltage[i].i = 0;
              //running_std_dev_voltage[i].i = 0;
              //data_accumulators[i] = window_acc();
              min_threshold_voltage[i].i = AMAX_VAL;
              max_threshold_voltage[i].i = AMAX_VAL;
              current_cell_count[i].i = 0;
              max_cell_count[i].i = std::numeric_limits<unsigned int>::max();
              logic_states[i].i = 0;
              time_in_state[i] = 0;
              turned_from_high_state_to_low[i] = false;
            }
          }
        }


        // id == 1: incoming minimum threshold voltage settings
        else if(id.i == 1) {
          byteint new_threshold_voltage_buffer[N_CHANNELS];
          for(int i=0; i<N_CHANNELS; i++) {
            Serial.readBytes(new_threshold_voltage_buffer[i].b, sizeof(int));
            reverse(new_threshold_voltage_buffer[i].b, sizeof(int));
          }
          set_threshold_voltages(min_threshold_voltage, new_threshold_voltage_buffer);
        }


        // id == 2: incoming cell selection maxima
        else if(id.i == 2){
          byteint new_cell_count_maxima[N_CHANNELS];
          for(u_int i=0; i<N_CHANNELS; i++){
            Serial.readBytes(new_cell_count_maxima[i].b, sizeof(int));
            reverse(new_cell_count_maxima[i].b, sizeof(int));
          }
          set_cell_selection_counts(max_cell_count, new_cell_count_maxima);
        }

        // id == 3: incoming maximum threshold voltage settings
        else if(id.i == 3) {
          byteint new_threshold_voltage_buffer[N_CHANNELS];
          for(int i=0; i<N_CHANNELS; i++) {
            Serial.readBytes(new_threshold_voltage_buffer[i].b, sizeof(int));
            reverse(new_threshold_voltage_buffer[i].b, sizeof(int));
          }
          set_threshold_voltages(max_threshold_voltage, new_threshold_voltage_buffer);
        }

        // id.i == 4: incoming PMT logic states
        else if (id.i == 4){
          byteint new_logic_states[N_CHANNELS];
          for(u_int i=0; i<N_CHANNELS; i++){
            Serial.readBytes(new_logic_states[i].b, sizeof(int));
            reverse(new_logic_states[i].b, sizeof(int));
          }
          set_logic_states(logic_states, new_logic_states);
          //set_ADC_modes(adc, pins, logic_states);
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
}
else { //in test mode, so keep the runstate as ON
  run_state.i = 1;
}


  // ---- Check run state ---- //
  // run_state == 0 means off, so go back to top of loop (return) and wait to turn on
  // run_state == 2 means PAUSED, so go back to top of loop and wait, but don't reset anything
  if (run_state.i == 0 || run_state.i == 2){
    return;
  }


  // ---- Cell selection ---- //
  // --- Detecting fluoresence on all N_CHANNELS color channels --- //


  // measure the new voltages, calculate measurement time
  // repeat on every loop; if we find that at least one channel is
  // above the minimum voltage, the while measurement loop below this
  // will be triggered, until the voltage falls again (a peak has passed)
  clock_time_before_measurement.i = micros();
  measure_voltages(adc, pins, logic_states, current_voltage);
  measurement_time = micros() - clock_time_before_measurement.i;
  for(u_int i=0; i<N_CHANNELS; i++){
    //data_accumulators[i](current_voltage[i].i);
    if(current_voltage[i].i >= (min_threshold_voltage[i].i)){
      time_in_state[i] = measurement_time;
    }
  }

  u_int while_loop_count = 0; // how many iterations the while loop has gone under
  while(at_least_one_channel_is_above_minimum(current_voltage, min_threshold_voltage, max_threshold_voltage, logic_states)){
       for(u_int i=0; i<N_CHANNELS; i++){
         previous_voltage[i].i = current_voltage[i].i;
       }
       clock_time_before_measurement.i = micros();
       measure_voltages(adc, pins, logic_states, current_voltage);
       measurement_time = micros() - clock_time_before_measurement.i;
       for(u_int i=0; i<N_CHANNELS; i++){
         if(current_voltage[i].i >= min_threshold_voltage[i].i){
           time_in_state[i] += measurement_time;
           if(current_voltage[i].i > max_voltage[i].i){
             max_voltage[i].i = current_voltage[i].i;
           }
         }
       }
       while_loop_count += 1;
       // in the loop too long, likely a user error (connected a non-ignore channel to a floating input); //reset things and break out. TODO: replace with GUI-level sanity checking
       if((while_loop_count * measurement_time) > MAX_TIME_IN_WHILE_LOOP){
         for(u_int i=0; i<N_CHANNELS; i++){
           time_in_state[i] = 0;
           max_voltage[i].i = 0;
         }
         break;
       }
     }

  // test if signal is maximum and, if so, how long it has been in an above-minimum state
  // if all criteria are met, set positive_signals[i] = true, false otherwise
  bool positive_signal[N_CHANNELS];
  for(u_int i=0; i<N_CHANNELS; i++){
    if((time_in_state[i] >= REQUIRED_TIME_ABOVE_MIN) \
    && (max_voltage[i].i <= max_threshold_voltage[i].i)){
        positive_signal[i] = true;
    }
    else{
      positive_signal[i] = false;
    }
  }


  // --- Calculating logical condition --- //
  bool should_we_capture_cell = false; // default to FALSE, possibly set to true after looking at all channels

  u_int n_nots = 0;
  u_int n_ors  = 0;
  u_int n_ands = 0;                   // number of each TRUE condition, across all channels

  bool stop_checking_ands = false;    // if one AND channel has no signal, don't check others

  for (u_int i=0; i<N_CHANNELS; i++){
    bool is_positive_signal = (positive_signal[i]);

    switch(logic_states[i].i) {

      // check for NOT conditions first
      case 3: {
        if(is_positive_signal){
          n_nots += 1;
        }
        break;
      }

      // check for OR (inclusive) conditions second:
      case 1: {
        if(is_positive_signal){
          n_ors += 1;
        }
        break;
      }

      // check for AND conditions last:
      case 2: {
        if (stop_checking_ands){
          break;
        }

        if(is_positive_signal){
          n_ands += 1;
        }
        else { // one of the AND channels isn't a good signal; stop checking
          n_ands = 0;
          stop_checking_ands = true;
        }
        break;
      }
    }
  }

  if (n_nots == 0 && (n_ors >= 1 || n_ands >= 2)) { // need minimum of 2 TRUE conditions for AND to make sense
    should_we_capture_cell = true;
  }
  else {
    should_we_capture_cell = false; // no conditions met, don't select a cell, start over from the top of the main loop
  }

  // --- Checking that we haven't hit ANY of the max cell counts on channels with positive signals --- //
  // TODO: consider whether or not this logic (limiting number of cells) has any practical use or should be discarded
  for (u_int i=0; i<N_CHANNELS; i++){
    if (positive_signal[i] == true){
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
    for (u_int i=0; i<N_CHANNELS; i++){
      if(positive_signal[i] == true){
        current_cell_count[i].i += 1;
      }
      // reset these things, start fresh for next signal
      max_voltage[i].i = 0;
      time_in_state[i] = 0;
      previous_voltage[i].i = 0;
      current_voltage[i].i = 0;
    }
    delayMicroseconds(PAUSE_AFTER_SELECTION_TIME); // TODO: replace with less arbitrary pause time; until voltage drops below min?
  }
  else{
    for(u_int i=0; i<N_CHANNELS; i++){
      max_voltage[i].i = 0;
      time_in_state[i] = 0;
      previous_voltage[i].i = 0;
      current_voltage[i].i = 0;
    }
  }

  // store last loop's voltages
  for(u_int i=0; i<N_CHANNELS; i++){
    previous_voltage[i].i = current_voltage[i].i;
  }

  Serial.flush();
  time1.i = (micros() - time0.i);


  // debugging - timing of the main loop needs to be < ~25us for reliable detection
  // set if(false) for off, if(true) for on (WILL SLOW DOWN LOOP)

  if(false) {
  //Serial.write(255);
  Serial.print(" ID");
  Serial.print(id.i);
  Serial.print(" TIME: ");
  Serial.print(time1.i);
  Serial.print(" RUNSTATE: ");
  Serial.print(run_state.i);
  Serial.print(" CURR_VOLTAGES: ");
  for(u_int i=0; i<N_CHANNELS; i++){
    Serial.print(current_voltage[i].i);
    Serial.print(" ");
  }
  Serial.print(" THRESH_VOLTAGES: ");
  for(u_int i=0; i<N_CHANNELS; i++){
    Serial.print(min_threshold_voltage[i].i);
    Serial.print(" ");
  }
  Serial.print(" CURR_CELL_COUNTS: ");
  for(u_int i=0; i<N_CHANNELS; i++){
    Serial.print(current_cell_count[i].i);
    Serial.print(" ");
  }
  Serial.print(" MAX_CELL_COUNTS: ");
  for(u_int i=0; i<N_CHANNELS; i++){
    Serial.print(max_cell_count[i].i);
    Serial.print(" ");
  }
  Serial.print(" LOGIC_STATES: ");
  for(u_int i=0; i<N_CHANNELS; i++){
    Serial.print(logic_states[i].i);
    Serial.print(" ");
  }
  Serial.print("\n");
  Serial.flush();
  }

}
