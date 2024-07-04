# https://xtermjs.org/docs/api/terminal/classes/terminal/#options
#https://pyscript.com/@agiammarchi/spike-ide-copy/latest
#BLE_CEEO_url = 'https://raw.githubusercontent.com/chrisbuerginrogers/SPIKE_Prime/main/BLE/BLE_CEEO.py'
#WEEE

from pyscript import document, window
import ampy
import restapi
import asyncio
import time
import file_os

ARDUINO_NANO = 128
SPIKE = 256

stop_loop = False #indicates when to stop loop (u want it to stop when user has access to repl)
sensor = True #for switching between if and else statements (going from user repl to sensors)
#defi
#making dictionary here because I think that it is less efficient if I were
# to send all these strings from chip to computer (thus chip only sends digits)
device_names = {
    48: "medium_motor",
    49: "big_motor",
    61: "color_sensor",
    62: "distance_sensor",
    63: "force_sensor",
    64: "light_matrix",
    65: "small_motor"
    
}

#making 
port_names = {
    0: 'A',
    1: 'B',
    2: 'C',
    3: 'D',
    4: 'E',
    5: 'F'
}
sensor_code = """

import device
import motor
import color_sensor
import color
import distance_sensor
import force_sensor

#test this
def big_motor_print(port_num):
    print("big_motor", port_num)
    abs_pos = motor.absolute_position(port_num)
    if (abs_pos < 0):
        abs_pos = abs_pos + 360
    return abs_pos

#color.RED = 1
#9 colors:
''' 
Table 1:

Red - 1
Green - 2
Blue - 3
Magenta - 4
Yellow 5
Orange - 6
Azure - 7 
Black - 8
White - 9

'''
#returns tuple with (color from table 1, r, g , b)
def color_sensor_print(port_num):
    print("color sensor", port_num)
    color_info = [-1,-1,-1,-1] #tuple with, color, r,g,b values 
    #variable I will use to identify color based on Table 1
    my_color = -1 #if not color is detected
    sensor_color = color_sensor.color(port_num) #color that sensor detects
    if sensor_color is color.RED:
        my_color = 1
    elif sensor_color is color.GREEN:
        my_color = 2
    elif sensor_color is color.BLUE:
        my_color = 3
    elif sensor_color is color.MAGENTA:
        my_color = 4
    elif sensor_color is color.YELLOW:
        my_color = 5
    elif sensor_color is color.ORANGE:
        my_color = 6
    elif sensor_color is color.AZURE:
        my_color = 7
    elif sensor_color is color.BLACK:
        my_color = 8
    elif sensor_color is color.WHITE:
        my_color = 9
    
    color_info[0] = my_color
    
    rgbi = color_sensor.rgbi(port_num)
    
    color_info[1] = rgbi[0] #red
    color_info[2] = rgbi[1] #green
    color_info[3] = rgbi[2] #blue
    
    color_info_tuple = tuple(color_info)
        
    #print("My-COlor: ", color_info_tuple)
    
    return color_info_tuple
    
def distance_sensor_print(port_num):
    print("distance sensor", port_num)
    return distance_sensor.distance(port_num)
    
def force_sensor_print(port_num):
    print("force sensor", port_num)
    return force_sensor.force(port_num)
    
    
def light_matrix_print(port_num):
    print("light matrix", port_num)
    return 1 #change this

#test this
def small_motor_print(port_num):
    print("small motor", port_num)
    abs_pos = motor.absolute_position(port_num)
    if (abs_pos < 0):
        abs_pos = abs_pos + 360
    return abs_pos

#absolute position goes like 0...179, -180, -179 = vals
#want 0...179, 180, 181,... 360 (then go back to 0)
#so return 360 + val
def medium_motor_print(port_num):
    print("medium motor", port_num)
    abs_pos = motor.absolute_position(port_num)
    if (abs_pos < 0):
        abs_pos = abs_pos + 360
    return abs_pos

function_dict = {
    48: medium_motor_print,
    49: big_motor_print,
    61: color_sensor_print,
    62: distance_sensor_print,
    63: force_sensor_print,
    64: light_matrix_print,
    65: small_motor_print
}


"""
#code for getting port information in tuple form
#tuple = (1 if connected & recognized, port number, sensor_id)
execute_code = """
    port_info = [()] * 6
    for i in range(6):
        #for each port get the device Id
        current_port = i
        try:
            #below is line that will give you error (potentially)
            port_id = device.id(current_port) #this should be either 49, or 61 or 62 or... 65 #handle exception when not found
            # Call the corresponding function if the device ID is found
            if port_id in function_dict:
                #function_dict[port_id](i)
                port_info[i] = (1, i, port_id)
            else:
                #print(f"No function defined for device ID {port_id}")
                port_info[i] = (0,0,0)
        except OSError as e: #nothing connected to it
            # Means port does not have any sensor connected to it
            port_info[i] = (0,0,0)
            #print("YAA")
            #print(f"Port {current_port} error: {e}")
"""

#execute code for thisL 
# [(1, 0, 61), (0, 0, 0), (1, 2, 63), (1, 3, 48), (1, 4, 62), (1, 5, 64)]
#



# Function to handle user input event


def on_data_jav(chunk):
    #print("IN data_jav")
    #print("Start-chunk")
    print(chunk)
    #print("end-chunk")


    
def on_disconnect():
    connect.innerText = 'Disconnected'
    connect.style.backgroundColor = 'red'
    document.getElementById('sensor_readings').style.backgroundColor = '#998887'
    document.getElementById('download-code').style.backgroundColor = '#998887'
    document.getElementById('custom-run-button').style.backgroundColor = '#998887'
    document.getElementById('download-code').style.cursor = 'auto'
    document.getElementById('sensor_readings').style.cursor = 'auto'
    document.getElementById('custom-run-button').style.cursor = 'auto'
    sensors.disabled = True
    download.disabled = True
    

async def on_connect(event):
    if terminal.connected:
        connect.innerText = 'Disconnected'
        connect.style.backgroundColor = 'yellow'
        await terminal.board.disconnect()
    else:
        await terminal.board.connect('repl')
        #enable buttons
        document.getElementById('repl').style.display = 'none' #to prevent user from inputting during paste
        if terminal.connected:
            connect.innerText = 'Connected!'
            connect.style.backgroundColor = 'green'
            document.getElementById('download-code').style.cursor = 'pointer'
            document.getElementById('sensor_readings').style.cursor = 'pointer'
            document.getElementById('custom-run-button').style.cursor = 'pointer'
                       
        #Initializing sensor code (below)
        print("Before paste")
        #await terminal.paste(sensor_code, 'hidden')
        await terminal.paste(sensor_code, 'hidden')
        print("After paste")

        document.getElementById('sensor_readings').style.backgroundColor = '#111827'
        document.getElementById('download-code').style.backgroundColor = '#111827'
        document.getElementById('files').style.visibility = 'visible'
        
        #initializng file list code, hide scroll bar
        document.getElementById('terminalFrameId').style.overflow = 'hidden'
        await file_os.getList(terminal, file_list)
        document.getElementById('terminalFrameId').style.overflow = 'scroll'
        document.getElementById('custom-run-button').style.backgroundColor = '#111827'
        await on_select(None)
        #show scroll bar

        #initializing user interface
        sensors.disabled = False 
        download.disabled = False
        document.getElementById('repl').style.display = 'block' #allow user to input only after paste is done
        #terminal.terminal.attachCustomKeyEventHandler(on_user_input)
    

def display_repl(event):
    document.getElementById('repl').style.display = 'block'
    #terminal.setOption('disableStdin', True)  # Disable user input


#def on_user_input(event):
#    print("asdlkjfd;slkfj;l kjlk;sdjafl;kdsajf;l ksdjl;ksazjf")    


#sensor_info and get terminal in same button
def on_sensor_info(event):  
    global sensor
    global stop_loop
    global device_names
    #print("STOP-LOOP", stop_loop)

    stop_loop = False
    if sensor: #means you want to display sensors
        download.disabled = True #disable it 
        connect.disabled = True
        sensor = False #so that on next click it displays terminal
        #turn off repl to prevent user from interfering with my repl sensor code
        document.getElementById('download-code').style.backgroundColor = '#998887'
        document.getElementById('repl').style.display = 'none'
        sensors.innerText = 'Get Terminal'
    #execute code for thisL 
    # [(1, 0, 61), (0, 0, 0), (1, 2, 63), (1, 3, 48), (1, 4, 62), (1, 5, 64)]
        #stop_loop = False
        # Add event listener for user input
        #event handler when user types in keyboard
        #counter = 0
        print("STOP-LOOP", stop_loop)
        while not stop_loop:
              #two lines below should go in while loop (checks every time the port info)
            await terminal.eval(execute_code, 'hidden')
            port_info_array = await terminal.eval("""port_info
                                """, 'hidden')
            #clearing it every time (very important)

            # sensor_info_html = ""  # Initialize HTML content for sensor info
            sensor_info_html = "<div class='sensor-info-container'>" # Initialize HTML content for sensor info

            #iterating over tuples/ports
            for t in port_info_array: #if sensors are switched somewhere her, then error cause u don't udpate port_info_array
                #solution would be to break out of loop if a bool is triggered(port disconnected)
                
                if t[0] == 1: #if something is connected to port
                    #call corresponding funcitons with corresponding ports
                    #t[2] is function/device id & t[1] is port #
                    if stop_loop:
                        break;
                    #number is tuple with some sort of sensor value
                    #if anything but color sensor (just display 1 value)
                        #then 
                    number = await terminal.eval(f"""
                        number = function_dict[{t[2]}]({t[1]})
                        number
                        
                    """, 'hidden')
                    #if it is the color sensor process number as a tuple
                    #where tuple is (color from table 1, r, g , b)
                    if (t[2] == 61):
                        #print("SIUU")
                        #pass
                        color_info = number
                        color_detected = ["Red", "Green", "Blue", "Magenta", "Yellow", "Orange", "Azure", "Black", "White", "Unknown"]
                        color_name = color_detected[color_info[0] - 1] if 0 < color_info[0] <= len(color_detected) else "Unknown"
                        sensor_info_html += f"""
                        <div class="sensor-info">
                            <div class="sensor-info-item">
                                <div class="sensor-stack-left">
                                    <span class="port-name">{port_names[t[1]]}</span>
                                </div>
                                <div class="sensor-stack-right">
                                    <span><img src="images/spike color_sensor_display.png" alt="color sensor"></span>
                                    <span class="sensor-value">
                                        <div class="colorCircle" style="background-color: {color_name.lower()};"></div>
                                        {color_detected[color_info[0] - 1]}
                                    </span>
                                </div>
                            </div>
                        </div>
                        """
                        # document.querySelector('.colorCircle').style.backgroundColor = 'green'
                        # <div class="sensor-info-item">
                        #     <span>Number: {color_info} (Color: {color_name})</span>
                        #     <span>Device: {device_names[t[2]]}</span>
                        #     <span>Port: {port_names[t[1]]}</span>
                        # </div>
                        # """

                    elif (t[2] == 48 or t[2] == 49): #medium motor
                        sensor_info_html += f"""
                        <div class="sensor-info">
                            <div class="sensor-info-item">
                                <div class="sensor-stack-left">
                                    <span class="port-name">{port_names[t[1]]}</span>
                                </div>
                                <div class="sensor-stack-right">
                                    <span><img src="images/spike medium_motor_display.png" alt="Motor"></span>
                                    <span class="sensor-value">{number}&deg;</span>
                                </div>
                            </div>
                        </div>
                        """
                    elif (t[2] == 62): #distance sensor
                        sensor_info_html += f"""
                        <div class="sensor-info">
                            <div class="sensor-info-item">
                                <div class="sensor-stack-left">
                                    <span class="port-name">{port_names[t[1]]}</span>
                                </div>
                                <div class="sensor-stack-right">
                                    <span><img src="images/spike distance_sensor_display.png" alt="distance sensor"></span>
                                    <span class="sensor-value">{number} mm</span>
                                </div>
                            </div>
                        </div>
                        """
                    elif (t[2] == 63): #force sensor
                        sensor_info_html += f"""
                        <div class="sensor-info">
                            <div class="sensor-info-item">
                                <div class="sensor-stack-left">
                                    <span class="port-name">{port_names[t[1]]}</span>
                                </div>
                                <div class="sensor-stack-right">
                                    <span><img src="images/spike push_sensor_display.png" alt="force sensor"></span>
                                    <span class="sensor-value">{number} N</span>
                                </div>
                            </div>
                        </div>
                        """
                    else:
                        sensor_info_html += f"""
                            <div class="sensor-info-item">
                                <span>{number} </span>
                                <span>Device: {device_names[t[2]]}</span>
                                <span>Port: {port_names[t[1]]}</span>
                            </div>
                        """ 



            sensor_info_html += "</div>"  # Close the container
            # Update the sensor info container with new HTML content
            document.getElementById('sensor-info').innerHTML = sensor_info_html
            # document.querySelector('.colorCircle').style.backgroundColor = 'green'

            #await asyncio.sleep(0.3)
                        #print("NAHH")
                        #t is just 1 number (display that number)
                        
                    #now display number, device (t[2]), and port t[1]
                    #instead of returning #, return array of tuple
                    
            #print("Number:", number)
            #time.sleep(1)
            #counter = counter + 1
        #print("Back_HERE: ", port_info_array)
    else: #go back to terminal
        #enable download button
        download.disabled = False
        connect.disabled = False
        stop_loop = True
        #asyncio.
        #time.sleep_ms(1000) #to allow while loop to finish current iteration
        #await asyncio.sleep(0.1)
        sensor = True #so that next time it hides repls
        sensors.innerText = 'Sensor Readings'
        document.getElementById('repl').style.display = 'block'
        document.getElementById('download-code').style.backgroundColor = '#111827'

        #this code is kind of important.
        #if the user spams the button, it prevents erros by disabling button for a short time
        #so that if multiple clicks are made quickly, the same while loop below the if
        #statement is not called twice
        #this would result on calling eval again when the first eval call has not yet 
        #finished. (resulting in error: can't eval 2 things at once)
        sensor_button = document.getElementById('sensor_readings')
        sensor_button.disabled = True
        download.disabled = True #prevent from downloading straight away also 
        await asyncio.sleep(0.2)  # Wait for 2 seconds
        sensor_button.disabled = False  # Re-enable the button
        download.disabled = False
       # document.getElementById('sensor_readings').style.display = 'block'
    

#NEXT STEP: download more tha n 1 file (length of path). make for loop (chat)
async def on_load(event):
    if terminal.connected:
        download.disabled = True #dont enable user to click downaload again if already in downlaod
        sensors.disabled = True #dont let user run sensors
        connect.disabled = True #dont allow user to disconnect
        document.getElementById('repl').style.display = 'none' #hide repl to prevent from seeing output in repl

        git_paths = path.value.split() #gets arrays of urls
        #download_statuses = [] #will store statuses for each file 
        
        #github = path.value #gets url (useless now)
        
        for current_path in git_paths:
            name = current_path.split('/')[-1] 
            print('path, name: ',current_path,name)
            reply = await restapi.get(current_path)
            status = await terminal.download(name,reply)
            sensors.disabled = False #re-enable it
            download.disabled = False
            connect.disabled = False
            if not status: 
                window.alert(f"Failed to load {name}. Click Ok to continue downloading other files")  
        document.getElementById('repl').style.display = 'block'
    else:
        window.alert('connect to a processor first')

#evaluates code when the green button is pressed
def handle_board(event):

    # run program for custom buttton to run pyscript editor
    if event.type == 'mpy-run':
        code = event.detail.code
    # default program without custom button
    else:
        code = event.code

    if terminal.connected:
        await terminal.eval(code)
        terminal.focus()
        return False  # return False to avoid executing on browser
    else:
        return True

async def on_select(event):
    my_green_editor.code = await file_os.read_code(terminal, file_list)

connect = document.getElementById('connect-spike')
download = document.getElementById('download-code')
path    = document.getElementById('gitpath')
sensors = document.getElementById('sensor_readings')
#get_repl = document.getElementById('get_repl')

my_green_editor = document.getElementById('MPcode') #for editor
my_green_editor.addEventListener('mpy-run', handle_board)
my_green_editor.handleEvent = handle_board

#for list of files
file_list = document.getElementById('files')
file_list.onchange = on_select

connect.onclick = on_connect
download.onclick = on_load
sensors.onclick = on_sensor_info
#start disabled until connected
sensors.disabled = True 
download.disabled = True
#get_repl.onclick = display_repl

terminal = ampy.Ampy(SPIKE)
terminal.disconnect_callback = on_disconnect #defined for when physical or coded disconnection happens
#terminal.newData_callback = on_data_jav
