BIN := main

CC := gcc

RELEASE_FLAGS := -O2
DEBUG_FLAGS := -Wall -Wextra -g
INCLUDE_DIR := $(PWD)/nn/include/
BUILD_DIR := build

SRC := main.c
OBJ := $(BUILD_DIR)/$(SRC:.c=.o)

.PHONY: all clean static dynamic debug run help

all: CFLAGS:=$(RELEASE_FLAGS)
all: dynamic

debug: CFLAGS:=$(DEBUG_FLAGS)
debug: 
	$(MAKE) -C nn CFLAGS="$(CFLAGS)"

run: dynamic $(BUILD_DIR)/$(BIN)
	$(BUILD_DIR)/$(BIN)

$(BUILD_DIR)/%.o: %.c
	@mkdir -p $(BUILD_DIR)
	$(CC) -c $(CFLAGS) $< -I$(INCLUDE_DIR) -o $@

static: $(OBJ) ./nn/lib/libnn.a
	$(CC) $< ./nn/lib/libnn.a -lm -o $(BUILD_DIR)/$(BIN)

./nn/lib/libnn.a:
	$(MAKE) -C nn static

dynamic: $(OBJ) ./nn/lib/libnn.so
	$(CC) $< -L$(PWD)/nn/lib -lm -lnn -Wl,-rpath,$(PWD)/nn/lib -o $(BUILD_DIR)/$(BIN)

./nn/lib/libnn.so:
	$(MAKE) -C nn CFLAGS=$(CFLAGS) dynamic

clean:
	@$(MAKE) -C nn clean
	@rm -rf $(BUILD_DIR)

help:
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@echo "  all         Build the project using release flags (-O2) and dynamic library"
	@echo "  debug       Build the project using debug flags (-Wall -Wextra -g)"
	@echo "  run         Run the dynamically linked executable after building it"
	@echo "  static      Build the project using the static library"
	@echo "  dynamic     Build the project using the dynamic library"
	@echo "  clean       Clean all build artifacts from both top-level and nn/"
	@echo "  help        Show all targets"