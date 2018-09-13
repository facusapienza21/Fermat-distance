
class DistanceCalculatorMethod:

    def __init__(self, fermat):
        self.fermat = fermat

    def fit(self, distances):
        raise NotImplementedError()

    def get_distance(self, a, b):
        raise NotImplementedError()

    def get_distances(self):
        raise NotImplementedError()
