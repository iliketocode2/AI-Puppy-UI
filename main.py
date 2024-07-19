# https://xtermjs.org/docs/api/terminal/classes/terminal/#options
#https://pyscript.com/@agiammarchi/spike-ide-copy/latest
#BLE_CEEO_url = 'https://raw.githubusercontent.com/chrisbuerginrogers/SPIKE_Prime/main/BLE/BLE_CEEO.py'
#WEEE

from pyscript import document, window, when #TODOO: delete when once done with on_upload_file
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

my_globals.init()

ARDUINO_NANO = 128
SPIKE = 256

    

def on_custom_disconnect(event=None):
    print_jav.print_custom_terminal("Disconnected from your Spike Prime.")
    #display_gif("nobgimages/aipuppy2_360-removebg-preview.png")
    #global sensor

    #if sensor data is displayed, hide it, bring back the terminal, and reset
    if (my_globals.sensors.onclick == sensor_mod.close_sensor):
        print('clearing sensor data')
        await sensor_mod.close_sensor()
    
    #Saving files
    await helper_mod.on_save(None)
    my_globals.physical_disconnect = False
    second_half_disconnect()
    

    #clear sensor display
    document.getElementById('sensor-info').innerHTML = ""   

#callback when disconnected physically
def second_half_disconnect(event=None):
    my_globals.connect.onclick = on_connect
    helper_mod.clean_up_disconnect()
    print_jav.print_custom_terminal("Saving your code...")


async def on_connect(event):
    helper_mod.disable_buttons([my_globals.sensors, my_globals.download, my_globals.connect, my_globals.custom_run_button, my_globals.save_btn, my_globals.upload_file_btn])
    my_globals.connect.innerHTML = 'Connecting...'
    await my_globals.terminal.board.connect('repl')

    if my_globals.terminal.connected:
        #enable buttons
        my_globals.progress_bar.style.display = 'block' #turn on progress bar to indicate begginning of initialization
        my_globals.progress_bar.value = 0

        document.getElementById('repl').style.display = 'none' #to prevent user from inputting during paste
        
        #Initializing sensor code (below)
        print("Before paste")
        #await terminal.paste(sensor_code, 'hidden')
        my_globals.progress_bar.value = 25
        await my_globals.terminal.paste(sensor_mod.sensor_code, 'hidden')
        print("After paste")
        my_globals.progress_bar.value = 50

        #initializng file list code, hide scroll bar
        document.getElementById('terminalFrameId').style.overflow = 'hidden'
        my_globals.progress_bar.value = 75
        print("Before-THEE-LIST")
        await file_os.getList(my_globals.terminal, my_globals.file_list)
        print("THEE-LIST")
        my_globals.progress_bar.value = 100
        document.getElementById('terminalFrameId').style.overflow = 'scroll'

        if my_globals.lesson_num == 3: #display this at the very beginning
            my_gif.display_gif("gifs/Lesson3/Multiple_sensors.gif")
        
        await helper_mod.remove_files()

        
        #enable disconnect
        my_globals.connect.classList.add('connected')
        my_globals.connect.innerHTML = 'Disconnect'
        my_globals.connect.onclick = on_custom_disconnect
        print_jav.print_custom_terminal("Connected to your Spike Prime. Welcome!")
        # display_gif("nobgimages/aipuppy5_480-removebg-preview.png")

        #initializing user interface
        helper_mod.enable_buttons([my_globals.connect, my_globals.custom_run_button, my_globals.sensors, my_globals.download, my_globals.save_btn, my_globals.upload_file_btn])
        #show gifs and files
        document.getElementById('files').style.visibility = 'visible'
        document.getElementById('repl').style.display = 'block' #allow user to input only after paste is done
        #terminal.terminal.attachCustomKeyEventHandler(on_user_input)

        my_globals.progress_bar.style.display = 'none'

    else:
        #allow user to connect back if they clicked 'cancel' when choosing the port to connect to
        second_half_disconnect()

#NEXT STEP: download more tha n 1 file (length of path). make for loop (chat)
async def on_load(event):
    print("on load")
    if my_globals.terminal.connected:
        helper_mod.disable_buttons([my_globals.download, my_globals.sensors, my_globals.connect, my_globals.custom_run_button])
        print_jav.print_custom_terminal("Downloading code, please wait...")
        document.getElementById('download-code').innerHTML = 'Downloading Code'
        # document.getElementById('repl').style.display = 'none' #hide repl to prevent from seeing output in repl

        git_paths = my_globals.path.value.split() #gets arrays of urls
        #download_statuses = [] #will store statuses for each file 
        
        #github = path.value #gets url (useless now)
        
        #sisenor
        my_globals.progress_bar.style.display = 'block'
        my_globals.percent_text.style.display = 'block'
        counter = 1

        for current_path in git_paths:
            name = current_path.split('/')[-1] 
            print('path, name: ',current_path,name)

            my_globals.percent_text.innerHTML = "Downloading " + name + " (" + str(counter) + "/" + str(len(git_paths)) + ")"

            reply = await restapi.get(current_path)
            #print("REPLY")
            #print(reply)
            #print("REPLY")
            status = await my_globals.terminal.download(name,reply)
            counter += 1
            if not status: 
                window.alert(f"Failed to load {name}. Click Ok to continue downloading other files")  
        
        #initializng file list code, hide scroll bar
        document.getElementById('terminalFrameId').style.overflow = 'hidden'
        await file_os.getList(my_globals.terminal, my_globals.file_list)
        document.getElementById('terminalFrameId').style.overflow = 'scroll'
        await helper_mod.remove_files() #remove every files from dropdown menu except desired lesson file
        #await on_select(None)
        #show scroll bar
        #copy

        my_globals.progress_bar.style.display = 'none'
        my_globals.percent_text.style.display = 'none'
        helper_mod.enable_buttons([my_globals.download, my_globals.sensors, my_globals.connect, my_globals.custom_run_button])
        print_jav.print_custom_terminal("Download complete!")
        #document.getElementById('download-code').innerHTML = 'Download Training Code'
        
        #document.getElementById('repl').style.display = 'block'
        
    else:
        window.alert('connect to a processor first')

'''
@when("click", "#local")
async def on_save(event): 
    filename = fileName.value
    name = filename.split('\\')[-1] if filename else 'test.txt'
    await files.save(content.value, name)
'''
#saving funcitons (in progress)
#grab file_list from globals. (get the value (check that it is oonly of length 1. ))

@when("change", "#fileRead")
async def on_upload_file(event): 
    print("JAV")
    path = my_globals.fileName.value
    print(path)
    code_retrieved = await my_globals.saving_js_module.read('fileRead') #saving_js_module is really an instance of the class 'Files' in save_jav.js
    #content.innerText = code_retrieved
    #making editor show the code just fetched
    my_globals.my_green_editor.code = code_retrieved
    print('file beginning: ',code_retrieved[:10])
    
#my_globals.upload_file_btn.onclick = on_upload_file





# expose stop_running_code function to JavaScript
window.stop_running_code = helper_mod.stop_running_code

#get_repl = document.getElementById('get_repl')

my_globals.save_btn.onclick = helper_mod.on_save
my_globals.my_green_editor.addEventListener('mpy-run', helper_mod.handle_board)
my_globals.my_green_editor.handleEvent = helper_mod.handle_board

#for list of files

my_globals.file_list.onchange = helper_mod.on_select

my_globals.connect.onclick = on_connect
my_globals.download.onclick = on_load
my_globals.sensors.onclick = sensor_mod.on_sensor_info

#start disabled until connected
helper_mod.disable_buttons([my_globals.sensors, my_globals.download, my_globals.custom_run_button, my_globals.save_btn, my_globals.upload_file_btn])
#get_repl.onclick = display_repl

my_globals.terminal.disconnect_callback = second_half_disconnect
my_globals.terminal.newData_callback = print_jav.on_data_jav #defined for when physical or coded disconnection happens

my_gif.set_dictionary()



@when("click", "#internet_button")
async def way_1_print(event):
    print("INTERNET BUTTON")

 