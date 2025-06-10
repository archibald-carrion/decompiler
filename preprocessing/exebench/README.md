# EDA on The Stack (v1)

The `main.py` script contains a CLI tool and two utility functions to extract the source code for
C functions, and their x86 assemblies, into files while also optionally collecting very basic EDA statistics
on file correspondence

This is a work in progress.

## Requirements

| Dependency | Version | Description |
|------------|---------|-------------|
|  `python`  | `3.11.2` | Core dependencies, CLI and language support of `Python` |
|  `venv`  | `3.11.2` | Virtual environment support of `Python` |
|  `pip`  | `23.0.1` | Package manager for `Python` |
|  `gcc`  | `12.2.0-14` | GNU Compiler Collection support for compiling `C` code |

For a rundown of required `python` packages, check & install via `requirements.txt`

You may install them via `pip` as follows:
```bash
python -m pip install -r ./requirements.txt
```

## Usage

Check usage for CLI tool via `python -m main -h`. Refer to the usage hints:
```bash
usage: main.py [-h] [--stats STATS] [--max_entries MAX_ENTRIES] data_dir c_dir asm_dir max_size {KB,MB,GB}
main.py: error: argument --stats: expected one argument
```

## Examples

For processing unlimited source files with a net size of at most 10 GB into the `sources` folder:
```bash
python -m main ./download ./c ./asm 10 GB
```

For something as similar as before, but limiting up to 500 files, and collecting their statistics
```bash
python -m main --stats ./stats.csv --max-entires 500 ./download ./c ./asm 10 GB
```

## Notes

You might want to redirect errors to their own log file, so they don't pollute the screen while
the CLI reports progress. You may do so redirecting the standard error stream (`stderr`) on your
shell of choice.

For example, on `zsh` or `bash`, one might do the following to redirect compilation error reports
to their own `error.log` file 
```bash
python -m main --stats stats.csv ./download ./c ./asm 2> error.log
```
