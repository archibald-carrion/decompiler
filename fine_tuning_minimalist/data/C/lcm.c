int lcm(int a, int b) { return a && b ? (a * b) / gcd(a, b) : 0; }
