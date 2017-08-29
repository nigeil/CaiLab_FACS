/*! \file global_defines.h
* contains all #define statements required by the microcontroller code. Values
* here can be changed at compile-time as needed to optimize measurement accuracy,
* measurement speed, number of PMT channels, and so on, as well as pin numbering.
*/

#ifndef GLOBAL_DEFINES_HEADER
#define GLOBAL_DEFINES_HEADER

// number of channels
#define N_CHANNELS 4

// analog pins for reading fluorescent voltage signals
/* old
#define REDPIN    A0
#define GREENPIN  A1
#define BLUEPIN   A2
#define YELLOWPIN A3

// digital pin for triggering electrode (droplet selection)
#define ELECTRODEPIN 2
*/

// new
#define REDPIN    A5
#define GREENPIN  A4
#define BLUEPIN   A3
#define YELLOWPIN A2

// digital pin for triggering electrode (droplet selection)
#define ELECTRODEPIN 21
#define ELECTRODE_ON_TIME 100 // in us
#define PAUSE_AFTER_SELECTION_TIME 250 // in us

// digital pin for LED status light (HIGH if runstate == 1, running)
//#define LEDSTATUSPIN 0 //old
#define LEDSTATUSPIN A21 //new

// analog settings
#define AREF ADC_REFERENCE::REF_3V3                        // reference voltage setting, 1.2V for low voltages
#define AREF_VAL 3.3                                       // for calculations, set to voltage of above
#define ASAMPSPEED ADC_SAMPLING_SPEED::VERY_HIGH_SPEED     // sampling speed; can set it high for low-impedence signals
#define ACONVSPEED ADC_CONVERSION_SPEED::VERY_HIGH_SPEED   // conversion speed; upclocks the ADC freq at accuracy cost
#define ARES adc->getMaxValue(ADC_0)                       // analog resolution, set to be the same for both ADCs0&1
#define N_AVERAGES 1                                       // the number of averages the ADC takes before returning a values
#define ARES_BITS 8                                        // analog resolution in bits, 8 is the lowest we can use (256 levels -> ~13mV per level)

// Division factor for converting integer voltages to floats
// i.e. INPUT: [0, max(int)] -> OUTPUT: [0/float_div_factor, max(int)/float_div_factor]
#define VOLTAGE_DIV_FACTOR 1000 // gives 3 decimal places
#define AMAX_VAL int(AREF_VAL * VOLTAGE_DIV_FACTOR)

// times required to be in above-min-threshold state before triggering
#define REQUIRED_TIME_ABOVE_MIN 15  // in us

// maximum time to stay in the measurement while loop
// really only used to make sure that we don't get stuck in the while loop when
// some channels are not set to IGNORE but are still connected to floating voltages
#define MAX_TIME_IN_WHILE_LOOP 1000 // us

#endif
