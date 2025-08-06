CC := gcc
CFLAGS := -Wall -Wextra -O2

BUILD_DIR := build

SRC := $(wildcard *.c)
BIN := $(SRC:.c=)
EXE := $(SRC:%.c=$(BUILD_DIR)/%)

.PRECIOUS: $(BUILD_DIR)/%.o
.PHONY: all clean area log sqrt

all: $(EXE)

$(BUILD_DIR)/%.o: %.c
	@mkdir -p $(BUILD_DIR)
	$(CC) -c $< -o $@

$(BUILD_DIR)/%: $(BUILD_DIR)/%.o
	$(CC) $^ -o $@ -lm

area: $(BUILD_DIR)/area
	@$(BUILD_DIR)/area

log: $(BUILD_DIR)/log
	@$(BUILD_DIR)/log

sqrt:  $(BUILD_DIR)/sqrt
	@$(BUILD_DIR)/sqrt

clean:
	@rm -rf $(BUILD_DIR)

help:
	@echo ""
	@echo "Usage: make <target>"
	@echo ""
	@echo "Available targets:"
	@echo "  all     - Build all executables ($(BIN))"
	@echo "  clean   - Remove all build output in '$(BUILD_DIR)'"
	@echo "  help    - Show this help message"
	@for bin in $(BIN); do \
		echo "  $$bin    - Build and run build/$$bin (if target defined)"; \
	done