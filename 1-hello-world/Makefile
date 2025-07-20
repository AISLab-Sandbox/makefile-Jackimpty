BIN := hello

CC := gcc

CFLAGS := -Wall -Wextra -O2
INCLUDE_DIR := .
BUILD_DIR := build

SRC := hello.c
OBJ := $(BUILD_DIR)/$(SRC:.c=.o)

.PHONY: all run clean help

all: run

$(BUILD_DIR)/$(BIN): $(OBJ)
	$(CC) $^ -o $@

$(BUILD_DIR)/%.o: %.c
	@mkdir -p $(BUILD_DIR)
	$(CC) -c $(CFLAGS) $< -I$(INCLUDE_DIR) -o $@

run: $(BUILD_DIR)/$(BIN)
	./$(BUILD_DIR)/$(BIN)

clean:
	@rm -rf $(BUILD_DIR)

help:
	@echo "Available targets:"
	@echo ""
	@echo "  make all     - Compile and run (default)"
	@echo "  make run     - Compile and run the binary"
	@echo "  make clean   - Remove the build directory"
	@echo "  make help    - Show this help message"