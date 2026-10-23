# Setup & Running Guide

Everything needed to get this project running and reproduce its results.

## Requirements

- **Python 3.x**
- **`psutil`** — used by `basic.py` and `efficient.py` to report peak memory

Install the dependency:

```bash
pip install psutil
```

No other third-party packages are needed. `basic.py` and `efficient.py` use
only the Python standard library beyond `psutil`; `compare.py` and
`benchmark.py` need nothing beyond that either.

> **Windows note:** if `python3` isn't recognized (it may resolve to a
> Microsoft Store install prompt instead of running Python), use `python`
> instead in all commands below. Check which one works with:
> ```bash
> python --version
> python3 --version
> ```

## Files in this project

| File | Purpose |
|---|---|
| `basic.py` | Basic Needleman-Wunsch dynamic programming alignment (O(mn) time, O(mn) space) |
| `efficient.py` | Hirschberg's linear-space divide-and-conquer alignment (O(mn) time, O(m+n) space) |
| `basic.sh` / `efficient.sh` | Shell wrappers around the two scripts above (POSIX shells only — use Git Bash or WSL on Windows, or just call the `.py` files directly) |
| `compare.py` | Randomized differential test: checks both algorithms always agree on optimal cost |
| `benchmark.py` | Sweeps input sizes, measures time + peak memory for both algorithms, writes `results.csv` |
| `results.csv` | Latest measured output of `benchmark.py` |
| `sample_input.txt` | Small example input in the compressed input format |
| `project_description.tex` | Write-up: problem statement, scoring scheme, algorithm details, complexity analysis |
| `results.tex` | Write-up of one specific `compare.py` + `benchmark.py` run's actual output |
| `Summary.pages` | Original project report (Apple Pages format) |

## Running the alignment algorithms

Both commands below run on the included `sample_input.txt` and print an
optimal alignment cost of **660**.

```bash
# Basic dynamic programming
python basic.py sample_input.txt basic_output.txt

# Hirschberg's memory-efficient algorithm
python efficient.py sample_input.txt efficient_output.txt
```

Each output file contains, one per line:
1. Minimum alignment cost
2. First aligned sequence
3. Second aligned sequence
4. Execution time (ms)
5. Peak memory usage (KB)

### Using your own input

Create a text file following the same format as `sample_input.txt`:

```
<seed string 1>
<insertion index>
<insertion index>
...
<seed string 2>
<insertion index>
...
```

Each sequence is a seed DNA string (over `A`, `C`, `G`, `T`) followed by a
list of 0-indexed positions where the string is spliced into itself,
roughly doubling its length each time. Then run either script with that
file as the input argument.

## Running the correctness check

```bash
python compare.py
```

Runs 200 random trials comparing both algorithms and asserts they always
agree on the optimal alignment cost (they are not required to produce
byte-identical alignment strings — see `results.tex` for why).

Optionally pass a trial count: `python compare.py 500`.

## Running the benchmark

```bash
python benchmark.py
```

Sweeps problem sizes `m+n = 128, 256, 512, 1024, 2048, 3072, 4096`, times
both algorithms, measures peak memory with `tracemalloc`, prints a summary
table, and overwrites `results.csv`. This can take a couple of minutes for
the larger sizes.

## Quick start (all of it)

```bash
pip install psutil
python basic.py sample_input.txt basic_output.txt
python efficient.py sample_input.txt efficient_output.txt
python compare.py
python benchmark.py
```
