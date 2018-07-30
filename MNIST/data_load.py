import numpy as np
import pandas as pd
import seaborn as sns
import scipy as sp
import random as rd
import sklearn.cluster as cl
import sklearn.metrics as mt
from sklearn import datasets
import sklearn.datasets as data
import matplotlib.pyplot as plt
from sklearn import manifold
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
from sklearn import decomposition
import heapq
import itertools
import pickle
from datetime import datetime
import itertools as itl
import os


from auxiliar_functions import *

plt.rc('text', usetex=True)       # Notacion LaTeX
plt.rc('font', family='serif')

def import_data_set (data, 
                     size = 1000,                             # for MINST is the number of each cluster
                     random_sample = True ,
                     ploteo = False, 
                     save = False, 
                     which_digits = [0,1,2,3,4,5,6,7,8,9],    # just for MNIST
                     numero_de_componentes = 30,              # just for MNIST, NORB
                     ratios = [0,1,2,3,4],                    # just for RINGS
                     size_per_ring = [100,200,400,900,1600],  # just for RINGS 
                     bridges = False,                         # just fot RINGS with bridges
                     n_bridges = [10,20,40,90],               # just for RINGS with bridges
                     dispersion = 0.1,                        # just for RINGS
                     category_instances = [(2,7)],           # just for NORB
                     elevacion = [4],                         # just for NORB, number in [0:8]
                     azimuth   = [0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30], # just for NORB, number in [0:34, res=2]
                     luz       = [3],                         # just for NORB, number in [1:6]
                     desplazo = True,                         # just for NORB
                     desplaza_v = [-12,-10,-8,-6,-4,-2,0,2,4,6,8,10,12,14], # just for NORB    
                     desplaza_h = [-12,-10,-8,-6,-4,-2,0,2,4,6,8,10,12,14], # just for NORB
                     export_crude = False,
                     metrica = 'euclidean' ):                 # just for MNIST, Swiss_roll_isomaps
    
    #os.chdir('/home/facu/Dropbox/Tesis de Matemática (Sapienza)/Programacion/Data Sets')
    
    if data == 'Swiss_roll_isomaps' :
        dic = sp.io.loadmat(file_name='swiss_roll_data')
        data = dic['X_data']
        
        XX = np.zeros((size,3))
        if random_sample:
            sub_set = np.random.choice(range(data.shape[1]), size=size, replace = False)
            XX[:,0] = data[0,sub_set]
            XX[:,2] = data[1,sub_set]
            XX[:,1] = data[2,sub_set]            
        else:
            XX[:,0] = data[0,0:size]
            XX[:,2] = data[1,0:size]
            XX[:,1] = data[2,0:size]
        
        if ploteo == True or save == True:
            import matplotlib.pyplot as plt
            from mpl_toolkits.mplot3d import Axes3D
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            ax.view_init(10,89)
            ax.scatter(xs=XX[:,0], ys=XX[:,1], zs=XX[:,2], s=4)
            plt.title('Distribucion 3D \n N=%s'%(size))
            if save == True:
                plt.savefig('SwissRollIsomaps_ploteo.svg', dpi=300, format='svg')
            if ploteo == True:
                plt.show()
            
        return {'data': XX, 'distance' : mt.pairwise.pairwise_distances(XX, metric=metrica) }
    
    if data == 'MNIST':
        
        mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)
        how_many = np.zeros(10)
        data_cruda = []
        labels_mnist = []
        i = 0
        saturation = np.zeros(10)
        normalized_label = {}

        for ii, x in enumerate(which_digits):
            saturation[x] = size
            normalized_label[ x ] = ii
            
        def numeric_label(a):
            for i in range(len(a)):
                if a[i] == 1:
                    return i

        while not np.array_equal(how_many, saturation):

            i += 1
            new_label = numeric_label(mnist.train.labels[i,])

            if new_label not in which_digits :
                continue

            new_label = normalized_label[ new_label ]

            if np.max(how_many) == 0:
                X0 = np.matrix(mnist.train.images[i,])
                labels_mnist.append( new_label )
                data_cruda.append( mnist.train.images[i,].reshape((28,28)) )
                how_many = how_many + mnist.train.labels[i,]


            elif np.max(how_many + mnist.train.labels[i,]) <= size:
                X0 = np.concatenate((X0,np.matrix(mnist.train.images[i,])), axis=0)
                labels_mnist.append( new_label )
                data_cruda.append( mnist.train.images[i,].reshape((28,28)) )
                how_many = how_many + mnist.train.labels[i,]

        pca = decomposition.PCA(n_components=numero_de_componentes)
        pca.fit(X0)
        XX = pca.transform(X0)
        X_transform = pca.inverse_transform(XX).reshape(len(labels_mnist),28,28)
        
        return {'data': XX, 'distance': mt.pairwise.pairwise_distances(XX, metric = metrica), 'labels':labels_mnist, "data_cruda": data_cruda, 'data_proyectada':X_transform }
    
    if data == 'NORB':
        
        # Data avaiable in https://cs.nyu.edu/~ylclab/data/norb-v1.0/
        
        #categoria = 2  #Aviones, categoria
        #instancia = 7  #Avion de pasajeros, primer indice de labels

        tamano = len(category_instances) * len(elevacion) * len(azimuth) * len(luz) * len(desplaza_v) * len(desplaza_h) # maximo = 9 * 9 * 6 = 81 * 6 = 486
        labels = []
            
        X_fotos  = np.load(file = '/home/facu/Dropbox/Tesis de Matemática (Sapienza)/Programacion/Data Sets/small_norb-master/NORB_fotos.npy')
        X_labels = np.load(file = '/home/facu/Dropbox/Tesis de Matemática (Sapienza)/Programacion/Data Sets/small_norb-master/NORB_labels.npy')
        # four-legged animals, human figures, airplanes, trucks, and cars :
        X_cat    = np.load(file = '/home/facu/Dropbox/Tesis de Matemática (Sapienza)/Programacion/Data Sets/small_norb-master/NORB_cat.npy')
    
        X0 = np.zeros((tamano,96,96))
        counter = 0
        for ii in range(X_labels.shape[0]):
            labeles = X_labels[ii,:]
            if (X_cat[ii],labeles[0]) in category_instances and labeles[1] in elevacion and labeles[2] in azimuth and labeles[3] in luz:
                if desplazo :
                    for delta_x in desplaza_h:
                        for delta_y in desplaza_v:
                            for x_cord in range(96):
                                for y_cord in range(96):
                                    X0[counter,x_cord,y_cord] = X_fotos[2*ii , (x_cord + delta_x)%96, (y_cord + delta_y)%96 ]
                            counter += 1
                            labels.append( category_instances.index( (X_cat[ii],labeles[0]) ) )
                else:
                    labels.append( category_instances.index( (X_cat[ii],labeles[0]) ) )
                    X0[counter,:,:] = X_fotos[2*ii,:,:]
                    counter += 1
                
        if counter != tamano:
            print('ERROR')
        print('size = ', tamano)
                
        X0_flat = np.zeros((tamano,96*96))
        for ii in range(tamano):
            X0_flat[ii,:] = X0[ii,:,:].flatten()
                
        pca = decomposition.PCA(n_components=numero_de_componentes)
        pca.fit(X0_flat)
        print('variabilidad explicada = ', sum(pca.explained_variance_ratio_))
        XX = pca.transform(X0_flat)
        
        if export_crude :
            X_transform = pca.inverse_transform(XX).reshape(tamano,96,96)
            return {'data': XX, 'distance': mt.pairwise.pairwise_distances(XX, metric = metrica), 'labels':labels, 'data_cruda': X0, 'data_proyectada':X_transform}
        else: 
            return {'data': XX, 'distance': mt.pairwise.pairwise_distances(XX, metric = metrica), 'labels':labels}
            
    if data == 'Rings':
        
        size = sum(size_per_ring)
        labels = []
        colour = [] 
        
        XX = np.zeros((size,2))

        counter = 0
        for j,r in enumerate(ratios) :
            for jj in range(size_per_ring[j]):
    
                R = np.random.normal(loc=r, scale=dispersion)
                O = np.random.uniform(low=0, high=2*np.pi)

                XX[counter,:]  = [R*np.cos(O), R*np.sin(O)]
                colour.append(nice_color( r ,cm.rainbow, vmin=-1, vmax=ratios[-1]+1 ))
                labels.append(j)
                
                counter += 1
                
        if bridges : 
            for j in range(len(ratios)-1):
                ratio_medio = np.divide(ratios[j] + ratios[j+1], 2)
                for k in range(n_bridges[j]):
                    
                    R = np.random.uniform(low = ratio_medio-0.5, high=ratio_medio+0.5)
                    O = np.random.uniform(low = j*np.pi, high = j*np.pi + 0.1/ratios[j+1])
                    new = np.array([[R*np.cos(O), R*np.sin(O)]])
                    XX = np.concatenate((XX,new), axis=0)
                    colour.append(nice_color( R ,cm.rainbow, vmin=-1, vmax=ratios[-1]+1 ))
                
        if ploteo == True or save == True:
            import matplotlib.pyplot as plt
            from mpl_toolkits.mplot3d import Axes3D
            plt.close()
            plt.scatter(XX[:,0],XX[:,1],s=2, c=colour)
            plt.title('Rings dataset')
            if save == True:
                plt.savefig('Rings_ploteo.svg', dpi=300, format='svg')
            if ploteo == True:
                plt.show()
                
        return {'data': XX, 'distance': mt.pairwise.pairwise_distances(XX, metric=metrica), 'colours':labels }
    
