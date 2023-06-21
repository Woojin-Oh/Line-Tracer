import numpy as np
import math
from scipy.interpolate import interp1d

prev_error_list = [None]
speed_list = [0]

#이상치(노이즈) 제거
def remove_outliers_tukey_2d(data, k=1.5):
    Q1, Q3= np.percentile(data[:, 0], [25, 75])
    IQR = Q3 - Q1

    lower_bound = Q1 - k * IQR
    upper_bound = Q3 + k * IQR

    column_mask = (data[:, 0] >= lower_bound) & (data[:, 0] <= upper_bound)
    filtered_data = data[column_mask]

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
        print(mean_x_1, mean_y_1, mean_x_2, mean_y_2)

    return mean_x_1, mean_y_1, mean_x_2, mean_y_2

def controller(state, observation,t_del):
    
    if observation.size == 0:
        u = [35,0]
        return u
        
        
    elif observation[0].size < 10:

        x = observation[0]
        x_median= np.median(x)

        #x 중앙값 기준 각도 조율
        error = 0 - x_median

        Kp = 110
        P_control = Kp * error
        theta_change = P_control
        theta_change_rad_t_del = (theta_change*np.pi/180)/t_del

        u = [35,theta_change_rad_t_del]
        return u
    
        
    else: 
        # 이상치 제거를 위해 Tukey Fences 적용
        filtered_data = remove_outliers_tukey_2d(observation.T)
        x_filtered = filtered_data[:, 0].reshape(-1, 1)
        y_filtered = filtered_data[:, 1].reshape(-1, 1)


        # 필터링된 데이터로 1차 방정식 계산
        x_1, y_1, x_2, y_2 = calculate_mean(x_filtered, y_filtered, 0.05, 0.25)
        degree = ((y_2 - y_1)/(x_2 - x_1)).item()
        x_intercept = (x_2 - y_2/degree).item()
        #y = a(x-b) -> x = 1.5/a + b
        x_median = 0.15/degree + x_intercept


        #기울기 값 이상하게 나오는거 방지
        if degree >0:
            degree = max(degree, 1.5)
        else:
            degree = min(degree, -1.5)
            
        theta_rad = math.atan(degree) #rad으로 변환
        theta_degree = theta_rad*180/np.pi
        print('theta(degree): ', theta_degree)


        #기울어진 각도 기준 조율
        if theta_degree >= 0:
            degree_loss = 90 - theta_degree
            degree_loss *= -1
        else:
            degree_loss = 90 + theta_degree
        
        print('degree_loss: ', degree_loss)


        #y=0.15인 x좌표 기준 각도 조율(PD제어)
        error = 0 - x_median

        if prev_error_list[-1] == None:
            prev_error = 0
        else:
            prev_error = prev_error_list[-1]
        prev_error_list[-1] = error

        Kp = 110
        Kd = 0.4

        P_control = Kp * error
        D_control = Kd * (error - prev_error) / t_del

        print('prev_error: ', prev_error)
        print('error: ', error)
        print('P_control(degree): ', P_control)
        print('D_control(degree): ', D_control)

        theta_change = degree_loss + P_control + D_control
        

        print('최종 theta_change(degree): ', theta_change)
        
        dist = 0.3 / math.sin(abs(theta_rad))
        x_points = np.array([0.3, 0.35])
        y_points = np.array([40, 5])
        print('dist: ', dist)

        interpolation_function = interp1d(x_points, y_points, kind='linear', fill_value = (40, 5),bounds_error=False, assume_sorted=True)
        speed = interpolation_function(dist)

        prev_speed = speed_list[-1]

        
        
        #트랙이 로봇의 중심에 있을 경우 속력 증가
        if abs(x_median)<0.04 and abs(90 - abs(theta_degree)) < 3:
            speed = 50
            if prev_speed >= 50:
                speed = prev_speed + 2
                
        
        speed_list[-1] = speed
        print('speed: ', speed)

        theta_change_rad_t_del = (theta_change*np.pi/180)/t_del
        u = [speed, theta_change_rad_t_del]
        return u
        
