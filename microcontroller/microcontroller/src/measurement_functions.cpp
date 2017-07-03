#include "measurement_functions.h"
#include "global_defines.h"

// MEASUREMENT

// read from 4 analog pins and convert to voltages
void measure_voltages(ADC* adc, u_int* pins, byteint* logic_states, byteint* voltages){
  const u_int multiply_factor = (AREF_VAL / ARES) * VOLTAGE_DIV_FACTOR;

  for(u_int i=0; i<N_CHANNELS; i++){
    if(logic_states[i].i != 0){
      voltages[i].i = (adc->analogRead(pins[i])) * multiply_factor;
    }
    else{
      voltages[i].i = 0;
    }
  }
  return;
};
