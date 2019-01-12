import time


def timedcall(f):
    def g(*args, **kwargs):
        start = time.process_time()
        result = f(*args, **kwargs)
        print('{} took {} seconds.'.format(repr(f.__name__), time.process_time() - start))
        return result
    return g
