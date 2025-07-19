BIN := main

CC := gcc
RELEASE_FLAGS := -O2
DEBUG_FLAGS := -Wall -Wextra -g

INCLUDE_DIR := ./
LINK_DIR := ./
BUILD_DIR := build

SRC := $(wildcard *.c)
OBJ := $(SRC:%.c=$(BUILD_DIR)/%.o)

.PHONY: all clean debug

all: CFLAGS := $(RELEASE_FLAGS)
all: ./$(BUILD_DIR)/$(BIN)
	./$(BUILD_DIR)/$(BIN)

debug:CFLAGS := $(DEBUG_FLAGS)
debug: ./$(BUILD_DIR)/$(BIN)
	./$(BUILD_DIR)/$(BIN)


$(BUILD_DIR)/%.o: %.c
	@mkdir -p $(BUILD_DIR)
	$(CC) -c $(CFLAGS) $< -I$(INCLUDE_DIR) -o $@

$(BUILD_DIR)/$(BIN): $(OBJ)
	$(CC) $^ -L$(LINK_DIR) -o $@

clean:
	rm -rf $(BUILD_DIR)