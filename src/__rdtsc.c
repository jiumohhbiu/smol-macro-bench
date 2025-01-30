#include "__rdtsc.h"

unsigned long long now()
{
    return __rdtsc();
}
