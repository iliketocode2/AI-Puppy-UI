"""
Main_Lesson4.py

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
    # Code reaction here
    
def reaction2():
    # Code reaction here

## UNCOMMENT THE TRICK FUNCTIONS BELOW TO ADD MORE ##

#def reaction3():
    # Code reaction here

#def reaction4():
    # Code reaction here

#def reaction5():
    # Code reaction here


### PUPPY TRAINING MODE ###
hub_color1 = color.AZURE
ai.button_color(hub_color1)
print('**Now in training mode')
train_num = 3 # Number of samples you want to take for teaching each reaction

print('**Use your color sensor to train your puppy to react to different foods!')
print('**Add %s data samples for your 1st reaction by placing a color in front of the sensor and pressing the right button!' % (train_num))
print('**You should hear a beep when a data point is recorded.')
# ADD training code for reaction 1 here!

    
hub_color2 = color.BLUE
ai.button_color(hub_color2)
sound.beep(440)

print('**Now add data samples for your next trick!')
print('**Make sure you are interacting with the sensor differently, so your puppy will be able to know what trick to perform after training!')
# ADD training code for reaction 2 here!


# Add code like the code above to train your puppy to have more reactions!!!


# PUPPY IS TRAINED

### PUPPY PLAY MODE ###
print('**Press right button to exit training mode!')
ai.wait_for_right_button() # Now in play mode!
hub_color3 = color.MAGENTA
ai.button_color(hub_color3)
sound.beep(880)
K = 3

while not button.pressed(button.LEFT):
    # ADD code for the nearest neighbor algorithm here!! Use the variables 'guess_colors' and 'guess'
    # Make sure you use 3D KNN!!!
    
    print('%d, %d, and %d is classified as %s' % (guess_colors[0], guess_colors[1], guess_colors[2], guess))
    if guess == "reaction1":
        reaction1()
    elif guess == "reaction2":
        reaction2()
    # Add more elif statements if you trained your puppy to do more tricks!
    utime.sleep(0.1)
