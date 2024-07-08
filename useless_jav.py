running_editor_code = False
key = "PRINT_KEY:"
number = 0
def jav_new_data(chunk): #called in every single incoming data 
    #iterate over chunk (proved to be relatively small)
    #Find key 
    global javi_buffer, key, running_editor_code, number
    if (running_editor_code):
        javi_buffer += chunk
        print("NEW DATA")
        #javi_buffer += chunk
        #print(chu)
        print(chunk)
        print("DONE-NEW")

        print("BUFFER")
        print(javi_buffer)
    
        
        if key in javi_buffer:
            #only perform this expensive search if there is a substring key
            num_keys = javi_buffer.count(key)
            print("Number of keys: ", num_keys)
            match = re.search(r'(\d+)\*\*ST\*\*', javi_buffer) #more expensive search 
            if match:
                number = match.group(1)
                print("GOT-IT: ", number)
                #if (number = 99): #do something to signify to stop calling dictionary
                    
            else:
                print("we havE A PROBLEM. No # next to key") #cause there is no umber next to the key
            javi_buffer = ''





'''
prev_num_lines = 0 #lines of repl (this is pointer = index) (original)
time_delay_jav = 3
length_repl_text_prev = 0
#lines_list = []

#(line1, line2) - current list length 2
# (line 1, line 2, line 3, line4) - now lenth 4
# I want 2 (starting point) - so 

#TODO0:Terminate while loop somehow so that it doesnt keep runnign on device 
async def check_buffer():
    global prev_num_lines, time_delay_jav, length_repl_text_prev
    while True:
        #boolean begin_print_check is just for efficiency so that it doesnt do this check when you are not running file (hit run button)
        if terminal.connected: #only check buffer if terminal es conected
            #buffer_jav = terminal.buffer
            #note: repl_text will contain all text from the beginning of the program
            repl_text = terminal.buffer #get text from buffer. Saves contents from buffer. Question: Can I clear buffer to make it more efficient?
            length_repl_text = len(repl_text)
            #TODOO: fix when hitting download again.
            #Important: this condition might not work if u download again (resets buffer) (prev val is now biggern than current)
            if length_repl_text_prev < len(repl_text): #only if repl text changed 
                #print("Length_repl")
                #print(length_repl_text)
                print("text_repl")
                print("Begin",repl_text,"ENd")

                lines = repl_text.splitlines() #save lines in array (each slot is a line)
                for i in range(len(lines)):
                    lines[i] += '!'
                print("LINE_Array+!")
                print("LINE_Array+!")
                print("LINE_Array+!")
                #print(lines)
                print("END+!")
                print("END+!")
                print("END+!")
                #if line does not contain ">>> at beginnig, it means it is a print statement"
                print("Length_lines: ", len(lines))
                # (extra sanity check: slightly unncecssary cause of 1st if statemennt
                if (prev_num_lines < len(lines)): #it means more lines have been put in buffer 
                    start_index = prev_num_lines #index start at 0 (start at 1 more index than previous list) (so no -1)
                    for i in range(start_index, len(lines)): #will iterate from newly added 1st element to last element
                        current_new_line = lines[i] 
                        #print("Curr-line: ", current_new_line) #correctly get print statements
                prev_num_lines = len(lines)  #now save index (length) last thing (update new length of lines list)
                length_repl_text_prev = len(repl_text)

            #print("AQUI: ", buffer_jav)
        await asyncio.sleep(time_delay_jav) #worked with 0.1 (to wait for other things to execute) #have it as 0.4 (jav rec)

print("AWUI")
'''
#move this line into the handle_board function
#asyncio.create_task(check_buffer()) #as soon as webpage is loaded, it will continously call this function

#KEY
#Pick an orange one (vscode editing vs pyscript) - have a webpage that moves two motors


# V1:\n**ST**MESSAGE**ED**\n
#V2: \n**ST**MESSAGE\n
#v3: \n**ST**#\n # the symbol'#' is just a number
# v4: **ST**#
#v5: #**ST**
javi_buffer = ''
#IDEA: stop looking for new lines as there are tons of them
#look for asteriscs on fist if stament. 
# do elifs to check for rest of characters 
# check before the lenght of the buffer to see if it is equal or greater to index you want to access
#
#found_asterisc = False
count_keys = 0
running_editor_code = False
key = "**ST**"
def jav_new_data(chunk): #called in every single incoming data 
    #iterate over chunk (proved to be relatively small)
    #Find key 
    global javi_buffer, count_keys, key, running_editor_code
    if (running_editor_code):
        javi_buffer += chunk
        print("NEW DATA")
        #javi_buffer += chunk
        #print(chu)
        print(chunk)
        print("DONE-NEW")

        print("BUFFER")
        print(javi_buffer)
    
        
        if key in javi_buffer:
            #only perform this expensive search if there is a substring key
            match = re.search(r'(\d+)\*\*ST\*\*', javi_buffer) #more expensive search 
            if match:
                number = match.group(1)
            else:
                print("we havE A PROBLEM. No # next to key") #cause there is no umber next to the key
            print("GOT-IT: ", number)
            javi_buffer = ''
       

    #ToDO: account for double print statem
    
    
    #only clear buffer if none of key characters are found
   

    
        

    # 1st chunk: \n*
    #2nd chunk: *ST
    # 
    #javi_buffer += chunkd


    '''

    if '*' in chunk: #initiate build found new line for the first time)
        found_new_line = True
        #sleep
        #che 

    word_focus = chunk
    if found_new_line: #if newline was detected at some point
        javi_buffer += chunk #start building string
        #check lenght of chunk
        # ex1: sf\n
        # 3 - 2 = 1 = length of key
        #ex2: re\ntt = 5 - 2 = 3
        
        start_index_new_line = word_focus.find('\n')
        #length starting from the new line character
        length_potential_key = len(word_focus) - start_index_new_line 
        #If pontential key is >= length of key, then proceed to check 
        if(length_potential_key >= 9): 
            
            pass
        start_index = chunk.find('\n') + 1  #index of character next to \n 
        javi_buffer += chunk
        #check for beginning sequence
        #save the number/message (return it)
    
    
    #if len(chunk) > 1: #means you can read the next character
    start_index = chunk.find('\n') + 1 #index of character next to \n 
    for i in range(start_index, len(chunk)):
        if(chunk[i]) == '*':
            pass
    
    '''


    '''
prev_num_lines = 0 #lines of repl (this is pointer = index) (original)
time_delay_jav = 3
length_repl_text_prev = 0
#lines_list = []

#(line1, line2) - current list length 2
# (line 1, line 2, line 3, line4) - now lenth 4
# I want 2 (starting point) - so 

#TODO0:Terminate while loop somehow so that it doesnt keep runnign on device 
async def check_buffer():
    global prev_num_lines, time_delay_jav, length_repl_text_prev
    while True:
        #boolean begin_print_check is just for efficiency so that it doesnt do this check when you are not running file (hit run button)
        if terminal.connected: #only check buffer if terminal es conected
            #buffer_jav = terminal.buffer
            #note: repl_text will contain all text from the beginning of the program
            repl_text = terminal.buffer #get text from buffer. Saves contents from buffer. Question: Can I clear buffer to make it more efficient?
            length_repl_text = len(repl_text)
            #TODOO: fix when hitting download again.
            #Important: this condition might not work if u download again (resets buffer) (prev val is now biggern than current)
            if length_repl_text_prev < len(repl_text): #only if repl text changed 
                #print("Length_repl")
                #print(length_repl_text)
                print("text_repl")
                print("Begin",repl_text,"ENd")

                lines = repl_text.splitlines() #save lines in array (each slot is a line)
                for i in range(len(lines)):
                    lines[i] += '!'
                print("LINE_Array+!")
                print("LINE_Array+!")
                print("LINE_Array+!")
                #print(lines)
                print("END+!")
                print("END+!")
                print("END+!")
                #if line does not contain ">>> at beginnig, it means it is a print statement"
                print("Length_lines: ", len(lines))
                # (extra sanity check: slightly unncecssary cause of 1st if statemennt
                if (prev_num_lines < len(lines)): #it means more lines have been put in buffer 
                    start_index = prev_num_lines #index start at 0 (start at 1 more index than previous list) (so no -1)
                    for i in range(start_index, len(lines)): #will iterate from newly added 1st element to last element
                        current_new_line = lines[i] 
                        #print("Curr-line: ", current_new_line) #correctly get print statements
                prev_num_lines = len(lines)  #now save index (length) last thing (update new length of lines list)
                length_repl_text_prev = len(repl_text)

            #print("AQUI: ", buffer_jav)
        await asyncio.sleep(time_delay_jav) #worked with 0.1 (to wait for other things to execute) #have it as 0.4 (jav rec)

print("AWUI")
'''
#move this line into the handle_board function
#asyncio.create_task(check_buffer()) #as soon as webpage is loaded, it will continously call this function

#KEY
#Pick an orange one (vscode editing vs pyscript) - have a webpage that moves two motors


# V1:\n**ST**MESSAGE**ED**\n
#V2: \n**ST**MESSAGE\n
#v3: \n**ST**#\n # the symbol'#' is just a number
# v4: **ST**#
#v5: #**ST**
javi_buffer = ''
#IDEA: stop looking for new lines as there are tons of them
#look for asteriscs on fist if stament. 
# do elifs to check for rest of characters 
# check before the lenght of the buffer to see if it is equal or greater to index you want to access
#
#found_asterisc = False
count_keys = 0
running_editor_code = False
key = "**ST**"
def jav_new_data(chunk): #called in every single incoming data 
    #iterate over chunk (proved to be relatively small)
    #Find key 
    global javi_buffer, count_keys, key, running_editor_code
    if (running_editor_code):
        javi_buffer += chunk
        print("NEW DATA")
        #javi_buffer += chunk
        #print(chu)
        print(chunk)
        print("DONE-NEW")

        print("BUFFER")
        print(javi_buffer)
    
        
        if key in javi_buffer:
            #only perform this expensive search if there is a substring key
            match = re.search(r'(\d+)\*\*ST\*\*', javi_buffer) #more expensive search 
            if match:
                number = match.group(1)
            else:
                print("we havE A PROBLEM. No # next to key") #cause there is no umber next to the key
            print("GOT-IT: ", number)
            javi_buffer = ''
       

    #ToDO: account for double print statem
    
    
    #only clear buffer if none of key characters are found
   

    
        

    # 1st chunk: \n*
    #2nd chunk: *ST
    # 
    #javi_buffer += chunkd


    '''

    if '*' in chunk: #initiate build found new line for the first time)
        found_new_line = True
        #sleep
        #che 

    word_focus = chunk
    if found_new_line: #if newline was detected at some point
        javi_buffer += chunk #start building string
        #check lenght of chunk
        # ex1: sf\n
        # 3 - 2 = 1 = length of key
        #ex2: re\ntt = 5 - 2 = 3
        
        start_index_new_line = word_focus.find('\n')
        #length starting from the new line character
        length_potential_key = len(word_focus) - start_index_new_line 
        #If pontential key is >= length of key, then proceed to check 
        if(length_potential_key >= 9): 
            
            pass
        start_index = chunk.find('\n') + 1  #index of character next to \n 
        javi_buffer += chunk
        #check for beginning sequence
        #save the number/message (return it)
    
    
    #if len(chunk) > 1: #means you can read the next character
    start_index = chunk.find('\n') + 1 #index of character next to \n 
    for i in range(start_index, len(chunk)):
        if(chunk[i]) == '*':
            pass
    
    '''
    




        
   # else: #u know you don't have key in chunk
      #  javi_buffer = '' #empty buffer



    #if chunk contains '*', then, build on javi_buffer (checking every time that it has currect next character
    # keep building javi_buffer