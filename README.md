# Fermat distance

Fermat is a Python library that computes the Fermat distance estimator (also called d-distance estimator) proposed in 'Weighted Geodesic Distance Following Fermat's Principle' (see https://openreview.net/pdf?id=BJfaMIJwG).

---
### Implementation

The optimization performet to compute the Fermat distance estimator (see https://openreview.net/pdf?id=BJfaMIJwG) runs all over the possible paths of points between each pair of points. A first approach is

   * FW: permorf the _Floyd-Warshall algorithm_ that gives the exact Fermat distance estimator in O( n^3 ) operations.
   
However, with probability arbitrary high we can restrict the minimum path search to paths where each consecutive pair of points are k-nearest neighbours, with k = O(log n). Then, we use
   
   * D: Computes an approximation of the Fermat distance using k nearest neighbours and the _Dijkstra algorithm_. The complexity is O( n * ( k *n * log n ) )

If the number of points n is too high and neither FW and D runs in appropiate times, we implemente a gready version based on  landmarks. Let consider a set of l of point in the data set (the landmarks) and denote s_j the distance of the point s to the landmark j. Then, we can bound the distance d(s,t) between any two points s and t as

_lower = max_j { | s_j - t_j | } <= d(s,t) <= min_j { s_j + t_j } = upper_

and estimate d(s,t) as a function of _lower_ and _upper_ (for example, d(s,t) ~ (_lower + upper_) / 2 ).

   * L: Computes an approximation of the Fermat distance using landmarks and k-nn. The complexity is O( l * ( k * n * log n ) ).

---
### Parameters

        - alpha: float
            Parameter of the Fermat distance.
            
        - path_method: string ['FW','D','L']
        
            Options are:

                    -'FW'    -- Computes the exact Fermat distance using the Floyd-Warshall algorithm. 

                    -'D'     --  Computes an approximation of the Fermat distance using k nearest neighbours and the
                             Dijkstra algorithm. 

                    -'L'     -- Computes an approximation of the Fermat distance using landmarks and k-nn.

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

---
### Features

- Exact and approximate algorithms to compute the Fermat distance.
- Examples explaining how to use this package.
    * [Quick start] 
    * [MNIST data set]

---
### Installation

###### Ubuntu

Run`'python3 setup.py build && sudo python3 setup.py install'`

If you are working in Anaconda, then:

...

---
### Support

If you have an open-ended or a research question:
-  'f.sapienza@aristas.com.ar'

---
### Citing Fermat distance

When [citing fermat in academic papers and theses], please use this
BibTeX entry:

    @inproceedings{
          sapienza2018weighted,
          title={Weighted Geodesic Distance Following Fermat's Principle},
          author={Facundo Sapienza and Pablo Groisman and Matthieu Jonckheere},
          year={2018},
          url={https://openreview.net/forum?id=BJfaMIJwG}
    }

[Quick start]:https://github.com/facusapienza21/Fermat-distance/tree/master/examples
[citing fermat in academic papers and theses]:https://scholar.google.com/citations?user=yWj-T4oAAAAJ&hl=en#d=gs_md_cita-d&p=&u=%2Fcitations%3Fview_op%3Dview_citation%26hl%3Den%26user%3DyWj-T4oAAAAJ%26citation_for_view%3DyWj-T4oAAAAJ%3Au5HHmVD_uO8C%26tzom%3D180
[MNIST data set]: https://github.com/facusapienza21/Fermat-distance/blob/master/examples/MNIST_example.ipynb
