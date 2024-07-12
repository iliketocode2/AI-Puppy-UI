from pyscript import document
import my_globals
import print_jav
import sensor_mod
import file_os

def stop_running_code():
    enable_buttons([my_globals.sensors, my_globals.download])
    global isRunning
    if my_globals.terminal.connected:
        await my_globals.terminal.send('\x03')
        print('stopped code')
    
    isRunning = False
    document.getElementById('gif').style.display = 'none'
    # document.getElementById('portInfo').style.display = 'block'
    print_jav.print_custom_terminal("Code execution ended. Please press the button to run the code again.")


def clean_up_disconnect():
    print("CLEANSHEESH")
    if(my_globals.sensors.onclick == sensor_mod.close_sensor and my_globals.physical_disconnect): 
        print_jav.print_custom_terminal("Physically Disconnected while reading sensors - RELOAD PAGE")
        document.getElementById(f"lesson{my_globals.lesson_num}-link").click() #reloadp
    if my_globals.terminal.connected:
        print('connected')
    print_jav.print_custom_terminal("Disconnected from your Spike Prime.")
    #my_globals.terminal.send('\x03') #to stop any program that is running
    print('after disconnect, passed x03')
    my_globals.terminal.board.disconnect()
    my_globals.sensors.disabled = True
    my_globals.download.disabled = True

    #allow user to connect back
    my_globals.connect.disabled = False
    my_globals.connect.innerText = 'Connect Spike Prime'

    # hide any gifs
    document.getElementById('gif').style.display = 'none'
    # document.getElementById('portInfo').style.display = 'block'

    #remove button active display when disconnect
    if (document.getElementById("connect-spike").classList.contains('connected')):
        document.getElementById("connect-spike").classList.remove('connected')
    if (document.getElementById("custom-run-button").classList.contains('active')):
        document.getElementById("custom-run-button").classList.remove('active')
    if (document.getElementById("download-code").classList.contains('active')):
        document.getElementById("download-code").classList.remove('active')
    if (document.getElementById("sensor_readings").classList.contains('active')):
        document.getElementById("sensor_readings").classList.remove('active')


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
        print('end of if statement')
    else:
        await on_select(None) #**needed for uploading 1st file

async def on_select(event):
    print("on selectsiuu")
    my_globals.my_green_editor.code = await file_os.read_code(my_globals.terminal, my_globals.file_list)

#evaluates code when the green button is pressed
async def handle_board(event):
    my_globals.found_key = False
    # run program for custom buttton to run pyscript editor
    if event.type == 'mpy-run':
        disable_buttons([my_globals.sensors, my_globals.download, my_globals.custom_run_button])
        print_jav.print_custom_terminal("Running code...")
        # document.getElementById('portInfo').style.display = 'none'
        document.getElementById('gif').style.visibility = 'visible'
        document.getElementById('gif').style.display = 'block'
        code = event.detail.code
    else:
        code = event.code

    if my_globals.terminal.connected and not my_globals.isRunning:
        my_globals.isRunning = True
        try:
            await my_globals.terminal.eval('\x05' + code + "#**END-CODE**#" + '\x04') #very important: somehow pastes the whole code before running
            #await terminal.eval('\x05'+"#**END-CODE**#"+'\x04')
            my_globals.terminal.focus()
            print("Hello_ish")
        except:
            print('EXCEPT ERROR')
            pass
        finally:
            if my_globals.isRunning:  #only print completion if not stopped manually
                print_jav.print_custom_terminal("...")
            enable_buttons([my_globals.custom_run_button]) #disable and enable custom button to prevent spamming and errors
            my_globals.isRunning = False
        return False  #return False to avoid executing on browser
    else:
        return True
    
#take in a list of document elements
#aka things that look like: sensors = document.getElementById('sensor_readings')
def disable_buttons(list_to_disable):
    for element in list_to_disable:
        element.disabled = True #for actual functioning
        element.classList.remove('active') #for displaying
def enable_buttons(list_to_disable):
    for element in list_to_disable:
        element.disabled = False #controls actually being able to click and activate it/calling corresponding function
        element.classList.add('active') #controls display