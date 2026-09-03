#include "ki/original/ki15d_8802d5b0.h"

uint64_t ki15d_8802d5b0(uint64_t input)
{
    uint64_t a2 = (input << 63) >> 31;
    const uint64_t v1 = (input << 31) >> 32;
    uint64_t v0 = (input << 44) >> 32;

    a2 = (a2 | v1) ^ v0;
    v0 = (a2 >> 20) & UINT64_C(0x0fff);
    return v0 ^ a2;
}
