import heapq
import numpy as np

from scipy.sparse import csr_matrix, dok_matrix
from scipy.sparse.csgraph import shortest_path

from fermat.path_methods.DistanceCalculatorMethod import DistanceCalculatorMethod

from fermat.cclasses import LCA

class CLandmarksMethod(DistanceCalculatorMethod):

    def __init__(self, fermat):
        super().__init__(fermat)
        self.landmarks_trees = []
        self.n = None
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
        m = dok_matrix((n, n), dtype='d')

        for row in range(n):
            for column, value in zip(near_columns[row], near_values[row]):
                m[row, column] = m[column, row] = value

            m[row, l] = m[l, row] = distances[l, row]

        return m

    def create_adj_matrix_all(self, landmarks, distances):

        k = self.fermat.k
        n = distances.shape[0]

        columns = []
        rows = []
        values = []

        for i in range(n):
            if i in landmarks:
                values.extend(distances[i, j] for j in range(n))
                columns.extend(range(n))
                rows.extend([i]*n)
            else:
                smallest_values_and_columns = heapq.nsmallest(k + 1, zip(distances[i].tolist()[0], list(range(n))))
                vs, cs = zip(*smallest_values_and_columns)
                values.extend(vs)
                columns.extend(cs)
                rows.extend([i]*len(vs))

        return csr_matrix((values, (rows, columns)), shape=(n, n))

    def fit(self, distances):

        self.n = distances.shape[0]

        landmarks = self.fermat.random.sample(range(distances.shape[0]), self.fermat.landmarks)

        adj = self.create_adj_matrix_all(landmarks, distances)

        distance, prev = shortest_path(
            csgraph=adj.power(self.fermat.alpha),
            method='D',
            return_predecessors=True,
            directed=False,
            indices=landmarks
        )

        for i in range(len(landmarks)):
            landmark_tree = LCA(landmarks[i], prev=prev[i], distances=distance[i])
            self.landmarks_trees.append(landmark_tree)

    def up(self, a, b):
        return min(lt.get_distance(a, b) for lt in self.landmarks_trees)

    def get_distance(self, a, b):
        return self.up(a, b)
        
    def get_distances(self):
        res = np.matrix(np.zeros((self.n, self.n)))
        for i in range(self.n):
            for j in range(i):
                res[i, j] = res[j, i] = self.get_distance(i, j)
        return res
