.PHONY: all test lint format clean

CFLAGS ?= -std=c11 -Wall -Wextra -Wpedantic
CLANG_FORMAT ?= clang-format
SOURCES := $(wildcard src/*.c src/*.h tests/*.c)

all: build/proje

build:
	mkdir -p $@

build/proje: src/main.c src/topla.c src/topla.h | build
	$(CC) $(CPPFLAGS) $(CFLAGS) $(LDFLAGS) -o $@ src/main.c src/topla.c $(LDLIBS)

build/test_topla: tests/test_topla.c src/topla.c src/topla.h | build
	$(CC) $(CPPFLAGS) -Isrc $(CFLAGS) $(LDFLAGS) -o $@ tests/test_topla.c src/topla.c $(LDLIBS)

test: build/test_topla
	./build/test_topla

lint:
	$(CLANG_FORMAT) --dry-run --Werror $(SOURCES)

format:
	$(CLANG_FORMAT) -i $(SOURCES)

clean:
	$(RM) build/proje build/test_topla
