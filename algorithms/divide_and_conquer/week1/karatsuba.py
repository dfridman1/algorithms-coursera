import argparse


def karatsuba(x, y):
    x, y = str(x), str(y)
    assert len(x) > 0 and len(y) > 0
    if len(x) == 1 or len(y) == 1:
        return int(x) * int(y)
    n_div_2 = min(len(x), len(y)) // 2
    a, b = x[:-n_div_2], x[-n_div_2:]
    c, d = y[:-n_div_2], y[-n_div_2:]
    ac = karatsuba(int(a), int(c))
    bd = karatsuba(int(b), int(d))
    ac_plus_ad = karatsuba(int(a) + int(b), int(c) + int(d)) - ac - bd
    return (10**(n_div_2*2)) * ac + (10**n_div_2) * ac_plus_ad + bd


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--x', type=int, default=3141592653589793238462643383279502884197169399375105820974944592)
    parser.add_argument('--y', type=int, default=2718281828459045235360287471352662497757247093699959574966967627)
    return parser.parse_args()


def main():
    args = parse_args()
    p = karatsuba(args.x, args.y)
    assert args.x * args.y == p
    print(p)


if __name__ == '__main__':
    main()
