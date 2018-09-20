import numpy as np
from scipy.sparse.csgraph import shortest_path

from fermat.path_methods.DistanceCalculatorMethod import DistanceCalculatorMethod


class FloydWarshallMethod(DistanceCalculatorMethod):

    def fit(self, distances):
        self.distances = shortest_path(
            csgraph=np.matrix(np.power(distances, self.fermat.alpha)),
            method='FW',
            directed=False
        )

    def get_distance(self, a, b):
        return self.distances[a, b]

    def get_distances(self):
        return self.distances
