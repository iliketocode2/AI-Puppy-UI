
from pyscript import window
import my_globals


#done
my_gif_dict_L1 = {
    "**Train your puppy to be HAPPY when stroked or patted!": "gifs/Lesson1/force_sensor_touch_button.gif",
    "**Press right button to exit training mode and play with your puppy!": "gifs/Lesson2/Press_right_button.gif",    #because numbers also adjust counter
    "**Puppy is trained!":"gifs/Lesson1/Javier-gif.gif"
    #13: put image of just pressing force sensor
}
#done
my_gif_dict_L2 = {
    "**Move the legs of your puppy so that it is sitting!": "gifs/Lesson2/Sitting_Down.gif", #this gif is a placeholder -- CHANGE LATER
    "**You should hear a beep when a data point is recorded.": "gifs/Lesson2/Recording_sitting.gif",
    "**Move the legs of your puppy so that it is standing!": "gifs/Lesson2/Standing-up.gif",
    "**Now add 5 data samples for standing!":"gifs/Lesson2/Recording_sitting.gif",
    "**Press right button to exit training mode and play with your puppy!" : "gifs/Lesson3/holding_button.png"
}

#done
my_gif_dict_L3 = {
    "**Use your chosen sensor to train your puppy to do tricks!": "gifs/Lesson3/getting_data.gif", #this gif is a placeholder -- CHANGE LATER
    "**Press right button to exit training mode and play with your puppy!": "gifs/Lesson3/holding_button.png"
}

my_gif_dict_L4 = {
    3: "gifs/Lesson1/force_sensor_touch_button.gif" #this gif is a placeholder -- CHANGE LATER
}

my_gif_dict_L5 = {
    3: "gifs/Lesson1/force_sensor_touch_button.gif" #this gif is a placeholder -- CHANGE LATER
}

my_gif_dict_L6 = {
    3: "gifs/Lesson1/force_sensor_touch_button.gif" #this gif is a placeholder -- CHANGE LATER
}
    
#display custom gifs in side panel
def display_gif(imageName):
    window.fadeImage(imageName)


def get_gif(gif_dict, print_statement):
    #if counter in my_dict, then display gif 
    if print_statement in gif_dict: #counter represents number of print statement
        display_gif(gif_dict[print_statement])


#function responsible for changing lesson_num
def set_dictionary():
    my_globals.lesson_num = window.checkCurrentLesson() #fixx this to call js function
    print("Curr_lesson: ", my_globals.lesson_num)
    if my_globals.lesson_num == 1:
        my_globals.current_gif_dictionary = my_gif_dict_L1
    elif my_globals.lesson_num == 2:
        my_globals.current_gif_dictionary = my_gif_dict_L2
    elif my_globals.lesson_num == 3:
        #call_si
        #display_gif("gifs/Lesson3/Multiple_sensors.gif")
        my_globals.current_gif_dictionary = my_gif_dict_L3
    elif my_globals.lesson_num == 4:
        my_globals.current_gif_dictionary = my_gif_dict_L4
    elif my_globals.lesson_num == 5:
        my_globals.current_gif_dictionary = my_gif_dict_L5
    elif my_globals.lesson_num == 6:
        my_globals.current_gif_dictionary = my_gif_dict_L6

