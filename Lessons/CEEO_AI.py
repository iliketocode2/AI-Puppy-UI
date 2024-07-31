"""
CEEO_AI.py

***********DO NOT CHANGE THIS FILE*********
(If you change this file, click download button to download original file again)
(Downloading will overwrite your file)

Authors: Izzy Morales, Rachael Azrialy

Description:
This module provides the CEEO_AI class, which encapsulates various AI 
functionalities for a robotic system. These functionalities include sensor 
data acquisition, K-Nearest Neighbors (KNN) algorithms for 1D and 3D data,
linear regression for predictive modeling, and reinforcement learning with 
Q-Learning.

"""
import hub, utime, color, motor, urandom
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
        self.qtable = {}
        self.alpha = 0.1
        self.gamma = 0.9
        self.epsilon = 0.1
    
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
            
    #DATA ACQUISITION 
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
    
    #1D KNN
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
    
    #3D KNN
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
    
    def generate_linear_model_3D(self):
        # Extract Inputs and Outputs from the lookup table
        Inputs = [item for sublist in self.lookup_table.values() for item in sublist]
        Outputs = [float(key) for key in self.lookup_table.keys()]
        n = len(Inputs)
        sumxy_r = sumxy_g = sumxy_b = 0
        sumx_r = sumx_g = sumx_b = 0
        sumy = 0
        sumSquarex_r = sumSquarex_g = sumSquarex_b = 0
        # Calculate sums
        for i in range(n):
            r, g, b = Inputs[i]  # Unpack the RGB tuple
            y = Outputs[i]
            sumxy_r += r * y
            sumxy_g += g * y
            sumxy_b += b * y
            sumx_r += r
            sumx_g += g
            sumx_b += b
            sumy += y
            sumSquarex_r += r ** 2
            sumSquarex_g += g ** 2
            sumSquarex_b += b ** 2
        # Calculate the slopes (m_r, m_g, m_b) and intercept (b)
        m_r = (n * sumxy_r - sumx_r * sumy) / (n * sumSquarex_r - sumx_r ** 2)
        m_g = (n * sumxy_g - sumx_g * sumy) / (n * sumSquarex_g - sumx_g ** 2)
        m_b = (n * sumxy_b - sumx_b * sumy) / (n * sumSquarex_b - sumx_b ** 2)
        b = (sumy - (m_r * sumx_r + m_g * sumx_g + m_b * sumx_b)) / n
        return m_r, m_g, m_b, b

    
    def linreg_prediction(self, dist, slope, intercept):
        if dist is None:
            return None
        else:
            # Use trained model to do predict time to go forward and move
            vel = slope*dist + intercept # Calculate v with the model
            print('\rd = '+str(dist)+'mm, v = '+str(int(vel)) + 'deg/s', end = '   ')
            return vel
    
    def linreg_prediction_3D(self, line_guess, slopes, intercept):
        # Extract the R, G, B values from the tuple
        slope_r, slope_g, slope_b = slopes
        r, g, b = line_guess
        # Use the trained model to predict the velocity
        vel = slope_r * r + slope_g * g + slope_b * b + intercept  # Calculate v with the model
        print('\rRGB = ' + str(rgb_tuple) + ', v = ' + str(int(vel)) + 'deg/s', end='   ')
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
        if vel == 0 or vel is None:
            motor.stop(legL,stop=motor.COAST)
            motor.stop(legR,stop=motor.COAST)
        else:
            motor.run(legL, self.legLdirection * int(vel))
            motor.run(legR, self.legRdirection * int(vel))
        
    #HUB BUTTON COLOR
    def button_color(self,colors):
        light.color(light.POWER,colors)
    
    #REINFORCEMENT LEARNING
    def get_state(self, sensor): 
        state = self.get_colors(sensor)
        state = tuple(state)
        return state
    
    def add_to_qtable(self, state, actions): # key for new state is determined
        for key in self.qtable.keys():
            if all(abs(state[i] - key[i]) <= 15 for i in range(3)):
                new_state = key
                return new_state
        # If no matching key is found, add the new state
        new_state = state
        qvalue = [0] * len(actions)
        self.qtable[new_state] = qvalue  # Assign the qvalue list directly, no need for extra brackets
        return new_state
        
    def reinforce_learn(self, reward, action, new_state, state):
        predict = self.qtable[state][action]
        target = reward + self.gamma * max(self.qtable[new_state])  # Q-Learning update rule
        self.qtable[state][action] += self.alpha * (target - predict)  # Update Q value
        print(f'Reward: {reward}, Q-table: {self.qtable}')  # Print reward and Q-table after each learning step
        
    def wait_for_reward(self, sensor):
        print('Give your puppy a small award if they did the right move and a big award if they reached the end spot!')
        print('OR press the right button to give your puppy no award')
        print('Press left button if puppy exits the dance floor')
        while True:
            if button.pressed(button.LEFT):
                self.wait_for_left_button()
                reward = -100
                done = True
                break
            elif button.pressed(button.RIGHT):
                self.wait_for_right_button()
                reward = -1
                done = False
                break
            elif fs.pressed(sensor):
                ftime = self.get_force(sensor)
                if ftime < 400:
                    reward = 1
                    done = False
                else:
                    reward = 10
                    done = True
                break
            else:
                utime.sleep(0.1)
        return reward, done
        
    def choose_action(self, state, actions, pro):
        k = urandom.uniform(0, 1) # epsilon-greedy strategy
        if self.epsilon > k and pro == False:
            print("Random action chosen")
            # Pick a random action
            action = urandom.choice(actions)
            #print("action is " + str(action))
        else:
            # Pick the best action from Q table
            # break ties between same max value 
            state_actions = self.qtable[state]
            max_val = max(state_actions)
            indices = []
            for ind, val in enumerate(state_actions):
                if(val == max_val):
                    indices.append(ind)
            action = urandom.choice(indices)
        return action
    
    #FORGET
    def forget(self):
        self.lookup_table.clear()
        self.qtable.clear()