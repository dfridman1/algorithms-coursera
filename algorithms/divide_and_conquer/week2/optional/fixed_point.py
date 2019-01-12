import argparse
import numpy as np
np.random.seed(42)

from algorithms.utils import timedcall


@timedcall
def fixed_point(array):
    lo, hi = 0, len(array)
    while hi-lo > 1:
        mid = (lo + hi) >> 1
        if array[mid] > mid:
            hi = mid
        else:
            lo = mid
    return lo if hi-lo == 1 and array[lo] == lo else None


@timedcall
def fixed_point_naive(array):
    for i, x in enumerate(array):
        if i == x:
            return i
    return -1


def create_array(n):
    assert n > 0
    enforce_fixed_point = np.random.randint(0, 2) == 0
    if enforce_fixed_point:
        fixed_p = np.random.choice(n)
        array = [fixed_p] * n
        if fixed_p > 0:
            array[:fixed_p] = np.random.choice(np.arange(-2*n, fixed_p), size=fixed_p, replace=False)
        if n-fixed_p-1 > 0:
            array[fixed_p+1:] = np.random.choice(np.arange(fixed_p+1, 2*n), size=n-fixed_p-1, replace=False)
    else:
        array = np.random.choice(np.arange(-n//4, 4*n+1), size=n, replace=False)
    assert len(set(array)) == n
    return sorted(array)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--n', type=int, default=10000)
    return parser.parse_args()


def main():
    args = parse_args()
    assert args.n > 0
    array = create_array(n=args.n)

    fixed_pt = fixed_point(array)
    fixed_pt_naive = fixed_point_naive(array)
    assert fixed_pt * fixed_pt_naive >= 0  # otherwise, one of the algorithms returns -1
    print(fixed_pt)


if __name__ == '__main__':
    main()
