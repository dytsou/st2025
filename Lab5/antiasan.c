#include <stdint.h>

void antiasan(unsigned long addr) {
    const uintptr_t offset = 0x7fff8000u;
    uintptr_t base = (uintptr_t)addr;
    uintptr_t shadow = (base + 0x87u) >> 3;
    uintptr_t end = shadow + offset;

    end = (((base + 0x87u + 0x58u) >> 3) + offset);
    *(volatile unsigned char *)end = 0;

    end = (((base + 0x87u + 0x60u) >> 3) + offset);
    *(volatile unsigned char *)end = 0;
}