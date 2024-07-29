import hub, utime, color, motor
import force_sensor as fs
import distance_sensor as ds
import color_sensor as cs
from hub import port, button, light_matrix, sound, light

class CEEO_AI:
    
    #INITIALIZE
    def __init__(self):
        self.lookup_table = {}
        self.legLdirection = 1
        self.legRdirection = -1
    
    #RIGHT BUTTON
    def wait_for_right_button(self):
        while True:
            if button.pressed(button.RIGHT):
                break
            utime.sleep(0.01)
        while button.pressed(button.RIGHT):
            utime.sleep(0.01)
            
    #LEFT BUTTON
    def wait_for_left_button(self):
        while True:
            if button.pressed(button.LEFT):
                break
            utime.sleep(0.01)
        while button.pressed(button.LEFT):
            utime.sleep(0.01)
            
    #DATA
    def get_data(self,dist,legs):
        velocities = []
        distances = []
        legL, legR = legs
        print('waiting for movement...')
        while abs(motor.velocity(legL)) < 5:
            utime.sleep(0.01)
        print('recording', end='')
        while motor.velocity(legL) != 0:
            print('.',end='')
            velocities.append(motor.velocity(legL)*10)
            distances.append(ds.distance(dist))
            utime.sleep(0.3)
        v_avg = int(sum(velocities) / len(velocities))
        d_avg = sum(distances) / len(distances)
        print('\n average velocity: ', v_avg, '. average distance', d_avg)
        return v_avg, d_avg
        
    def add_data(self, key, value):
        if key in self.lookup_table:
            self.lookup_table[key].append(value)
            print(value)
        else:
            self.lookup_table[key] = [value]
            print(value)
    
    #1-D KNN
    def KNN_1D(self, sample, k):
        if sample is None:
            return None
        else:
            total_values = 0
            # Iterate over each key-value pair in the dictionary
            for key, values in self.lookup_table.items():
                # Add the length of the list (number of values) to total_values
                total_values += len(values)
            differences = [(0,"")]*total_values
            i = 0
            for key, values in self.lookup_table.items():
                for value in values:
                    differences[i] = (self.diff(sample, value), key) # add [0] to value and sample if not working
                    i += 1
            differences.sort()
            nearest_neighbors = differences[:k]
            nearest_labels = [point[1] for point in nearest_neighbors]
            guess = max(nearest_labels, key=nearest_labels.count)
            return guess
    
    #3-D KNN
    def KNN_3D(self, sample, k):
        total_values = 0
        # Iterate over each key-value pair in the dictionary
        for key, values in self.lookup_table.items():
            # Add the length of the list (number of values) to total_values
            total_values += len(values)
        differences = [(0,"")]*total_values
        i = 0
        for key, values in self.lookup_table.items():
            for value in values:
                differences[i] = (self.diff_3D(sample, value), key)
                i += 1
        differences.sort()
        nearest_neighbors = differences[:k]
        nearest_labels = [point[1] for point in nearest_neighbors]
        guess = max(nearest_labels, key=nearest_labels.count)
        return guess
    
    #LINEAR REGRESSION
    def generate_linear_model(self):
        # Linear regression with least squares method
        Inputs = [item for sublist in self.lookup_table.values() for item in sublist]
        Outputs = [float(key) for key in self.lookup_table.keys()]
        n = len(Inputs)
        sumxy = 0
        sumx = 0
        sumy = 0
        sumSquarex = 0
        # Calculate sums
        for i in range(n):
            x = Inputs[i]
            y = Outputs[i]
            sumxy += x * y
            sumx += x
            sumy += y
            sumSquarex += x ** 2
        # Calculate the slope (m) and intercept (b)
        m = (n * sumxy - sumx * sumy) / (n * sumSquarex - sumx ** 2)
        b = (sumy - m * sumx) / n
        return m, b
    
    def linreg_prediction(self, dist, slope, intercept):
        # Use trained model to do predict time to go forward and move
        vel = slope*dist + intercept # Calculate v with the model
        print('\rd = '+str(dist)+'mm, v = '+str(int(vel)) + 'deg/s', end = '   ')
        return vel
        
    #DIFFERENCE
    def diff(self, a, b):
        return abs(a-b)
        
    #EUCLIDEAN DISTANCE
    def diff_3D(self, sample, point):
        #Calculate the distance between two N-dimensional points
        d = 0
        for i in range(len(sample)):
            d += pow(sample[i] - point[i], 2)
        return pow(d, 0.5)
        
    #DISTANCE SENSOR
    def get_distance(self, dist_port):
        while not button.pressed(button.LEFT):
            dist = ds.distance(dist_port)
            if dist != -1:
                return dist
            else:
                pass
        
    #FORCE SENSOR
    def get_force(self, force_port):
        btime = self.button_timer(force_port)
        return btime
        
    #LIGHT
    def get_light(self, refl_port):
        reflection = cs.reflection(refl_port)
        return reflection
    
    #COLOR SENSOR
    def get_colors(self, color_port):
        colors = [cs.rgbi(color_port)[0], cs.rgbi(color_port)[1], cs.rgbi(color_port)[2]]
        return colors
    
    #BUTTON TIMER
    def button_timer(self, force_port):
        #Record and measure the length of the next button press
        #Check to see if user wishes to prematurely end training
        while not fs.force(force_port) > 0:
            if button.pressed(button.LEFT):
                break
            utime.sleep(0.01)
        #If they press the button, measure the length in milliseconds
        time = 0
        while fs.force(force_port) > 0:
            utime.sleep(0.001)
            time += 1 #Measure press in ms for more accuracy
        return time
    
    #MOTOR POSITIONS
    def get_motor_position(self,legs):
        legL, legR = legs
        posL = motor.absolute_position(legL)
        posR = motor.absolute_position(legR)
        print('Left Position: ',posL)
        print('Right Position: ',posR)
        positions = posL, posR
        return positions
    
    def go_to_position(self, legs, positions):
        legL, legR = legs
        posL, posR = positions
        motor.run_to_absolute_position(legL, posL, 720)
        motor.run_to_absolute_position(legR, posR, 720)
        
    #MOTOR DRIVING
    def puppy_drive(self, vel, legs):
        legL, legR = legs
        if vel == 0:
            motor.stop(legL,stop=motor.COAST)
            motor.stop(legR,stop=motor.COAST)
        else:
            motor.run(legL, self.legLdirection * int(vel))
            motor.run(legR, self.legRdirection * int(vel))
        
    #HUB BUTTON COLOR
    def button_color(self,colors):
        light.color(light.POWER,colors)
    
    #FORGET
    def forget(self):
        self.lookup_table.clear()
