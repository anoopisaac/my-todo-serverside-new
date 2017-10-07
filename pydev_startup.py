import sys
import os
#Assuming that pdvsd is located in the working folder
#sys.path.append(os.getcwd()+"\ptvsd-3.2.0") 
import ptvsd


# print (os.getcwd())
print (ptvsd)
#Fee free to change the secret and port number 
ptvsd.enable_attach(secret = None, address = ('localhost', 7600))
#The debug server has started and you can now use VS Code to attach to the application for debugging
print("Google App Engine has started, ready to attach the debugger")