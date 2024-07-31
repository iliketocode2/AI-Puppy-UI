"""
Main_Lesson6.py

Author: Izzy Morales

Description:
This script is designed to train a robotic puppy to perform a dance sequence 
using reinforcement learning (RL). The puppy will learn to perform various 
actions, including movements and dance moves, based on sensor input and rewards
provided by the user.

"""


import hub, color_sensor as cs, color, motor, motor_pair, utime, random, CEEO_AI
from hub import port, button, light_matrix, sound
ai = CEEO_AI.CEEO_AI()

##################################################################################################################################################
#                                                                  WHAT IS THE GOAL?                                                                 #
#                                        Students will train their puppy to do a dance sequence using RL!                                        #
#                        Actions will not only include just forward, right, left, and backwards, but also some dance moves!                      #
#                                                     Students will code the dance moves!                                                        #
##################################################################################################################################################

# Ports
c_sensor = port.B
f_sensor = port.F
legL = port.D
legR = port.C
motor_pair.pair(motor_pair.PAIR_1, legR, legL)

# Define actions
actions = [0, 1, 2, 3]

# You have to figure out how to make your puppy move accurately to each square and what dance move you can incorporate into the code
# HINT: Have your puppy face "forwards" after each move so the direction of forward, backward, left, and right does not change if the puppy is facing a new diection

# Create function for actions!
def puppy_move(action): # puppy takes a step, but dance
    if action == 0:
        # Code what the puppy should do here!
    elif action == 1:
        # Code what the puppy should do here!
    elif action == 2:
        # Code what the puppy should do here!
    elif action == 3:
        # Code what the puppy should do here!


##### TRAINING PUPPY ##### 
num_eps = 15
num_steps = 25
rewards_history = []
timesteps = []

print('**Put puppy on goal state and press right button!')
ai.wait_for_right_button()
goal_state = ai.get_state(c_sensor) # The puppy needs to know what the last square is in its dance so it knows when to stop!
print('**Goal state: ',goal_state)
goal_state = ai.add_to_qtable(goal_state, actions)
print(goal_state)
pro = False # Puppy is not a pro dancer yet because you need to train it!

for i in range(num_eps):
    print('**Reset puppy to starting position! Practice Round ' + str(i) + ' .....')
    ai.wait_for_right_button() # Press right button to begin practice round! Make sure puppy is on starting square!
    rew = 0
    ti = 0
    print('**Practice Round Beginning ' + str(i))
    state = ai.get_state(c_sensor) # Finds the color of the square the puppy is on
    state = ai.add_to_qtable(state, actions) # Stores the color in a Q table
    for j in range(num_steps):
        print('**Timestep ' + str(j))
        action = ai.choose_action(state, actions, pro) # Uses Q table to choose the best action based on the square puppy is on, or chooses a random action
        print('**Action chosen is ' + str(action))
        puppy_move(action)
        new_state = ai.get_state(c_sensor)
        new_state = ai.add_to_qtable(new_state, actions)
        #print("New state is " + states[new_state]) maybe ai.states, idk
        reward, done = ai.wait_for_reward(f_sensor) # Puppy waits for you to give it an award
        print('**Reward received is ' + str(reward))
        ai.reinforce_learn(reward, action, new_state, state) # Puppy learns from the reward, which is added to the Q table
        # The more bad rewards puppy gets for doing a certain action on a certain square, the less likely the puppy is to do it and vice versa!
        rew += reward
        state = new_state
        ti += 1
        if(done):
            print('**Dance move complete!')
            print('**Practice round reward sum ' + str(rew))
            rewards_history.append(rew)
            print(rewards_history) # Used to be above the line above
            timesteps.append(ti)
            light_matrix.show_image(light_matrix.IMAGE_COW)
            break

##### CAN PUPPY DANCE ON ITS OWN? #####
pro = True # Puppy is a professional dancer! (hopefully)
light_matrix.show_image(light_matrix.IMAGE_TORTOISE)
ai.wait_for_right_button() # Press the right button to have the puppy start your dance sequence it learned!
light_matrix.show_image(light_matrix.IMAGE_DUCK) # Lego hub will show a duck when puppy is starting

state = ai.get_state(c_sensor)
state = ai.add_to_qtable(state, actions)
while state != goal_state: # When puppy reaches the final square in its dance move, it will stop!
    print('**State is ' + str(state))
    action = ai.choose_action(state, actions, pro)
    print('**Action chosen is ' + str(action))
    utime.sleep(0.5)
    puppy_move(action)
    utime.sleep(0.5)
    new_state = ai.get_state(c_sensor)
    new_state = ai.add_to_qtable(new_state, actions)
    state = new_state
    utime.sleep(1)
    

# Puppy is a pro!!!
print('**Puppy is a dancing pro!')
light_matrix.show_image(light_matrix.IMAGE_FABULOUS)