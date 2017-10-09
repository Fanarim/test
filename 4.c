#include <stddef.h>
#include <stdio.h>
#include <string.h>


int main(){
  // 2 variables
  char str[] = "ABCDEFG";

  int tmp, i;

  for (i = 0; i < strlen(str)/2; i++){
      tmp = str[i];
      str[i] = str[strlen(str)-i-1];
      str[strlen(str)-i-1] = tmp;
  }

  printf("%s\n", str);


  // not exactly "in place", "ABCDEFG" is read-only string literal
  // 3 variables
  char* str2 = "ABCDEFG";
  int length = strlen(str2);
  char reversed[length];

  for (i = 0; i < length; i++){
    reversed[length-i-1] = *str2;
    str2++;
  }

  str2 = reversed;
  printf("%s\n", str2);

  return 0;
}
