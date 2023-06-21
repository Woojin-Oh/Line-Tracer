
import matplotlib.pyplot as plt
from Tools.TrackGenerator1 import *

# Generate custom tracks
def track1():
    # Generate Tracks
    track_x = []
    track_y = []

    xs, ys = line_generator(x0=3.0, y0=4.0, x1=2.0, y1=5.0, mode=(1,2))
    track_x.extend(xs)
    track_y.extend(ys)

    xs, ys = line_generator(x0=2.0, y0=5.0, x1=3.0, y1=6.0, mode=(2,2))
    track_x.extend(xs)
    track_y.extend(ys)

    xs, ys = line_generator(x0=3.0, y0=6.0, x1=4.0, y1=7.0, mode=(1,1))
    track_x.extend(xs)
    track_y.extend(ys)

    xs, ys = line_generator(x0=4.0, y0=7.0, x1=3.0, y1=8.0, mode=(2,1))
    track_x.extend(xs)
    track_y.extend(ys)

    xs, ys = line_generator(x0=3.0, y0=8.0, x1=1.0, y1=10.0, mode=(1,2))
    track_x.extend(xs)
    track_y.extend(ys)

    xs, ys = line_generator(x0=1.0, y0=10.0, x1=5.0, y1=13.0, mode=(2,2))
    track_x.extend(xs)
    track_y.extend(ys)

    xs, ys = line_generator(x0=5.0, y0=13.0, x1=6.0, y1=15.0, mode=(1,1))
    track_x.extend(xs)
    track_y.extend(ys)
    
    xs, ys = line_generator(x0=6.0, y0=15.0, x1=7.0, y1=17.0, mode=(2, 2))
    track_x.extend(xs)
    track_y.extend(ys)

    xs, ys = line_generator(x0=7.0, y0=17.0, x1=8.0, y1=15.0, mode=(2, 1))
    track_x.extend(xs)
    track_y.extend(ys)
    
    xs, ys = line_generator(x0=8.0, y0=15.0, x1=9.0, y1=13.0, mode=(1, 2))
    track_x.extend(xs)
    track_y.extend(ys)   

    xs, ys = line_generator(x0=9.0, y0=13.0, x1=10.0, y1=15.0, mode=(1, 1))
    track_x.extend(xs)
    track_y.extend(ys)
        
    xs, ys = line_generator(x0=10.0, y0=15.0, x1=11.0, y1=17.0, mode=(2, 2))
    track_x.extend(xs)
    track_y.extend(ys)

    xs, ys = line_generator(x0=11.0, y0=17.0, x1=12.0, y1=15.0, mode=(2, 1))
    track_x.extend(xs)
    track_y.extend(ys)

    xs, ys = line_generator(x0=12.0, y0=15.0, x1=15.0, y1=13.0, mode=(1,2))
    track_x.extend(xs)
    track_y.extend(ys)

    xs, ys = line_generator(x0=15.0, y0=13.0, x1=16.0, y1=12.0, mode=(2, 1))
    track_x.extend(xs)
    track_y.extend(ys)

    xs, ys = line_generator(x0=16.0, y0=12.0, x1=14.0, y1=10.0, mode=(1, 1))
    track_x.extend(xs)
    track_y.extend(ys)
    
    xs, ys = line_generator(x0=14.0, y0=10.0, x1=12.0, y1=11.0, mode=(1, 2))
    track_x.extend(xs)
    track_y.extend(ys)
    
    xs, ys = line_generator(x0=12.0, y0=11.0, x1=10.0, y1=12.0, mode=(2, 1))
    track_x.extend(xs)
    track_y.extend(ys)
    
    xs, ys = line_generator(x0=10.0, y0=12.0, x1=7.0, y1=10.0, mode=(2, 2))
    track_x.extend(xs)
    track_y.extend(ys)
    

    xs, ys = line_generator(x0=7.0, y0=10.0, x1=14.0, y1=7.0, mode=(1, 2))
    track_x.extend(xs)
    track_y.extend(ys)

    xs, ys = line_generator(x0=14.0, y0=7.0, x1=16.0, y1=6.0, mode=(2, 1))
    track_x.extend(xs)
    track_y.extend(ys)

    xs, ys = line_generator(x0=16.0, y0=6.0, x1=12.0, y1=1.0, mode=(1, 1))
    track_x.extend(xs)
    track_y.extend(ys)

    xs, ys = line_generator(x0=12.0, y0=1.0, x1=10.0, y1=4.0, mode=(1, 2))
    track_x.extend(xs)
    track_y.extend(ys)

    xs, ys = line_generator(x0=10.0, y0=4.0, x1=8.0, y1=6.0, mode=(2, 1))
    track_x.extend(xs)
    track_y.extend(ys)

    xs, ys = line_generator(x0=8.0, y0=6.0, x1=6.0, y1=5.0, mode=(2, 2))
    track_x.extend(xs)
    track_y.extend(ys)

    xs, ys = line_generator(x0=6.0, y0=5.0, x1=3.0, y1=4.0, mode=(1, 1))
    track_x.extend(xs)
    track_y.extend(ys)
    
    

        
    # Convert to numpy arrays for the noise addition
    track_x = np.array(track_x)
    track_y = np.array(track_y)

    track_x_noisy = track_x.copy()
    track_y_noisy = track_y.copy()

    # Deviation of the noise
    noise_std_dev = 0.01

    np.random.seed(0)

    noise_x = np.random.normal(loc=0, scale=noise_std_dev, size=track_x.shape)
    noise_y = np.random.normal(loc=0, scale=noise_std_dev, size=track_y.shape)

    track_x_noisy = track_x + noise_x
    track_y_noisy = track_y + noise_y

    max_deviation = 0.3
    deviation_probability = 0.05

    num_points = len(track_x_noisy)
    num_points_to_deviate = int(num_points * 0.1)

    indices_to_deviate = np.random.choice(range(num_points),num_points_to_deviate)

    for i in indices_to_deviate:
        deviation_x = np.random.uniform(-max_deviation, max_deviation)
        deviation_y = np.random.uniform(-max_deviation, max_deviation)
        track_x_noisy[i] += deviation_x
        track_y_noisy[i] += deviation_y

    return track_x_noisy, track_y_noisy, track_x, track_y

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    track_x_noisy, track_y_noisy, track_x, track_y = track1()
    #draw track
    plt.scatter(track_x,track_y)
    ax = plt.gca()
    ax.set_aspect('equal')
    plt.grid('True')
    plt.xlim((0, 20))
    plt.ylim((0, 20))
    plt.pause(30)
    plt.xlim((0,10))



# See PyCharm help at https://www.jetbrains.com/help/pycharm/

if __name__ == '__main__':
    track_x, track_y = track1()
    #draw track
    plt.scatter(track_x,track_y)
    ax = plt.gca()
    ax.set_aspect('equal')
    plt.grid('True')
    plt.xlim((0, 20))
    plt.ylim((0, 20))
    plt.pause(30)
    plt.xlim((0,10))



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
