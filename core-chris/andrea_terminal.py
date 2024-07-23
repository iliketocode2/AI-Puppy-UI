# https://xtermjs.org/docs/api/terminal/classes/terminal/#options
# https://pyscript.com/@agiammarchi/spike-ide-copy/latest
# https://cdn.jsdelivr.net/npm/micro-repl@0.5.1/serial.js

from pyscript import window
from pyscript.js_modules.micro_repl import default as Board
import json

try:
    # if not reachable / available it fails
    window.navigator.serial.requestPort
except:
    window.alert('you have to use Chrome to talk over serial')

class Terminal():
    def __init__(self, baudrate = 115200):
        self.connected = False
        self.terminal = None
        self.disconnect_callback = None
        self.newData_callback = None
        self.buffer = ''
        self.board = Board({
            "baudRate": baudrate,
            "dataType": "string",
            "onconnect": self.on_connect,
            "ondisconnect": self.on_disconnect,
            "ondata": self.on_data,
            "onresult": json.loads,
            "onerror": window.alert,
            "fontSize": '24',
            "fontFamily": 'Courier New',
            "theme": {
                "background": "white",
                "foreground": "black",
            },
        })

    def on_data(self, chunk):
        self.buffer += chunk
        if self.newData_callback: self.newData_callback(chunk)
    
    def on_connect(self):
        self.connected = True
        self.terminal = self.board.terminal

    def on_disconnect(self):
        self.connected = False
        #self.terminal.reset()
        self.terminal = None
        if self.disconnect_callback: self.disconnect_callback()

    async def on_reset(self, error):
        self.reset.disabled = True
        await self.board.reset()
        self.reset.disabled = False

    async def eval(self,payload, hidden=False):
        return await self.board.eval(payload, hidden=hidden)

    async def paste(self,payload, hidden=False):
        return await self.board.paste(payload, hidden=hidden)

    def focus(self):
        self.board.terminal.focus()

