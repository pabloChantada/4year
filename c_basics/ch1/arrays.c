#include <stdio.h>

void main() {
    int c, i, nwhite, nother;   
    int ndigit[10];  // Array to count the number of occurrences of each digit

    nwhite = nother = 0;
    for (i = 0; i < 10; ++i) {
        ndigit[i] = 0;  // Initialize the count for each digit to 0
    }

    while ((c = getchar()) != EOF) {
        if (c >= '0' && c <= '9') {
            /**
             * Increments the count of a digit character in the ndigit array.
             * 
             * This line takes a character 'c' that represents a digit ('0' to '9'),
             * converts it to its corresponding array index by subtracting the ASCII value
             * of '0' (c - '0'), and increments the count stored at that index in the ndigit array.
             * 
             * For example:
             * - If c = '5', then c - '0' = 5, so ndigit[5] is incremented
             * - If c = '0', then c - '0' = 0, so ndigit[0] is incremented
             * 
             * This is commonly used in frequency counting programs to track how many times
             * each digit appears in the input.
             */
            ++ndigit[c - '0'];  // Increment the count for the corresponding digit
        } else if (c == ' ' || c == '\n' || c == '\t') {
            ++nwhite;  // Increment the count for whitespace characters
        } else {
            ++nother;  // Increment the count for other characters
        }
    }

    printf("Digits: ");
    for (i = 0; i < 10; ++i) {
        printf(" %d", ndigit[i]);  // Print the count for each digit
    }
    printf(", white space: %d, other: %d\n", nwhite, nother);  // Print the count for whitespace and other characters
}