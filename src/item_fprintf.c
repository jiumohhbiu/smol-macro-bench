#include "item_fprintf.h"

#include <assert.h>

#include <math.h>
#include <string.h>

static void init(item_t *dst, const char *name, size_t name_size, double mass, double volume)
{
    dst->name_size = name_size;
    dst->mass = mass;
    dst->volume = volume;
    memcpy(dst->name, name, name_size + 1);
}

static int is_valid_name_size(size_t name_size)
{
    return 0 < name_size && name_size <= ITEM_MAX_NAME_SIZE;
}

static int is_valid_mass(double mass)
{
    return isfinite(mass) && mass > 0;
}

static int is_valid_volume(double volume)
{
    return isfinite(volume) && volume > 0;
}

int item_fscan(FILE *file, item_t *dst)
{
    assert(file);
    assert(dst);

    char name[ITEM_MAX_NAME_SIZE + 1 + 1];
    if (!fgets(name, sizeof name, file))
        return ITEM_FSCAN_INVALID_NAME_READ;
    size_t name_size = strlen(name);
    if (name[name_size - 1] != '\n')
        return ITEM_FSCAN_INVALID_NAME_READ;
    name[--name_size] = '\0';
    if (!is_valid_name_size(name_size))
        return ITEM_FSCAN_INVALID_NAME_VALUE;

    double mass;
    if (fscanf(file, "%lf\n", &mass) != 1)
        return ITEM_FSCAN_INVALID_MASS_READ;
    if (!is_valid_mass(mass))
        return ITEM_FSCAN_INVALID_NAME_VALUE;

    double volume;
    if (fscanf(file, "%lf\n", &volume) != 1)
        return ITEM_FSCAN_INVALID_VOLUME_READ;
    if (!is_valid_volume(volume))
        return ITEM_FSCAN_INVALID_VOLUME_VALUE;

    init(dst, name, name_size, mass, volume);
    return ITEM_FSCAN_OK;
}

size_t item_fimport_all(FILE *file, item_t *items, size_t max_size)
{
    assert(file);
    assert(items);

    if (max_size == 0)
        return 0;

    size_t new_size = 0;
    item_t t;
    int rc = item_fscan(file, &t);
    while (new_size < max_size && rc == ITEM_FSCAN_OK && feof(file) == 0)
    {
        items[new_size++] = t;
        rc = item_fscan(file, &t);
    }
    if (rc != ITEM_FSCAN_OK || new_size == max_size)
        return 0;
    items[new_size++] = t;
    return new_size;
}

int item_fprint(FILE *file, const item_t *item)
{
    assert(file);
    assert(item);

    return fprintf(file, "%s\n%lf\n%lf\n", item->name, item->mass, item->volume);
}

double item_density(const item_t *item)
{
    assert(item);

    return item->mass / item->volume;
}

size_t item_name_copy(char *dst, size_t dst_size, const item_t *item)
{
    assert(dst);
    assert(item);
    assert(dst_size >= item->name_size + 1);

    memcpy(dst, item->name, item->name_size + 1);
    return item->name_size;
}
