/*! \file helper_types.h
* contains type statements for types required by the microcontroller codes
*/

#ifndef HELPER_TYPES_HEADER
#define HELPER_TYPES_HEADER

#include <stdint.h>
#include <Arduino.h>

/*! \struct byteint
* byteint is a structure that contains a 4-byte integer as well
* as an array of 4-bytes that represents the integer in big-endian
* order. Used in order to faciilitate faster, byte-by-byte serial
* communications.
*/
struct byteint{
  char b[sizeof(int)];
  uint32_t i;
};

//typedef uint32_t u_int;
//typedef uint8_t u_char;

#endif
