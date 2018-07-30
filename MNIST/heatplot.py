import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def rescale_matrix(distances, size):
    
    n = len(distances)
    
    if size > n:
        size = n
        
    blocks = [(int(i*n/size), int((i+1)*n/size))  for i in range(size)]
    
    return  [[  
        sum(sum(row[x0:x1]) for row in distances[y0:y1] )/(x1-x0)/(y1-y0)    
        for x0, x1 in blocks] 
        for y0, y1 in blocks
    ]
    
    
def reorder_matrix(distances, order):
    r = list(zip(*[distances[i] for i in order]))
    return list(zip(*[r[i] for i in order]))


def draw_heatplot(distances, size, order=None, **args):
    if order:
        distances = reorder_matrix(distances, order)
    distances = rescale_matrix(distances, size)
    sns.heatmap(distances, square=True, **args)
    plt.show()
    
   