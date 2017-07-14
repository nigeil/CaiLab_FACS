#include "Arduino.h"
#include "global_defines.h"
#include "Gaussian.h"
#include "waveforms.h"

void square_wave_test(int* pins, int peak_height, int peak_width, int peak_spacing, int n_peaks) {
  for(int j=0; j<n_peaks; j++) {
    // rise on all channels
    for(int i=0; i<N_CHANNELS; i++){
      analogWrite(pins[i], peak_height);
    }
    // stay high
    delayMicroseconds(peak_width);
    // fall on all channels
    for(int i=0; i<N_CHANNELS; i++){
      analogWrite(pins[i], ANALOG_WRITE_MIN_VALUE);
    }
    // stay low
    delayMicroseconds(peak_spacing);
  }
}

void basic_pulse_test(int* pins, int peak_width, int peak_spacing, int n_peaks){
  for(int j=0; j<n_peaks; j++){
    for(int i=0; i<N_CHANNELS; i++){
      digitalWrite(pins[i], HIGH);
  }
    delayMicroseconds(peak_width);
    for(int i=0; i<N_CHANNELS; i++){
      digitalWrite(pins[i], LOW);
    }
    delayMicroseconds(peak_spacing);
  }
}

void gaussian_pulse_test(int* pins, int peak_height, int peak_width, int peak_spacing, int n_peaks){
  int peak_position = peak_spacing / 2;
  int val = 0; // current value of the gaussian
  Gaussian pulse = Gaussian(peak_position, peak_width);
  for(int j=0; j<n_peaks; j++){
    for(int t=0; t<peak_spacing; t+=5){
      val = int(peak_height * pulse.plot(t));
      for(int i=0; i<N_CHANNELS; i++){
        analogWrite(pins[i], val);
      }
    }
  }
}

void step_pulse_test(int* pins, int peak_height, int peak_width, int peak_spacing, int n_peaks){
  int val = 0; // current value of the gaussian
  int t_increment = peak_width / 3;
  int peak_position = 0;
  for(int j=0; j<n_peaks; j++){
    for(int t=0; t<peak_spacing; t+=t_increment){
      if(t<peak_position){
        val = 0;
      }
      else if(t == peak_position){
        val = peak_height / 4;
      }
      else if (t == peak_position + 1 * t_increment) {
        val = peak_height;
      }
      else if (t == peak_position + (2 * t_increment)){
        val = peak_height / 3;
      }
      else{
        val = 0;
      }
      for(int i=0; i<N_CHANNELS; i++){
        analogWrite(pins[i], val);
        delayMicroseconds(t_increment);
      }
    }
  }
}


void sine_wave_test(int* pins, int freq);
