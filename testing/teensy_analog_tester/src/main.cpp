// Code to generate signals of various sizes (heights/widths/frequencies)
// on multiple analog output pins for the purposes of testing the teensy
// that is supposed to be reading such signals from the PMT

#include "Arduino.h"
#include "global_defines.h"
#include "function_generating_tests.h"

// defines and setup

int pins[N_CHANNELS] = {REDPIN, GREENPIN, BLUEPIN, YELLOWPIN};

int peak_height;
int peak_width;
int peak_spacing;
int n_peaks;


void setup(){
  //set PWM freq and resolution
  for(int i=0; i<N_CHANNELS; i++){
    pinMode(pins[i], OUTPUT);
    analogWriteFrequency(pins[i], PWM_FREQUENCY);
  }
  analogWriteResolution(ANALOG_WRITE_RESOLUTION);
  pinMode(1, OUTPUT);
}


// begin main tests
void loop(){
  // test 1
  //peak_height = ANALOG_WRITE_MAX_VALUE / 2;
  //peak_width  = 1000;    // us
  //peak_spacing = 5000; // us
  //n_peaks = N_PEAKS;
  //square_wave_test(pins, peak_height, peak_width, peak_spacing, n_peaks);
  //basic_pulse_test(pins, peak_width, peak_spacing, n_peaks);
  //gaussian_pulse_test(pins, peak_height, peak_width, peak_spacing, n_peaks);
  //step_pulse_test(pins, peak_height, peak_width, peak_spacing, n_peaks);
  // wait between tests
  //delayMicroseconds(TIME_TO_WAIT_AFTER_TEST);

  digitalWrite(1, HIGH);
  delayMicroseconds(30);
  digitalWrite(1, LOW);
  delayMicroseconds(2000);
}
