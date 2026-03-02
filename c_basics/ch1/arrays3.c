#include <stdio.h>

void main() {
    int c, i;
    int freq[128];  // ASCII characters
    
    // Initialize array
    for (i = 0; i < 128; i++) {
        freq[i] = 0;
    }
    
    // Count character frequencies
    while ((c = getchar()) != EOF) {
        if (c < 128) {
            // Since c is a integer, we can use [c]
            // We update the int value in the list from 0 to 128
            ++freq[c]; 
        }
    }
    
    // Print histogram for printable characters
    for (i = 33; i < 127; i++) {  // printable ASCII (skip space for clarity)
        if (freq[i] > 0) {
            printf("%c: ", i);
            int j;
            for (j = 0; j < freq[i]; j++) {
                putchar('*');
            }
            putchar('\n');
        }
    }
    
    // Print space separately if it exists
    if (freq[' '] > 0) {
        printf("(space): ");
        int j;
        for (j = 0; j < freq[' ']; j++) {
            putchar('*');
        }
        putchar('\n');
    }
}
