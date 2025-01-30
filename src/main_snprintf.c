#include "item_snprintf.h"

#include <stdlib.h>
#include <stdio.h>
#include <time.h>


#define STR_(x) #x
#define STR(x) STR_(x)

#ifndef TIMER
#error Try to compile with -DTIMER=TIMER
#else
#include STR(TIMER)
#endif

#ifndef NAME_SIZE
#error Try to compile with -DNAME_SIZE=N (N > 0)
#endif

#if NAME_SIZE < 1
#error Try to compile with -DNAME_SIZE=N (N > 0)
#endif

#ifndef ITEMS_SIZE
#error Try to compile with -DITEMS_SIZE=N (N > 0)
#endif

#if ITEMS_SIZE < 1
#error Try to compile with -DITEMS_SIZE=N (N > 0)
#endif


#ifndef TTR
#error Try to compile with -DTTR=N (N > 99)
#endif

#if TTR < 10000000
#error Try to compile with -DTTR=N (N > 99)
#endif

void init_str(char *str, size_t n)
{
    for (size_t i = 0; i < n; ++i)
        str[i] = rand() % (127 - 32) + 32;
    str[n] = '\0';
}

// https://youtu.be/nXaxk27zwlk?si=stMNr7YaXbFMjy0I&t=2440
void escape(void *p)
{
    asm volatile("" : : "g"(p) : "memory");
}

// https://youtu.be/nXaxk27zwlk?si=stMNr7YaXbFMjy0I&t=2440
void clobber()
{
    asm volatile("" : : : "memory");
}

int main()
{
    srand(time(NULL));

    unsigned long long accum = 0;
    size_t i = 0;
    for (; accum < TTR; ++i)
    {
        item_t items[ITEMS_SIZE];
        for (size_t j = 0; j < ITEMS_SIZE; ++j)
        {
            init_str(items[j].name, NAME_SIZE);
            items[j].name_size = NAME_SIZE;
            items[j].mass = (double) rand();
            items[j].volume = (double) rand();
        }

        char buffer[ITEM_REPR_MAXSIZE + 1];
        escape(buffer);
        unsigned long long start = now();
        for (size_t j = 0; j < ITEMS_SIZE; ++j)
        {
            item_repr(buffer, sizeof buffer, &items[j]);
            clobber();
        }
        unsigned long long end = now();

        accum += end - start;
    }
    printf("%llu\n", accum / i);
    return 0;
}
