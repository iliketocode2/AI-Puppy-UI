"""
my_gif.py

This module handles the display of custom GIFs for various lessons in the 
puppy training program. The GIFs are displayed in a side panel based on 
specific print statements and lesson number.

Authors: Javier Laveaga and William Goldman

Contributors: Emmett Berryman and Izzy Morales (GIFs)

"""


from pyscript import window
import my_globals


# Dictionary containing lesson-specific GIFs for Lesson 1
my_gif_dict_L1 = {
    "**Train your puppy to be HAPPY when stroked or patted!": 
        "gifs/Lesson1/force_sensor_touch_button.gif",
    "**Press right button to exit training mode and play with your puppy!": 
        "gifs/Lesson2/Press_right_button.gif", 
    "**Puppy is trained!":
        "gifs/Lesson1/Javier-gif.gif"
    
}

# Dictionary containing lesson-specific GIFs for Lesson 2
my_gif_dict_L2 = {
    "**Move the legs of your puppy so that it is sitting!": 
        "gifs/Lesson2/2gif1.gif", 
    "**You should hear a beep when a data point is recorded.": 
        "gifs/Lesson2/2gif2.gif",
    "**Move the legs of your puppy so that it is standing!": 
        "gifs/Lesson2/2gif3.gif",
    "**Now add 5 data samples for standing!":
        "gifs/Lesson2/2gif4.gif",
    "**Press right button to exit training mode and play with your puppy!" : 
        "gifs/Lesson2/2gif5.gif"
}

# Dictionary containing lesson-specific GIFs for Lesson 3
my_gif_dict_L3 = {
    "**You should hear a beep when a data point is recorded.": 
        "gifs/Lesson3/0gifright.gif"
}

# Placeholder dictionaries for Lessons 4, 5, and 6
my_gif_dict_L4 = {
    #this gif is a placeholder -- CHANGE LATER
    3: "gifs/Lesson1/force_sensor_touch_button.gif" 
}

my_gif_dict_L5 = {
    "**Collect data for forward speed and distance" : 
        "gifs/Lesson5/5gifforward.gif",
    "**Collect data for backwards speed and distance": 
        "gifs/Lesson5/5gifbackward.gif",
}

my_gif_dict_L6 = {
    #this gif is a placeholder -- CHANGE LATER
    3: "gifs/Lesson1/force_sensor_touch_button.gif" 
}
    
#display custom gifs in side panel
def display_gif(imageName):
    """
    Display the specified GIF in the side panel.
    
    Args:
        imageName (str): The path to the GIF image to be displayed.
    """
    window.fadeImage(imageName)


def get_gif(gif_dict, print_statement):
    """
    Check if the print statement exists in the given GIF dictionary 
    and display the corresponding GIF if it does.
    
    Args:
        gif_dict (dict): The dictionary containing print statements as keys and
                        GIF paths as values.
        print_statement (str): The print statement to check for in dictionary.
    """
    if print_statement in gif_dict: 
        display_gif(gif_dict[print_statement])


#function responsible for changing lesson_num
def set_dictionary():
    """
    Set the current GIF dictionary based on the current lesson number.
    The lesson number is fetched from the global context.
    """
    my_globals.lesson_num = window.checkCurrentLesson() 
    print("Curr_lesson: ", my_globals.lesson_num)
    if my_globals.lesson_num == 1:
        my_globals.current_gif_dictionary = my_gif_dict_L1
    elif my_globals.lesson_num == 2:
        my_globals.current_gif_dictionary = my_gif_dict_L2
    elif my_globals.lesson_num == 3:
        my_globals.current_gif_dictionary = my_gif_dict_L3
    elif my_globals.lesson_num == 4:
        my_globals.current_gif_dictionary = my_gif_dict_L4
    elif my_globals.lesson_num == 5:
        my_globals.current_gif_dictionary = my_gif_dict_L5
    elif my_globals.lesson_num == 6:
        my_globals.current_gif_dictionary = my_gif_dict_L6

