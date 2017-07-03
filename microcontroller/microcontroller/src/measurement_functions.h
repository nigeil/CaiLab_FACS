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

#endif
