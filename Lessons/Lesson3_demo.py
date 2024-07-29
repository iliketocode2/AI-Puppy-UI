import hub, utime, motor, color, CEEO_AI
from hub import port, button, light_matrix, sound, light
ai = CEEO_AI.CEEO_AI()

### ADD YOUR SENSOR, MOTORS, AND PORTS HERE ###
# Choose one sensor to use for this lesson!
sensor = port.A # distance sensor
legL = port.D #a motor
legR = port.C #a motor
motors = [legL,legR]

# Make sure you edited the code above to match your puppy's ports!

### WHAT DO YOU WANT TO TRAIN YOUR PUPPY TO DO? ###
# Add up to 2-5 tricks here! Comment out the functions you don't use
def trick1():
    # Code trick here
    print("trick1")
    
def trick2():
    # Code trick here
    print("trick2")

#def trick3():
    # Code trick here

#def trick4():
    # Code trick here

#def trick5():
    # Code trick here


### PUPPY TRAINING MODE ###
train_color1 = color.AZURE
ai.button_color(train_color1)
print('**Now in training mode')
train_num = 5 # Number of samples you want to take for teaching each trick

print('**Use your chosen sensor to train your puppy to do tricks!')
print('**Add %s data samples for your 1st trick by interacting with the sensor and pressing the right button!' % (train_num))
print('**You should hear a beep when a data point is recorded.')
for i in range(train_num):
    ai.wait_for_right_button()
    ai.add_data('trick1',ai.get_distance(sensor)) # ADD SENSOR COMMAND HERE, GET RID OF STRING
    sound.beep(220)
    utime.sleep(0.75)
    
train_color2 = color.BLUE
ai.button_color(train_color2)
sound.beep(440)

print('**Now add data samples for your next trick!')
print('**Make sure you are interacting with the sensor differently, so your puppy will be able to know what trick to perform after training!')
for i in range(train_num):
    ai.wait_for_right_button()
    ai.add_data('trick2',ai.get_distance(sensor)) # ADD SENSOR COMMAND HERE, GET RID OF STRING
    sound.beep(220)
    utime.sleep(0.75)
# Add code like the code above to train your puppy to do more tricks!!!

# PUPPY IS TRAINED


### PUPPY PLAY MODE ###
print('**Press right button to exit training mode and play with your puppy!')
ai.wait_for_right_button() # Now in play mode!
play_color = color.MAGENTA
ai.button_color(play_color)
sound.beep(880)
print('**Puppy is trained!')
K = 3
while not button.pressed(button.LEFT):
    guess_sensor = ai.get_distance(sensor)# PUT SENSOR COMMAND HERE
    guess = ai.KNN_1D(guess_sensor, K)
    if guess == 'trick1':
        trick1()
    elif guess == 'trick2': 
        trick2()
    # Add more elif statements if you trained your puppy to do more tricks!
    utime.sleep(0.1)
