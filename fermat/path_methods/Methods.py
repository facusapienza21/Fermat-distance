from fermat.path_methods.DistanceCalculatorMethod import DistanceCalculatorMethod


class Methods:

    def __init__(self):

        from fermat.path_methods.DijkstraMethod import DijkstraMethod
        from fermat.path_methods.FloydWarshallMethod import FloydWarshallMethod
        from fermat.path_methods.LandmarksMethod import LandmarksMethod

        self.methods = {
            'L': LandmarksMethod,
            'FW': FloydWarshallMethod,
            'D': DijkstraMethod
        }

    def byName(self, name, fermat) -> DistanceCalculatorMethod:
        if name in self.methods.keys():
            return self.methods[name](fermat)
        else:
            raise Exception('Unknown method name: {}'.format(name))
