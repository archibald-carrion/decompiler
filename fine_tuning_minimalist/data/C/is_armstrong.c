int is_armstrong(int n) { int t=n, s=0, d=0, p=1; while(t) { d++; t/=10; } t=n; while(t) { p=1; for(int i=0;i<d;i++) p*=t%10; s+=p; t/=10; } return s==n; }
