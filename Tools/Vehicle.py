import numpy as np
import matplotlib.pyplot as plt
from Homework.dynamics import *
import matplotlib.patches as patches

class Vehicle(): #로봇 모델
    def __init__(self,x0,y0,theta0,t_del):
        #x0, y0: initial pose, theta0: initial heading, t_del: control time interval
        print("sensor")
        self.x = x0
        self.y = y0
        self.theta = theta0

        # spec of the sensor
        self.sensor_width = 0.3 #(m)
        self.sensor_height = 0.3

        # control frequency
        self.t_del = t_del #time interval t_Del

    def __update_state__(self,u): #update x, y, theta for the given u
        [self.x, self.y, self.theta]=dynamics(self.x,self.y,self.theta,u,self.t_del)

    def __observe__(self, track_x, track_y): # retrieve sensor data
        # transformation matrix
        T = np.array([[np.sin(self.theta), np.cos(self.theta), self.x],
                     [-np.cos(self.theta), np.sin(self.theta), self.y],
                     [0, 0, 1]])
        track = np.array([track_x, track_y,[1]*len(track_x)])
        #transform
        points = np.matmul(np.linalg.inv(T), track)
        points_in_sensor = []
        for ii in range(0,points.shape[1]):
            if abs(points[0,ii])<self.sensor_width and\
                    (points[1,ii] > 0) and (points[1,ii] <self.sensor_height):\
                    points_in_sensor.append(points[0:2,ii])
        points_in_sensor=np.transpose(np.array(points_in_sensor))
        #points_in_sensor=points
        return points_in_sensor

    def draw_robot(self,ax):
        sensor = np.transpose(np.array([[-self.sensor_width,0,1],[-self.sensor_width,self.sensor_height,1],
                                              [self.sensor_width,self.sensor_height,1],[self.sensor_width,0,1],
                                        [-self.sensor_width,0,1]]))
        T = np.array([[np.sin(self.theta), np.cos(self.theta), self.x],
                      [-np.cos(self.theta), np.sin(self.theta), self.y],
                      [0, 0, 1]])
        sen_r = np.matmul(T,sensor)

        ax.plot(self.x, self.y,'+')
        ax.plot(sen_r[0,0:4],sen_r[1,0:4],color='blue')


