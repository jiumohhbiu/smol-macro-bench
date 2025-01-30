#ifndef ITEM_H__
#define ITEM_H__

#include <stdio.h>
#include <stddef.h>

#define ITEM_MAX_NAME_SIZE NAME_SIZE

#define ITEM_FSCAN_OK 0

#define ITEM_FSCAN_INVALID_NAME_READ    1
#define ITEM_FSCAN_INVALID_NAME_VALUE   2
#define ITEM_FSCAN_INVALID_MASS_READ    3
#define ITEM_FSCAN_INVALID_MASS_VALUE   4
#define ITEM_FSCAN_INVALID_VOLUME_READ  5
#define ITEM_FSCAN_INVALID_VOLUME_VALUE 6

typedef struct
{
    char name[ITEM_MAX_NAME_SIZE + 1];
    size_t name_size;
    double mass;
    double volume;
} item_t;

int item_fscan(FILE *file, item_t *dst);
size_t item_fimport_all(FILE *file, item_t *items, size_t max_size);

int item_fprint(FILE *file, const item_t *item);

double item_density(const item_t *item);
size_t item_name_copy(char *dst, size_t dst_size, const item_t *item);


#endif // ITEM_H__
