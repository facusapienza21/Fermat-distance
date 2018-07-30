import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def trueround(number, places=0):

    place = 10**(places)
    rounded = (int(number*place + 0.5if number>=0 else -0.5))/place
    if rounded == int(rounded):
        rounded = int(rounded)
    return rounded


def trueround(number, places=0):

    place = 10**(places)
    rounded = (int(number*place + 0.5if number>=0 else -0.5))/place
    if rounded == int(rounded):
        rounded = int(rounded)
    return rounded


def plot_test(indicator, 
              all_ready_d, 
              median_performance,
              mean_Isomap, 
              best_Isomap, 
              median_Isomap, 
              data_set = '', 
              which_score = 'Mutual Information', 
              save = True, 
              show = True):

    plt.close()

    best = [np.max(indicator[d])  for d in all_ready_d]
    mean = [np.mean(indicator[d]) for d in all_ready_d]
    median = [np.median(indicator[d]) for d in all_ready_d]
    quant1 = [np.percentile(indicator[d] , q = 25) for d in all_ready_d]
    quant3 = [np.percentile(indicator[d] , q = 75) for d in all_ready_d]
    #quant_minus = [np.percentile(variation_of_information[d] , q = 10) for d in all_ready_d]
    #quant_maxus = [np.percentile(variation_of_information[d] , q = 90) for d in all_ready_d]

    #plt.plot(all_ready_d, best, label = 'best', color='#c0392b', lw=2)
    plt.plot(all_ready_d, mean, label = 'mean', color='#2980b9', lw=2)
    plt.plot(all_ready_d, median, label = 'median', color='#27ae60', lw=2)
    plt.plot(all_ready_d, median_performance,label='best clustering', color='#d35400',lw=2)
    plt.title( which_score )
    plt.xlabel('$d$')
    #plt.ylabel(which_score)
    #plt.ylim([-0.01, 1.01])
    plt.axhline(y=best_Isomap, color = '#c0392b', ls='dotted')
    plt.axhline(y=mean_Isomap, color = '#2980b9', ls='dotted')
    plt.axhline(y=median_Isomap, color = '#27ae60', ls='dotted')
    plt.grid()
    #plt.fill_between(all_ready_d, quant_minus, quant_maxus, facecolor='#bdc3c7', interpolate=True)
    plt.fill_between(all_ready_d, quant1, quant3, facecolor='#95a5a6', interpolate=True)
    plt.legend()
    if save:
        plt.savefig(data_set + '_' + which_score +'_kmedoids_run_d'+str(j)+'.svg', dpi = 300)
    if show:
        plt.show()



def variation_of_information (lab1, lab2):
    
    import sklearn.metrics as mt
    import numpy as np
    
    def entropy(lab):
        
        res = 0
        from collections import Counter
        repetitions = Counter(lab)
        for cluster in repetitions.keys():
            p = repetitions[cluster] / len(lab)
            res += - p * np.log(p)
        return res
        
    return entropy(lab1) + entropy(lab2) - 2 * mt.mutual_info_score(lab1, lab2) 



def median_labeling (list_of_labelings):
    
    import numpy as np
    
    size = len(list_of_labelings)
    centroid = 0 
    initial_distance = np.inf
    for i in range(size):
        closeness = 0
        for j in range(size):
            closeness += variation_of_information(list_of_labelings[i], list_of_labelings[j]) ** 2
        if closeness < initial_distance: 
            centroid = i
            initial_distance = closeness
    
    return list_of_labelings[centroid]
    


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
    
