### System

import shutil
import os
import sys
from subprocess import Popen, PIPE, STDOUT

#try:

#Alters the interface theme by removing the folder and copying the respective theme to the new interface folder

if sys.argv[1] == "Dark":
    os.system("rm -r interface")
    os.system("cp -R Interface_Dark_Theme interface")
elif sys.argv[1] == "Light":
    os.system("rm -r interface")
    os.system("cp -R Interface_Light_Theme interface")
else:
    print("[ERROR] Invalid argument, try \"Ligh\" or \"Dark\"")
#except:
#    print("[ERROR] Invalid arguments, Running example: python3 App_theme_selector Dark")
	
