from pyscript import document
import ampy
def init():
    #variables
    global sensor, stop_loop, ARDUINO_NANO, SPIKE, javi_buffer, found_key, physical_disconnect
    global current_gif_dictionary, lesson_num
    stop_loop = False #indicates when to stop loop (u want it to stop when user has access to repl)
    ARDUINO_NANO = 128
    SPIKE = 256
    javi_buffer = ""
    found_key = False
    current_gif_dictionary = {} 
    lesson_num = -1
    physical_disconnect = True


    #elements
    global connect, download, path, sensors, custom_run_button, my_green_editor, file_list
    connect = document.getElementById('connect-spike')
    download = document.getElementById('download-code')
    path    = document.getElementById('gitpath')
    sensors = document.getElementById('sensor_readings')
    custom_run_button = document.getElementById('custom-run-button')
    my_green_editor = document.getElementById('MPcode') #for editor
    #for list of files
    file_list = document.getElementById('files')

  
    #terminal
    global terminal
    terminal = ampy.Ampy(SPIKE)