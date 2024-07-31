"""
Main_Lesson1.py

Authors: Izzy Morales, Rachael Azrialy

Description:
This script trains a robotic puppy to respond with emotions (happy or sad) based 
on interaction with a force sensor. The puppy uses a K-Nearest Neighbors (KNN) 
algorithm to classify the force sensor input as either a happy or sad 
interaction.


"""

import hub, utime, motor, color, CEEO_AI
from hub import port, button, light, sound, light_matrix
ai = CEEO_AI.CEEO_AI()

### SENSOR, MOTORS, AND PORTS HERE ###
f_sensor = port.F

### PUPPY TRAINING MODE ###
hub_color1 = color.AZURE
ai.button_color(hub_color1)

print('**Jav-MEssi') #change to see if changes sync on lesson files (Jul 30)
print('**Now in training mode')

train_num = 3

print('**Train your puppy to be HAPPY when stroked or patted!')
print('**A stroke means you press the touch sensor for a long time and a pat means you press the touch sensor for a shorter amount of time!') # no need for this on webpage, gif will explain
print('**Press right button to record a data point before using the touch sensor. You are recording %s data points.' % (train_num))
print('**Make sure Force Sensor is plugged into port F')

for i in range(train_num):
    ai.wait_for_right_button()
    ai.add_data('happy', ai.get_force(f_sensor))
    sound.beep(220)
    utime.sleep(0.25)

hub_color2 = color.BLUE
ai.button_color(hub_color2)
sound.beep(440)

print('**Train your puppy to be SAD when stroked or patted!')

print('**Press right button to record a data point before using the touch sensor. You are recording %s data points.' % (train_num))

for i in range(train_num):
    ai.wait_for_right_button()
    ai.add_data('sad', ai.get_force(f_sensor))
    sound.beep(220)
    utime.sleep(0.25)
    
# PUPPY IS TRAINED

### PUPPY PLAY MODE ###
print('**Press right button to exit training mode and play with your puppy!')

ai.wait_for_right_button() # Now in play mode!
hub_color3 = color.MAGENTA
ai.button_color(hub_color3)
sound.beep(880)

print('**Puppy is trained!')
print('**Press force sensor to see faces')

K = 3
while not button.pressed(button.LEFT):
    guess_time = ai.get_force(f_sensor)
    guess = ai.KNN_1D(guess_time, K)
    if guess == 'happy':
        light_matrix.show_image(light_matrix.IMAGE_HAPPY)
    elif guess == 'sad':
        light_matrix.show_image(light_matrix.IMAGE_SAD)
        utime.sleep(0.1)
