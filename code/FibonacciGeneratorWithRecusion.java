import java.util.Scanner;

public class FibonacciGeneratorWithRecusion {

    private int generateFibonacciNumber(int n) {
        if (n <= 0) {
            return 0;
        }
        if (n == 1 || n == 2) {
            return 1;
        }
        return generateFibonacciNumber(n - 1) + generateFibonacciNumber(n - 2);
    }

    public static void main(String[] args) {
        FibonacciGeneratorWithRecusion fg = new FibonacciGeneratorWithRecusion();
        System.out.println("************** Fibonacci Series using recursion *****************");
        System.out.println("Enter number: ");
        int number = new Scanner(System.in).nextInt();
        for (int i = 0; i <= number; i++) {
            System.out.println(i + " -->  " + fg.generateFibonacciNumber(i) + " ");
        }
    }
}
