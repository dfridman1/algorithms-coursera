import argparse
import numpy as np
import time
from collections import namedtuple

np.random.seed(42)


Point = namedtuple('Point', 'x y')


def timedcall(f):
    def g(*args, **kwargs):
        start = time.process_time()
        result = f(*args, **kwargs)
        print('{} took {} seconds.'.format(repr(f.__name__), time.process_time() - start))
        return result
    return g


@timedcall
def closest_pair(points, leaf_size=2):
    assert leaf_size >= 2
    if len(points) < 2:
        return None
    p_x = sorted(points, key=lambda point: point.x)
    p_y = sorted(points, key=lambda point: point.y)
    return _closest_pair(p_x, p_y, leaf_size=leaf_size)


def _closest_pair(p_x, p_y, leaf_size):
    if len(p_x) <= leaf_size:
        return _closest_pair_naive(p_x)
    mid = len(p_x) // 2
    l_x, r_x = p_x[:mid], p_x[mid:]
    l_y, r_y = _decompose(p_y, pivot=r_x[0].x)

    points = []
    pair = _closest_pair(l_x, l_y, leaf_size=leaf_size)
    if pair is not None:
        points.append(pair)
    pair = _closest_pair(r_x, r_y, leaf_size=leaf_size)
    if pair is not None:
        points.append(pair)
    delta = min(map(lambda pair: distance(*pair), points))
    pair = _closest_split_pair(p_x, p_y, delta=delta)
    if pair is not None:
        points.append(pair)
    return min(points, key=lambda pts: distance(*pts))


def _closest_split_pair(p_x, p_y, delta):
    pivot_point = p_x[len(p_x) // 2]
    lo, hi = pivot_point.x - delta, pivot_point.x + delta
    p_y = [p for p in p_y if lo <= p.x <= hi]
    best_pair, min_dist = None, delta
    for i, p in enumerate(p_y):
        for j in range(i+1, min(i+8, len(p_y))):
            q = p_y[j]
            dist = distance(p, q)
            if dist < min_dist:
                best_pair = (p, q)
                min_dist = dist
    return best_pair


def _decompose(p_y, pivot):
    l_y, r_y = [], []
    for p in p_y:
        (l_y if p.x < pivot else r_y).append(p)
    return l_y, r_y


@timedcall
def closest_pair_naive(points):
    return _closest_pair_naive(points)


def _closest_pair_naive(points):
    n = len(points)
    best_pair, min_dist = None, float('inf')
    for i in range(n):
        for j in range(i+1, n):
            dist = distance(points[i], points[j])
            if dist < min_dist:
                best_pair = (points[i], points[j])
                min_dist = dist
    return best_pair


def distance(point_a, point_b):
    return np.sqrt((point_a.x - point_b.x)**2 + (point_a.y - point_b.y)**2)


def random_points(size):
    assert size > 0
    xs = np.random.randn(size)
    ys = np.random.randn(size)
    points = [Point(x=x, y=y) for x, y in zip(xs, ys)]
    return points


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--n', type=int, default=512)
    parser.add_argument('--leaf_size', type=int, default=2)
    return parser.parse_args()


def main():
    args = parse_args()
    assert args.leaf_size >= 2 and args.n >= 2
    points = random_points(size=args.n)

    p, q = closest_pair(points)
    p_naive, q_naive = closest_pair_naive(points)
    assert distance(p, q) == distance(p_naive, q_naive)
    print(p, q)
    print('distance = {}'.format(distance(p, q)))


if __name__ == '__main__':
    main()
