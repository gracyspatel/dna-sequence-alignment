"""
Differential test: basic.py (Needleman-Wunsch) vs efficient.py (Hirschberg).

Checks the property that actually holds -- both algorithms find an alignment of the
same optimal cost. They do NOT generally return the same alignment strings: when two
alignments tie at the optimal cost, the two algorithms break the tie differently, so
string-level agreement is reported as an observation rather than asserted.

Usage:
    python3 compare.py [trials]
"""
import random
import sys

from basic import dp_align
from efficient import ALPHA, DELTA, hirschberg


def alignment_cost(a, b):
    return sum(DELTA if x == '_' or y == '_' else ALPHA[(x, y)] for x, y in zip(a, b))


def main():
    trials = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    random.seed(0)

    cost_matches = 0
    string_matches = 0
    failures = []

    for _ in range(trials):
        X = ''.join(random.choice('ACGT') for _ in range(random.randint(1, 80)))
        Y = ''.join(random.choice('ACGT') for _ in range(random.randint(1, 80)))

        basic_cost, basic_X, basic_Y = dp_align(X, Y)
        eff_X, eff_Y = hirschberg(X, Y)
        eff_cost = alignment_cost(eff_X, eff_Y)

        if basic_cost == eff_cost:
            cost_matches += 1
        else:
            failures.append((X, Y, basic_cost, eff_cost))

        if (basic_X, basic_Y) == (eff_X, eff_Y):
            string_matches += 1

        # Both outputs must also be consistent with their own input sequences.
        assert basic_X.replace('_', '') == X and basic_Y.replace('_', '') == Y
        assert eff_X.replace('_', '') == X and eff_Y.replace('_', '') == Y

    print(f"trials                        : {trials}")
    print(f"identical optimal cost        : {cost_matches}/{trials}")
    print(f"byte-identical alignment pair : {string_matches}/{trials} "
          f"({string_matches / trials * 100:.0f}%)")

    if failures:
        print(f"\nFAIL -- {len(failures)} cost mismatch(es):")
        for X, Y, bc, ec in failures[:5]:
            print(f"  basic={bc} efficient={ec}  X={X[:40]} Y={Y[:40]}")
        sys.exit(1)

    print("\nPASS -- Hirschberg matches the DP optimum on every trial.")
    print("Differing alignment strings are equally-optimal ties, not errors.")


if __name__ == '__main__':
    main()
