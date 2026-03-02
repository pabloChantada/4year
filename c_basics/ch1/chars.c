#include <stdio.h>

/*
 * EOF is an integer defined in <stdio.h>, 
 * but the specific numeric value doesn't matter as long
 * as it is not the same as any char value.
 */
void old_main() {
    int c;

    c = getchar();  // Read a character from input
    // EOF -> end of file
    while (c != EOF) {
        putchar(c);     // Output the character read
        c = getchar();  // Read the next character from input until EOF is reached
    }
}

void main() {
    int c;

    while ((c = getchar()) != EOF) {
        printf("Value of expresion: %d\n", (c != EOF));
        printf("Value of EOF: %d\n", EOF);
        putchar(c);
    }
}
/**
 * A better way to write the loop is:
    main() {
        int c;

        while ((c = getchar()) != EOF) {
            putchar(c);
        }
 */