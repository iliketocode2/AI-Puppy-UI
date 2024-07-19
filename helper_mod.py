from pyscript import document, window
import my_globals
import print_jav
import sensor_mod
import file_os
import helper_mod

def stop_running_code():
    if my_globals.terminal.connected:
        await my_globals.terminal.send('\x03')
        print('stopped code')

        #document.getElementById('gif').style.display = 'none' #do not do this
        window.fadeImage('') #do this to clear gifs

        print_jav.print_custom_terminal("Code execution ended. Please press the button to run the code again.")
        my_globals.found_key = False
        enable_buttons([my_globals.sensors, my_globals.download, my_globals.upload_file_btn, my_globals.save_btn])



def clean_up_disconnect():
    print("CLEANSHEESH")
    #if you are reading sensors and you physicaly disconnect
    if(my_globals.sensors.onclick == sensor_mod.close_sensor and my_globals.physical_disconnect): 
        print_jav.print_custom_terminal("Physically Disconnected while reading sensors - RELOAD PAGE")
        document.getElementById(f"lesson{my_globals.lesson_num}-link").click() #reload page
    if my_globals.terminal.connected:
        print('connected')
    print_jav.print_custom_terminal("Disconnected from your Spike Prime.")
    #my_globals.terminal.send('\x03') #to stop any program that is running
    #print('after disconnect, passed x03')
    my_globals.terminal.board.disconnect()

    #allow user to connect back
    my_globals.connect.innerText = 'Connect Spike Prime'
    disable_buttons([my_globals.sensors, my_globals.download, my_globals.custom_run_button, my_globals.save_btn, my_globals.upload_file_btn])

    # hide any gifs
    document.getElementById('gif').style.display = 'none'
    # document.getElementById('portInfo').style.display = 'block'

    #make the connect button green
    if (document.getElementById("connect-spike").classList.contains('connected')):
        document.getElementById("connect-spike").classList.remove('connected')
    

#removes files from the dropdown list of files (not the microprocessor). Removes all files except the one needed for the current lesson
async def remove_files():
    # make only the file that matches the page appear
    for i in range(my_globals.file_list.options.length - 1, -1, -1):
        option = my_globals.file_list.options.item(i)
        option_text = option.text
        if option_text != my_globals.proper_name_of_file[my_globals.lesson_num]:
            my_globals.file_list.removeChild(option)
    
    if my_globals.file_list.options.length == 0:
        new_option = document.createElement('option')
        new_option.text = "You do not have the right file. Please click the download button"
        # new_option.value = "new_file.py" # how you could add a new file
        my_globals.file_list.appendChild(new_option)
        my_globals.download.style.display = 'block'
        print('end of if statement')
    else:
        print('not empty')
        #my_globals.download.style.display = 'none'
        await on_select(None) #**needed for uploading 1st file

async def on_select(event):
    print("on selectsiuu")
    my_globals.my_green_editor.code = await file_os.read_code(my_globals.terminal, my_globals.file_list)

#evaluates code when the green button is pressed
async def handle_board(event):
    if event.type == 'mpy-run':
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


async def on_save(event):
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
        print("ENABLED BUTTONS ON SAVE")

    else:
        #print(my_globals.my_green_editor.code)
        window.alert("You do not have exactly 1 file in file-list")