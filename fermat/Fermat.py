import random

from fermat.path_methods.Methods import Methods


class Fermat:

    def __init__(self, alpha, path_method='L', k=None, landmarks=None, estimator='up', seed=None):
        """
        Initialization of the Fermat model

        Parameters
        -----------
        alpha: float
            Parameter of the Fermat distance.

        path_method: string ['FW','D','L']

            Options are:

                    'FW'    -- Computes the exact Fermat distance using the Floyd-Warshall algorithm. The complexity is
                             O[N^3] where N is the number of data points.

                    'D'     --  Computes an approximation of the Fermat distance using k nearest neighbours and the
                             Dijkstra algorithm. The complexity is O[N*(k*N*log N)]

                    'L'     -- Computes an approximation of the Fermat distance using landmarks and k-nn. The complexity
                             is O[l*(k*N*log N)] where l is the number of landmarks considered.

        k: integer, optional
            Number of nearest neighbors to be considered.
            Incompatible with path_method == 'FW'

        landmarks: integer, optional
            Number of landmarks considered in the Fermat distance computation.
            Only available when path_method = 'L'

        estimator: string ['up', 'down', 'mean', 'no_lca'] (default: 'up')
            When computing an approximation of the Fermat distance, there are lower and upper bounds of the true value.
            If estimator == 'no_lca', the distance for a pair of points is calculated as the minimum sum of the distance
                from both points to one of the landmarks.
            If estimator == 'up', the distance for a pair of points is calculated as the minimum sum of the distance
                from both points to the lowest common ancestor in the distance tree of one of the landmarks.
            If estimator == 'down', the distance for a pair of points is calculated as the maximum difference of the
                distance from both points to one of the landmarks.
            If estimator == 'mean', the  mean between 'up' and 'down' estimators.
            Only available when path_method = 'L'

        seed: int, optional
            Only available when path_method = 'L'


        Returns
        -----------
        Fermat class object


        Examples
        -----------
        # init an exact Fermat distance model
        f_exact = Fermat(alpha = 3, path_method='FW', seed = 1)

        # init an approx Fermat distance model
        f_aprox = Fermat(alpha, path_method='L', k=10, landmarks=50)



        """
        self.alpha = alpha
        self.k = k
        self.landmarks = landmarks
        self.estimator = estimator

        # TODO: Validate parameters dependencies

        self.seed = seed
        self.random = random.Random(self.seed)

        self.path_method = Methods().byName(path_method, self)

    def fit(self, distances):
        """

        Parameters
        -----------
        distances: np.matrix
            Matrix with pairwise distances



        """
        return self.path_method.fit(distances)

    def get_distance(self, a, b):
        """

        Parameters
        -----------
        a: int
            Index of a data point

        b: int
            Index of a data point

        Returns
        -----------
        Float: the Fermat distance between points a and b


        """

        return self.path_method.get_distance(a, b)

    def get_distances(self):
        """

        Parameters
        -----------
        -

        Returns
        -----------
        np.matrix with the pairwise Fermat distances

        """

        return self.path_method.get_distances()
