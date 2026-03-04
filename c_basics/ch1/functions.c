#include <stdio.h>
#include <stdlib.h>
/*
 * A function is defined as:
 * type name (params) {
 *  declarations
 *  statements
 * }
 */

long long power(long long base, int n);

int main(int argc, char *argv[]){
    int i;
    int max_number;

    if (argc < 2) {
        printf("Usage: %s <max_number>\n", argv[0]);
        return 1;
    }

    max_number = atoi(argv[1]);

    for (i = 0; i < max_number; ++i) {
        printf("%d %lld %lld\n", i, power(2,i), power(-3,i));
    }

    return 0;
}

/*
 * This power function it's a simple example since it only
 * works with positive and small integers.
 * For a better implementation, you should use: pow(m,n) from
 * the standart library
 */

long long power(long long base, int n) {
    int i;
    long long p;

    p = 1; 

    for (i = 1; i <= n; ++i) {
        p = p * base;
    }
    return p;
}
