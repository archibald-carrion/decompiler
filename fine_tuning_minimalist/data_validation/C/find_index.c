int find_index(const int *arr, int len, int value) {
    for (int i = 0; i < len; ++i) {
        if (arr[i] == value) return i;
    }
    return -1;
}
