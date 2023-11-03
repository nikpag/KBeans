SHELL=/bin/bash
CC=gcc
MPICC=mpicc
OPT=-O3
WARN=-Wall
LINKMATH=-lm
PRINT=-DPRINT_RESULTS
CONV=-DTEST_CONV

.PHONY: all
all: $(shell echo {jacobi,gauss,redblack}-{serial,mpi}-{debug,conv,noconv})

%-serial-debug: %-serial.c utils.c
	$(CC) $(OPT) $(PRINT) $(CONV) $^ -o $@ $(LINKMATH)

%-serial-conv: %-serial.c utils.c
	$(CC) $(OPT) $(CONV) $^ -o $@ $(LINKMATH)

%-serial-noconv: %-serial.c utils.c
	$(CC) $(OPT) $^ -o $@ $(LINKMATH)

%-mpi-debug: %-mpi.c utils.c
	$(MPICC) $(OPT) $(PRINT) $(CONV) $^ -o $@ $(LINKMATH)

%-mpi-conv: %-mpi.c utils.c
	$(MPICC) $(OPT) $(CONV) $^ -o $@ $(LINKMATH)

%-mpi-noconv: %-mpi.c utils.c
	$(MPICC) $(OPT) $^ -o $@ $(LINKMATH)

.PHONY: clean
clean:
	rm -f {jacobi,gauss,redblack}-{serial,mpi}-{debug,conv,noconv}
