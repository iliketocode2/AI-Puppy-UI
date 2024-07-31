"""
main.py

This module provides the main functionality for interfacing with the Spike Prime
system, using PyScript, handling connections, file downloads, sensor data, 
and user interactions through a web interface.

Authors:
    - Javier Laveaga
    - William Goldman

References:
    - xterm.js: https://xtermjs.org/docs/api/terminal/classes/terminal/#options
"""


from pyscript import document, window, when
from js import window
import ampy
import restapi
import asyncio
import time
import file_os
import my_globals
import sensor_mod
import print_jav
import my_gif
import helper_mod

my_globals.init() #initializing my global variables

ARDUINO_NANO = 128
SPIKE = 256

def on_custom_disconnect(event=None):
    """
    Handle custom disconnection event from the Spike Prime.
    
    Args:
        event (optional): The event triggering the disconnection.
    """
    print_jav.print_custom_terminal("Disconnected from your Spike Prime.")
    #if sensor data is displayed, hide it, bring back the terminal, and reset
    if (my_globals.sensors.onclick == sensor_mod.close_sensor):
        print('clearing sensor data')
        await sensor_mod.close_sensor()
    
    #give user option to save or not
    document.getElementById('overlay').style.display = 'flex'
    



#callback when disconnected physically
def second_half_disconnect(event=None):
    """
    Handle the second half of the disconnection process. Callback when method 
    disconnect is called on terminal.
    
    Args:
        event (optional): The event triggering the disconnection.
    """
    my_globals.connect.onclick = on_connect
    window.fadeImage(' ') #do this to clear gifs
    helper_mod.clean_up_disconnect()
    
async def call_get_list():
    """
    Calls function get_list, which gets the list of files on SPIKE. 
    It calls it a max amount of 10 times until it succeeds. 
    (This was done becaue get_list gives errors sometimes when it gets 
    called. It usually works on the second try)
    
    """
    #ERROR CHECKING
    timeout = 1  # Timeout duration in seconds (change this)
    timeout_count = 0
    max_timeout_count = 10 * timeout  # Adjust as necessary
    while True:
        try:
            await file_os.getList(my_globals.terminal, my_globals.file_list)
            print("get_list completed successfully")
            break
        except Exception as e:
            print(f"An error occurred while calling get_list: {e}")
            timeout_count += 1
            print("TIMEOUT", timeout_count)
            if timeout is not None and timeout_count >= max_timeout_count:
                print("PROBLEM HERE")
                document.getElementById(f"""lesson{my_globals.lesson_num}
                                        -link""").click() #reload page
                break
        
        #(this is why timeout is in seconds --> 0.1 * max_timeout_count = 
        # 1 sec)
        await asyncio.sleep(0.1)  # Short delay before retrying 
    #ERROR CHECKING
    

async def on_connect(event):
    """
    Handle connection event to the Spike Prime.
    
    Args:
        event (optional): The event triggering the connection.
    """
    helper_mod.disable_buttons([my_globals.sensors, my_globals.download, 
            my_globals.connect, my_globals.custom_run_button, 
            my_globals.save_btn, my_globals.upload_file_btn])
    my_globals.connect.innerHTML = 'Connecting...'
    await my_globals.terminal.board.connect('repl')

    if my_globals.terminal.connected:
        #enable buttons
        #turn on progress bar to indicate begginning of initialization
        my_globals.progress_bar.style.display = 'block' 
        my_globals.progress_bar.value = 0

        #to prevent user from inputting during paste
        document.getElementById('repl').style.display = 'none' 
        
        #Initializing sensor code (below)
        print("Before paste")
        my_globals.progress_bar.value = 25
        await my_globals.terminal.paste(sensor_mod.sensor_code, 'hidden')
        print("After paste")
        my_globals.progress_bar.value = 50

        #initializng file list code, hide scroll bar
        document.getElementById('terminalFrameId').style.overflow = 'hidden'
        my_globals.progress_bar.value = 75
        print("Before-THEE-LIST")

        await call_get_list()


        print("THEE-LIST")
        my_globals.progress_bar.value = 100
        document.getElementById('terminalFrameId').style.overflow = 'scroll'

        #enable disconnect
        my_globals.connect.classList.add('connected')
        my_globals.connect.innerHTML = 'Disconnect'
        my_globals.connect.onclick = on_custom_disconnect
        print_jav.print_custom_terminal("""Connected to your Spike Prime. 
                                        Welcome!""")

        #show gifs and files
        document.getElementById('files').style.visibility = 'visible'
        #allow user to input only after paste is done
        document.getElementById('repl').style.display = 'block' 
        #terminal.terminal.attachCustomKeyEventHandler(on_user_input)

        my_globals.progress_bar.style.display = 'none'
     
        
        await helper_mod.check_files() #updated (displays sensors)
    else:
        #allow user to connect back if they clicked 'cancel' 
        #when choosing the port to connect to
        second_half_disconnect()

async def on_load(event):
    """
    Handle load event for downloading files (on html) code to the Spike Prime.
    Downloads files specified in the html textarea with id = 'gitpath'
    This is my_globals.path
    
    Args:
        event (optional): The event triggering the load.
    """
    print("on load")
    await sensor_mod.close_sensor() #close sensors
    print("SIMON")
    if my_globals.terminal.connected:
        print_jav.print_custom_terminal("Downloading code, please wait...")

        git_paths = my_globals.path.value.split() #gets arrays of urls
        #enable progress bar
        my_globals.progress_bar.style.display = 'block'
        my_globals.percent_text.style.display = 'block'
        
        counter = 1 #number of files
        for current_path in git_paths:
            name = current_path.split('/')[-1] 
            print('path, name: ',current_path,name)

            my_globals.percent_text.innerHTML = (
                "Downloading " + name + " (" + str(counter) + "/" + 
                str(len(git_paths)) + ")"
            )

            reply = await restapi.get(current_path)
            status = await my_globals.terminal.download(name,reply)
            counter += 1
            if not status: 
                window.alert(
                    f"Failed to load {name}. Click Ok to continue " 
                    "downloading other files"
                    
                )  
        
        #initializng file list code, hide scroll bar
        document.getElementById('terminalFrameId').style.overflow = 'hidden'

        await call_get_list()

        document.getElementById('terminalFrameId').style.overflow = 'scroll'
    
        my_globals.progress_bar.style.display = 'none'
        my_globals.percent_text.style.display = 'none'
        #await asyncio.sleep(0.4)  # Short delay before enablign download
        print_jav.print_custom_terminal("Download complete!")
        #check to see that you have appropriate files and update UI
        await helper_mod.check_files() #enables buttons by calling on_select
        
    else:
        window.alert('connect to a processor first')

@when("change", "#fileRead")
async def on_upload_file(event): 
    """
    Handle file upload event from the local system. 
    Gets programmatically called when clicking upload button
    
    Args:
        event (optional): The event triggering the file upload.
    """
    print("JAV")
    path = my_globals.fileName.value
    print(path)
    #saving_js_module is really an instance of the class 'Files' 
    # in file_library.js
    code_retrieved = await my_globals.saving_js_module.read('fileRead') 
    #content.innerText = code_retrieved
    #making editor show the code just fetched
    my_globals.my_green_editor.code = code_retrieved
    print('file beginning: ',code_retrieved[:10])
    

def yes_on_disconnect(event):
    """
    Handle confirmation of saving data on disconnection.
    
    Args:
        event (optional): The event triggering the confirmation - 
        clicking the yes button.
    """
    document.getElementById('overlay').style.display = 'none'
    my_globals.save_on_disconnect = True
    await helper_mod.on_save(None) 
    my_globals.physical_disconnect = False
    second_half_disconnect()
    document.getElementById('sensor-info').innerHTML = ""   
    helper_mod.enable_buttons([my_globals.connect])

    
def no_on_disconnect(event):
    """
    Handle denial of saving data on disconnection.
    
    Args:
        event (optional): The event triggering the denial. - 
        clicking the no button
    """
    document.getElementById('overlay').style.display = 'none'
    my_globals.save_on_disconnect = True
    my_globals.physical_disconnect = False
    second_half_disconnect()
    #clear sensor display
    document.getElementById('sensor-info').innerHTML = ""  
    helper_mod.enable_buttons([my_globals.connect]) 
    


# expose stop_running_code function to JavaScript
window.stop_running_code = helper_mod.stop_running_code

# expose debugging_time function to JavaScript
window.debugging_time = helper_mod.debugging_time
window.not_debugging = helper_mod.not_debugging

# expose stop_running_code function to JavaScript
window.on_save = helper_mod.on_save

#assigning buttons to functions to be called onclick
my_globals.save_btn.onclick = helper_mod.on_save
my_globals.my_green_editor.addEventListener('mpy-run', helper_mod.handle_board)
my_globals.my_green_editor.handleEvent = helper_mod.handle_board

#Assigning clicks to functions
my_globals.file_list.onchange = helper_mod.on_select
my_globals.connect.onclick = on_connect
my_globals.download.onclick = on_load
my_globals.sensors.onclick = sensor_mod.on_sensor_info
my_globals.yes_btn.onclick = yes_on_disconnect
my_globals.no_btn.onclick = no_on_disconnect


#start disabled until connected
helper_mod.disable_buttons([my_globals.sensors, my_globals.download, 
                    my_globals.custom_run_button, my_globals.save_btn, 
                    my_globals.upload_file_btn])

my_globals.debug_btn.disabled = True
my_globals.terminal_btn.disabled = True

helper_mod.enable_buttons([my_globals.connect])
#set a callback function that is called when disconnection happens
my_globals.terminal.disconnect_callback = second_half_disconnect
#set a callback function that is called every time data is received 
#this function is called every time the user types on repl/debug for example
my_globals.terminal.newData_callback = print_jav.on_data_jav 

#set current dictionary for desired lesson
my_gif.set_dictionary()


 
