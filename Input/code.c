// // a. Unary Operators
// int test_unary_operators() {
	
//     // Standard case
//     int a;
//     a = 5;
//     int b;
//     b = -a;
//     debug b; // Expected: -5

	
//     // Complex case
//     int c;
//     c = !0;
//     debug c; // Expected: 1


//     // Bottleneck case
//     int e;
//     e = -(-(-a));
//     debug e; // Expected: -5

//     return 0;
// }

// // b. Binary Operators
// int test_binary_operators() {

//     // Standard case
//     int a;
// 	int b;
//     a = 5;
//     b = 3;
//     int c;
//     c = a + b;
//     debug c; // Expected: 8

//     // Complex case
//     int d;
//     d = a * b;
//     debug d; // Expected: 15

//     // Bottleneck case
//     int e;
//     e = (a * b) / (b - a);
//     debug e; // Expected: -7

// 	// // TODO : dependent on athoer feature
//     // // Additional bottleneck with many operations
//     // int f;
//     // int g;
//     // f = 1;
//     // g = 0;
//     // for (int i = 0; i < 1000000; i=i+1) {
//     //     f = f * 2;
//     //     g = g + f;
//     // }
//     // debug g; // Expected: large sum (overflow possible depending on int size)

//     return 0;
// }


// // c. Expressions
// int test_expressions() {

//     // Standard case
//     int b;
//     b = 5;
//     int c;
//     c = 3;
//     int d;
//     d = 2;
//     int result;
//     result = (b + c) * d;
//     debug result; // Expected: 16

//     // Complex case (resultat decimal)
//     int complex_result;
//     complex_result = (((b + c) * d) - d) / (b - c);
//     debug complex_result; // Expected: Complex expression result = 7

// 	// TODO : KO test giving 60 instead of 61
//     // Bottleneck case: deeply nested expressions (resultat decimal)
//     int depth;
//     depth = (((((((b + c) * d) + d) - b) * c) + d) / d) * c;
//     debug depth; // Expected: Deeply nested result = 61

//     return 0;
// }

// // d. Loops
// int test_loops() {
//     // Standard case
//     int i;
//     for (i = 0; i < 3; i=i+1) {
//         debug i; // Expected: 0, 1, 2
//     }

//     // Complex case: Nested loops
//     int j;
//     int sum;
//     sum = 0;
//     for (i = 0; i < 10; i=i+1) {
//         for (j = 0; j < 10; j=j+1) {
//             sum = sum + (i * j);
//         }
//     }
//     debug sum; // Expected: Sum of 10x10 matrix of i*j = 2025

//     // Bottleneck case: large iteration loop
//     int large_sum;
//     large_sum = 0;
//     for (i = 0; i < 10000;i=i+1) {
//         large_sum = large_sum+i;
//     }
//     debug large_sum; // Expected: 499999500
//     // break
//     int k;
//     for (k = 0; k < 10; k=k+1) {
//         if (k == 5) {
//             break;
//         }
//         debug k; // Expected: 0, 1, 2, 3, 4
//     }

//     // continue
//     int l;
//     for (l = 0; l < 10; l=l+1) {
//         if (l == 5) {
//             continue;
//         }
//         debug l; // Expected: 0, 1, 2, 3, 4, 6, 7, 8, 9
//     }

//     // while
//     int m;
//     m = 0;
//     debug 619;
//     while (m < 10) {
//         debug m; // Expected: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
//         m=m+1;
//     }

//     // do-while
//     int n;
//     n = 0;
//     debug 66191;
//     do {
//         debug n; // Expected: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
//         n=n+1;
//     } while (n < 10);
//     return 0;
// }

// // e. Variables
// int test_variables() {
//     // Standard case
//     int a;
//     a = 10;
//     debug a; // Expected: 10

//     // Complex case: large array
//     int arr[3];
//     arr[0] = 1;
//     arr[1] = 2;
//     arr[2] = 3;
//     debug arr[2]; // Expected: 3

//     // // Bottleneck case: 2D array
//     // int matrix[100][100];
//     // int sum = 0;
//     // for (int i = 0; i < 100; i=i+1) {
//     //     for (int j = 0; j < 100; j=j+1) {
//     //         matrix[i][j] = i * j;
//     //         sum += matrix[i][j];
//     //     }
//     // }
//     // debug sum; // Expected: Sum of 100x100 matrix = 2025

//     return 0;
// }

// // f. Instructions (if-else)
// int test_instructions() {
//     // Standard case
//     int a;
//     int b;
//     a = 5;
//     b = 3;
//     int result;
//     if (a < b) {
//         result = 1;
//     } else {
//         result = 0;
//     }
//     debug result; // Expected: 0

// 	// will not be used for the moment
//     // Complex case
//     int i;
//     int large_conditional;
//     large_conditional = 0;
//     for (i = 0; i < 11; i=i+1) {
//         if (i % 2 == 0) {
//             large_conditional = large_conditional + i;
//         }
//     }
//     debug large_conditional; // Expected: 30

//     return 0;
// }

// // g. Functions
// int add(int a, int b) {
//     return a + b;
// }
// // Bottleneck case: recursion
// int factorial(int n) {
//     if (n <= 1) return 1;
//     int res; 
//     res = factorial(n - 1);
//     res = res * n ;
//     return res;
// }

// int test_functions() {
//     // Standard case
//     int result;
//     result = add(5, 3);
//     debug result; // Expected: 8

//     // Complex case: multiple function calls
//     int complex_result;
//     complex_result = add(add(5, 3), add(4, 2));
//     debug complex_result; // Expected: 14

// 	// TODO : Cannot declare a function in a function
//     // Bottleneck case: recursion
//     int fact;
//     fact = factorial(10);
//     debug fact; // Expected: 3628800

//     return 0;
// }

// h. Pointers
int test_pointers() {
    // Standard case
    // int *tab;
    // tab = malloc(10*16);

    // tab[0] = 1;

    // int a;
    // a = tab[0];

    // debug a;  // Expected: 1

    // free(tab);
    
    int valeur;
    valeur = 42;         // Declare an int variable
    int *pointeur;
    pointeur = &valeur; // Create a pointer to the int variable

    // Print the value using the pointer
    debug *pointeur; // Dereference the pointer to get the value

    // Modify the value using the pointer
    *pointeur = 100; // Change the value of 'valeur' through the pointer

    // Print the modified value
    debug valeur; // Should print 100
    
    // // Complex case: pointer arithmetic
    // int arr[10] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9};
    // int* ptr = arr;
    // debug *(ptr + 5); // Expected: 5

    // // Bottleneck case: pointer arithmetic in loop
    // int sum;
    // sum = 0;
    // for (int i = 0; i < 10; i++) {
    //     sum += *(ptr + i);
    // }
    // debug sum; // Expected: 45

    return 0;
}

// // i. Library
// int test_library() {
//     return 0;
// }

int main() {
    
	//PASSED
    // test_unary_operators();
	
	//PASSED
    // test_binary_operators();
	
	//PASSED
    // test_expressions();
    
	//PASSED 
	// test_loops();
    
	//NOT TESTED TODO : Write tests 
	// test_variables();
    
	//PASSED
	// test_instructions();
    
	//PASSED but TODO : Cannot declare a function in a function
	// test_functions();

	//NOT TESTED
    test_pointers();
    
	//NOT TESTED
	// test_library();

    return 0;
}
