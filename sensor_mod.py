import my_globals
import asyncio
from pyscript import document
import time
import helper_mod

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
    #print("color sensor", port_num)
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

    return my_color
    
def distance_sensor_print(port_num):
    #print("distance sensor", port_num)
    return distance_sensor.distance(port_num)
    
def force_sensor_print(port_num):
    #print("force sensor", port_num)
    return force_sensor.force(port_num)
    
    
def light_matrix_print(port_num):
    #print("light matrix", port_num)
    return 1 #change this

#test this
def small_motor_print(port_num):
    #print("small motor", port_num)
    abs_pos = motor.absolute_position(port_num)
    if (abs_pos < 0):
        abs_pos = abs_pos + 360
    return abs_pos

#absolute position goes like 0...179, -180, -179 = vals
#want 0...179, 180, 181,... 360 (then go back to 0)
#so return 360 + val
def medium_motor_print(port_num):
    #print("medium motor", port_num)
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

port_info = [()] * 6

"""
#code for getting port information in tuple form
#tuple = (1 if connected & recognized, port number, sensor_id)
execute_code = """
    for i in range(6):
        #for each port get the device Id
        current_port = i
        try:
            #below is line that will give you error (potentially)
            port_id = device.id(current_port) #this should be either 49, or 61 or 62 or... 65 #handle exception when not found
            # Call the corresponding function if the device ID is found
            if port_id in function_dict:
                number = function_dict[port_id](i)
                port_info[i] = (1, i, port_id, number)
            else:
                #print(f"No function defined for device ID {port_id}")
                port_info[i] = (0,0,0,0)
        except OSError as e: #nothing connected to it
            # Means port does not have any sensor connected to it
            port_info[i] = (0,0,0,0)
            #print("YAA")
            #print(f"Port {current_port} error: {e}")

port_info


"""




#sensor_info and get terminal in same button
async def on_sensor_info(event):
    print("ON-SENSOR")  

    #global sensor
    global device_names
    #await terminal.send('\x03')
    #print("STOP-LOOP", stop_loop)

    my_globals.stop_loop = False

    # next time sensors clicked, will hide sensor info
    my_globals.sensors.onclick = close_sensor
    helper_mod.disable_buttons([my_globals.download, my_globals.custom_run_button, my_globals.upload_file_btn, my_globals.save_btn])
    sensor = False #so that on next click it displays terminal

    #document.getElementById('repl').style.display = 'none'

    # sensors.innerText = 'Get Terminal'
    my_globals.sensors.innerText = 'Close'
    #execute code for thisL 
    # [(1, 0, 61), (0, 0, 0), (1, 2, 63), (1, 3, 48), (1, 4, 62), (1, 5, 64)]
    print("STOP-LOOP", my_globals.stop_loop)
    color_detected = ["Red", "Green", "Blue", "Magenta", "Yellow", "Orange", "Azure", "Black", "White", "Unknown"]

    while not my_globals.stop_loop:
        #two lines below should go in while loop (checks every time the port info)
        
        #if and break statements added because if disconnected physically (aka suddenly), we must not do eval. 
        #if not my_globals.terminal.connected:
        #    break
        #print("Before execute")
        port_info_array = await my_globals.terminal.eval(execute_code, 'hidden') 


        # sensor_info_html = ""  # Initialize HTML content for sensor info
        sensor_info_html = "<div class='sensor-info-container'>" # Initialize HTML content for sensor info

        #iterating over tuples/ports
        #print("before port_array")
        for t in port_info_array: #if sensors are switched somewhere her, then error cause u don't udpate port_info_array
            #solution would be to break out of loop if a bool is triggered(port disconnected)
            
            if t[0] == 1: #if something is connected to port
                #call corresponding funcitons with corresponding ports
                if my_globals.stop_loop:
                    break
                #number is tuple with some sort of sensor value
                #if anything but color sensor (just display 1 value)
                    #then 

                if not my_globals.terminal.connected:
                    break
                #t[2] is function/device id & t[1] is port #
                number = t[3]


                #if it is the color sensor process number as a tuple
                #where tuple is (color from table 1, r, g , b)
                # changed color_info[0] to number. since number is now the color number
                if (t[2] == 61):
                    #print("SIUU")
                    #pass
                    #checking to see that color returned by SPIKE is in list of known colors
                    color_name = color_detected[number - 1] if 0 < number <= len(color_detected) else "Unknown"
                    # document.querySelector('.colorCircle').style.backgroundColor = 'green'
                    # <div class="sensor-info-item">
                    #     <span>Number: {color_info} (Color: {color_name})</span>
                    #     <span>Device: {device_names[t[2]]}</span>
                    #     <span>Port: {port_names[t[1]]}</span>
                    # </div>
                    # """
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
                                    {color_detected[number - 1]}
                                </span>
                            </div>
                        </div>
                    </div>
                    """
                elif (t[2] == 48 or t[2] == 49 or t[2] == 65): #medium motor
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
                elif (t[2] == 64): #light matrix
                    sensor_info_html += f"""
                    <div class="sensor-info">
                        <div class="sensor-info-item">
                            <div class="sensor-stack-left">
                                <span class="port-name">{port_names[t[1]]}</span>
                            </div>
                            <div class="sensor-stack-right">
                                <span><img src="images/spike light_matrix_display.png" alt="light matrix"></span>
                                <span class="sensor-value">{number}</span>
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
        #print("In_LOOOP")
        document.getElementById('sensor-info').innerHTML = sensor_info_html
        print("In LOOP ")

    print("STOP-LOOP True")

async def close_sensor(event=None):
    print("In_CLose")
    helper_mod.disable_buttons([my_globals.sensors, my_globals.download])
    my_globals.stop_loop = True
    #(min of 0.32 - worst case scenario (when you trigger stop_loop boolean
    # in close sensor right before calling eval in while loop of on_sensor info ))
    await asyncio.sleep(0.5) #to allow while loop to finish its current iteration 

    # next time sensors clicked, will hide sensor info
    my_globals.sensors.onclick = on_sensor_info
    helper_mod.enable_buttons([my_globals.download, my_globals.custom_run_button, my_globals.upload_file_btn, my_globals.save_btn])
   # await asyncio.sleep(1)  # Wait for 2 seconds
    document.getElementById('sensor-info').innerHTML = " "
    print("CLEARED")
    #asyncio.
    #time.sleep_ms(1000) #to allow while loop to finish current iteration
    #await asyncio.sleep(0.1)
    my_globals.sensor = True #so that next time it hides repls
    my_globals.sensors.innerText = 'Sensors'

    #**PREVENTS SPAMMING
    #this code is kind of important.
    #if the user spams the button, it prevents erros by disabling button for a short time
    #so that if multiple clicks are made quickly, the same while loop below the if
    #statement is not called twice
    #this would result on calling eval again when the first eval call has not yet 
    #finished. (resulting in error: can't eval 2 things at once)
    #helper_mod.disable_buttons([my_globals.sensors, my_globals.download])
    #await asyncio.sleep(0.2) 
    
    #clear all sensor info -- redundant but prevents lag errors
    #document.getElementById('sensor-info').innerHTML = "" 
    print("REACHED")
    #show terminal
    document.getElementById('repl').style.display = 'block'
    helper_mod.enable_buttons([my_globals.download, my_globals.custom_run_button, my_globals.upload_file_btn, my_globals.save_btn, my_globals.sensors])
   