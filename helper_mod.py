from pyscript import document, window
import my_globals
import print_jav
import sensor_mod
import file_os
import helper_mod
import asyncio

import time
def stop_running_code():
    my_globals.isRunning = False
    my_globals.found_key = False
    if my_globals.terminal.connected:
        await my_globals.terminal.send('\x03')
        print_jav.print_custom_terminal("Code execution ended. Please press the button to run the code again.")
        #await asyncio.sleep(0.1)  # prevent spamming 
        enable_buttons([my_globals.sensors, my_globals.download, my_globals.custom_run_button, my_globals.save_btn, my_globals.upload_file_btn, my_globals.connect])

        await sensor_mod.on_sensor_info(None) #display sensors
        print('stopped code')

        #document.getElementById('gif').style.display = 'none' #do not do this
        window.fadeImage('') #do this to clear gifs

    
        #enable_buttons([my_globals.sensors, my_globals.download, my_globals.upload_file_btn, my_globals.save_btn])



def clean_up_disconnect():
    print("CLEANSHEESH")
    #if you are reading sensors and you physicaly disconnect
    if(my_globals.sensors.onclick == sensor_mod.close_sensor): 
        print_jav.print_custom_terminal("Physically Disconnected while reading sensors - RELOAD PAGE")
        document.getElementById(f"lesson{my_globals.lesson_num}-link").click() #reload page
    #print('after disconnect, passed x03')
    if my_globals.terminal.connected:
        print('connected')
        print('after disconnect, passed x03')
        my_globals.terminal.send('\x03') #to stop any program that is running
        my_globals.terminal.board.disconnect()
    else:
        print("DISCONNECTED")
    if(my_globals.isRunning):
        document.getElementById('custom-run-button').click() #Display is not a ring running anymore

    print_jav.print_custom_terminal("Disconnected from your Spike Prime.")


    #allow user to connect back
    my_globals.connect.innerText = 'Connect'
    disable_buttons([my_globals.sensors, my_globals.download, my_globals.custom_run_button, my_globals.save_btn, my_globals.upload_file_btn])
    enable_buttons([my_globals.connect])

    

    #make the connect button green
    if (document.getElementById("connect-spike").classList.contains('connected')):
        document.getElementById("connect-spike").classList.remove('connected')
    

#removes files from the dropdown list of files (not the microprocessor). Removes all files except the one needed for the current lesson
async def remove_files():
    window.stopFadingWarningIcon() #important for resetting fading (avoids conflicts of having multiple fadings at once)
    # make only the file that matches the page appear
    for i in range(my_globals.file_list.options.length - 1, -1, -1):
        option = my_globals.file_list.options.item(i)
        option_text = option.text
        if option_text != my_globals.proper_name_of_file[my_globals.lesson_num]:
            my_globals.file_list.removeChild(option)
    
    if my_globals.file_list.options.length == 0:
        new_option = document.createElement('option')
        new_option.text = "You do not have the right file. Please click the download button"
        window.startFadingWarningIcon() 
        # new_option.value = "new_file.py" # how you could add a new file
        my_globals.file_list.appendChild(new_option)
        #my_globals.download.style.display = 'block' #nobueno- problems in shifting download icon
        print('end of if statement')
    else:
        print('not empty')
        window.stopFadingWarningIcon()

        #timeout for on_select (this could have been done by just calling on_select once)
        #but we are calling on_select multiple times until it doesn't give errors (usually it doesnt)
        #my_globals.download.style.display = 'none'
        timeout = 1  # Timeout duration in seconds (change this)
        timeout_count = 0
        max_timeout_count = 10 * timeout  # Adjust as necessary
        
        while True:
            try:
                await on_select(None)  # Attempt to call on_select
                print("on_select completed successfully")
                break
            except Exception as e:
                print(f"An error occurred while calling on_select: {e}")
                timeout_count += 1
                print("TIMEOUT", timeout_count)
                if timeout is not None and timeout_count >= max_timeout_count:
                    print("PROBLEM HERE")
                    document.getElementById(f"lesson{my_globals.lesson_num}-link").click() #reload page
                    break
            
            #(this is why timeout is in seconds --> 0.1 * max_timeout_count = 1 sec)
            await asyncio.sleep(0.1)  # Short delay before retrying 


async def on_select(event):
    print("on selectsiuu")
    my_globals.my_green_editor.code = await file_os.read_code(my_globals.terminal, my_globals.file_list)

#evaluates code when the green button is pressed
#running code = no sensors: stop code: running sensors/ start code
#times_array = []
async def handle_board(event):
   

    if event.type == 'mpy-run':
        my_globals.isRunning = True
        print("SIUUU")
        #global times_array
        #start_time = time.time()
        await sensor_mod.close_sensor()
        #end_time = time.time()
        #times_array.append(end_time - start_time)
        #print("My_array:", times_array)
        if my_globals.terminal.connected:
            disable_buttons([my_globals.sensors, my_globals.download, my_globals.custom_run_button, my_globals.upload_file_btn, my_globals.save_btn])
            print_jav.print_custom_terminal("Running code...")

            document.getElementById('gif').style.visibility = 'visible'
            document.getElementById('gif').style.display = 'block'
            code = event.detail.code

            await my_globals.terminal.eval('\x05' + code + "#**END-CODE**#" + '\x04')
            my_globals.terminal.focus()
            enable_buttons([my_globals.custom_run_button])
            return False  #return False to avoid executing on browser
        else:
            print('terminal not connected')
            return True
    # else:
    #     code = event.code

#take in a list of document elements
#aka things that look like: sensors = document.getElementById('sensor_readings')
def disable_buttons(list_to_disable):
    for element in list_to_disable:
        element.disabled = True #for actual functioning
        if element.id == 'custom-run-button':
            #element.classList.remove('is-active')  # remove the 'is-active' class
            element.classList.add('disabled')  # add a 'disabled' class
        else:
            element.classList.remove('active') #for displaying other buttons
def enable_buttons(list_to_disable):
    for element in list_to_disable:
        element.disabled = False #controls actually being able to click and activate it/calling corresponding function
        if element.id == 'custom-run-button':
            element.classList.remove('disabled')  # remove the 'disabled' class
        else:
            element.classList.add('active') #controls display for other buttons

#function that is called in JS when disconnecting
async def disconnect_calls_on_save():
    await on_save(None)
    await asyncio.sleep(2)  # allow download to finish before enabling sensors


async def on_save(event):
    await sensor_mod.close_sensor()
    if (my_globals.file_list.options.length == 1):
        helper_mod.disable_buttons([my_globals.sensors, my_globals.download, my_globals.connect, my_globals.custom_run_button, my_globals.save_btn, my_globals.upload_file_btn])
        #SAVING LOCALLY
        #print("AQUI")
        my_editor_code = my_globals.my_green_editor.code
        #print(my_globals.my_green_editor.code)
        #print("AQUI")
        current_option = my_globals.file_list.options.item(0) #get 1st and only file
        name_file = current_option.text # "CEEO_AI.py" for example
        print("MY_option", name_file)
        await my_globals.saving_js_module.save(my_editor_code, name_file)

        #SAVING ON SPIKE
        print_jav.print_custom_terminal("Saving code on SPIKE, please wait...")
        print_jav.print_custom_terminal("...")
        print_jav.print_custom_terminal("...")
        print_jav.print_custom_terminal("...")
        my_globals.progress_bar.style.display = 'block'
        status = await my_globals.terminal.download(name_file, my_editor_code)
        if not status: 
            window.alert(f"Failed to load {name_file}. Click Ok to continue downloading other files")  
        my_globals.progress_bar.style.display = 'none'
        print_jav.print_custom_terminal("Saved on SPIKE!")
        helper_mod.enable_buttons([my_globals.download, my_globals.sensors, my_globals.connect, my_globals.custom_run_button, my_globals.save_btn, my_globals.upload_file_btn])
        await asyncio.sleep(0.1)  # allow download to finish before enabling sensors
        
        #when the function on_save is called when disconnecting (either by yes_on_disconnect or no_on_disconnect)
        if (not my_globals.save_on_disconnect):
            await sensor_mod.on_sensor_info(None) #display sensors (only call this )
        print("ENABLED BUTTONS ON SAVE")

    else:
        #print(my_globals.my_green_editor.code)
        window.alert("You do not have exactly 1 file in file-list")