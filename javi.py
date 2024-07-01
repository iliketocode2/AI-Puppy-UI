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

