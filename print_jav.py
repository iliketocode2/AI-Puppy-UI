"""
print_jav.py

Authors: Javier Laveaga

This script processes data chunks, extracts print statements, and displays them
in a custom terminal.It assumes that print statements will come after the key
#**END-CODE**# is printed to the repl. This is meant to be placed at the end
of the code that is running (done automatically in helper_mod.handle_board)

"""

import my_globals
from pyscript import document, window
import my_gif


def find_print_statements(buffer):
    """
    Extracts print statements from the buffer.

    Args:
        buffer (str): The buffer containing potential print statements.

    Returns:
        list: A list of print statements found in the buffer.
    """
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
    """
    Processes incoming data chunks, extracting and handling print statements. If
    print statements are found, it will print them to the custom terminal.

    Args:
        chunk (str): The data chunk to be processed.

    Returns:
        str: The remaining buffer after processing.
    """
    my_globals.javi_buffer += chunk
    
    if not my_globals.found_key:
        key_index = my_globals.javi_buffer.find("#**END-CODE**#")
        if key_index == -1: #if not found
            last_newline_pos = my_globals.javi_buffer.rfind("\n")
            if last_newline_pos != -1: #if new line is found
                #look for things after new line
                my_globals.javi_buffer = my_globals.javi_buffer[
                    last_newline_pos + 1:] 
        else:
            print("FOUND)")
            my_globals.found_key = True
            start_point = my_globals.javi_buffer.find("\n", key_index)
            #start at key index
            my_globals.javi_buffer = my_globals.javi_buffer[start_point + 1:] 
    
    if my_globals.found_key:
        print_statements = find_print_statements(my_globals.javi_buffer)
        if print_statements:
            for statement in print_statements:
                #print(f"Extracted print statement: {statement.strip()}")
                print_statement = statement.strip()
                print_custom_terminal(print_statement) #print to print terminal
                if print_statement.find("OSError:") != -1:
                    print_custom_terminal("""Make sure your devices are 
                                            plugged into the proper ports!""")

                my_gif.get_gif(my_globals.current_gif_dictionary, 
                               print_statement)

            
            last_newline_pos = my_globals.javi_buffer.rfind("\n")
            if last_newline_pos != -1:
                my_globals.javi_buffer = my_globals.javi_buffer[
                    last_newline_pos + 1:]
    
    return my_globals.javi_buffer

def on_data_jav(chunk):
    """
    Handles incoming data chunks and processes them. This function gets called
    every time data / text is sent or written to the repl. (Ex: typing)

    Args:
        chunk (str): The data chunk to be handled.
    """
    my_globals.javi_buffer = process_chunks(chunk)

#display custom code in editor, give delay on autoscroll function to ensure 
# all new content has loaded
def print_custom_terminal(string):
    """
    Appends a string to the custom terminal and autoscrolls to the bottom.

    Args:
        string (str): The string to be displayed in the custom terminal.
    """
    if (string != "<awaitable>"):
        my_globals.custom_terminal_ele.innerHTML += string + '<br> <br>'
        window.setTimeout(window.scrollTerminalToBottom, 0)


