CC := gcc
CFLAGS := -Wall -Wextra -O2

BUILD_DIR := lib

SRC := $(wildcard src/nn/*.c)
INCLUDE_DIR := ./include/
OBJ := $(SRC:src/nn/%.c=$(BUILD_DIR)/%.o)

all: static dynamic

static: $(BUILD_DIR)/libnn.a
#	$(CC) $(MAIN) -L. -lmath -o main_static

$(BUILD_DIR)/libnn.a: $(OBJ)
	ar rcs $@ $^

dynamic: $(BUILD_DIR)/libnn.so
#	$(CC) $(MAIN) -L. -lmath -o main_shared

$(BUILD_DIR)/libnn.so: $(OBJ)
	$(CC) -shared -o $@ $^

$(BUILD_DIR)/%.o: src/nn/%.c include/nn/%.h
	@mkdir -p $(BUILD_DIR)
	$(CC) -fPIC -c $< -I$(INCLUDE_DIR) -o $@

clean:
	rm -rf lib 