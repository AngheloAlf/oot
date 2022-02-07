#ifndef CPP_VECTOR_HPP
#define CPP_VECTOR_HPP

#ifdef __cplusplus
extern "C" {
#endif

#include "ultra64.h"

#define REAL_ASSERT_MACRO
#include "macros.h"

#ifdef __cplusplus
}
#endif

template <typename T> class CppVector {
    T* _arr;
    u32 _capacity;
    u32 _current;

    typedef void* (*AllocatorType)(u32);
    typedef void* (*ReallocatorType)(void*, u32);
    typedef void  (*DeallocatorType)(void*);

    AllocatorType _allocatorCallback;
    ReallocatorType _reallocatorCallback;
    DeallocatorType _deallocatorCallback;

public:
    CppVector(AllocatorType alloc, ReallocatorType realloc, DeallocatorType dealloc) noexcept {
        _allocatorCallback = alloc;
        _reallocatorCallback = realloc;
        _deallocatorCallback = dealloc;

        _current = 0;
        _capacity = 5;
        osSyncPrintf("Vector: Allocating %i elements of size %i bytes each. Total: %i bytes\n", _capacity, sizeof(T), sizeof(T) * _capacity);
        _arr = static_cast<T*>(_allocatorCallback(sizeof(T) * _capacity));
        ASSERT(_arr != nullptr, "_arr != nullptr", "", 0);

        osSyncPrintf("Vector: Allocated pointer %X\n", _arr);
    }

    ~CppVector() noexcept {
        osSyncPrintf("Vector: Destroying pointer %X\n", _arr);
        _deallocatorCallback(_arr);
    }

    void reserve(u32 new_capacity) noexcept {
        osSyncPrintf("Vector: reserve(%i)\n", new_capacity);
        if (new_capacity < _capacity) {
            return;
        }

        _capacity = new_capacity;
        _arr = static_cast<T*>(_reallocatorCallback(_arr, sizeof(T) * _capacity));
        ASSERT(_arr != nullptr, "_arr != nullptr", "", 0);
    }

    void push_back(T data) noexcept {
        if (_current == _capacity) {
            _capacity *= 2;
            _arr = static_cast<T*>(_reallocatorCallback(_arr, sizeof(T) * _capacity));
            ASSERT(_arr != nullptr, "_arr != nullptr", "", 0);
        }

        // Inserting data
        _arr[_current] = data;
        _current++;
    }

    T& operator[] (u32 pos) noexcept {
        return _arr[pos];
    }

    u32 size() noexcept {
        return _current;
    }

    u32 capacity() noexcept {
        return _capacity;
    }

};

#endif
