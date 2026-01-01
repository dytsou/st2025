CC=gcc

.PHONY: all run clean
all: bss_overflow_asan

bss_overflow_asan: bss_overflow.c libantiasan.so
	$(CC) -fsanitize=address -Og -g -o $@ $< -lantiasan -L.

libantiasan.so: antiasan.c
	$(CC) -g -fPIC -c antiasan.c
	$(CC) -shared antiasan.o -o libantiasan.so

run: bss_overflow_asan
	LD_LIBRARY_PATH=. ./bss_overflow_asan

clean:
	rm -f bss_overflow_asan antiasan.o libantiasan.so
