int sum_digits(int n) { int s=0; while(n) { s+=n%10; n/=10; } return s; }
