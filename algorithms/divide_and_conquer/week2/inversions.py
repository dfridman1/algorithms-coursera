import argparse



def count_inversions(array):
    if len(array) < 2:
        return array, 0
    mid = len(array) // 2
    left, left_inversions = count_inversions(array[:mid])
    right, right_inversions = count_inversions(array[mid:])
    array, cross_inversions = merge(left, right)
    return array, left_inversions + right_inversions + cross_inversions


def merge(left, right):
    array, inversions = [], 0
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] > right[j]:
            inversions += len(left) - i
            array.append(right[j])
            j += 1
        else:
            array.append(left[i])
            i += 1
    while i < len(left):
        array.append(left[i])
        i += 1
    while j < len(right):
        array.append(right[j])
        j += 1
    return array, inversions


def count_inversions_naive(array):
    inversions = 0
    for j in range(len(array)):
        for i in range(j):
            inversions += array[i] > array[j]
    return inversions


def read_data(filepath):
    with open(filepath, 'r') as fp:
        data = map(int, fp.read().splitlines())
    return list(data)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--in_file', default='data/data.txt')
    return parser.parse_args()


def main():
    args = parse_args()
    data = read_data(args.in_file)
    _, inversions = count_inversions(data)
    print(inversions)


if __name__ == '__main__':
    main()
