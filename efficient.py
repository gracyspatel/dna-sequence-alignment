"""
In this program, we shall execute the memory-efficient version of sequence alignment using divide-and-conquer with backward space optimization.

Time Complexity: O(m*n)
Space Complexity: O(m+n)
"""

import sys
import time
import psutil

# Penalty constants 
DELTA = 30

ALPHA = {
    ('A','A'):0,   ('A','C'):110, ('A','G'):48,  ('A','T'):94,
    ('C','A'):110, ('C','C'):0,   ('C','G'):118, ('C','T'):48,
    ('G','A'):48,  ('G','C'):118, ('G','G'):0,   ('G','T'):110,
    ('T','A'):94,  ('T','C'):48,  ('T','G'):110, ('T','T'):0,
}

# Input parsing — identical spec to basic.py

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
    result = starter
    for pos in operations:
        result = result[:pos+1] + result + result[pos+1:]
    return result



# Space-efficient alignment cost for one row

def last_row_costs(X, Y):
    num_cols = len(Y)

    # Previous row starts as the base case: aligning "" vs Y[0..j]
    prev_row = [j * DELTA for j in range(num_cols + 1)]

    for ch_x in X:
        curr_row = [0] * (num_cols + 1)
        curr_row[0] = prev_row[0] + DELTA         
        for j in range(1, num_cols + 1):
            take_both = prev_row[j-1] + ALPHA[(ch_x, Y[j-1])]
            skip_x    = prev_row[j]   + DELTA
            skip_y    = curr_row[j-1] + DELTA
            curr_row[j] = min(take_both, skip_x, skip_y)
        prev_row = curr_row

    return prev_row


# tiny sub-problem: full DP + traceback (used when either dim <= 1)

def small_dp(X, Y):
    rows, cols = len(X), len(Y)
    OPT = [[0] * (cols + 1) for _ in range(rows + 1)]

    for r in range(rows + 1):
        OPT[r][0] = r * DELTA
    for c in range(cols + 1):
        OPT[0][c] = c * DELTA

    for r in range(1, rows + 1):
        for c in range(1, cols + 1):
            OPT[r][c] = min(
                OPT[r-1][c-1] + ALPHA[(X[r-1], Y[c-1])],
                OPT[r-1][c]   + DELTA,
                OPT[r][c-1]   + DELTA,
            )

    out_X, out_Y = [], []
    r, c = rows, cols
    while r > 0 or c > 0:
        if r > 0 and c > 0 and OPT[r][c] == OPT[r-1][c-1] + ALPHA[(X[r-1], Y[c-1])]:
            out_X.append(X[r-1]); out_Y.append(Y[c-1])
            r -= 1; c -= 1
        elif r > 0 and OPT[r][c] == OPT[r-1][c] + DELTA:
            out_X.append(X[r-1]); out_Y.append('_')
            r -= 1
        else:
            out_X.append('_'); out_Y.append(Y[c-1])
            c -= 1

    return ''.join(out_X[::-1]), ''.join(out_Y[::-1])



# Hirschberg divide-and-conquer alignment
# Time: O(mn)   Space: O(m+n)

def hirschberg(X, Y):
    m, n = len(X), len(Y)

    # base cases
    if m == 0:
        return '_' * n, Y

    if n == 0:
        return X, '_' * m

    if m == 1 or n == 1:
        return small_dp(X, Y)

    # Divide step
    mid = m // 2

    
    fwd = last_row_costs(X[:mid], Y)
    bwd = last_row_costs(X[mid:][::-1], Y[::-1])

    # Find the column split in Y that minimises total cost
    best = float('inf')
    split = 0
    for col in range(n + 1):
        total = fwd[col] + bwd[n - col]
        if total < best:
            best  = total
            split = col

    #Conquer step
    left_X,  left_Y  = hirschberg(X[:mid],  Y[:split])
    right_X, right_Y = hirschberg(X[mid:],  Y[split:])

    return left_X + right_X, left_Y + right_Y


# Resource measurement
def current_mem_kb():
    return psutil.Process().memory_info().rss / 1024


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python3 efficient.py <input_file> <output_file>")
        sys.exit(1)

    input_path  = sys.argv[1]
    output_path = sys.argv[2]

    str1, str2 = read_input(input_path)

    mem_before = current_mem_kb()
    start_time = time.time()

    alignment1, alignment2 = hirschberg(str1, str2)

    end_time  = time.time()
    mem_after = current_mem_kb()

    # Compute cost from the aligned strings
    total_cost = 0
    for a, b in zip(alignment1, alignment2):
        if a == '_' or b == '_':
            total_cost += DELTA
        else:
            total_cost += ALPHA[(a, b)]

    time_ms = (end_time - start_time) * 1000.0
    mem_kb  = mem_after - mem_before

    with open(output_path, 'w') as out:
        out.write(str(total_cost) + '\n')
        out.write(alignment1      + '\n')
        out.write(alignment2      + '\n')
        out.write(str(time_ms)    + '\n')
        out.write(str(mem_kb)     + '\n')
