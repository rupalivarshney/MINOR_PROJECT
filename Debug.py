#################################################################
#   Filename:   Debug.py
#   Desc:       This file contains logging method for debugging
#
#################################################################

def Debug(message, method = None, module = None):
    if module != None:
        if method != None:
            print(message, method, module)
        else: print(message, module)
    else: print(message)
