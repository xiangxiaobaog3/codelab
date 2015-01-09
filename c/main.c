#include <stdio.h>
#include <unistd.h>

#define dprint(expr) printf(#expr " = %d\n", expr)

int strlen_p(char *s)
{
    char *p = s;
    while (*p != '\0')
        p++;
    return p - s;
}

int strlen_s(char *s)
{
    int n;
    for (n = 0; *s != '\0'; s++)
    {
        n++;
    }
    return n;
}

void
test_pointer()
{
    int x = 1, y = 2, z[10];
    int *ip;  /* ip is a pointer to int */

    ip = &x;
    *ip = *ip + 1;
    printf("%d", *ip);
}

void 
swap(int v[], int i, int j)
{
    int temp;
    temp = v[i];
    v[i] = v[j];
    v[j] = temp;
}

void 
qsort(int v[], int left, int right)
{

    int i, last;
    if (left >= right)
        return;
    swap(v, left, (left + right)/2);
    last = left;

    for (i = left+1; i < right; ++i)
    {
        if (v[i] < v[left]) 
            swap(v, ++last, i);
    }
    swap(v, left, last);
    qsort(v, left, last-1);
    qsort(v, last+1, right);
}

void
printd(int n)
{
    if (n < 0) {
        putchar('-');
        n = -n;
    }

    if (n / 10)
        printd(n / 10);
    putchar(n % 10 + '0');
}


int main(int argc, char *argv[])
{
    /* printd(123); */
    /* int ns[] = {3, 2, 1, 5, 7}; */
    /* qsort(ns, 0, 5); */
    /* for (int i = 0; i < (sizeof(ns) / sizeof(int)); ++i) */
    /* { */
    /*     printf("%d", ns[i]); */
    /* } */
    /* printf("\n"); */
    /* int x, y = 10; */
    /* dprint(x+y); */
    char ss[] = "abcdefghij";
    char *ip;
    ip = &ss[5];
    /* ip = ss; */
    printf("%d", strlen_s(ip));
    /* test_pointer(); */
    return 0;
}
