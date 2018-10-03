# Fermat

Fermat is a Python library that computes the Fermat distance estimator (also called d-distance estimator) proposed in 'Weighted Geodesic Distance Following Fermat's Principle' (see https://openreview.net/pdf?id=BJfaMIJwG).

# Implementation

The optimization performet to compute the Fermat distance estimator (see https://openreview.net/pdf?id=BJfaMIJwG) runs all over the possible paths of points between each pair of points. A first approach the is

   * FW: permorf the _Floyd-Warshall algorithm_ that gives the exact Fermat distance estimator in O(n^3) operations.
   
However, with probability arbitrary high we can restrict the minimum path search to paths where each consecutive pair of points are k-nearest neighbours, with k = O(log n). Then, we use
   
   * D: Computes an approximation of the Fermat distance using k nearest neighbours and the _Dijkstra algorithm_. The complexity is O( N*(k*N*log N) )

If the number of points n is too high and neither FW and D runs ij appropiate times, we implemente a grady version based on the idea of landmarks. Let consider a set of l points y_1, ... , y_l \in { x_1, ... , x_n } , with l << n, and 

   * L: Computes an approximation of the Fermat distance using landmarks and k-nn. The complexity is O( l*(k*N*log N) ).


# Features
---

- Exact and approximate algorithms to compute the Fermat distance.
- Examples explaining how to use this package.
    * [Quick start] 
    * [MNIST data set]


# Installation
---
Run `python3 setup.py build && sudo python3 setup.py install`

# Support
---

If you have an open-ended or a research question:
-  f.sapienza@aristas.com.ar



# Citing Fermat distance
---

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
