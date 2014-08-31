int foo(int n) {
    int p = 1; // c1              1
    int i = 1; // c1              1
    while (i<n) { // c2           n
        int j = 1; // c1          n - 1
        while (j < i) { // c2     
            p = p * j; // c1 + c3 1
            j = j + 1; // c1 + c4 1
        }
        i = i + 1;     // c1 + c4 n - 1
    }
    return p; // c5
}
