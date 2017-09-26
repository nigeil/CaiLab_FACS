/*! \file helper_functions.h
* contains statements and documentation of utility functions
*/

#ifndef HELPER_FUNCTIONS_HEADER
#define HELPER_FUNCTIONS_HEADER


/*! \fn bytes_to_int
* takes an array of 4 bytes and converts them to an unsigned integer
*/
int bytes_to_int(char *);

/*! \fn int_to_bytes
* takes an unsigned integer and converts it to an array
* of 4 bytes
*/
void int_to_bytes(int, char*);

/*! \fn reverse
* given an array of char and the size of the array in
* number of items (int), reverses said array elementwise in-place
*/
void reverse(char*, int);



#endif
