.PHONY: all run run1 run2 clean

all:
	@gcc -o chal chal.c

run: run1 run2

run1:
	@cat 1.txt | ./chal

run2:
	@cat 2.txt | ./chal

clean:
	rm -f chal
