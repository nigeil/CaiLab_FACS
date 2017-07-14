#ifndef GLOBAL_DEFINES_HEADER
#define GLOBAL_DEFINES_HEADER

/*! pins used to output signals and the number of them */
#define REDPIN    A0
#define GREENPIN  A1
#define BLUEPIN   A2
#define YELLOWPIN A3

#define N_CHANNELS 4

/*! PWM freq and PWM resolution are linked inversely */
#define PWM_FREQUENCY 3750000
#define ANALOG_WRITE_RESOLUTION 4
#define ANALOG_WRITE_MIN_VALUE 0
#define ANALOG_WRITE_MAX_VALUE ((ANALOG_WRITE_RESOLUTION * ANALOG_WRITE_RESOLUTION) - 1)

/*! number of trials per function generator test */
#define N_PEAKS 100

/*! time to wait between subsequent tests */
#define TIME_TO_WAIT_AFTER_TEST 1000000

#endif
