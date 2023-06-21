import numpy as np
#from scipy.integrate import*

    
def dynamics(x,y,theta,u,t_del):
    
    
    x_next = x + u[0] * t_del * np.cos(theta)
    y_next = y + u[0] * t_del * np.sin(theta)
    theta_next = theta + u[1] * t_del

    theta_next = (theta_next + np.pi) % (2 * np.pi) - np.pi
    return x_next, y_next, theta_next

    
    
'''
    
#dynamics_exact
def dynamics(x,y,theta,u,t_del):
    #calculate k, integral range t1, t2
    k = round(theta/(u[2]*t_del))
    t1 = round(k*t_del, 2)
    t2 = round(t1+t_del, 2)

    x_next = x + u[0]*quad(cos_func,t1,t2,u[2])[0]
    y_next = y + u[1]*quad(sin_func,t1,t2,u[2])[0]  
    theta_next = theta + u[2]*t_del
    return x_next, y_next, theta_next

def cos_func(t, w):
    return np.cos(w*t)

def sin_func(t,w):
    return np.sin(w*t)
    '''