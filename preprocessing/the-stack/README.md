# EDA on The Stack (v1)

The `main.py` script contains a CLI tool and two utility functions to download and assemble source
C files into assemblies whenever possible, while also optionally collecting very basic EDA statistics
on file size of the sources and assemblies.

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
python -m main -h
usage: main.py [-h] [--size-stats] {download,do,d,assemble,asm,a} ...

Download and assemble source c files from The Stack

positional arguments:
  {download,do,d,assemble,asm,a}
                        Download or assemble sources

options:
  -h, --help            show this help message and exit
  --stats               Path to file in which to store brief statistics for the process
```

Check usage reference for downloading via `python -m main <download|do|d> -h`
```bash
python -m main -h
usage: main.py download [-h] [--max_files MAX_FILES] dir max_size {KB,MB,GB}

positional arguments:
  dir                   Path to output directory of downloaded files
  max_size              Maximum size (in units) of downloaded content for the entire file collection
  {KB,MB,GB}            Unit of size to use when limiting download size (bytes)

options:
  -h, --help            show this help message and exit
  --max_files MAX_FILES
                        Maximum amount of files to download
```

Check usage reference for assembling via `python -m main <assemble|asm|a> -h`
```bash
usage: main.py assemble [-h] [--flags FLAGS] input_dir output_dir

positional arguments:
  input_dir      Path to directory where source C files directly reside under
  output_dir     Path to output directory of assembled files

options:
  -h, --help     show this help message and exit
  --flags FLAGS  Additional flags to pass to the GCC utility invocation
```

## Examples

For downloading unlimited source files with a net size of at most 10 GB into the `sources` folder:
```bash
python -m main download sources 10 GB
```

For something as similar as before, but limiting up to 500 files, and collecting their statistics
```bash
python -m main --stats stats.csv download --max-files 500 sources 10 GB
```

For assembling all source files under the `sources` folder into the `assemblies` folder:
```bash
python -m main assemble sources assemblies
```

For something as similar as before, but collecting their statistics and adding extra flags to `gcc`
```bash
python -m main --stats stats.csv --flags "-Wa,-L -Wall" sources assemblies
```

## Notes

You might want to redirect errors to their own log file, so they don't pollute the screen while
the CLI reports progress. You may do so redirecting the standard error stream (`stderr`) on your
shell of choice.

For example, on `zsh` or `bash`, one might do the following to redirect compilation error reports
to their own `error.log` file 
```bash
python -m main --stats stats.csv asm ./download ./asm 2> error.log
```

Aditionally, we rely on `gcc` reported return value as a signal of assembly success / failure.
If warnings or non-terminting errors are reported, one might get an undercount of successfully built
assembly code. By default, the `--flags` flag contains `-pass-exit-codes` to help mitigate this.
Consider including it into your own invocations