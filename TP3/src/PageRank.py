import numpy as np

def poweriteration(n, matrix, alpha):
    I = np.ones((n, 1))/n
    P = I
    err = 1
    while err > 1e-5:
        old = P
        P = matrix @ P
        P = (1-alpha)*P + alpha*I
        P = P + (1-np.sum(np.absolute(P)))*I
        err = np.sum(np.absolute(P-old))
    return P

def personalized_poweriteration(n, matrix, P0, alpha):
    P = P0
    err = 1
    while err > 1e-5:
        old = P
        P = matrix @ P
        P = (1-alpha)*P + alpha*P0
        P = P + (1-np.sum(np.absolute(P)))*P0
        err = np.sum(np.absolute(P-old))
    return P