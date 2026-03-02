#include <stdio.h>

void main() {
    float fahr, celsius;
    float lower, upper, epoch;

    lower = 0;
    upper = 300;
    epoch = 20;

    fahr = lower;
    printf("Fahr \t Celsius\n");
    while (fahr <= upper) {
        celsius = (5.0 / 9.0) * (fahr - 32.0);
        // %3.0f -> at least 3 char wide, no decimal
        // Among others, printf also recognizes %o for octal, 
        // %x for hexadecimal, %c for character, 
        // %s for character string and %% for itself.
        printf("%3.0f \t %6.1f\n", fahr, celsius);
        fahr = fahr + epoch;
    }
}