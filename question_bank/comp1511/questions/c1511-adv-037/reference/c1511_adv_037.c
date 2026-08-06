#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct buffer {
    int *data;
    size_t length;
    size_t capacity;
};

static void push(struct buffer *buffer, int value) {
    if (buffer->length == buffer->capacity) {
        size_t new_capacity = buffer->capacity == 0 ? 4 : buffer->capacity * 2;
        int *grown = realloc(buffer->data, new_capacity * sizeof *grown);
        if (grown == NULL) exit(1);
        buffer->data = grown;
        buffer->capacity = new_capacity;
    }
    buffer->data[buffer->length++] = value;
}

static int drop(struct buffer *buffer, int *value) {
    if (buffer->length == 0) return 0;
    *value = buffer->data[--buffer->length];
    return 1;
}

static void reverse_range(int *data, size_t left, size_t right) {
    while (left < right) {
        int temporary = data[left];
        data[left++] = data[right];
        data[right--] = temporary;
    }
}

static void roll(struct buffer *buffer, size_t amount) {
    if (buffer->length == 0) return;
    amount %= buffer->length;
    if (amount == 0) return;
    reverse_range(buffer->data, 0, buffer->length - 1);
    reverse_range(buffer->data, 0, amount - 1);
    reverse_range(buffer->data, amount, buffer->length - 1);
}

static void unique(struct buffer *buffer) {
    size_t write = 0;
    for (size_t read = 0; read < buffer->length; read++) {
        size_t earlier = 0;
        while (earlier < write && buffer->data[earlier] != buffer->data[read]) earlier++;
        if (earlier == write) buffer->data[write++] = buffer->data[read];
    }
    buffer->length = write;
}

static void print_buffer(const struct buffer *buffer) {
    if (buffer->length == 0) { puts("EMPTY"); return; }
    for (size_t i = 0; i < buffer->length; i++) {
        printf("%s%d", i == 0 ? "" : " ", buffer->data[i]);
    }
    putchar('\n');
}

int main(void) {
    struct buffer buffer = {NULL, 0, 0};
    char command[16];
    while (scanf("%15s", command) == 1) {
        if (strcmp(command, "END") == 0) break;
        if (strcmp(command, "PUSH") == 0) {
            int value;
            if (scanf("%d", &value) != 1) return 2;
            push(&buffer, value);
        } else if (strcmp(command, "DROP") == 0) {
            int value;
            if (drop(&buffer, &value)) printf("DROPPED %d\n", value);
            else puts("EMPTY");
        } else if (strcmp(command, "ROLL") == 0) {
            size_t amount;
            if (scanf("%zu", &amount) != 1) return 2;
            roll(&buffer, amount);
        } else if (strcmp(command, "UNIQUE") == 0) {
            unique(&buffer);
        } else if (strcmp(command, "PRINT") == 0) {
            print_buffer(&buffer);
        }
    }
    free(buffer.data);
    return 0;
}
