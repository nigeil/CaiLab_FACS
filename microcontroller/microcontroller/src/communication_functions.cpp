#include "communication_functions.h"
#include "helper_types.h"
#include "helper_functions.h"

// SENDERS

// send the measured voltages back to the computer
void send_voltages(byteint* voltages){
  u_char send_buffer[1 + N_CHANNELS * sizeof(int)];

  // send data ID to computer
  send_buffer[0] = 1;

  // send voltages as 4-byte ints
  u_int index = 1;
  for(int i=0; i<N_CHANNELS; i++){
    int_to_bytes(voltages[i].i, voltages[i].b);
    for(u_int j=0; j<sizeof(int); j++){
      send_buffer[index] = voltages[i].b[j];
      //send_buffer[index] = char(1);
      index = index + 1;
    }
  }

  Serial.write(send_buffer, 1 + N_CHANNELS * sizeof(int));
  return;
};


void send_min_thresh_voltages(byteint* voltages){
  u_char send_buffer[1 + N_CHANNELS * sizeof(int)];

  // send data ID to computer
  send_buffer[0] = 4;

  // send voltages as 4-byte ints
  u_int index = 1;
  for(int i=0; i<N_CHANNELS; i++){
    int_to_bytes(voltages[i].i, voltages[i].b);
    for(u_int j=0; j<sizeof(int); j++){
      send_buffer[index] = voltages[i].b[j];
      //send_buffer[index] = char(1);
      index = index + 1;
    }
  }

  Serial.write(send_buffer, 1 + N_CHANNELS * sizeof(int));
  return;
};

void send_max_thresh_voltages(byteint* voltages){
  u_char send_buffer[1 + N_CHANNELS * sizeof(int)];

  // send data ID to computer
  send_buffer[0] = 6;

  // send voltages as 4-byte ints
  u_int index = 1;
  for(int i=0; i<N_CHANNELS; i++){
    int_to_bytes(voltages[i].i, voltages[i].b);
    for(u_int j=0; j<sizeof(int); j++){
      send_buffer[index] = voltages[i].b[j];
      //send_buffer[index] = char(1);
      index = index + 1;
    }
  }

  Serial.write(send_buffer, 1 + N_CHANNELS * sizeof(int));
  return;
};

// send the number of sorted cells back to the computer
void send_cell_counts(byteint* cell_counts){
  byte send_buffer[1 + (N_CHANNELS * sizeof(int))];

  // send data ID to computer
  send_buffer[0] = 2; //identifier byte

  // send cell counts as 4-byte ints
  u_int index = 1;
  for(u_int i=0; i<N_CHANNELS; i++){
    int_to_bytes(cell_counts[i].i, cell_counts[i].b);
    for(u_int j=0; j<sizeof(int); j++){
      send_buffer[index] = cell_counts[i].b[j];
      //send_buffer[index] = char(1);
      index = index + 1;
    }
  }

  Serial.write(send_buffer, 1 + (N_CHANNELS * sizeof(int)));
  return;
};

// send the number of sorted cells back to the computer
void send_max_cell_counts(byteint* cell_counts){
  byte send_buffer[1 + (N_CHANNELS *  sizeof(int))];

  // send data ID to computer
  send_buffer[0] = 5; //identifier byte

  // send cell counts as 4-byte ints
  u_int index = 1;
  for(u_int i=0; i<N_CHANNELS; i++){
    int_to_bytes(cell_counts[i].i, cell_counts[i].b);
    for(u_int j=0; j<sizeof(int); j++){
      send_buffer[index] = cell_counts[i].b[j];
      //send_buffer[index] = char(1);
      index = index + 1;
    }
  }

  Serial.write(send_buffer, 1 + (N_CHANNELS * sizeof(int)));
  return;
};


// send time to complete last loop
void send_loop_time(byteint loop_time){
  byte send_buffer[1 + (1 * sizeof(int))];

  // send data ID to computer
  send_buffer[0] = 3; //identifier byte

  // send cell counts as 4-byte ints
  u_int index = 1;
  for(u_int j=0; j<sizeof(int); j++){
    send_buffer[index] = loop_time.b[j];
    index = index + 1;
  }

  Serial.write(send_buffer, 1 + (1 * sizeof(int)));
  return;
};


// send the current PMT logic states back to the computer
void send_logic_states(byteint* logic_states){
  byte send_buffer[1 + (N_CHANNELS * sizeof(int))];

  // send data ID to computer
  send_buffer[0] = 7; //identifier byte

  // send logic states as 4-byte ints
  u_int index = 1;
  for(u_int i=0; i<N_CHANNELS; i++){
    int_to_bytes(logic_states[i].i, logic_states[i].b);
    for(u_int j=0; j<sizeof(int); j++){
      send_buffer[index] = logic_states[i].b[j];
      index = index + 1;
    }
  }

  Serial.write(send_buffer, 1 + (N_CHANNELS * sizeof(int)));
  return;
};
