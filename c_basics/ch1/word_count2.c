#include <stdio.h>

#define IN 1  /* inside a word */
#define OUT 0 /* outside a word */

void main() {
    int c, nl, nw, nc, state;
    nl = nw = nc = 0;
    state = OUT;  // We start with the state of being outside a word

    // Read characters until EOF is reached
    while ((c = getchar()) != EOF) {
        // If we encounter a blank, new line or tab, we are outside a word
        if (c == ' ' || c == '\n' || c == '\t') {
            if (state == IN) {
                putchar('\n');
                state = OUT;
            }
        } else {
            putchar(c);
            state = IN;
        }
    }

    printf("Lines: %d\nWords: %d\nCharacters: %d\n", nl, nw, nc);
}