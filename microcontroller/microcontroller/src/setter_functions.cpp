#include "setter_functions.h"

// call when new threshold values have been recieved (as bytes) from the computer
void set_threshold_voltages(byteint* thresh_voltages, byteint* new_thresh_voltages){
  for(int i=0; i<N_CHANNELS; i++){
    new_thresh_voltages[i].i = bytes_to_int(new_thresh_voltages[i].b);
    thresh_voltages[i].i = new_thresh_voltages[i].i;
    for(u_int j=0; j<sizeof(int); j++){
      thresh_voltages[i].b[j] = new_thresh_voltages[i].b[j];
    }
  }
  return;
}


// call when new cell counts have been recieved (as bytes) from the computer
void set_cell_selection_counts(byteint* max_cell_counts, byteint* new_cell_max_counts){
  for(u_int i=0; i<N_CHANNELS; i++){
    new_cell_max_counts[i].i = bytes_to_int(new_cell_max_counts[i].b);
    max_cell_counts[i].i = new_cell_max_counts[i].i;
    for(u_int j=0; j<sizeof(int); j++){
      max_cell_counts[i].b[j] = new_cell_max_counts[i].b[j];
    }
  }
  return;
}


// call when new PMT logic states have been recieved (as bytes) from the computer
void set_logic_states(byteint* logic_states, byteint* new_logic_states){
  for (u_int i=0; i<N_CHANNELS; i++){
    new_logic_states[i].i = bytes_to_int(new_logic_states[i].b);
    logic_states[i].i = new_logic_states[i].i;
    for (u_int j=0; j<sizeof(int); j++){
      logic_states[i].b[j] = new_logic_states[i].b[j];
    }
  }
  return;
}
