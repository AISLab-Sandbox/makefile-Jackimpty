BIN := main

CC := gcc

# CFLAGS := -Wall -Wextra -O2
INCLUDE_DIR := $(PWD)/nn/include/
BUILD_DIR := build

SRC := main.c
OBJ := $(BUILD_DIR)/$(SRC:.c=.o)

.PHONY: all clean static dynamic


all:
	$(MAKE) -C nn

$(BUILD_DIR)/%.o: %.c
	@mkdir -p $(BUILD_DIR)
	$(CC) -c $(CFLAGS) $< -I$(INCLUDE_DIR) -o $@

static: $(OBJ) ./nn/lib/libnn.a
	$(CC) $< ./nn/lib/libnn.a -lm -o $(BUILD_DIR)/$(BIN)

./nn/lib/libnn.a:
	$(MAKE) -C nn static

dynamic: $(OBJ) ./nn/lib/libnn.so
	$(CC) $< -L$(PWD)/nn/lib -lm -lnn -Wl,-rpath,$(PWD)/nn/lib -o $(BUILD_DIR)/$(BIN)
#	$(CC) $< ./nn/lib/libnn.so -Wl,-rpath,$(PWD)/nn/lib -o $(BUILD_DIR)/$(BIN)
#	$(CC) $< ./nn/lib/libnn.so -o $(BUILD_DIR)/$(BIN)
#	export LD_LIBRARY_PATH=$(PWD)/nn/lib

./nn/lib/libnn.so:
	$(MAKE) -C nn dynamic

clean:
	@$(MAKE) -C nn clean
	@rm -rf $(BUILD_DIR)
