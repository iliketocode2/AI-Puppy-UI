from pyscript.js_modules.micro_repl import default as Board


sensor_code = '''
import hub, utime, color
import force_sensor as fs
import distance_sensor as ds
import color_sensor as cs
from hub import port, button, light_matrix, sound, light

dist = port.E
col = port.B
forc = port.C

while True:
    print("Distance: ", ds.distance(dist))
    
    print("Force: ", fs.force(forc))
    
    print("Red: ", cs.rgbi(col)[0])
    print("Green: ", cs.rgbi(col)[1])
    print("Blue: ", cs.rgbi(col)[2])

'''

good_code = sensor_code.replace('\n', '\r\n')

def on_data(chunk):
    print('on data', chunk)

#async def main():
#    await board.eval(good_code, hidden=False)

board = Board({
    "baudRate": 115200,
    "dataType": "string",
    #"onconnect": on_connect,
   # "ondisconnect": on_disconnect,
    "ondata": on_data,
    #"onerror": on_error,
    "fontSize": '24',
    "fontFamily": 'Courier New',
    "theme": {
        "background": "white",
        "foreground": "black",
    }
})


'''
#code for geting rgbi in sensor_code

color_info[0] = my_color
    
    rgbi = color_sensor.rgbi(port_num)
    
    color_info[1] = rgbi[0] #red
    color_info[2] = rgbi[1] #green
    color_info[3] = rgbi[2] #blue
    
    color_info_tuple = tuple(color_info)
        
    #print("My-COlor: ", color_info_tuple)
    
    return color_info_tuple


'''

'''
back in python:

 #if it is the color sensor process number as a tuple
                #where tuple is (color from table 1, r, g , b)
                if (t[2] == 61):
                    #print("SIUU")
                    #pass
                    color_info = number
                    color_detected = ["Red", "Green", "Blue", "Magenta", "Yellow", "Orange", "Azure", "Black", "White", "Unknown"]
                    color_name = color_detected[color_info[0] - 1] if 0 < color_info[0] <= len(color_detected) else "Unknown"
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
                                    {color_detected[color_info[0] - 1]}
                                </span>
                            </div>
                        </div>
                    </div>
                    """

'''

'''
JS code: 
/* 
    let is_running = false;
    // connect 'run python code' js button to mpy-editor
    runButton.addEventListener('click', function() {
        if (!is_running) {
            // run the code
            const editor = document.getElementById(this.getAttribute('data-editor-id'));
            if (editor) {
                const event = new CustomEvent('mpy-run', {
                    bubbles: true,
                    detail: { code: editor.code }
                });
                editor.dispatchEvent(event);
                this.innerHTML = 'Stop Running Code';
                is_running = true;
            }
        } else {
            // stop the code
            window.stop_running_code(); //calling python function
            this.innerHTML = 'Run Python Code';
            is_running = false;
        }
    });
    */


'''

#called when displaying all sensors except the color sensor
def display_sensors(source, alt, number, port_name, sensor_info_html):
    sensor_info_html += f"""
    <div class="sensor-info">
        <div class="sensor-info-item">
            <div class="sensor-stack-left">
                <span class="port-name">{port_name}</span>
            </div>
            <div class="sensor-stack-right">
                <span><img src="{source}" alt="{alt}"></span>
                <span class="sensor-value">{number}</span>
            </div>
        </div>
    </div>
    """
    return sensor_info_html

source = "images/spike medium_motor_display.png"
                    alt = "Motor"
                    port_name = port_names[t[1]]
                    sensor_info_html = display_sensors(source, alt, number,
                                                    port_name, sensor_info_html) 