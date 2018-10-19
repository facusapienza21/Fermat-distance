# Fermat distance documentation

**class Fermat**

__init__(self, alpha, path_method='L', k=None, landmarks=None, estimator='up', seed=None)

Parameters
   
  - alpha: float
      Parameter of the Fermat distance.

  - path_method: string ['FW','D','L']

      Options are:

      - 'FW': Computes the exact Fermat distance using the Floyd-Warshall algorithm. 

      - 'D': Computes an approximation of the Fermat distance using k nearest neighbours and the
                       Dijkstra algorithm. 

      - 'L': Computes an approximation of the Fermat distance using landmarks and k-nn.

  - k: integer, optional
      Number of nearest neighbors to be considered.
      Incompatible with path_method == 'FW'

  - landmarks: integer, optional
      Number of landmarks considered in the Fermat distance computation.
      Only available when path_method = 'L'

  - estimator: string ['up', 'down', 'mean', 'no_lca'] (default: 'up')

      When computing an approximation of the Fermat distance, there are lower and upper bounds of the true value.
      - If estimator == 'no_lca', the distance for a pair of points is calculated as the minimum sum of the distance from both points to one of the landmarks.
      - If estimator == 'up', the distance for a pair of points is calculated as the minimum sum of the distance from both points to the lowest common ancestor in the distance tree of one of the landmarks.
      - If estimator == 'down', the distance for a pair of points is calculated as the maximum difference of thedistance from both points to one of the landmarks.
      - If estimator == 'mean', the  mean between 'up' and 'down' estimators.

      Only available when path_method = 'L'

  - seed: int, optional
      Only available when path_method = 'L'

#### Methods

  - fit(X)
    - Parameters
      - X: input distances matrix
    - Return
      - self

  - get_distance(a, b)
    - Parameters
      - a: int, index of the first data point
      - b: int, index of the second data point
    - Return
      - float, the Fermat distance between poins a and b
      
  - get_distances()
    - Parameters
      - None
    - Return
      - np.matrix, Fermat distance between all pairs of points


### Example of use
- Examples explaining how to use this package.
    * [Quick start] 
    * [MNIST data set]
    

[Quick start]:https://github.com/facusapienza21/Fermat-distance/tree/master/examples
[MNIST data set]: https://github.com/facusapienza21/Fermat-distance/blob/master/examples/MNIST_example.ipynb
