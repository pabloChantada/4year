#include <stdio.h>

void main() {
    float fahr, celsius;
    float lower, upper, epoch;

    lower = -17.8;
    upper = 148.9;
    epoch = 30;

    celsius = lower;
    printf("Celsius \t Fahr\n");
    while (celsius <= upper) {
        fahr = (9.0f / 5.0f) * celsius + 32.0f;
        printf("%7.1f\t%6.1f\n", celsius, fahr);
        celsius = celsius + epoch;
    }
}