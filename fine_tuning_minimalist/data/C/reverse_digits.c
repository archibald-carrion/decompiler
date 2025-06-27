int reverse_digits(int n) { int r = 0; while(n) { r = r * 10 + n % 10; n /= 10; } return r; }
