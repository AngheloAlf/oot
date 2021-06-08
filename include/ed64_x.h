#ifndef _ED64_X_H_
#define _ED64_X_H_

#include "ultra64.h"

int ed64_x_fifo_write(const void *src, u32 n_blocks);
void *ed64_x_proutSyncPrintf(void *arg, const char *str, u32 count);

#endif
