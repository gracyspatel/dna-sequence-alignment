# Sequence Alignment

Implementation of global DNA sequence alignment using two algorithms:

- **Basic Dynamic Programming (DP)**
- **Memory-Efficient Divide and Conquer (Hirschberg's Algorithm)**

This project compares the two approaches in terms of alignment cost, execution time, and memory usage. Both find an alignment of the same optimal cost; Hirschberg's trades a modest amount of runtime for a very large reduction in memory.

---

## Overview

The goal of this project is to solve the global sequence alignment problem efficiently. Two different algorithms are implemented:

1. **Basic Dynamic Programming**
   - Uses the full dynamic programming table.
   - Straightforward implementation.
   - Higher memory consumption.

2. **Memory-Efficient Divide and Conquer**
   - Implements Hirschberg's algorithm.
   - Produces an alignment of the same optimal cost.
   - Significantly reduces memory usage by storing only the required DP rows.

The project also evaluates the practical performance of both algorithms by measuring CPU time and peak memory usage across different input sizes.

---

## Project Structure

```
Sequence-Alignment/
│
├── basic.py          # Basic Dynamic Programming implementation
├── efficient.py      # Hirschberg's memory-efficient implementation
├── basic.sh          # Runs the basic implementation
├── efficient.sh      # Runs the efficient implementation
├── compare.py        # Differential test: both algorithms vs. the DP optimum
├── benchmark.py      # Time/memory sweep across input sizes -> results.csv
├── results.csv       # Measured output of benchmark.py
├── sample_input.txt  # Small example in the input format described below
└── Summary.pages     # Project report
```

---

## Algorithms

### 1. Basic Dynamic Programming

The standard Needleman-Wunsch algorithm constructs the complete dynamic programming table and performs traceback to recover the optimal alignment.

**Complexity**

- Time: **O(m × n)**
- Space: **O(m × n)**

---

### 2. Memory-Efficient Divide & Conquer

The second implementation uses Hirschberg's algorithm, which recursively divides the alignment problem into smaller subproblems while storing only two rows of the DP table at any time.

**Complexity**

- Time: **O(m × n)**
- Space: **O(m + n)**

---

## Scoring Scheme

### Gap Penalty

```
30
```

### Mismatch Cost Matrix

|     | A | C | G | T |
|-----|---:|---:|---:|---:|
| **A** | 0 |110|48|94|
| **C** |110|0|118|48|
| **G** |48|118|0|110|
| **T** |94|48|110|0|

---

## Input Format

The input file contains compressed sequence information.

Each sequence is generated from:

- An initial DNA string
- A list of insertion indices

The program reconstructs the complete DNA sequences before performing global alignment.

---

## Running the Project

`sample_input.txt` is included so both commands run as-is. Both print an optimal cost of
`660` on it.

### Basic Algorithm

```bash
./basic.sh sample_input.txt output.txt
```

or

```bash
python3 basic.py sample_input.txt output.txt
```

### Memory-Efficient Algorithm

```bash
./efficient.sh sample_input.txt output.txt
```

or

```bash
python3 efficient.py sample_input.txt output.txt
```

---

## Output

The output file contains:

- Minimum alignment cost
- First aligned sequence
- Second aligned sequence
- Execution time
- Peak memory usage

---

## Performance Comparison

Reproduce with `python3 benchmark.py`, which writes `results.csv`. Peak memory is measured
with `tracemalloc` (actual allocation during the call) rather than an RSS delta, since RSS
reflects allocator behaviour rather than what the algorithm asked for.

| m + n | Basic time | Efficient time | Basic peak | Efficient peak | Memory saved | Time cost |
|---:|---:|---:|---:|---:|---:|---:|
| 128 | 4.0 ms | 6.6 ms | 147 KB | 14 KB | 90.4% | 1.67x |
| 512 | 47.7 ms | 89.1 ms | 2,337 KB | 38 KB | 98.4% | 1.87x |
| 1024 | 300.9 ms | 419.4 ms | 9,292 KB | 76 KB | 99.2% | 1.39x |
| 2048 | 1,455.9 ms | 1,914.2 ms | 37,026 KB | 151 KB | 99.6% | 1.31x |
| 4096 | 6,422.0 ms | 8,697.2 ms | 147,786 KB | 299 KB | **99.8%** | 1.35x |

### CPU Time

Both algorithms are **O(m × n)** in time. In practice Hirschberg's is **1.3–1.9x slower**,
because the divide step recomputes forward and backward cost rows at every level of the
recursion. That is the expected trade: it buys asymptotically lower memory by doing more
arithmetic, not less.

### Memory Usage

The basic DP implementation holds the full **O(m × n)** table; Hirschberg's keeps only
**O(m + n)** rows. The gap widens with input size — 90% at m+n=128, **99.8% at m+n=4096**
(147.8 MB down to 0.3 MB) — because the basic table grows quadratically while the efficient
one grows linearly.

### Correctness

`python3 compare.py` runs a randomized differential test against the DP optimum:

```
trials                        : 200
identical optimal cost        : 200/200
byte-identical alignment pair : 48/200 (24%)
```

Both algorithms always agree on the **optimal cost**. They frequently return *different*
alignment strings, and that is correct behaviour, not a bug: when several alignments tie at
the optimal cost, the full-table traceback and the recursive split break the tie differently.
Any claim that the two produce byte-identical alignments would be false — the guarantee is
cost-optimality, not a unique alignment.

---

## Requirements

- Python 3.x
- `psutil` — used by `basic.py` and `efficient.py` to report peak memory in their output files

```bash
pip install psutil
```

The alignment algorithms themselves use only the standard library; `benchmark.py` and
`compare.py` need no third-party packages beyond that.

---

## Applications

- DNA sequence alignment
- Computational biology
- Bioinformatics
- Genome comparison
- Evolutionary analysis

---

## References

- Needleman, S. B., & Wunsch, C. D. (1970). *A General Method Applicable to the Search for Similarities in the Amino Acid Sequence of Two Proteins.*
- Hirschberg, D. S. (1975). *A Linear Space Algorithm for Computing Maximal Common Subsequences.*

---

## Authors

Course project on Sequence Alignment implementing and comparing classical Dynamic Programming and Hirschberg's memory-efficient algorithm.