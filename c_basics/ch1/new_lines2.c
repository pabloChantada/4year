#include <stdio.h>

void main() {
    int c, count;
    count = 0;  

    while ((c = getchar()) != EOF) {
        // We encounter the first blank
        if (c == ' ') {
            ++count;
            // If there are more than 1 blanks, we omit them to print the char
            if (count == 1) {
                putchar(c);
            }
        } else {
            // Restart the count when we encounter a non-blank character
            count = 0;
            putchar(c);
        }
    }
}