// a. Unary Operators
int test_unary_operators() {
    // Standard case
    int a = 5;
    int b = -a;
    debug b; // Expected: -5

    // Complex case
    int c = !0;
    debug c; // Expected: 1

    // Bottleneck case
    // int d = ~0;
    // debug d; // Expected: -1
    int e = -(-(-a));
    debug e; // Expected: -5

    return 0;
}

// b. Binary Operators
int test_binary_operators() {
    // Standard case
    int a = 5, b = 3;
    int c = a + b;
    debug c; // Expected: 8

    // Complex case
    int d = a * b;
    debug d; // Expected: 15

    // Bottleneck case
    int e = (a * b) / (a - b);
    debug e; // Expected: -15

    // // Additional bottleneck with many operations
    // int f = 1, g = 0;
    // for (int i = 0; i < 1000000; i++) {
    //     f = f * 2;
    //     g += f;
    // }
    // debug g; // Expected: large sum (overflow possible depending on int size)
    
    return 0;
}

// c. Expressions
int test_expressions() {
    // Standard case
    int b = 5, c = 3, d = 2;
    int result = (b + c) * d;
    debug result; // Expected: 16

    // Complex case (resultat decimal)
    int complex_result = (((b + c) * d) - d) / (b - c);
    debug complex_result; // Expected: Complex expression result = 7

    // Bottleneck case: deeply nested expressions (resultat decimal)
    int depth = (((((((b + c) * d) + d) - b) * c) + d) / d) * c;
    debug depth; // Expected: Deeply nested result = 61

    return 0;
}

// d. Loops
int test_loops() {
    // Standard case
    int i;
    for (i = 0; i < 3; i++) {
        debug i; // Expected: 0, 1, 2
    }

    // Complex case: Nested loops
    int j, sum = 0;
    for (i = 0; i < 10; i++) {
        for (j = 0; j < 10; j++) {
            sum += i * j;
        }
    }
    debug sum; // Expected: Sum of 10x10 matrix of i*j = 2025

    // Bottleneck case: large iteration loop
    int large_sum = 0;
    for (i = 0; i < 1000000; i++) {
        large_sum += i;
    }
    debug large_sum; // Expected: 499999500000

    return 0;
}

// e. Variables
int test_variables() {
    // Standard case
    int a = 10;
    debug a; // Expected: 10

    // Complex case: large array
    int arr[3] = {1, 2, 3};
    debug arr[2]; // Expected: 3

    // // Bottleneck case: 2D array
    // int matrix[100][100];
    // int sum = 0;
    // for (int i = 0; i < 100; i++) {
    //     for (int j = 0; j < 100; j++) {
    //         matrix[i][j] = i * j;
    //         sum += matrix[i][j];
    //     }
    // }
    // debug sum; // Expected: Sum of 100x100 matrix = 2025

    return 0;
}

// f. Instructions (if-else)
int test_instructions() {
    // Standard case
    int a = 5, b = 3;
    int result;
    if (a > b) {
        result = 1;
    } else {
        result = 0;
    }
    debug result; // Expected: 1

    // // Complex case
    // int large_conditional = 0;
    // for (int i = 0; i < 10000; i++) {
    //     if (i % 2 == 0) {
    //         large_conditional += i;
    //     }
    // }
    // debug large_conditional; // Expected: Sum of even numbers under 10000

    return 0;
}

// g. Functions
int add(int a, int b) {
    return a + b;
}

int test_functions() {
    // Standard case
    int result = add(5, 3);
    debug result; // Expected: 8

    // Complex case: multiple function calls
    int complex_result = add(add(5, 3), add(4, 2));
    debug complex_result; // Expected: 14

    // Bottleneck case: recursion
    int factorial(int n) {
        if (n <= 1) return 1;
        return n * factorial(n - 1);
    }

    int fact = factorial(10);
    debug fact; // Expected: 3628800

    return 0;
}

// h. Pointers
int test_pointers() {
    // Standard case
    int a = 10;
    int* p = &a;
    debug *p; // Expected: 10

    // Complex case: pointer arithmetic
    int arr[10] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9};
    int* ptr = arr;
    debug *(ptr + 5); // Expected: 5

    // Bottleneck case: pointer arithmetic in loop
    int sum = 0;
    for (int i = 0; i < 10; i++) {
        sum += *(ptr + i);
    }
    debug sum; // Expected: 45

    return 0;
}

// i. Library
int test_library() {
    // Standard case (no actual printf available, simulate)
    int hello = 1;
    debug hello; // Expected: 1

    // Bottleneck: large simulated library usage
    int lib_bottleneck = 0;
    for (int i = 0; i < 100000; i++) {
        lib_bottleneck += 1;
    }
    debug lib_bottleneck; // Expected: 100000

    return 0;
}

int main() {
    // Call all tests
    test_unary_operators();
    test_binary_operators();
    test_expressions();
    test_loops();
    test_variables();
    test_instructions();
    test_functions();
    test_pointers();
    test_library();

    return 0;
}
