"""
Measures CPU time and peak memory for both algorithms across problem sizes and
writes results.csv.

Memory is measured with tracemalloc (peak Python allocation during the call), not
an RSS delta. RSS is a noisy proxy -- it reflects whatever the allocator happened to
return to the OS -- whereas tracemalloc measures what the algorithm actually allocated,
which is the quantity the O(m*n) vs O(m+n) claim is about.

Usage:
    python3 benchmark.py
"""
import csv
import time
import tracemalloc

from basic import dp_align
from efficient import hirschberg

SIZES = [64, 128, 256, 512, 1024, 1536, 2048]
SEED_A = 'ACTG'
SEED_B = 'TACG'


def make_pair(target_len):
    X = (SEED_A * (target_len // len(SEED_A) + 1))[:target_len]
    Y = (SEED_B * (target_len // len(SEED_B) + 1))[:target_len]
    return X, Y


def measure(fn, X, Y):
    tracemalloc.start()
    start = time.perf_counter()
    fn(X, Y)
    elapsed_ms = (time.perf_counter() - start) * 1000.0
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return elapsed_ms, peak / 1024.0


def main():
    rows = []
    print(f"{'m+n':>6} {'basic ms':>10} {'eff ms':>10} {'basic KB':>12} "
          f"{'eff KB':>10} {'mem saved':>10} {'time cost':>10}")

    for size in SIZES:
        X, Y = make_pair(size)
        basic_ms, basic_kb = measure(dp_align, X, Y)
        eff_ms, eff_kb = measure(hirschberg, X, Y)

        mem_saved_pct = (1 - eff_kb / basic_kb) * 100
        time_ratio = eff_ms / basic_ms

        rows.append({
            'problem_size_m_plus_n': len(X) + len(Y),
            'basic_time_ms': round(basic_ms, 2),
            'efficient_time_ms': round(eff_ms, 2),
            'basic_peak_kb': round(basic_kb, 1),
            'efficient_peak_kb': round(eff_kb, 1),
            'memory_reduction_pct': round(mem_saved_pct, 1),
            'time_ratio_efficient_over_basic': round(time_ratio, 2),
        })

        print(f"{len(X)+len(Y):>6} {basic_ms:>10.1f} {eff_ms:>10.1f} {basic_kb:>12.1f} "
              f"{eff_kb:>10.1f} {mem_saved_pct:>9.1f}% {time_ratio:>9.2f}x")

    with open('results.csv', 'w', newline='') as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    best = max(r['memory_reduction_pct'] for r in rows)
    worst_time = max(r['time_ratio_efficient_over_basic'] for r in rows)
    print(f"\nwrote results.csv")
    print(f"peak memory reduction (largest input): {best:.1f}%")
    print(f"worst-case runtime penalty:            {worst_time:.2f}x slower")


if __name__ == '__main__':
    main()
