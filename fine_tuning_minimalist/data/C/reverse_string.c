void reverse_string(char* s) { int l=0; while(s[l]) l++; for(int i=0;i<l/2;i++) { char t=s[i]; s[i]=s[l-1-i]; s[l-1-i]=t; } }
