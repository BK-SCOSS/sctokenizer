#include <stdio.h>
#include <conio.h>

void main()
{
    int i=0, s=0,n;
    printf("Nhap vao so n:");
    scanf("%d", &n);
    while(i++<n)
        s=s+i;
    printf("Tong la: %d\n", s);
    getch();
}