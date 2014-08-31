// practice_with_pointers.cpp: 练习熟练指针

#include <iostream>

using namespace std;


// Passing parameters by reference
// void Duplicate(int& a, int& b, int& c) {
void Duplicate(int& a, int& b, int& c) {
    a *= 2;
    b *= 2;
    c *= 2;
}

void DoIt(int &foo, int goo) {
    foo = goo + 3;
    goo = foo + 4;
    foo = goo + 3;
    goo = foo;

}


// Do it in old c way
void Duplicate1(int *a, int *b, int *c) {
    *a *= 2;
    *b *= 2;
    *c *= 2;
}



int main() {
    int *intptr; // Declare a pointer that holds the address
    // of memory location that can store an integer.
    // Note of the use of * to indicate this is a pointer variable

    intptr = new int; // Allocate memory for the pointer.
    *intptr = 5; // store 5 in the memory address stored in intptr

    int *ptr;
    ptr = new int;
    *ptr = 5;
    *ptr = *ptr + 1;
    int myint = 5;

    int *ptr1;
    ptr1 = new int;
    float *ptr2 = new float; // do it all in one statement
    *ptr2 = 1.0;
    float *ptr3;
    ptr3 = ptr2;
    cout << *ptr3 << endl;
    cout << ptr3 << endl;
    cout << ptr2 << endl;

    delete ptr1; // free the storage;
    delete ptr2;
    cout << *ptr3 << endl;

    int x=1, y=3, z=7;
    Duplicate(x, y, z);

    cout << "x=" << x << ", y=" << y << ", z=" << z << endl;;

    Duplicate1(&x, &y, &z);

    cout << "x=" << x << ", y=" << y << ", z=" << z << endl;

    int *foo, *goo;
    foo = new int;
    *foo = 1;

    goo = new int;
    *goo = 3;
    *foo = *goo + 3; // foo = 6

    foo = goo; // assigment foo = 3;

    *goo = 5; // foo = goo = 5
    *foo = *goo + *foo; // foo = goo = 10

    DoIt(*foo, *goo);
    cout << (*foo) << endl;

    return 0;
}
