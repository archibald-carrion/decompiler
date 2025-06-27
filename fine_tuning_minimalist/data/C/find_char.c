int find_char(const char* s, char c) { int i = 0; while(s[i]) { if(s[i] == c) return i; i++; } return -1; }
