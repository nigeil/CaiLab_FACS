#include "measurement_functions.h"
#include "global_defines.h"

// MEASUREMENT

// read from 4 analog pins and convert to voltages
// TODO: randomly order the measurements, so RED isn't always first,
// and YELLOW not always last (when hitting minimum peak width (time-wise)
// you find more false-negatives for YELLOW than RED, 2017-07-13)
// Can be done by shuffling an array of indices and using those sequentially
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
/*
void measure_voltages(ADC* adc, u_int* pins, byteint* logic_states, byteint* voltages){
  const u_int multiply_factor = (AREF_VAL / ARES) * VOLTAGE_DIV_FACTOR;
  const u_int adc_module_number[2] = {ADC_0, ADC_1};
  u_int j = 0; // iterator for the ADC_MODULE_NUMBER array, may not be used
  for(u_int i=0; i<N_CHANNELS; i++){
    if(logic_states[i].i != 0){
      if(adc->isContinuous(adc_module_number[j])){
        voltages[i].i = adc->analogReadContinuous(adc_module_number[j]) * multiply_factor;
        j += 1;
      }
      else{
        voltages[i].i = adc->analogRead(pins[i]) * multiply_factor;
      }
    }
  }

}
*/
/*
void set_ADC_modes(ADC* adc, u_int* pins, byteint* logic_states){
  // determine how many channels we need to read from (not in ignore (0) state)
  u_int n_channels_in_use = 0;
  for(u_int i=0; i<N_CHANNELS; i++){
    if(logic_states[i].i != 0){
      n_channels_in_use += 1;
    }
  }

  // if using only 1 or 2 channels, we can use continuous reads
  if(n_channels_in_use == 1 || n_channels_in_use == 2){
    const u_int adc_module_number[2] = {ADC_0, ADC_1};
    u_int j = 0;
    for(u_int i = 0; i<N_CHANNELS; i++){
      if(logic_states[i].i != 0){
        adc->startContinuous(pins[i], adc_module_number[j]);
        j += 1;
      }
    }
  }

  // otherwise, we must revert to single-shot reads; turn off continuous reading
  else{
    adc->stopContinuous(ADC_0);
    adc->stopContinuous(ADC_1);
  }
}
*/

bool at_least_one_channel_is_above_minimum(byteint* current_voltage, byteint* min_threshold_voltage, byteint* max_threshold_voltage, byteint* logic_states){
  bool ret = false;
  for(u_int i=0; i<N_CHANNELS; i++){
    if((current_voltage[i].i > min_threshold_voltage[i].i) \
    && (logic_states[i].i != 0) \
    && (min_threshold_voltage[i].i < max_threshold_voltage[i].i)){
      ret = true;
      break;
    }
  }
  return ret;
}
