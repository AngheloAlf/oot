#ifdef __cplusplus
extern "C" {
#endif

#include "global.h"

#ifdef __cplusplus
}
#endif

#include "cpp_test.h"
#include "libcpp/cpp_vector.hpp"

void Test_Vector() {
    CppVector<int> example(ZeldaArena_Malloc, ZeldaArena_Realloc, ZeldaArena_Free);
    size_t i = 0;

    example.reserve(10);
    for (i = 0; i < 10; i++) {
        example.push_back(10-i);
    }


    for (i = 0; i < example.size(); i++) {
        osSyncPrintf("%i: %i\n", i, example[i]);
    }
}
