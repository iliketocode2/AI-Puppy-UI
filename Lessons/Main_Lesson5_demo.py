"""
Lesson5_demo.py

****THIS CODE WILL RUN SINCE IT IS COMPLETED** 

Author: Izzy Morales

Description:
This script is designed to train a robotic puppy using distance and force 
sensors, and motor ports. The user can train the puppy to move forwards 
or backwards based on the sensor data and linear regression or KNN algorithms.


"""

import hub, utime, motor, color, CEEO_AI
import force_sensor as fs
from hub import port, button, light, sound
ai = CEEO_AI.CEEO_AI()

### SENSOR, MOTORS, AND PORTS HERE ###
d_sensor = port.A
f_sensor = port.F
legL = port.D
legR = port.C
motors = [legL,legR]

### PUPPY TRAINING MODE ###
hub_color1 = color.AZURE
ai.button_color(hub_color1)
print('**Now in training mode')
train_num = 2

# Data collecting
print('**Collect data for forward speed and distance')
for i in range(train_num):
    ai.wait_for_right_button()
    [v_avg,d_avg] = ai.get_data(d_sensor,motors)
    print('**Data collected!')
    ai.add_data(v_avg,d_avg)
    sound.beep(220)
    utime.sleep(0.75)
hub_color2 = color.BLUE
ai.button_color(hub_color2)
sound.beep(440)
utime.sleep(1) #for greater pause b/t 2 gifs (not needed for code functionality)
print('**Collect data for backwards speed and distance')
for i in range(train_num):
    ai.wait_for_right_button()
    [v_avg,d_avg] = ai.get_data(d_sensor,motors)
    print('**Data collected!')
    ai.add_data(v_avg,d_avg)
    sound.beep(220)
    utime.sleep(0.75)

# Get linear model
[slope,intercept] = ai.generate_linear_model()
    
# PUPPY IS TRAINED

### PUPPY PLAY MODE ###
print('**Press right button to exit training mode!')
ai.wait_for_right_button() # Now in play mode!
play_color = color.MAGENTA
ai.button_color(play_color)
sound.beep(880)
# Linear regression
while not button.pressed(button.LEFT):
    guess_dist = ai.get_distance(d_sensor)
    guess = ai.linreg_prediction(guess_dist, slope, intercept)
    ai.puppy_drive(guess,motors)
    utime.sleep(0.1)
motor.stop(legL)
motor.stop(legR)
print('\n**Press right button to switch to K-Nearest Neighbor!')
ai.wait_for_right_button()
# Nearest Neighbor
K = 3
while not button.pressed(button.LEFT):
    guess_dist = ai.get_distance(d_sensor)
    guess = ai.KNN_1D(guess_dist,K)
    ai.puppy_drive(guess,motors)
    utime.sleep(0.1)
motor.stop(legL)
motor.stop(legR)
