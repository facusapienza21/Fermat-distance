import random

from path_methods.Methods import Methods


class Fermat:

    def __init__(self, alpha, path_method='L', k=None, landmarks=None, estimator='up', seed=None, jobs=None):
        self.alpha = alpha
        self.k = k
        self.landmarks = landmarks
        self.estimator = estimator
        self.jobs = jobs

        # TODO: Validate parameters dependencies

        self.seed = seed
        self.random = random.Random(self.seed)

        self.path_method = Methods().byName(path_method, self)

    def fit(self, distances):
        return self.path_method.fit(distances)

    def get_distance(self, a, b):
        return self.path_method.get_distance(a, b)

    def get_distances(self):
        return self.path_method.get_distances()
