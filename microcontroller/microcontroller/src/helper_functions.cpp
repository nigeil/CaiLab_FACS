#include "helper_functions.h"
#include "helper_types.h"
// CONVERSIONS

// Converting from bytes to a 4 byte intger
int bytes_to_int(char* the_bytes){
  return u_int(the_bytes[3] << 24) | (the_bytes[2] << 16) | (the_bytes[1] << 8) | (the_bytes[0]);
};

// Converting from a 4 byte integer to a string of bytes
// Can't return an array, so must pass it as a parameter and modify in-function
void int_to_bytes(int the_int, char* byte_buffer){
  for (u_int i = 0; i < sizeof(int); i++) {
    byte_buffer[3 - i] = char(the_int >> (i * 8));
    //byte_buffer[i] = char(the_int >> (i * 8));
  }
};

// Reverses a byte array in-place, size given by count
void reverse(char* arr, int count){
   int temp;
   for (int i = 0; i < count/2; ++i)
   {
      temp = arr[i];
      arr[i] = arr[count-i-1];
      arr[count-i-1] = temp;
   }
}
