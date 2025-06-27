int is_palindrome(int n) { int r=0, t=n; while(t) { r=r*10+t%10; t/=10; } return n==r; }
