import numpy as np
import scipy as sp
from heapq import *


def d_distance( distance_matrix, 
		d_param , 
		k_nn, 
		dimension = 2,           # deberia irse esto
		indices_to_do = 'all', 
		normalization = True):

    Large = distance_matrix.shape[0]                                  
    adj_list = [[] for i in range(Large)]
    
    out_dist = np.zeros((Large, Large))
    tree = {}
    
    for i in range(Large):
        
        local_distances = np.array([distance_matrix[i,j] for j in range(Large)])
        order = nsmallest(k_nn, range(Large), local_distances.take)
        
        for j in order:
            adj_list[i].append( (j ,np.power(distance_matrix[i,j], d_param )) )

    if indices_to_do == 'all':   
        to_do = range(Large)
    else:
        to_do = indices_to_do
        
    for i in to_do:
        
        out_dist[i,:], tree[i] = Dijkstra(adj = adj_list, src=i)


    if normalization:
        normalization_factor = np.divide( d_param-1 , dimension )
        for i in range(out_dist.shape[0]):
            for j in range(out_dist.shape[1]):
                out_dist[i,j] = out_dist[i,j] * np.power(Large,normalization_factor)
            
    return out_dist, tree



### Auxiliar functions

def Dijkstra(adj, src):

    q = [(0, src, -1)]

    seen = [False] * len(adj)

    tree = []
    distance = [-1] * len(adj)

    while q:
        cost, v, prev = heappop(q)

        if not seen[v]:
            
            seen[v] = True
            tree.append((v, prev))
            distance[v] = cost

            for v2, c in adj[v]:
                if not seen[v2]:
                    heappush(q, (cost + c, v2, v))
                    
    return distance, tree[1:]
