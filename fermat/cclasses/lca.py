import ctypes as C
import os

class c_RMQ(C.Structure):
    _fields_ = [
        ('table', C.POINTER(C.c_double)),
        ('n', C.c_int),
        ('logn', C.c_int)
    ]


class c_LCA(C.Structure):
    _fields_ = [
        ('prev', C.POINTER(C.c_int)),
        ('et', C.POINTER(C.c_int)),
        ('n', C.c_int),
        ('root', C.c_int),
        ('distances', C.POINTER(C.c_double)),
        ('right', C.POINTER(C.c_int)),
        ('rmq', c_RMQ)
    ]

def init_fermat_c_lib():
    c_lib_path = os.path.join(os.path.dirname(__file__), 'lib', 'fermatlib.so')
    if os.path.isfile(c_lib_path):
        c_lib = C.CDLL(c_lib_path)

        c_lib.create_rmq.restype = c_RMQ

        c_lib.free_rmq.argtypes = [c_RMQ]

        c_lib.query_rmq.argtypes = [c_RMQ, C.c_int, C.c_int]
        c_lib.query_rmq.restype = C.c_double

        c_lib.create_lca.restype = c_LCA

        c_lib.free_lca.argtypes = [c_LCA]

        c_lib.get_distance.argtypes = [c_LCA, C.c_int, C.c_int]
        c_lib.get_distance.restype = C.c_double

        return c_lib

c_fl = init_fermat_c_lib()

class LCA:

    def __init__(self, root, prev, distances):
        prev[root] = root
        n = len(prev)
        assert len(distances) == n
        self.c_lca = c_fl.create_lca(
            C.c_int(root),
            (C.c_int * n)(*prev),
            C.c_int(n),
            (C.c_double * n)(*distances)
        )
        self.root = root
        
    def __del__(self):
        if self.c_lca:
            c_fl.free_lca(self.c_lca)

    def get_distance(self, a, b):
        return c_fl.get_distance(self.c_lca, a, b)

    def get_distances(self):
        res = (C.c_double * self.c_lca.n**2)()
        c_fl.get_distances(self.c_lca, res)
        return res

    def root_distance(self, a):
        return self.c_lca.distances[a]
        

class RMQ:

    def __init__(self, xs):
        n = len(xs)
        self.c_rmq = c_fl.create_rmq((C.c_double * n)(*xs), C.c_int(n))

    def query(self, x, y):
        return c_fl.query_rmq(self.c_rmq, x, y)

    def __del__(self):
        c_fl.free_rmq(self.c_rmq)


if __name__ == '__main__':
    xs = [3.809, 10.508, 8.391, 18.772, 4.527, 9.56, 17.068, 14.57, 16.965, 15.689]

    my_rmq = RMQ(xs)

    for x, y in [(0, 1), (0, 5), (1, 8), (0, 1), (0, 9), (8, 9)]:
        print("rmq({}, {}): {:3f}".format(x, y, my_rmq.query(x, y)))

    for _ in range(1000):
        my_rmq = RMQ(xs)

    prev = [0, 0, 1, 2, 2, 1, 0, 6]
    distances = [0, 1, 2, 3, 3, 2, 1, 1]

    n = len(prev)

    for _ in range(1000):
        LCA(0, prev, distances)
