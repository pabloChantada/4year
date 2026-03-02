#include <stdio.h>

void main() {
    int c, nl, tabs, blanks;

    nl = 0;
    tabs = 0;
    blanks = 0;
    while ((c = getchar()) != EOF) {
        if (c == '\n') {
            ++nl;
        } else if (c == '\t') {
            ++tabs;
        } else if (c == ' ') {
            ++blanks;
        }
    }
    printf("New lines: %d\n", nl);
    printf("Tabs: %d\n", tabs);
    printf("Blanks: %d\n", blanks);
}