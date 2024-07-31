"""
Lesson4_demo.py

****THIS CODE WILL RUN SINCE IT IS COMPLETED** 

Author: Izzy Morales

Description:
This script is designed to train a robotic puppy using a color sensor 
and motor ports. The user can train the puppy to react to different colors 
as if they were different foods.

"""

import hub, utime, motor, color, CEEO_AI
from hub import port, button, light_matrix, sound, light
ai = CEEO_AI.CEEO_AI()

### ADD YOUR SENSOR, MOTORS, AND PORTS HERE ###
# Use the color sensor for this activity!
c_sensor = port.B
legL = port.D
legR = port.C
motors = [legL,legR]

# Make sure you edited the code above to match your puppy's ports!

### HOW DO YOU WANT YOUR PUPPY TO REACT TO DIFFERENT FOODS? ###
# Add up to 2-5 reactions here! Comment out the functions you don't use
def reaction1():
    light_matrix.show_image(light_matrix.IMAGE_FABULOUS)
    
def reaction2():
    light_matrix.show_image(light_matrix.IMAGE_HAPPY)

#def reaction3():
    # Code reaction here

#def reaction4():
    # Code reaction here

#def reaction5():
    # Code reaction here


### PUPPY TRAINING MODE ###
train_color = color.AZURE
ai.button_color(train_color)
print('Now in training mode')
train_num = 3 # Number of samples you want to take for teaching each reaction

print('**Use your color sensor to train your puppy to react to different foods!')
print('**Add %s data samples for your 1st reaction by placing a color in front of the sensor and pressing the right button!' % (train_num))
print('**You should hear a beep when a data point is recorded.')
for i in range(train_num):
    ai.wait_for_right_button()
    ai.add_data('reaction1',ai.get_colors(c_sensor)) # ADD SENSOR FUNCTION HERE
    sound.beep(220)
    utime.sleep(0.75)

    
train_color2 = color.BLUE
ai.button_color(train_color2)
sound.beep(440)

print('**Now add data samples for your next trick!')
print('**Make sure you are interacting with the sensor differently, so your puppy will be able to know what trick to perform after training!')
for i in range(train_num):
    ai.wait_for_right_button()
    ai.add_data('reaction2',ai.get_colors(c_sensor)) # ADD SENSOR FUNCTION HERE
    sound.beep(220)
    utime.sleep(0.75)


# Add code like the code above to train your puppy to have more reactions!!!


# PUPPY IS TRAINED

### PUPPY PLAY MODE ###
print('**Press right button to exit training mode!')
ai.wait_for_right_button() # Now in play mode!
play_color = color.MAGENTA
ai.button_color(play_color)
sound.beep(880)
K = 3

while not button.pressed(button.LEFT):
    guess_colors = ai.get_colors(c_sensor)
    guess = ai.KNN_3D(guess_colors, K)
    print('%d, %d, and %d is classified as %s' % (guess_colors[0], guess_colors[1], guess_colors[2], guess))
    if guess == "reaction1":
        reaction1()
    elif guess == "reaction2":
        reaction2()
    # Add more elif statements if you trained your puppy to do more tricks!
    utime.sleep(0.1)
