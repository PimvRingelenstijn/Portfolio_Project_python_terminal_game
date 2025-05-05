# function for nice terminal messages
def terminal_message(message, input = False):
    # Determine max scentence length in message
    len_message = 0
    split_message = message.split("\n")
    for scentence in split_message:
        if len_message < len(scentence):
            len_message = len(scentence)
    
    # blank line for top and bottem message
    blank_line = "-" * len_message 
    
    # check if message is input or regular print statement
    if input:
        # return with added blank line
        return blank_line + "\n" + message + "\n" + blank_line + "\n"
    else: return blank_line + "\n" + message + "\n" + blank_line