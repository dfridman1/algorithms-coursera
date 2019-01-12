import argparse
import numpy as np
np.random.seed(42)

from algorithms.utils import timedcall


@timedcall
def unimodal_peak(array):
    lo, hi = 0, len(array)
    while hi-lo > 1:
        mid = (lo + hi) >> 1
        if array[mid] < array[mid-1]:
            hi = mid
        else:
            lo = mid
    return lo if hi-lo == 1 else None


@timedcall
def unimodal_peak_naive(array):
    return np.argmax(array) if len(array) > 0 else None


def create_unimodal_array(n):
    assert n > 0
    array = list(range(n))
    peak_index = np.random.choice(n)
    return array[:peak_index] + array[peak_index:][::-1]


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--n', type=int, default=10000000)
    return parser.parse_args()


def main():
    args = parse_args()
    assert args.n > 0
    array = create_unimodal_array(n=args.n)
    peak = unimodal_peak(array)
    naive_peak = unimodal_peak_naive(array)
    assert peak == naive_peak
    print(peak)


if __name__ == '__main__':
    main()
