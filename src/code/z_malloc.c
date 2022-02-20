#include "global.h"

#define LOG_SEVERITY_NOLOG 0
#define LOG_SEVERITY_ERROR 2
#define LOG_SEVERITY_VERBOSE 3

s32 gZeldaArenaLogSeverity = LOG_SEVERITY_ERROR;
Arena sZeldaArena;

void ZeldaArena_CheckPointer(void* ptr, u32 size, const char* name, const char* action) {
    if (ptr == NULL) {
        if (gZeldaArenaLogSeverity >= LOG_SEVERITY_ERROR) {
            osSyncPrintf("\n");
            // "%s: %u bytes %s failed\n"
            osSyncPrintf("%s: %u bytes <%s failed>\n", name, size, action);
            __osDisplayArena(&sZeldaArena);
            osSyncPrintf("\n");
        }
    } else if (gZeldaArenaLogSeverity >= LOG_SEVERITY_VERBOSE) {
        osSyncPrintf("\n");
        // "%s: %u bytes %s succeeded\n"
        osSyncPrintf("%s: %u bytes <%s succeeded>\n", name, size, action);
        osSyncPrintf("\n");
    }
}

void* ZeldaArena_Malloc(u32 size) {
    void* ptr = __osMalloc(&sZeldaArena, size);

    ZeldaArena_CheckPointer(ptr, size, "zelda_malloc", "Secure"); // "Secure"
    return ptr;
}

void* ZeldaArena_MallocDebug(u32 size, const char* file, s32 line) {
    void* ptr = __osMallocDebug(&sZeldaArena, size, file, line);

    ZeldaArena_CheckPointer(ptr, size, "zelda_malloc_DEBUG", "Secure"); // "Secure"
    return ptr;
}

void* ZeldaArena_MallocR(u32 size) {
    void* ptr = __osMallocR(&sZeldaArena, size);

    ZeldaArena_CheckPointer(ptr, size, "zelda_malloc_r", "Secure"); // "Secure"
    return ptr;
}

void* ZeldaArena_MallocRDebug(u32 size, const char* file, s32 line) {
    void* ptr = __osMallocRDebug(&sZeldaArena, size, file, line);

    ZeldaArena_CheckPointer(ptr, size, "zelda_malloc_r_DEBUG", "Secure"); // "Secure"
    return ptr;
}

void* ZeldaArena_Realloc(void* ptr, u32 newSize) {
    ptr = __osRealloc(&sZeldaArena, ptr, newSize);
    ZeldaArena_CheckPointer(ptr, newSize, "zelda_realloc", "再Secure"); // "Re-securing"
    return ptr;
}

void* ZeldaArena_ReallocDebug(void* ptr, u32 newSize, const char* file, s32 line) {
    ptr = __osReallocDebug(&sZeldaArena, ptr, newSize, file, line);
    ZeldaArena_CheckPointer(ptr, newSize, "zelda_realloc_DEBUG", "再Secure"); // "Re-securing"
    return ptr;
}

void ZeldaArena_Free(void* ptr) {
    __osFree(&sZeldaArena, ptr);
}

void ZeldaArena_FreeDebug(void* ptr, const char* file, s32 line) {
    __osFreeDebug(&sZeldaArena, ptr, file, line);
}

void* ZeldaArena_Calloc(u32 num, u32 size) {
    void* ret;
    u32 n = num * size;

    ret = __osMalloc(&sZeldaArena, n);
    if (ret != NULL) {
        bzero(ret, n);
    }

    ZeldaArena_CheckPointer(ret, n, "zelda_calloc", "Secure"); // "Secure"
    return ret;
}

void ZeldaArena_Display() {
    osSyncPrintf("Zelda heap display\n"); // "Zelda heap display"
    __osDisplayArena(&sZeldaArena);
}

void ZeldaArena_GetSizes(u32* outMaxFree, u32* outFree, u32* outAlloc) {
    ArenaImpl_GetSizes(&sZeldaArena, outMaxFree, outFree, outAlloc);
}

void ZeldaArena_Check() {
    __osCheckArena(&sZeldaArena);
}

void ZeldaArena_Init(void* start, u32 size) {
    gZeldaArenaLogSeverity = LOG_SEVERITY_ERROR;
    __osMallocInit(&sZeldaArena, start, size);
}

void ZeldaArena_Cleanup() {
    gZeldaArenaLogSeverity = LOG_SEVERITY_ERROR;
    __osMallocCleanup(&sZeldaArena);
}

u8 ZeldaArena_IsInitalized() {
    return __osMallocIsInitalized(&sZeldaArena);
}
