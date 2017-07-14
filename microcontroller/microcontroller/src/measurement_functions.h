/*! \file measurement_functions.h
* contains functions to measure voltages from the anolog input pins
*/
#ifndef MEASUREMENT_FUNCTIONS_HEADER
#define MEASUREMENT_FUNCTIONS_HEADER

#include "global_defines.h"
#include "helper_types.h"
#include <ADC_Module.h>
#include <ADC.h>

/*! \fn measure_voltages
* measures the voltages on all analog input pins
*/

void measure_voltages(ADC*, u_int*, byteint*, byteint*);

/*! \fn set_ADC_modes
based on the set logic states, set the ADC to continuously measure up to 2 analog pins
or, if more than 2 channels are being used, turn off continuous mode and revert to single-shot modes
for all pins
*/

void set_ADC_modes(ADC*, u_int*, byteint*);


/*! \fn at_least_one_channel_is_above_minimum
returns true iff:
-one active (not IGNORE) channel has a voltage above the minimum threshold
-that channel has min_threshold < max_threshold (if this is not the case, the user has made an error at the GUI level, so ignore the channel)
*/
bool at_least_one_channel_is_above_minimum(byteint*, byteint*, byteint*, byteint*);

#endif
