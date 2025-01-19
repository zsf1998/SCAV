int add(int num1, int num2) 
{
  return num1 + num2; 
} 

int add(int num1, int num2, int num3) 
{
  return num1 + num2 + num3; 
} 

int main(int argc, char**) 
{ 
  int i = 42; 

  return add(argc, add(42, i), 4 * 7); 
}
