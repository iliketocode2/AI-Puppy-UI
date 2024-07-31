"""
Main_Lesson5.py

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

# CODE TRAINING HERE! You have to get the avg velocity and distance data, and then add it to the data collection/table

hub_color2 = color.BLUE
ai.button_color(hub_color2)
sound.beep(440)

utime.sleep(1) #for greater pause b/t 2 gifs (not needed for code functionality)
print('**Collect data for backwards speed and distance')
# CODE TRAINING HERE! You have to get the avg velocity and distance data, and then add it to the data collection/table
# Same as above!

# Get linear model
[slope,intercept] = ai.generate_linear_model()
    
# PUPPY IS TRAINED

### PUPPY PLAY MODE ###
print('**Press right button to exit training mode!')
ai.wait_for_right_button() # Now in play mode!
hub_color3 = color.MAGENTA
ai.button_color(hub_color3)
sound.beep(880)
print('**Puppy is trained!')
# Linear regression

    # Code what the puppy guesses with the linear regression function in this loop!
    # You have to get the distance and have the puppy use it to guess what to do!


# Nearest Neighbor

    # Code what the puppy guesses with the KNN function in this loop!
    # You have to get the distance and have the puppy use it to guess what to do!

