int is_sorted(const int *arr, int len) {
    for (int i = 1; i < len; ++i) {
        if (arr[i-1] > arr[i]) return 0;
    }
    return 1;
}
