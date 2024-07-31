"""
Main_Lesson3.py

Author: Izzy Morales

Description:
This script is designed for students to train a robotic puppy using various 
sensors and motor ports. The user can define up to 5 tricks, train the puppy 
with sensor data, and then play with the puppy by having it perform the trained
tricks.

"""
import hub, utime, motor, color, CEEO_AI
from hub import port, button, light_matrix, sound, light
ai = CEEO_AI.CEEO_AI() # Library of CEEO AI functions

### ADD YOUR SENSOR, MOTORS, AND PORTS HERE ###
# Choose one sensor to use for this lesson!
sensor = port.A # You can rename this based on the sensor you are using
legL = port.D
legR = port.C
motors = [legL,legR]

# Make sure you edited the code above to match your puppy's ports!

### WHAT DO YOU WANT TO TRAIN YOUR PUPPY TO DO? ###
# Add up to 2-5 tricks here! Comment out the functions you don't use
def trick1():
    # Code trick here
    
def trick2():
    # Code trick here

## UNCOMMENT THE TRICK FUNCTIONS BELOW TO ADD MORE ##

#def trick3():
    # Code trick here

#def trick4():
    # Code trick here

#def trick5():
    # Code trick here


### PUPPY TRAINING MODE ###
hub_color1 = color.AZURE # This line and the line below changes the color of the hub button so you know when puppy is in training mode!
ai.button_color(hub_color1)
print('**Now in training mode')
train_num = 5 # Number of samples you want to take for teaching each trick

print('**Use your chosen sensor to train your puppy to do tricks!')
print('**Add %s data samples for your 1st trick by interacting with the sensor and pressing the right button!' % (train_num))
print('**You should hear a beep when a data point is recorded.')
for i in range(train_num): # For loop repeats the code inside of it! Adding more data values will improve the puppy's learning!
    ai.wait_for_right_button()
    ai.add_data('trick1',SENSOR FUNCTION HERE) # ADD SENSOR FUNCTION HERE
    sound.beep(220)
    utime.sleep(0.25)
    
hub_color2 = color.BLUE # Changing the hub button color because we're switching the trick being trained
ai.button_color(hub_color2)
sound.beep(440)

print('**Now add data samples for your next trick!')
print('**Make sure you are interacting with the sensor differently, so your puppy will be able to know what trick to perform after training!')
for i in range(train_num):
    ai.wait_for_right_button()
    ai.add_data('trick2',SENSOR FUNCTION HERE) # ADD SENSOR FUNCTION HERE
    sound.beep(220)
    utime.sleep(0.25)
# Add code like the code above to train your puppy to do more tricks!!! If you want to do this it would be a good idea to add more for loops!


# PUPPY IS TRAINED


### PUPPY PLAY MODE ###
print('**Press right button to exit training mode and play with your puppy!')
ai.wait_for_right_button() # Now in play mode!
hub_color3 = color.MAGENTA
ai.button_color(hub_color3)
sound.beep(880)
print('**Puppy is trained!')
K = 3 # How many nearest neighbors do you want to consider?
while not button.pressed(button.LEFT):
    guess_sensor = # PUT SENSOR FUNCTION HERE
    guess = ai.KNN_1D(guess_sensor, K)
    if guess == 'trick1':
        trick1()
    elif guess == 'trick2': 
        trick2()
    # Add more elif statements if you trained your puppy to do more tricks!
    utime.sleep(0.1)