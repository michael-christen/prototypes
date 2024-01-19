#include <stdio.h>

#if 0
int main(int argc, char *argv[]) {
    printf("Hello World\n");
}
#endif

int foo (int *p);

int
main (void)
{
      int *p = 0;   /* null pointer */
        return foo (p);
}

int
foo (int *p)
{
      int y = *p;
        return y;
}
