
import my_globals
from pyscript import document, window
import my_gif

#display custom code in editor, give delay on autoscroll function to ensure all new content has loaded
def print_custom_terminal(string):
    document.getElementById('customTerminalMessage').innerHTML += string + " <br>"
    window.setTimeout(window.scrollTerminalToBottom, 0)

##**END-CODE**# sfjflk \n
#(this is when find_print_statemetns should be called)1st print \n
def find_print_statements(buffer):
    statements = []
    start_index = 0
    while start_index < len(buffer):
        end_new_line_index = buffer.find("\n", start_index)
        if end_new_line_index == -1:
            break
        statement = buffer[start_index:end_new_line_index]
        statements.append(statement)
        start_index = end_new_line_index + 1
    return statements

def process_chunks(chunk):
    my_globals.javi_buffer += chunk
    #print("BUFFER:",javi_buffer)
    
    if not my_globals.found_key:
        key_index = my_globals.javi_buffer.find("#**END-CODE**#")
        if key_index == -1: #if not found
            last_newline_pos = my_globals.javi_buffer.rfind("\n")
            if last_newline_pos != -1: #if new line is found
                my_globals.javi_buffer = my_globals.javi_buffer[last_newline_pos + 1:] #look for things after new line
        else:
            print("FOUND)")
            my_globals.found_key = True
            start_point = my_globals.javi_buffer.find("\n", key_index)
            my_globals.javi_buffer = my_globals.javi_buffer[start_point + 1:] #start at key index
    
    if my_globals.found_key:
        print_statements = find_print_statements(my_globals.javi_buffer)
        if print_statements:
            for statement in print_statements:
                #print(f"Extracted print statement: {statement.strip()}")
                print_statement = statement.strip()
                #print("SISENOR: ", print_statement)
                print_custom_terminal(print_statement) #print to print terminal

                #add custom repsonses on error here!
                if print_statement.find("OSError:") != -1:
                    print_custom_terminal("Make sure your devices are plugged into the proper ports!")

                my_gif.get_gif(my_globals.current_gif_dictionary, print_statement)

            
            last_newline_pos = my_globals.javi_buffer.rfind("\n")
            if last_newline_pos != -1:
                my_globals.javi_buffer = my_globals.javi_buffer[last_newline_pos + 1:]
    
    return my_globals.javi_buffer

def on_data_jav(chunk):
    # print("ON-DATA: ", chunk)
    
    # print("IN BUFFER", my_globals.javi_buffer)
    my_globals.javi_buffer = process_chunks(chunk)

#display custom code in editor, give delay on autoscroll function to ensure all new content has loaded
def print_custom_terminal(string):
    my_globals.custom_terminal_ele.innerHTML += string + " <br>"
    window.setTimeout(window.scrollTerminalToBottom, 0)


