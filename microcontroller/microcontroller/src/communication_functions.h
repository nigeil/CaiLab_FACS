

#ifndef COMMUNICATION_FUNCTIONS_HEADER
#define COMMUNICATION_FUNCTIONS_HEADER

#include <Arduino.h>
#include "global_defines.h"
#include "helper_types.h"

void send_voltages(byteint* );

void send_min_thresh_voltages(byteint* );

void send_max_thresh_voltages(byteint* );

void send_cell_counts(byteint* );

void send_max_cell_counts(byteint* );

void send_loop_time(byteint );

void send_logic_states(byteint* );

#endif
