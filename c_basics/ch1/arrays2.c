#include <stdio.h>

#define MAX_WORD_LENGTH 15
#define IN 1
#define OUT 0

void main() {
    int c, i, j, state, word_length;
    int lengths[MAX_WORD_LENGTH];
    
    // Initialize the lengths array to 0
    for (i = 0; i < MAX_WORD_LENGTH; i++) {
        lengths[i] = 0;
    }
    
    state = OUT;
    word_length = 0;
    
    while ((c = getchar()) != EOF) {
        // If we encounter a blank, new line or tab, we are outside a word
        if (c == ' ' || c == '\n' || c == '\t') {
            if (state == IN) {
                // If the word length is less than MAX_WORD_LENGTH,
                // we increment the count for that length
                if (word_length < MAX_WORD_LENGTH) {
                    ++lengths[word_length];
                }
                word_length = 0;
                state = OUT;
            }
        } else {
            // We are inside a word, so we increment the word length
            state = IN;
            ++word_length;
        }
    }
    
    // Histogram of word lengths
    for (i = 1; i < MAX_WORD_LENGTH; i++) {
        printf("%2d: ", i);
        for (j = 0; j < lengths[i]; j++) {
            putchar('*');
        }
        putchar('\n');
    }
}
