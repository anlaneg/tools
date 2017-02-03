#include "module.h"
#include <stdio.h>

int init1(void)
{
    printf("hello one\n");
    return 0;
}

int destory(void)
{
    printf("bye bye\n");
    return 0;
}

int init2(void)
{
    printf("hello two\n");
    return 0;
}

int init3(void)
{
    printf("hello three\n");
    return 0;
}

int main(int argc,char**argv)
{
    return 0;
}

module_init(1,init1);
module_init(2,init2);
module_init(3,init3);
module_destory(3,destory);
