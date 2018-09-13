import heapq
import numpy as np

from scipy.sparse import csr_matrix, dok_matrix
from scipy.sparse.csgraph import shortest_path

from path_methods.DistanceCalculatorMethod import DistanceCalculatorMethod


class DistanceOnTree:

    def __init__(self, root, prev, distances):
        n = len(prev)
        self.et = self.euler_tour(root, prev)
        self.root = root
        self.distances = distances
        self.right = self.get_right(self.et, n)
        self.rmq = self.get_rmq([distances[x] for x in self.et])

    def euler_tour(self, root, prev):
        children = [[] for _ in prev]
        for node, prev in enumerate(prev):
            if node != root and prev >= 0:  # -9999 is used to indicate that there is no previous node
                children[prev].append(node)

        res = []

        def aux(cur):
            res.append(cur)
            for child in children[cur]:
                aux(child)
                res.append(cur)

        aux(root)

        return res

    def get_right(self, et, n):
        res = [-1 for _ in range(n)]
        for index, node in enumerate(et):
            res[node] = index
        return res

    def get_rmq(self, xs):
        res = [xs[:]]
        n = len(xs)
        p = 1
        while p < n:
            res.append(
                [min(res[-1][i], res[-1][i + p]) if i + p < n else res[-1][i] for i in range(n)]
            )
            p *= 2
        return res

    def get_lca_distance(self, a, b):
        x, y = sorted([self.right[a], self.right[b]])
        d = (y - x).bit_length() - 1
        return min(self.rmq[d][x], self.rmq[d][y - (1 << d) + 1])

    def get_distance(self, a, b):
        return 0 if a == b else self.distances[a] + self.distances[b] - 2 * self.get_lca_distance(a, b)


class LandmarksMethod(DistanceCalculatorMethod):

    def __init__(self, fermat):
        super().__init__(fermat)
        self.landmarks_trees = []
        assert fermat.k is not None

    def get_near_points(self, distances):

        k = self.fermat.k
        n = distances.shape[0]

        columns = []
        values = []

        for i in range(n):
            smallest_values_and_columns = heapq.nsmallest(k+1, zip(distances[i].tolist()[0], list(range(n))))
            vs, cs = zip(*smallest_values_and_columns)

            columns.append(cs)
            values.append(vs)

        return columns, values

    def create_adj_matrix(self, l, near_columns, near_values, distances):

        n = distances.shape[0]
        m = dok_matrix((n, n), dtype='f')

        for row in range(n):
            for column, value in zip(near_columns[row], near_values[row]):
                m[row, column] = m[column, row] = value

            m[row, l] = m[l, row] = distances[l, row]

        return m

    def fit(self, distances):

        landmarks = self.fermat.random.sample(range(distances.shape[0]), self.fermat.landmarks)

        near_columns, near_values = self.get_near_points(distances)

        for l in landmarks:
            adj = self.create_adj_matrix(l, near_columns, near_values, distances)

            distance, prev = shortest_path(
                csgraph=adj.power(self.fermat.alpha),
                method='D',
                return_predecessors=True,
                directed=False,
                indices=[l]
            )

            landmark_tree = DistanceOnTree(l, prev=prev[0], distances=distance[0])

            self.landmarks_trees.append(landmark_tree)

    def up(self, a, b):
        return min(lt.get_distance(a, b) for lt in self.landmarks_trees)

    def down(self, a, b):
        return max(abs(lt.distances[a] - lt.distances[b]) for lt in self.landmarks_trees)

    def old_up(self, a, b):
        return min(lt.distances[a] + lt.distances[b] for lt in self.landmarks_trees)

    def get_distance(self, a, b):
        if self.fermat.estimator == 'up':
            return self.up(a, b)
        if self.fermat.estimator == 'down':
            return self.down(a, b)
        if self.fermat.estimator == 'mean':
            return (self.up(a, b) + self.down(a, b)) / 2
        if self.fermat.estimator == 'old_up':
            return self.old_up(a, b)

    def get_distances(self):
        pass






