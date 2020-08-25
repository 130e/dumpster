#include<stdlib.h>
#include<stdio.h>
#include<time.h>

int main(int argc, char** argv)
{
  int can = atoi(argv[1]);
  srand(time(NULL));
  int rands[8];

  for (int i=0; i<7; i++) {
    rands[i] = rand();
  }

  can -= rands[1]+rands[5]+rands[2]-rands[3]+rands[7]+rands[4]-rands[6];

  printf("%x\n", can);
}
