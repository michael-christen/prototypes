#include<iostream>
#include<typeinfo>

int main() {
  float x = 5;
  decltype(x) y = 2;
  ::std::cout << "Hello " << typeid(y).name() << ::std::endl;
}
