# This script compiles all .c files in the current directory to assembly with three optimization levels (O0, Ofast, Os)
# and stores the output in ../ASM/<opt_level>/<filename>.s

C_DIR="."
ASM_ROOT="../ASM"
OPTS=("O0" "Ofast" "Os")

# Create ASM subfolders if they don't exist
for opt in "${OPTS[@]}"; do
    mkdir -p "$ASM_ROOT/$opt"
done

for cfile in "$C_DIR"/*.c; do
    base=$(basename "$cfile" .c)
    for opt in "${OPTS[@]}"; do
        gcc -S -$opt "$cfile" -o "$ASM_ROOT/$opt/$base.s"
    done
done
