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

void ifs()
{
	int i, j, k;

	if (0) {
		if (i < 3)
			j++;

		if (i < 4)
			j++;
		else
			k++;

		if (i < 4)
			if (j < 5)
				j++;
			else
				k++;

		if (i < 4)
			if (j < 5)
				j++;
			else
				k++;
		else
			k--;

		if (i < 4)
			k--;
		else
			if (j < 5)
				j++;
			else
				k++;

		if (i < 4)
			if (j < 5)
				j--;
			else
				k--;
		else
			if (j < 5)
				j++;
			else
				goto l;
	} else {
		if (i < 3) {
			j = 2 + 3;
			j = 2 & 3;
			j = 2 || 3;
		}

		if (i < 4) {
			j++;
		} else {
			k++;
		}

		if (i < 4) {
			if (j < 5) {
l:
				j++;
			} else {
				k++;
			}
		}

		if (i < 4) {
			if (j < 5) {
				j++;
			}
		} else {
			k++;
		}

		if (i < 4) {
			if (j < 5) {
				j++;
			} else {
				k++;
			}
		} else {
			k--;
		}

		if (i < 4) {
			k--;
		} else {
			if (j < 5) {
				j++;
			} else {
				k++;
			}
		}

		if (i < 4) {
			if (j < 5) {
				j--;
			} else {
				k--;
			}
		} else {
			if (j < 5) {
				j++;
			} else {
				k++;
				goto l;
			}
		}
	}

	i++;

	if (i)
		i++;
	i--;
}

void test_goto()
{
	int i;

	i = 0;
l:
	i++;
	if (i < 5)
		goto l;
	i = 42;
	goto end;
end:
	i = i;
}

int many_rets()
{
	int i;

	return 1;
	if (1)
		return 3;
	else
		return 4;
	i++;
	i >>= 2 + 3 ^ 4 + 0 ? 1 : 2;
	return 2;
}

int many_rets2()
{
	int i;

	if (1)
		return 3;
	else
		return 4;
	i++;
	i >>= 2 + 3 ^ 4 + 0 ? 1 : 2;
	return 2;
}

int many_rets3()
{
	int i;

	if (1)
		return 3;
	i++;
	i >>= 2 + 3 ^ 4 + 0 ? 1 : 2;
	return 2;
}

int simple_if()
{
	int i;

	if (1)
		i = 0;
	i++;
	i >>= 2 + 3 ^ 4 + 0 ? 1 : 2;
	return 2;
}

void test_while()
{
	int i;

	i = 0;

	while (i < 5) {
		i++;
		if (i > 2)
			i *= i % 2 ? 5 : 4;
	}
}

void test_do_while()
{
	int i;

	i = 0;

	do {
		i++;
	} while (i < 5);
}

void test_loops()
{
	int i, j, k, l;

	k = -5;

	for (i = 0; i < SIZE; i++) {
		j++;
		do {
			k = -j;
			j--;
			while (k++) {
				l = !l;
			}
		} while (j > i);
	}
}

void test_continue_and_break()
{
	int i;

	for (i = 0; i < SIZE; i++) {
		if (i < 3)
			continue;
		if (i > SIZE - 2)
			break;
	}
}

void test_while_if()
{
	int i;
	
	i = 0;

	while (i < 100) {
		i++;

		if (i < 5)
			i *= 2;

		i-= 2;
	}
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

