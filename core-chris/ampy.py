from pyscript import window
import asyncio
import andrea_terminal 

code ='''
import os
def cksm(file):
    s = os.stat(file)[6]
    f = open(file,'rb')
    msg = f.read()
    f.close()
    v = 21
    for c in msg.decode():
        v ^= ord(c)
    return s,v
'''

class Ampy(andrea_terminal.Terminal):
    def __init__(self, buffer_size = 256, status = None, baudrate = 115200):
        super().__init__(baudrate)
        self.buffer_size = buffer_size
        self.status = status
        self.update(0)
        self.path = None

    def update(self, value):
        if self.status: self.status.value = value

    async def send(self, payload, eol = True ):
        data = payload + '\r\n' if eol else payload
        await self.eval(data)
        
    async def read_until(self, min_len, ending, timeout = 1):
        data = self.buffer
        timeout_count = 0
        while True:
            if data.find(ending)>=0:  # done
                break
            elif len(data)<len(self.buffer): # new data
                data = self.buffer
                timeout_count = 0
            else:
                timeout_count += 1
                if timeout is not None and timeout_count >= 10 * timeout: #used to be 100 *
                    print('data: ',data.encode(), '  ending: ',ending.encode())
                    window.alert('Timeout in read_until')
                    break
                await asyncio.sleep(0.01)     
        return data

    async def send_get(self, payload, expected, tries = 1, timeout = 10):
        for retry in range(0, tries): 
            self.buffer = '' 
            if payload: await self.send(payload, eol = False)             
            data = await self.read_until(1, expected, timeout)
            if data.find(expected)>=0:
                return True
        window.alert('incorrect response', data)
                    
    async def go_raw(self):
        await self.send_get('\r\x01', 'raw REPL; CTRL-B to exit\r\n>', 5)
        #await self.send_get('\x04', 'soft reboot\r\n', 1)
        await self.send_get('\x04', '>', 1)
        print('rebooted')
        #await self.send_get('\x03', 'raw REPL; CTRL-B to exit\r\n', 1, 10)

    async def close_raw(self):
        await self.send('\r\x02', eol = False) # ctrl-B: enter friendly REPL
        
    async def send_code(self, filename, data):
        await self.send("f = open('%s', 'wb')"%(filename))
        size = len(data)
        for i in range(0, size, self.buffer_size):
            chunk_size = min(self.buffer_size, size - i)
            chunk = repr(data[i : i + chunk_size])
            await self.send("f.write(%s)"%(chunk)) 
            await asyncio.sleep(0.01)
            await self.send_get('\x04','OK',1 , 10)
            self.update(10 + 90*(i+1)/size)
        await self.send("f.close()")
        await self.send_get('\x04','OK',1 , 10)
        
    def checksum(self, msg):
        v = 21
        for c in msg.decode():
            v ^= ord(c)
        return v

    async def download(self, filename, data, check = True):
        file_size = len(data.encode()) 
        cs = self.checksum(data.encode())
        
        self.send('\r\x03',eol = False)
        await asyncio.sleep(0.1)
        await self.send_get(f'# switching to raw mode and downloading {filename}\r\n','>>>',1)
        self.send('\x03', eol = False)
        await asyncio.sleep(0.1)
        await self.go_raw()
        self.update(10)
        await self.send_code(filename, data) 
        await self.send_get('\x04','OK',1 , 10)
        await self.send(code)
        await self.send_get('\x04','OK',1 , 10)
        await self.close_raw()
        self.update(100)

        if check:
            await self.send_get('\r\n# checking filesize and checksum\r\n', '>>>', 1, 1)
            await self.send_get(f"({file_size},{cs}) == cksm('{filename}')\r\n", '>>>', 5, 100)
            await asyncio.sleep(0.5)
            try:
                success = self.buffer.split('\n')[1]
            except:
                return False
            return success
        return True

  