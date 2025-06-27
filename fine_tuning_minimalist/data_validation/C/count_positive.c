int count_positive(const int *arr, int len) {
    int count = 0;
    for (int i = 0; i < len; ++i) {
        if (arr[i] > 0) count++;
    }
    return count;
}
