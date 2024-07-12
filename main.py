# https://xtermjs.org/docs/api/terminal/classes/terminal/#options
#https://pyscript.com/@agiammarchi/spike-ide-copy/latest
#BLE_CEEO_url = 'https://raw.githubusercontent.com/chrisbuerginrogers/SPIKE_Prime/main/BLE/BLE_CEEO.py'
#WEEE

from pyscript import document, window
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

my_globals.init()

ARDUINO_NANO = 128
SPIKE = 256

    


def on_custom_disconnect(event=None):
    print_custom_terminal("Disconnected from your Spike Prime.")
    #display_gif("nobgimages/aipuppy2_360-removebg-preview.png")
    #global sensor

    #if sensor data is displayed, hide it, bring back the terminal, and reset
    if (my_globals.sensors.onclick == sensor_mod.close_sensor):
        print('clearing sensor data')
        await sensor_mod.close_sensor()

    second_half_disconnect()
    my_globals.physical_disconnect = False

    #clear sensor display
    document.getElementById('sensor-info').innerHTML = ""   

def second_half_disconnect(event=None):
    if(my_globals.sensors.onclick == sensor_mod.close_sensor and my_globals.physical_disconnect): 
        print_custom_terminal("Physically Disconnected while reading sensors - RELOAD PAGE")
        document.getElementById(f"lesson{my_globals.lesson_num}-link").click() #reloadp
    if my_globals.terminal.connected:
        print('connected')
    print_custom_terminal("Disconnected from your Spike Prime.")
    #my_globals.terminal.send('\x03') #to stop any program that is running
    print('after disconnect, passed x03')
    my_globals.terminal.board.disconnect()
    my_globals.sensors.disabled = True
    my_globals.download.disabled = True

    #allow user to connect back
    my_globals.connect.disabled = False
    my_globals.connect.onclick = on_connect
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

proper_name_of_file = {
    1: "/flash/Main_Lesson1.py",
    2: "/flash/Main_Lesson2.py",
    3: "/flash/Main_Lesson3.py",
    4: "/flash/Main_Lesson4.py",
    5: "/flash/Main_Lesson5.py",
    6: "/flash/Main_Lesson6.py"
}

file_list_element = document.getElementById('files')
options = file_list_element.options

async def on_connect(event):

    global file_list_element
    global options

    if my_globals.terminal.connected:
        my_globals.connect.innerText = 'Connect back'
        #connect.classList.remove('connected')
        await my_globals.terminal.board.disconnect()
    else:
       # if (lesson_num == 4):
       #    print("YUIAIOFJFDAAAAAAA")
        my_globals.sensors.disabled = True
        my_globals.download.disabled = True
        my_globals.connect.disabled = True
        my_globals.custom_run_button.disabled = True
        my_globals.connect.innerHTML = 'Connecting...'
        await my_globals.terminal.board.connect('repl')

        if my_globals.terminal.connected:
            #enable buttons
            document.getElementById('repl').style.display = 'none' #to prevent user from inputting during paste

            #Initializing sensor code (below)
            print("Before paste")
            #await terminal.paste(sensor_code, 'hidden')
            await my_globals.terminal.paste(sensor_mod.sensor_code, 'hidden')
            print("After paste")

            #initializng file list code, hide scroll bar
            document.getElementById('terminalFrameId').style.overflow = 'hidden'
            print("Before-THEE-LIST")
            await file_os.getList(my_globals.terminal, my_globals.file_list)
            #print(file_list)
            print("THEE-LIST")
            document.getElementById('terminalFrameId').style.overflow = 'scroll'

            if my_globals.lesson_num == 3: #display this at the very beginning
                display_gif("gifs/Lesson3/Multiple_sensors.gif")
            
            
            # make only the file that matches the page appear
            for i in range(options.length - 1, -1, -1):
                option = options.item(i)
                option_text = option.text
                if option_text != proper_name_of_file[my_globals.lesson_num]:
                    file_list_element.removeChild(option)
            
            if file_list_element.options.length == 0:
                new_option = document.createElement('option')
                new_option.text = "You do not have the right file. Please click the download button"
                # new_option.value = "new_file.py" # how you could add a new file
                file_list_element.appendChild(new_option)
                print('end of if statement')
            else:
                await on_select(None) #**needed for uploading 1st file
                

            #enable disconnect
            my_globals.connect.classList.add('connected')
            my_globals.connect.innerHTML = 'Disconnect'
            my_globals.connect.onclick = on_custom_disconnect
            print_custom_terminal("Connected to your Spike Prime. Welcome!")
            # display_gif("nobgimages/aipuppy5_480-removebg-preview.png")

            #initializing user interface
            my_globals.connect.disabled = False
            my_globals.custom_run_button.disabled = False
            my_globals.sensors.disabled = False 
            my_globals.download.disabled = False
            #show gifs and files
            document.getElementById('files').style.visibility = 'visible'
            document.getElementById('repl').style.display = 'block' #allow user to input only after paste is done
            #terminal.terminal.attachCustomKeyEventHandler(on_user_input)

        else:
            #allow user to connect back if they clicked 'cancel' when choosing the port to connect to
            second_half_disconnect()
    

#def display_repl(event):
#    document.getElementById('repl').style.display = 'block'
    #terminal.setOption('disableStdin', True)  # Disable user input 

    

#NEXT STEP: download more tha n 1 file (length of path). make for loop (chat)
async def on_load(event):
    if my_globals.terminal.connected:
        my_globals.download.disabled = True #dont enable user to click downaload again if already in downlaod
        my_globals.sensors.disabled = True #dont let user run sensors
        my_globals.connect.disabled = True #dont allow user to disconnect
        print_custom_terminal("Downloading code, please wait...")
        document.getElementById('download-code').innerHTML = 'Downloading Code'
        my_globals.sensors.classList.remove('active')
        my_globals.custom_run_button.classList.remove('active')
        # document.getElementById('repl').style.display = 'none' #hide repl to prevent from seeing output in repl

        git_paths = my_globals.path.value.split() #gets arrays of urls
        #download_statuses = [] #will store statuses for each file 
        
        #github = path.value #gets url (useless now)
        
        for current_path in git_paths:
            name = current_path.split('/')[-1] 
            print('path, name: ',current_path,name)
            reply = await restapi.get(current_path)
            status = await my_globals.terminal.download(name,reply)
            my_globals.sensors.disabled = False #re-enable it
            my_globals.download.disabled = False
            my_globals.connect.disabled = False
            if not status: 
                window.alert(f"Failed to load {name}. Click Ok to continue downloading other files")  

        my_globals.download.disabled = False #dont enable user to click downaload again if already in downlaod
        my_globals.sensors.disabled = False #dont let user run sensors
        my_globals.connect.disabled = False 
        my_globals.sensors.classList.add('active') #controls display
        my_globals.custom_run_button.classList.add('active') #controls display
        print_custom_terminal("Download complete!")
        document.getElementById('download-code').innerHTML = 'Download Training Code'
        
        #document.getElementById('repl').style.display = 'block'
        
        #copy
        #initializng file list code, hide scroll bar
        document.getElementById('terminalFrameId').style.overflow = 'hidden'
        await file_os.getList(my_globals.terminal, my_globals.file_list)
        document.getElementById('terminalFrameId').style.overflow = 'scroll'
        #await on_select(None)
        #show scroll bar
        #copy
    else:
        window.alert('connect to a processor first')

isRunning = False
#evaluates code when the green button is pressed
def handle_board(event):
    global isRunning
    global found_key
    found_key = False
    # run program for custom buttton to run pyscript editor
    if event.type == 'mpy-run':
        my_globals.sensors.disabled = True 
        my_globals.download.disabled = True
        print_custom_terminal("Running code...")
        # document.getElementById('portInfo').style.display = 'none'
        document.getElementById('gif').style.visibility = 'visible'
        document.getElementById('gif').style.display = 'block'
        code = event.detail.code
    else:
        code = event.code

    if my_globals.terminal.connected and not isRunning:
        isRunning = True
        try:
            await my_globals.terminal.eval('\x05' + code + "#**END-CODE**#" + '\x04') #very important: somehow pastes the whole code before running
            #await terminal.eval('\x05'+"#**END-CODE**#"+'\x04')
            my_globals.terminal.focus()
            print("Hello_ish")
        except:
            print('EXCEPT ERROR')
            pass
        finally:
            if isRunning:  #only print completion if not stopped manually
                print_custom_terminal("...")
            isRunning = False
        return False  #return False to avoid executing on browser
    else:
        return True

def stop_running_code():
    my_globals.sensors.disabled = False 
    my_globals.download.disabled = False
    global isRunning
    if my_globals.terminal.connected:
        await my_globals.terminal.send('\x03')
        print('stopped code')
    
    isRunning = False
    document.getElementById('gif').style.display = 'none'
    # document.getElementById('portInfo').style.display = 'block'
    print_custom_terminal("Code execution ended. Please press the button to run the code again.")

# expose stop_running_code function to JavaScript
window.stop_running_code = stop_running_code


async def on_select(event):
    global file_list_element
    my_globals.my_green_editor.code = await file_os.read_code(my_globals.terminal, file_list_element)

#display custom code in editor, give delay on autoscroll function to ensure all new content has loaded
def print_custom_terminal(string):
    document.getElementById('customTerminalMessage').innerHTML += string + " <br>"
    window.setTimeout(window.scrollTerminalToBottom, 0)
    
#display custom gifs in side panel
def display_gif(imageName):
    window.fadeImage(imageName)


#get_repl = document.getElementById('get_repl')


my_globals.my_green_editor.addEventListener('mpy-run', handle_board)
my_globals.my_green_editor.handleEvent = handle_board

#for list of files

my_globals.file_list.onchange = on_select

my_globals.connect.onclick = on_connect
my_globals.download.onclick = on_load
my_globals.sensors.onclick = sensor_mod.on_sensor_info

#start disabled until connected
my_globals.sensors.disabled = True 
my_globals.download.disabled = True
#get_repl.onclick = display_repl

my_globals.terminal.disconnect_callback = second_half_disconnect
my_globals.terminal.newData_callback = print_jav.on_data_jav #defined for when physical or coded disconnection happens

my_gif.set_dictionary()

#while (True):
#    if (not my_globals.terminal.connected):
#        my_globals.terminal.send('\x03')

