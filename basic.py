"""
In this program, we will execute the basic version of sequence alignment using standard dynamic programming.

Time Complexity: O(m*n)
Space Complexity: O(m*n)
"""

import sys
import time
import psutil

DELTA = 30

ALPHA = {
    ('A','A'):0,   ('A','C'):110, ('A','G'):48,  ('A','T'):94,
    ('C','A'):110, ('C','C'):0,   ('C','G'):118, ('C','T'):48,
    ('G','A'):48,  ('G','C'):118, ('G','G'):0,   ('G','T'):110,
    ('T','A'):94,  ('T','C'):48,  ('T','G'):110, ('T','T'):0,
}


def read_input(path):
    with open(path, 'r') as fh:
        raw = [line.strip() for line in fh.readlines()]
    tokens = [t for t in raw if t]

    cursor = 0

    first_base = tokens[cursor]
    cursor += 1

    first_ops = []
    while cursor < len(tokens) and tokens[cursor].isdigit():
        first_ops.append(int(tokens[cursor]))
        cursor += 1

    second_base = tokens[cursor]
    cursor += 1

    second_ops = []
    while cursor < len(tokens):
        second_ops.append(int(tokens[cursor]))
        cursor += 1

    str1 = build_string(first_base, first_ops)
    str2 = build_string(second_base, second_ops)
    return str1, str2


def build_string(starter, operations):
    """
    We will repeatedly double a string by inserting a copy of itself
    at the given 0-indexed position.
    """
    result = starter
    for pos in operations:
        result = result[:pos+1] + result + result[pos+1:]
    return result



# The following is O(m*n) dynamic programming alignment

def dp_align(X, Y):
    rows = len(X)
    cols = len(Y)

    OPT = [[0] * (cols + 1) for _ in range(rows + 1)]

    for r in range(rows + 1):
        OPT[r][0] = r * DELTA
    for c in range(cols + 1):
        OPT[0][c] = c * DELTA

    for r in range(1, rows + 1):
        for c in range(1, cols + 1):
            option_match = OPT[r-1][c-1] + ALPHA[(X[r-1], Y[c-1])]
            option_gap_Y = OPT[r-1][c]   + DELTA
            option_gap_X = OPT[r][c-1]   + DELTA
            OPT[r][c] = min(option_match, option_gap_Y, option_gap_X)

    optimal_cost = OPT[rows][cols]

    out_X = []
    out_Y = []
    r, c = rows, cols

    while r > 0 or c > 0:
        if r > 0 and c > 0 and OPT[r][c] == OPT[r-1][c-1] + ALPHA[(X[r-1], Y[c-1])]:
            out_X.append(X[r-1])
            out_Y.append(Y[c-1])
            r -= 1
            c -= 1
        elif r > 0 and OPT[r][c] == OPT[r-1][c] + DELTA:
            out_X.append(X[r-1])
            out_Y.append('_')
            r -= 1
        else:
            out_X.append('_')
            out_Y.append(Y[c-1])
            c -= 1

    aligned_X = ''.join(out_X[::-1])
    aligned_Y = ''.join(out_Y[::-1])

    return optimal_cost, aligned_X, aligned_Y


# Resource measurement
def current_mem_kb():
    return psutil.Process().memory_info().rss / 1024


# Entry point
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python3 basic.py <input_file> <output_file>")
        sys.exit(1)

    input_path  = sys.argv[1]
    output_path = sys.argv[2]

    str1, str2 = read_input(input_path)

    mem_before = current_mem_kb()
    start_time = time.time()

    cost, alignment1, alignment2 = dp_align(str1, str2)

    end_time  = time.time()
    mem_after = current_mem_kb()

    time_ms = (end_time - start_time) * 1000.0
    mem_kb  = mem_after - mem_before

    with open(output_path, 'w') as out:
        out.write(str(cost)    + '\n')
        out.write(alignment1   + '\n')
        out.write(alignment2   + '\n')
        out.write(str(time_ms) + '\n')
        out.write(str(mem_kb)  + '\n')
