import sys
import time
import cProfile
path = 'C:/Coding/PBL_project(제어)'
sys.path.append(path)
#from sklearn.linear_model import LinearRegression
#from sklearn.linear_model import RANSACRegressor

def remove_outliers_tukey_2d(data, k=1.5):
    filtered_data = data.copy()
    for column in range(data.shape[1]):
        Q1 = np.percentile(data[:, column], 25)
        Q3 = np.percentile(data[:, column], 75)
        IQR = Q3 - Q1
        lower_bound = Q1 - k * IQR
        upper_bound = Q3 + k * IQR
        column_mask = (data[:, column] >= lower_bound) & (data[:, column] <= upper_bound)
    filtered_data = filtered_data[column_mask]
    return filtered_data
# 조건에 맞는 좌표들의 평균 구하기
def calculate_mean(x_coords, y_coords, value1, value2):
    mask1 = y_coords < value1
    mask2 = y_coords > value2

    selected_x_coords_1 = x_coords[mask1]
    selected_x_coords_2 = x_coords[mask2]

    selected_y_coords_1 = y_coords[mask1]
    selected_y_coords_2 = y_coords[mask2]

    count_1, count_2 = len(selected_x_coords_1), len(selected_x_coords_2)

    if count_1 > 0 and count_2 > 0:
        mean_x_1 = np.mean(selected_x_coords_1)
        mean_y_1 = np.mean(selected_y_coords_1)

        mean_x_2 = np.mean(selected_x_coords_2)
        mean_y_2 = np.mean(selected_y_coords_2)

    #해당 범위에 data가 없는 경우, 0.15를 기준으로 다시 구함
    else:
        y_median = np.median(np.sort(y_coords))

        mask_mid = y_coords < y_median
        selected_x_coords_mid = x_coords[mask_mid]
        selected_y_coords_mid = y_coords[mask_mid]
        mean_x_1 = np.mean(selected_x_coords_mid)
        mean_y_1 = np.mean(selected_y_coords_mid)
    
        mask_mid_2 = y_coords > y_median
        selected_x_coords_mid_2 = x_coords[mask_mid_2]
        selected_y_coords_mid_2 = y_coords[mask_mid_2]
        mean_x_2 = np.mean(selected_x_coords_mid_2)
        mean_y_2 = np.mean(selected_y_coords_mid_2)

    return mean_x_1, mean_y_1, mean_x_2, mean_y_2


from Examples.TrackGenerator1_example_original import *
from Tools.Vehicle import Vehicle
from Homework.controller import *
import matplotlib.pyplot as plt
import numpy as np

T_DEL = 0.01 # seconds: time interval

# generate track
track_x_noisy, track_y_noisy, track_x, track_y = track1()

#define a robot
robot = Vehicle(12, 7, np.pi/2, T_DEL)
#robot = Vehicle(1, 10, np.pi/2, T_DEL)
#robot = Vehicle(1, 11, -np.pi/2, T_DEL)



ax1 = plt.subplot(1,3,1)
ax2 = plt.subplot(1,3,2)
ax3 = plt.subplot(1,3,3)
t_start = time.time()
for tt in range(0,10000):
#for tt in range(0,10000):
    if tt % 180 == 0:
         print('here')
    top_view = robot.__observe__(track_x,track_y)

    

    # read sensor data
    # 수정사항 : __observe__ 에는 noisy track이 들어가도록 해주세요.
    points_in_sensor = robot.__observe__(track_x_noisy,track_y_noisy)

    #points_in_sensor = robot.__observe__(track_x,track_y)
    # print(points_in_sensor)

    print('tt: ', tt)
    u = controller([robot.x, robot.y, robot.theta], points_in_sensor, T_DEL)  
    robot.__update_state__(u)
    #print('_______________')
    #print('time: ', (t_current- t_start))
    if robot.x == 'nan':
        break
    print('x: ', robot.x)
    print('y: ', robot.y)


    
    
    # draw track
    ax1.clear()
    ax1.scatter(track_x, track_y,color='red', s=2)
    ax1.set_aspect('equal')
    ax1.grid('True')

    #  draw the robot
    robot.draw_robot(ax1)
    ax1.set_xlim((0, 20))
    ax1.set_ylim((0, 20))
    plt.pause(0.001)

    if points_in_sensor.size != 0:
    
        if len(points_in_sensor[0]) > 0 : 
            #model = LinearRegression()

            #model = RANSACRegressor(max_trials=200, min_samples=0.6)


            x = points_in_sensor[0]
            y = points_in_sensor[1]
            
            
            #Tukey fences
            # 이상치 제거를 위해 Tukey Fences 적용
            data = np.column_stack((x, y))
            filtered_data = remove_outliers_tukey_2d(data)

            # 필터링된 데이터로 RANSAC 회귀 모델 생성 및 훈련
            x_filtered = filtered_data[:, 0].reshape(-1, 1)
            y_filtered = filtered_data[:, 1].reshape(-1, 1)

            # 모델 학습
            #print('x = ',x)
            #print('y = ',y)
            #model.fit(x_filtered.reshape(-1, 1), y_filtered)
            #model.fit(x.reshape(-1, 1), y)

            x_1, y_1, x_2, y_2 = calculate_mean(x_filtered, y_filtered, 0.05, 0.25)
            
            degree = ((y_2 - y_1)/(x_2 - x_1)).item()
            x_intercept = (x_2 - y_2/degree).item()
        
        
    
    
    #draw sensor data
    ax2.clear()
    if len(points_in_sensor)>0:
        ax2.scatter(points_in_sensor[0,:],points_in_sensor[1,:], s=2)
        #ax2.plot(x, model.predict(x.reshape(-1, 1)), color='red', label='Linear Regression') #owj
        #if x.size != 0:
                #ax2.plot(x, degree*(x-x_intercept), color='red', label='Linear Regression') #owj


    ax2.set_xlim((-robot.sensor_width, robot.sensor_width))
    ax2.set_ylim((0, robot.sensor_height))
    ax2.set_aspect('equal')
    ax2.set_title('Points in sensor')
    ax2.grid('True')

    #top view visualize

    ax3.clear()
    if len(top_view)>0:
        #ax3.scatter(top_view[0,:],top_view[1,:], s=2)
        ax3.scatter(x_filtered,y_filtered, s=2)
        if x.size != 0:
                ax3.plot(x, degree*(x-x_intercept), color='red', label='Linear Regression') #owj

    ax3.set_xlim((-robot.sensor_width, robot.sensor_width))
    ax3.set_ylim((0, robot.sensor_height))
    ax3.set_aspect('equal')
    ax3.set_title('Filtered data')
    ax3.grid('True')

    plt.pause(0.001)
    t_current = time.time()
    #print('time: ', (t_current- t_start))
    

    
    if points_in_sensor.size == 0:
        break
    
    print('_______________')
    