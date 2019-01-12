import argparse
import time
import numpy as np
np.random.seed(42)


def timedcall(f):
    def g(*args, **kwargs):
        start = time.process_time()
        result = f(*args, **kwargs)
        g.elapsed = time.process_time() - start
        print('{} took {} seconds.'.format(repr(f.__name__), g.elapsed))
        return result
    return g


@timedcall
def strassen_multiply(x, y, leaf_size=1):
    validate_input(x, y)
    return _strassen_multiply(x, y, leaf_size=leaf_size)


def _strassen_multiply(x, y, leaf_size):
    if x.shape[0] <= leaf_size or x.shape[1] <= leaf_size or y.shape[1] <= leaf_size:
        return _naive_multiply(x, y)
    m, n1, n2 = x.shape[0] // 2, x.shape[1] // 2, y.shape[1] // 2
    a, b, c, d = x[:m, :n1], x[:m, n1:], x[m:, :n1], x[m:, n1:]
    e, f, g, h = y[:n1, :n2], y[:n1, n2:], y[n1:, :n2], y[n1:, n2:]

    p1 = _strassen_multiply(a, f - h, leaf_size=leaf_size)
    p2 = _strassen_multiply(a + b, h, leaf_size=leaf_size)
    p3 = _strassen_multiply(c + d, e, leaf_size=leaf_size)
    p4 = _strassen_multiply(d, g - e, leaf_size=leaf_size)
    p5 = _strassen_multiply(a + d, e + h, leaf_size=leaf_size)
    p6 = _strassen_multiply(b - d, g + h, leaf_size=leaf_size)
    p7 = _strassen_multiply(a - c, e + f, leaf_size=leaf_size)

    q1 = p4 + p5 + p6 - p2
    q2 = p1 + p2
    q3 = p3 + p4
    q4 = p1 + p5 - p3 - p7

    return np.concatenate(
        [
            np.concatenate([q1, q2], axis=1),
            np.concatenate([q3, q4], axis=1)
        ],
        axis=0
    )


@timedcall
def naive_multiply(x, y):
    validate_input(x, y)
    return _naive_multiply(x, y)


def _naive_multiply(x, y):
    output = np.zeros(shape=(x.shape[0], y.shape[1]), dtype=x.dtype)
    for r in range(x.shape[0]):
        for c in range(y.shape[1]):
            t = 0
            for k in range(x.shape[1]):
                t += x[r, k] * y[k, c]
            output[r, c] = t
    return output


def validate_input(x, y):
    assert x.ndim == 2 and y.ndim == 2 and x.shape[1] == y.shape[0]


def random_matrices(n, max_value):
    assert n > 0 and max_value > 0
    x = np.random.randint(-max_value, max_value+1, size=(n, n))
    y = np.random.randint(-max_value, max_value+1, size=(n, n))
    return x, y


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--n', type=int, default=128)
    parser.add_argument('--leaf_size', type=int, default=8)
    parser.add_argument('--max_value', type=int, default=100)
    return parser.parse_args()


def main():
    args = parse_args()
    assert (args.n & (args.n - 1)) == 0, "n must be a power of 2"
    x, y = random_matrices(n=args.n, max_value=args.max_value)
    p1 = naive_multiply(x, y)
    p2 = strassen_multiply(x, y, leaf_size=args.leaf_size)
    print(np.array_equal(p1, p2))


if __name__ == '__main__':
    main()
