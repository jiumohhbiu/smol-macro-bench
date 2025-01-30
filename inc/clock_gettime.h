#ifndef CLOCK_GETTIME_H
#define CLOCK_GETTIME_H

#include <time.h>

#define CLOCK_ID CLOCK_MONOTONIC_RAW

unsigned long long now();

#endif
