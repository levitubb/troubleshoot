from filefunctions import *
import tkinter
from tkinter import filedialog
import os


zipname = "Liberty PRIME 2.0 Troubleshooting Bundle - 2023-11-15 13.23.27.zip"
zipname = "Liberty PRIME 2.0 Troubleshooting Bundle - 2023-09-18 10.05.56.zip"
zipname = "Liberty PRIME 2.0 Troubleshooting Bundle - 2023-01-13 09.26.42.zip"
# zipname = "C:/Users/lt259/Desktop/Liberty PRIME 2.0 Troubleshooting Bundle - 2023-11-21 10.32.48.zip"


root = tkinter.Tk()
root.withdraw() #use to hide tkinter window

# def search_for_file_path ():
#     currdir = os.getcwd()
#     tempdir = filedialog.askopenfilename(parent=root, initialdir=currdir, title='Please select a directory')
#     if len(tempdir) > 0:
#         print ("You chose: %s" % tempdir)
#     return tempdir
# zipname = search_for_file_path()
# print ("\nfile_path_variable = ", zipname)

levels = findlevels(zipname)
# print(levels)

errors = errorlog(zipname, levels)
print(errors)

errorcontext(zipname, errors, 3)

log_info = dict()
log_info = log(zipname, levels)
print(log_info)
