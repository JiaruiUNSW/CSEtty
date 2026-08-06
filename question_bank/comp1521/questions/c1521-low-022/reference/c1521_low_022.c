#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>

int main(void) {
    int32_t a, b;
    if (scanf("%" SCNd32 " %" SCNd32, &a, &b) != 2) return 1;
    uint32_t ua = (uint32_t)a;
    uint32_t ub = (uint32_t)b;
    uint32_t sum = ua + ub;
    uint32_t sign_a = ua >> 31;
    uint32_t sign_b = ub >> 31;
    uint32_t sign_sum = sum >> 31;
    int32_t result;
    if (sign_a == 0 && sign_b == 0 && sign_sum == 1) {
        result = INT32_MAX;
    } else if (sign_a == 1 && sign_b == 1 && sign_sum == 0) {
        result = INT32_MIN;
    } else {
        result = (int32_t)sum;
    }
    printf("%" PRId32 "\n", result);
    return 0;
}
