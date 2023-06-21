# This is a sample Python script.
import numpy as np

NGRID = 0.001 # Do not change

def ellipse_x_to_y(a,b,x): # return the absolute value of y
    y = b*np.sqrt(1-(x**2)/(a**2))
    return y

def ellipse_y_to_x(a,b,y):
    x = a * np.sqrt(1 - (y ** 2) / (b ** 2))
    return x

def line_generator(x0, y0, x1, y1, mode): #
    # (x0, y0): xy position of first left point
    # (x1, y1): xy position of second point
    # lx, ly: length of boxes
    # mode: shape of the line (1,1), (1,2), (2,1), (2,2)
    # return xs and ys: where xs and ys are x,y positions of points on the line
    if x0 > x1: #if x0 is more on the right then x1
        x0, x1, y0, y1 = x1, x0, y1, y0
    lx = abs(x1-x0)*2 #곱하기 2
    ly = abs(y1-y0)*2
    a = lx/2
    b=  ly/2
    if mode==(1,1):
        xc = x0 # center of ellipse
        yc = y1
        xs = [0.0]
        ys = [-b]
        while xs[-1]< a-NGRID and ys[-1] < -NGRID :
            next1 = np.array((xs[-1]+NGRID,-ellipse_x_to_y(a,b,xs[-1]+NGRID)))
            next2 = np.array((ellipse_y_to_x(a,b,ys[-1]+NGRID), ys[-1]+NGRID))
            #print(next1, next2)
            if np.sum(next1**2) < np.sum(next2**2):
                xs.append(next1[0])
                ys.append(next1[1])
            else:
                xs.append(next2[0])
                ys.append(next2[1])
        xs.append(a)
        ys.append(0)

    elif mode==(1,2):
        xc = x1 # center of ellipse
        yc = y0
        xs = [-a]
        ys = [0.0]
        while xs[-1]< -NGRID and ys[-1] > -b-NGRID :
            next1 = np.array((xs[-1]+NGRID,-ellipse_x_to_y(a,b,xs[-1]+NGRID)))
            next2 = np.array((-ellipse_y_to_x(a,b,ys[-1]+NGRID), ys[-1]-NGRID))
            #print(next1, next2)
            if np.sum(next1**2) < np.sum(next2**2):
                xs.append(next1[0])
                ys.append(next1[1])
            else:
                xs.append(next2[0])
                ys.append(next2[1])
        xs.append(0)
        ys.append(-b)
    elif mode==(2,1):
        xc = x0 # center of ellipse
        yc = y1
        xs = [0.0]
        ys = [b]
        while xs[-1]< a-NGRID and ys[-1] > NGRID :
            next1 = np.array((xs[-1]+NGRID,ellipse_x_to_y(a,b,xs[-1]+NGRID)))
            next2 = np.array((ellipse_y_to_x(a,b,ys[-1]-NGRID), ys[-1]-NGRID))

            #print(next1, next2) 최대한 촘촘하게 하기 위해 next1, next2 중에 비교(NGRID만큼 움직이면서 비교)
            if np.sum(next1**2) < np.sum(next2**2):
                xs.append(next1[0])
                ys.append(next1[1])
            else:
                xs.append(next2[0])
                ys.append(next2[1])
        xs.append(a)
        ys.append(0)

    elif mode == (2, 2):
        xc = x1  # center of ellipse
        yc = y0
        xs = [-a]
        ys = [0]
        while xs[-1] < - NGRID and ys[-1] < b - NGRID:
            next1 = np.array((xs[-1] + NGRID, ellipse_x_to_y(a, b, xs[-1] + NGRID)))
            next2 = np.array((-ellipse_y_to_x(a, b, ys[-1] + NGRID), ys[-1] + NGRID))

            if np.sum(next1 ** 2) < np.sum(next2 ** 2):
                xs.append(next1[0])
                ys.append(next1[1])
            else:
                xs.append(next2[0])
                ys.append(next2[1])
        xs.append(0)
        ys.append(b)


    xs = np.array(xs)+xc
    ys = np.array(ys)+yc
    return xs, ys
