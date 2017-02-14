#include <stdio.h>
#include <stdlib.h>

int testmain(int argc,char**argv)
{
    if(argc != 4)
    {
        fprintf(stderr,"Invalid parameter\n");
        return 1;
    }

    char* end = NULL;
    int a = strtol(argv[1],&end,10);
    if(*end)
    {
        fprintf(stderr,"Invalid parameter %p %cA\n",end,a);
        return 1;
    }

    int b = strtol(argv[2],&end,10);
    if(*end)
    {
        fprintf(stderr,"Invalid parameter B\n");
        return 1;
    }

    int c = strtol(argv[3],&end,10);
    if(*end)
    {
        fprintf(stderr,"Invalid parameter result\n");
        return 1;
    }

    if(c != add(a,b))
    {
        fprintf(stderr,"result not expect\n");
        return 1;
    }

    return 0;
}

int main(int argc,char**argv)
{
    return testmain(argc,argv);
}
