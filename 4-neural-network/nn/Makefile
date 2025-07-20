CC := gcc

BUILD_DIR := lib

SRC := $(wildcard src/nn/*.c)
INCLUDE_DIR := ./include/
OBJ := $(SRC:src/nn/%.c=$(BUILD_DIR)/%.o)

all: static dynamic

static: $(BUILD_DIR)/libnn.a

$(BUILD_DIR)/libnn.a: $(OBJ)
	ar rcs $@ $^

dynamic: $(BUILD_DIR)/libnn.so

$(BUILD_DIR)/libnn.so: $(OBJ)
	$(CC) -shared -o $@ $^  -lm

$(BUILD_DIR)/%.o: src/nn/%.c include/nn/%.h
	@mkdir -p $(BUILD_DIR)
	$(CC) -fPIC -c $(CFLAGS) $< -I$(INCLUDE_DIR) -o $@

clean:
	@rm -rf lib

help:
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@echo "  all        Build both static and dynamic libraries"
	@echo "  static     Build the static library: lib/libnn.a"
	@echo "  dynamic    Build the dynamic library: lib/libnn.so"
	@echo "  clean      Remove all generated object files and libraries"
	@echo "  help       Show all targets"