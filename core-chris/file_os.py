from pyscript import document
import json

code = '''
import os, ubinascii, sys

def listdir(directory):
    result = set()
    def _listdir(dir_or_file):
        try:
            children = os.listdir(dir_or_file)
        except OSError:
            os.stat(dir_or_file)
            result.add(dir_or_file)
        else:
            if children:
                for child in children:
                    if dir_or_file == '/':
                        next = dir_or_file + child
                    else:
                        next = dir_or_file + '/' + child
                    _listdir(next)
            else:
                result.add(dir_or_file)
    _listdir(directory)
    return sorted(result)
'''  
'''    def send(self, payload, eol = True):
        data = payload + '\r\n' if eol else payload
        self.eval(data, hidden = False)
        '''

async def getList(terminal, list):
    await terminal.paste(code, hidden = True)
    # grab the list of files
    array = await terminal.eval("""
        result = listdir("/")
        result
    """, True)
    print(array)
    list.options.length = 0
    for name in array:
        if not '.py' in name or name.find('/.') == 0:
            continue
        print(name)
        option = document.createElement('option')
        option.text = name
        option.value = name
        list.add(option)

async def read_code(terminal, list):
    print(list.value)
    result = await terminal.eval(f"""
        f = open({json.dumps(list.value)}, "rb")
        result = f.read().decode('utf-8')
        f.close()
        result
    """,True)
    return result

