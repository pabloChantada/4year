#include <stdio.h>
#define MAXLINE 1000 /* maximum input line size */

int getline(char line[], int maxline);
void copy(char to[], char from[]);

int main(){
    int len; // Current line length
    int max; // Max length seen so far

    char line[MAXLINE]; // Initialize the array with the max line size, its the current input line array
    char longest[MAXLINE]; // This is the array that will hold the longest line

    max = 0;
    while ((len = getline(line, MAXLINE)) > 0) {
        // If the current line is greater than the max,
        // we copy the current line into the longest line array and update the max length
        if (len > max) {
            max = len;
            copy(longest, line);
        }
    if (max > 0) { // If there was a line, print the longest line
        printf("Current longest line: %s", longest);
    }
    return 0;
    }
}


// getline: read a line into s, return length
int getline(char s[], int lim) {
    int c, i;

    // We arent at the limit
    // We havent reached the end of the file
    // The current character is not a newline
    for (i=0; i < lim-1 && (c=getchar())!=EOF && c!='\n'; ++i) {
        // We add the current character to the array and increment the index
        s[i] = c;
    }
    // If the current character is a newline, we add it to the array and increment the index
    if (c == '\n') {
        s[i] = c;
        ++i;
    }
    // We add a null character to the end of the array to terminate the string
    s[i] = '\0';
    return i;
}

// copy: copy 'from' into 'to'; assume to is big enough
void copy(char to[], char from[]) {
    int i;

    i = 0;
    // We copy each character from the 'from' array to the 'to' array until we reach the null character
    while ((to[i] = from[i]) != '\0') {
        ++i;
    }
}
