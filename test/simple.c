/* This is a 
 * multiline comment
 */
// This is a single line comment
#include <stdio.h>          //An include
	#include <stdlib.h>

#define SIZE 10
#define for_each_start(i, start, size)\
    for (i = start; i < size; i++)
#define for_each(i, size)\
    for_each_start(i, 0, size)

int i;
int i1, i2;
const int * const b;
static int eax;
volatile long long int d;
int a[SIZE];

void f1()
{
    int i;

    for_each(i, SIZE)
        printf("%d ", a[i]);
    printf("\n");
}

void f2()
{
    int i;

again:
    for_each_start(i, a[0], SIZE){
        printf("%d ", a[i]);
        if (a[i] < a[0])
            goto incr;
    }
    goto end;
incr:
    a[i]++;
    printf("\n");
    goto again;
end:
    printf("\n");
}

void f3()
{
    int i;

    for (i = 0; i < SIZE; i++)
        printf("%d ", a[i]);
    printf("\n");
}

int main(int argc, char **argv)
{
    int i;

    a[0] = SIZE - 5;
    for (i = 1; i < SIZE; i++)
        a[i] = a[i - 1] + 2;
    a[5] = 0;
    f1();
    f2();
    f3();
    return 0;
}

