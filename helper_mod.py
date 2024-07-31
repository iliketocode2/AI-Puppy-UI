"""
helper_mod.py

Authors: Javier Laveaga, William Goldman

This script handles various operations for interacting with the Spike Prime 
board, including stopping code execution, cleaning up after disconnection, 
removing files, selecting files, handling board events, and enabling/disabling 
buttons.

"""

from pyscript import document, window
import my_globals
import print_jav
import sensor_mod
import file_os
import helper_mod
import asyncio
import my_gif

def stop_running_code():
    """
    Stops the currently running code, performs necessary cleanup, a
    nd updates the UI.

    This function stops the code execution on the Spike Prime, updates 
    the status in the UI, re-enables the buttons, and clears any displayed gifs.
    It assumes that the terminal is connected and that necessary global 
    variables are updated accordingly.

    Raises:
        None

    Returns:
        None
    """
    my_globals.isRunning = False
    my_globals.found_key = False
    if my_globals.terminal.connected:
        my_gif.display_gif("") #clear gifs when stop running
        await my_globals.terminal.send('\x03')
        print_jav.print_custom_terminal("""Code execution ended. Please press 
                                        the button to run the code again.""")
        enable_buttons([my_globals.sensors, my_globals.download, 
                        my_globals.custom_run_button, my_globals.save_btn, 
                        my_globals.upload_file_btn, my_globals.connect,
                        my_globals.file_list, my_globals.debug_btn, 
                        my_globals.terminal_btn])

        await sensor_mod.on_sensor_info(None) #display sensors
        print('stopped code')

        #document.getElementById('gif').style.display = 'none' #do not do this
        window.fadeImage('') #do this to clear gifs

def debugging_time():
    #disable file list 
    #file_list - file list globals
    helper_mod.disable_buttons([my_globals.debug_btn, my_globals.terminal_btn,
                                my_globals.file_list])
    await sensor_mod.close_sensor()
    helper_mod.enable_buttons([my_globals.terminal_btn])
    my_globals.terminal_btn.style.backgroundColor = "red"

#in custom terminal
def not_debugging():
    helper_mod.disable_buttons([my_globals.terminal_btn])
    helper_mod.enable_buttons([my_globals.debug_btn, my_globals.download, 
                            my_globals.sensors, my_globals.connect, 
                            my_globals.custom_run_button, my_globals.save_btn, 
                            my_globals.upload_file_btn, my_globals.file_list])
    my_globals.terminal_btn.style.backgroundColor = "#ccc"
    await sensor_mod.on_sensor_info(None)





def clean_up_disconnect():
    """
    Cleans up after a disconnection event, stops any running program, 
    and updates the UI.

    This function handles the disconnection of the Spike Prime, stops any 
    running program, updates the UI to reflect the disconnection, and 
    re-enables/disables appropriate buttons. 
    
    It is called by the disconnect callback in main.py (second_half_disconnect)

    Raises:
        None

    Returns:
        None
    """
    print("CLEANSHEESH")
    #if you are reading sensors and you physicaly disconnect
    if(my_globals.sensors.onclick == sensor_mod.close_sensor): 
        print_jav.print_custom_terminal("""Physically Disconnected while 
                                        reading sensors - RELOADING PAGE""")
        #reloads page
        document.getElementById(f"lesson{my_globals.lesson_num}-link").click() 
    if my_globals.terminal.connected:
        print('connected')
        print('after disconnect, passed x03')
        my_globals.terminal.send('\x03') #to stop any program that is running
        my_globals.terminal.board.disconnect()
    else:
        print("DISCONNECTED")
    if(my_globals.isRunning):
        #stops animation of run buttton (displaying purposes)
        document.getElementById('custom-run-button').click() 

    print_jav.print_custom_terminal("Disconnected from your Spike Prime.")

    #allow user to connect back
    my_globals.connect.innerText = 'Connect'
    disable_buttons([my_globals.sensors, my_globals.download, 
                     my_globals.custom_run_button, my_globals.save_btn, 
                     my_globals.upload_file_btn, my_globals.file_list,
                     my_globals.debug_btn, my_globals.terminal_btn])
    enable_buttons([my_globals.connect])

    #make the connect button green
    if (my_globals.connect.classList.contains('connected')):
        my_globals.connect.classList.remove('connected')
    


async def check_files():
    """
    Iterates through the list of files and checks to see if it contains
    the appropriate Main Lesson file and CEEO_AI.py. If it does, it
    opens the lesson file automatically on the editor. 

    If it doesn't it prompts you to click on download button with a warning

    Raises:
        None

    Returns:
        None
    """
   
    #important for resetting fading (avoids conflicts of having multiple
    # fadings at once)
    window.stopFadingWarningIcon() 
    # check to see if proper files are contained (Lesson file and CEEO)
    Lesson_file_found = False
    ceeo_file_found = False
    for i in range(my_globals.file_list.options.length - 1, -1, -1):
        option = my_globals.file_list.options.item(i)
        option_text = option.text
        if option_text == my_globals.proper_name_of_file[my_globals.lesson_num]:
            Lesson_file_found = True
        if option_text == "/flash/CEEO_AI.py":
            print("AQUIUIUUIIUI")
            ceeo_file_found = True
            
    
    if not Lesson_file_found or not ceeo_file_found:
        new_option = document.createElement('option')
        error_string = (
            "You do not have the right file. Please click the download button"
        )
        new_option.text = error_string
        window.startFadingWarningIcon() 
        my_globals.file_list.appendChild(new_option)
        #makes error_string be the 'file' that is selected
        my_globals.file_list.value = error_string
        print('end of if statement')
        enable_buttons([my_globals.sensors, my_globals.download, 
                my_globals.custom_run_button, my_globals.save_btn, 
                my_globals.upload_file_btn, my_globals.connect, 
                my_globals.file_list, my_globals.debug_btn, 
                my_globals.terminal_btn])
        await sensor_mod.on_sensor_info(None) #display sensors
    else:
        #so that the lesson file is displayed automatically
        my_globals.file_list.value = my_globals.proper_name_of_file[
                                            my_globals.lesson_num] 
        print('not empty')
        window.stopFadingWarningIcon()
        await on_select(None)  # Attempt to call on_select
        
             


async def on_select(event):
    """
    Handles the file selection event, attempts to read the selected file's code,
    and updates the editor.

    This function is triggered when a file is selected from the dropdown. 
    It attempts to read the code from the selected file and updates the editor 
    with the file's content. The function retries in case of errors up to a 
    maximum timeout count and updates the UI accordingly.

    Args:
        event (Event): The event object representing the file selection event.

    Raises:
        Exception: If reading the file's code fails repeatedly until 
        the timeout count is reached.

    Returns:
        None
    """
    await sensor_mod.close_sensor()
    print("on selectsiuu")
    #We are calling on_select multiple times until it doesn't give errors 
    # (usually it doesn't)
    timeout = 1  # Timeout duration in seconds (change this) 
    #**will remain in seconds if asyncion.sleep remains at 0.1
    timeout_count = 0
    max_timeout_count = 10 * timeout  # Adjust as necessary
    
    while True:
        try:
            my_globals.my_green_editor.code = await file_os.read_code(
                my_globals.terminal, my_globals.file_list)
            print("on_select completed successfully")
            break
        except Exception as e:
            print(f"An error occurred while calling on_select: {e}")
            timeout_count += 1
            print("TIMEOUT", timeout_count)
            if timeout is not None and timeout_count >= max_timeout_count:
                print("PROBLEM HERE")
                document.getElementById(
                    f"lesson{my_globals.lesson_num}-link").click() #reload page
                break
        
        #(this is why timeout is in seconds --> 0.1 * max_timeout_count = 1 sec)
        await asyncio.sleep(0.1)  # Short delay before retrying 
    enable_buttons([my_globals.sensors, my_globals.download, 
                    my_globals.custom_run_button, my_globals.save_btn, 
                    my_globals.upload_file_btn, my_globals.connect, 
                    my_globals.file_list, my_globals.debug_btn, 
                    my_globals.terminal_btn])
    await sensor_mod.on_sensor_info(None) #display sensors

#evaluates code when the green button is pressed
async def handle_board(event):
    """
    Handles the board event when the green run button is pressed 
    and evaluates the code.

    This function is triggered by an event, specifically when the custom run 
    button ('mpy-run') is pressed. It updates the global state, 
    disables certain buttons, displays a loading indicator, and sends code to 
    the terminal for evaluation. It also handles cases where the terminal 
    is not connected.

    Args:
        event (Event): The event object representing the button press, 
        containing details like the code to run.

    Raises:
        None

    Returns:
        bool: see below
    """
    if event.type == 'mpy-run': #even of hitting our custom run button
        my_globals.isRunning = True
        print("SIUUU")
        await sensor_mod.close_sensor()
        if my_globals.terminal.connected:
            disable_buttons([my_globals.sensors, my_globals.download, 
                             my_globals.custom_run_button, 
                             my_globals.upload_file_btn, my_globals.save_btn,
                             my_globals.debug_btn, my_globals.terminal_btn])
            print_jav.print_custom_terminal("Running code...")
            if my_globals.lesson_num == 3: #display this at the very beginning
                my_gif.display_gif("gifs/Lesson3/0gifsensor.gif")

            document.getElementById('gif').style.visibility = 'visible'
            document.getElementById('gif').style.display = 'block'
            code = event.detail.code

            await my_globals.terminal.eval('\x05' + code + "#**END-CODE**#" + 
                                           '\x04')
            my_globals.terminal.focus()
            enable_buttons([my_globals.custom_run_button])
            return False  #return False to avoid executing on browser
        else:
            print('terminal not connected')
            return True
    # 'else' is needed only if using the default editor run button (we hid it)
    # else:
    #     code = event.code 



def disable_buttons(list_to_disable):
    """
    Disables a list of buttons and updates their display state.

    This function iterates over a list of button elements and disables them,
    preventing user interaction. It also updates the visual state of the buttons
    by adding a 'disabled' class to the 'custom-run-button' and removing the 
    'active' class from other buttons.

    Args:
        list_to_disable (list): A list of document elements representing buttons
        to be disabled.

    Returns:
        None
    """
    for element in list_to_disable:
        element.disabled = True #for actual functioning
        if element.id == 'custom-run-button':
            element.classList.add('disabled')  # add a 'disabled' class
        elif (element.classList.contains('button1')): #if you are a button 1
            element.classList.remove('active')
        


def enable_buttons(list_to_disable):
    """
    Enables a list of buttons and updates their display state.

    This function iterates over a list of button elements and enables them,
    allowing user interaction. It also updates the visual state of the buttons
    by removing the 'disabled' class from the 'custom-run-button' and adding 
    the 'active' class to other buttons.

    Args:
        list_to_enable (list): A list of document elements representing 
        buttons to be enabled.

    Returns:
        None
    """
    for element in list_to_disable:
        #controls actually being able to click and activate it/calling 
        #corresponding function
        element.disabled = False #includes disabling select
        if element.id == 'custom-run-button':
            element.classList.remove('disabled')  # remove the 'disabled' class
        elif (element.classList.contains('button1')): #if you are a button 1
            element.classList.add('active') #controls display for other buttons
        


async def on_save(event):
    """
    Handles the process of saving code from the editor and updating the user 
    interface.

    This function performs the following tasks:
    1. Closes any active sensors.
    2. Disables buttons to prevent user interaction during the save process.
    3. Saves the current code locally on the user's computer.
    4. Saves the code onto a SPIKE robot.
    5. Updates the user interface to reflect the saving status.
    6. Re-enables the buttons and updates the sensor display if the save is 
        not triggered by a disconnect event.

    Args:
        event (Event): The event object triggered by the save action. 
        This parameter is currently not used in the function but is required 
        for asynchronous handling.

    Returns:
        None
    """
    await sensor_mod.close_sensor()

    #SAVING LOCALLY
    my_editor_code = my_globals.my_green_editor.code #code in editor
    #get name of file that is currently selected (value)
    name_file = my_globals.file_list.value # "CEEO_AI.py" for example
    print("MY_option", name_file)
    #passing code and name of file (to save locally on computer)
    await my_globals.saving_js_module.save(my_editor_code, name_file)

    #SAVING ON SPIKE robot
    print_jav.print_custom_terminal("Saving code on SPIKE, please wait...")
    print_jav.print_custom_terminal("...")
    print_jav.print_custom_terminal("...")
    print_jav.print_custom_terminal("...")
    my_globals.progress_bar.style.display = 'block'
    status = await my_globals.terminal.download(name_file, my_editor_code)
    if not status: 
        window.alert(f"""Failed to load {name_file}. 
                        Click Ok to continue downloading other files""")  
    my_globals.progress_bar.style.display = 'none'
    print_jav.print_custom_terminal("Saved on SPIKE!")
    helper_mod.enable_buttons([my_globals.download, my_globals.sensors, 
                               my_globals.connect, my_globals.custom_run_button,
                               my_globals.save_btn, my_globals.upload_file_btn, 
                               my_globals.file_list, my_globals.debug_btn])
    await asyncio.sleep(0.1)  # allow download to finish before enabling sensors
    
    #only display sensors when save is called by clicking save button
    #prevents errors when calling save on disconnect
    if (not my_globals.save_on_disconnect):
        await sensor_mod.on_sensor_info(None) #display sensors (only call this)
        print("ENABLED BUTTONS ON SAVE")




