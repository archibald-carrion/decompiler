import polars as pl

def load_dataset():
    """
    Returns a sample Polars DataFrame containing pairs of C code and corresponding assembly code.
    """
    data = [
        {
            "c_code": "int add(int a, int b) { return a + b; }",
            "assembly_code": "add:\n    mov eax, edi\n    add eax, esi\n    ret"
        },
        {
            "c_code": "int mul(int x, int y) { return x * y; }",
            "assembly_code": "mul:\n    mov eax, edi\n    imul eax, esi\n    ret"
        }
    ]
    df = pl.DataFrame(data)
    return df