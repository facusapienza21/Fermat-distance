import numpy as np

def generate_swiss_roll(oscilations, A, n):

    mean1 = [0.3,0.3]
    mean2 = [0.3,0.7]
    mean3 = [0.7,0.3]
    mean4 = [0.7,0.7]
    cov   = [[0.01,0],[0,0.01]]

    X1 = np.random.multivariate_normal(mean1, cov, n)
    X2 = np.random.multivariate_normal(mean2, cov, n)
    X3 = np.random.multivariate_normal(mean3, cov, n)
    X4 = np.random.multivariate_normal(mean4, cov, n)
    XX = np.concatenate((X1,X2,X3,X4), axis=0)

    labels = [0]*n + [1]*n + [2]*n + [3]*n

    X = np.zeros((XX.shape[0],3))
    for i in range(X.shape[0]):
        x, y = XX[i,0], XX[i,1]
        X[i,0] = x * np.cos( oscilations * x ) 
        X[i,1] = A*y
        X[i,2] = x * np.sin( oscilations * x ) 
        
    return X,labels
