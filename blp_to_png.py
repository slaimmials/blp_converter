import os, sys, math
from sys import *
import PIL.BlpImagePlugin
from PIL import Image

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

if len(sys.argv) != 2:
    print("Usage: blp_to_png.py \"path to folder OR file\"")
    exit()
    
singleFile = False
try:
    a = os.listdir(sys.argv[1])
except FileNotFoundError:
    print(bcolors.FAIL + sys.argv[1] + ": not exists" + bcolors.ENDC)
    exit()
except NotADirectoryError:
    singleFile = True

if singleFile:
    try:
        file = os.fsencode(sys.argv[1])
        sys.stdout.write('Converting...')
        with Image.open(file) as im:
            im.save(os.fsdecode(file)[:-4] + ".png")
        sys.stdout.write("\b"*len('Converting...') + bcolors.OKGREEN + "Conversion success!" + bcolors.ENDC)
        sys.stdout.flush()
    except PIL.BlpImagePlugin.BLPFormatError as e:
        sys.stdout.write("\b"*len('Converting...') + bcolors.FAIL + 'Conversion ended with error!' + bcolors.ENDC)
        sys.stdout.flush()
    except OSError:
        sys.stdout.write("\b"*len('Converting...') + bcolors.FAIL + 'Conversion ended with error!' + bcolors.ENDC)
        sys.stdout.flush()
        print()
    exit()

errs = 0
converted = 0
filesCount = 0
loadText = ""
lastFile = ""

def clamp(value, mi, ma):
    if value < mi:
        return mi
    elif value > ma:
        return ma
    return value

def scan(dir):
    fullPath = os.fsdecode(dir)
    for file in os.listdir(dir):
        filename = os.fsdecode(file)
        if filename.endswith(".blp"):
            global filesCount
            filesCount += 1
        elif os.path.isdir(fullPath + "\\" + filename):
            scan(os.fsencode(fullPath + "\\" + filename))

def convert_dir(dir):
    fullPath = os.fsdecode(dir)
    for file in os.listdir(dir):
        filename = os.fsdecode(file)
        if filename.endswith(".blp"):
            errored = False
            try:
                with Image.open(fullPath + "\\" + filename) as im:
                    im.save(fullPath + "\\" + filename[:-4] + ".png")
            except PIL.BlpImagePlugin.BLPFormatError as e:
                errored = True
            except OSError:
                errored = True
            if errored:
                global errs
                errs = errs +  1
            else:
                global converted
                converted += 1
            global loadText
            global lastFile
            fileColor = ""
            if errored:
                fileColor = bcolors.FAIL
            fills = math.floor(((errs+converted)/filesCount*100)/10)
            semifills = math.floor((((errs+converted)/filesCount*100)%10//5))
            loadText = bcolors.OKCYAN + len(loadText)*"\b" + "[" + fills*"▓" + semifills*"▒" + (10-(fills+semifills))*" " + "] " + str(math.floor((errs+converted)/filesCount*100)) + "% " + str(converted) + "/" + str(filesCount) + " " + fileColor + filename + bcolors.ENDC + clamp(len(lastFile)-len(filename),1,99)*" " + bcolors.ENDC
            sys.stdout.write(loadText)
            loadText = "[" + fills*"#" + (10-fills)*" " + "] " + str(math.floor((errs+converted)/filesCount*100)) + "% " + str(errs+converted) + "/" + str(filesCount) + " "+ filename + clamp(len(lastFile)-len(filename),1,99)*" "
            sys.stdout.flush()
            lastFile = filename
        elif os.path.isdir(fullPath + "\\" + filename):
            convert_dir(os.fsencode(fullPath + "\\" + filename))

directory = os.fsencode(sys.argv[1])

scan(directory)
loadText = "[          ] 0% 0/"+str(filesCount)
sys.stdout.write(loadText)
sys.stdout.flush()

convert_dir(directory)

print("\n\n" + bcolors.OKGREEN + "╓Conversion ended\n╠with errors:", str(errs) + "\n╚normally:", str(converted) + bcolors.ENDC)
