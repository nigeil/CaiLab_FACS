/*! \file setter_functions.h
* contains declarations of functions involved in setting/updating the values
* of arrays in the microcontroller code, e.g. the current voltage levels
*/

#ifndef SETTER_FUNCTIONS_HEADER
#define SETTER_FUNCTIONS_HEADER

#include "global_defines.h"
#include "helper_types.h"
#include "helper_functions.h"

/*! \fn set_threshold_voltages
* sets the array of threshold voltages (1 item per channel) elementwise
* to the new array of threshold voltages as read from the serial line
*/
void set_threshold_voltages(byteint*, byteint*);

/*! \fn set_cell_selection_counts
* sets the array of maximum cell selection counts (1 item per channel) elementwise
* to the new array of cell selection counts as read from the serial line
*/
void set_cell_selection_counts(byteint*, byteint*);


/*! \fn set_logic_states
* sets the array of logic states (1 item per channel) elementwise
* to the new array of logic states as read from the serial line
*/
void set_logic_states(byteint*, byteint*);

#endif
