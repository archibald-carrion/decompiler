int is_perfect(int n) { int s=1; for(int i=2;i<=n/2;i++) if(n%i==0) s+=i; return n>1 && s==n; }
