"""
my_globals.py

This module initializes and manages global variables and elements used 
throughout the application. It handles the setup for various UI elements, 
global settings, and configurations related to the SPIKE and Arduino 
environments.

Authors:
    - Javier Laveaga
    - William Goldman

Functions:
    - init(): Initializes global variables, UI elements, and configurations.

Global Variables:
    - stop_loop: Indicates when to stop the sensors loop.
    - ARDUINO_NANO: Buffer size for Arduino Nano.
    - SPIKE: Buffer size for SPIKE.
    - javi_buffer: Buffer for printing module.
    - found_key: Flag indicating whether a key has been found.
    - current_gif_dictionary: Dictionary for storing current GIFs.
    - custom_terminal_ele: Element for displaying custom terminal messages.
    - lesson_num: Current lesson number.
    - physical_disconnect: Flag indicating if a physical disconnect is allowed.
    - isRunning: Flag indicating whether the system is currently running.

    - proper_name_of_file: Dictionary mapping lesson numbers to their respective
                            file paths.

    - connect: Button element for connecting to SPIKE.
    - download: Button element for downloading code.
    - upload_file_btn: Button element for uploading files.
    - custom_run_button: Button element for running custom code.
    - path: Element displaying the Git path.
    - sensors: Element displaying sensor readings.
    - my_green_editor: Editor element for code input.
    - progress_bar: Element displaying the progress of operations.
    - file_list: Element displaying the list of files.
    - percent_text: Element displaying the progress percentage.
    - percent_div: Element containing the progress percentage.
    - fileName: Element for file input when uploading a file
    - save_on_disconnect: Flag indicating whether to save on disconnect.
    - yes_btn: Button element for confirming save on disconnect.
    - no_btn: Button element for canceling save on disconnect.

    - saving_js_module: Instance of the file_library module for file saving 
                        and uploading.
    - terminal: Instance of the ampy.Ampy class, 
                configured for SPIKE or Arduino Nano.

Dependencies:
    - pyscript: Provides access to document and JS modules.
    - ampy: Provides the Ampy class for terminal operations.
    - file_library: Provides methods for file saving and uploading.
"""
from pyscript import document
from pyscript.js_modules import file_library
import ampy
def init():
    """
    Initializes global variables, UI elements, and configurations for the 
    application. Sets up the environment for interaction with SPIKE and Arduino 
    devices, and prepares necessary UI components and global settings.

    """
    #variables
    global sensor, stop_loop, ARDUINO_NANO, SPIKE, javi_buffer, found_key
    global physical_disconnect, proper_name_of_file, isRunning
    global current_gif_dictionary, lesson_num, custom_terminal_ele

    #indicates when to stop sensors loop
    stop_loop = False 

    #Buffer sizes (using SPIKE for now)
    ARDUINO_NANO = 128
    SPIKE = 256

    #globals for printing purposes
    javi_buffer = ""  #buffer for printing module
    found_key = False
    current_gif_dictionary = {} 
    custom_terminal_ele = document.getElementById('customTerminalMessage')

    lesson_num = -1

    physical_disconnect = True
    isRunning = False

    proper_name_of_file = {
        1: "/flash/Main_Lesson1.py",
        2: "/flash/Main_Lesson2.py",
        3: "/flash/Main_Lesson3.py",
        4: "/flash/Main_Lesson4.py",
        5: "/flash/Main_Lesson5.py",
        6: "/flash/Main_Lesson6.py"
    }

    #elements
    global connect, download, path, sensors, custom_run_button, my_green_editor
    global file_list, progress_bar, percent_text
    global percent_div, save_btn, upload_file_btn, fileName, save_on_disconnect
    global yes_btn, no_btn, debug_btn, terminal_btn

    #buttons
    save_btn = document.getElementById('save_button')
    connect = document.getElementById('connect-spike')
    download = document.getElementById('download-code')
    upload_file_btn = document.getElementById('chooseFileButton')
    custom_run_button = document.getElementById('custom-run-button')
    debug_btn = document.getElementById('defaultTerminalButton')
    terminal_btn = document.getElementById('customTerminalButton')

    path    = document.getElementById('gitpath')
    sensors = document.getElementById('sensor_readings')
    my_green_editor = document.getElementById('MPcode') #for editor
    progress_bar = document.getElementById('progress')
    
    file_list = document.getElementById('files') #for list of files

    percent_text = document.getElementById('progress-percent')
    percent_div = document.getElementById('progressDiv')

    #for uploading files
    fileName = document.getElementById('fileRead') 

    #for saving on disconnect
    save_on_disconnect = False
    yes_btn = document.getElementById('Yes-btn')
    no_btn = document.getElementById('No-btn')
    
    #JS-class instances for file saving and uploading
    global saving_js_module
    saving_js_module = file_library.newFile()

    #terminal
    global terminal
    #terminal = ampy.Ampy(SPIKE, progress_bar) #use this if using arduino
    terminal = ampy.Ampy(ARDUINO_NANO, progress_bar)