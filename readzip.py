from filefunctions import *
import tkinter
from tkinter import filedialog
import os
import streamlit as st


zipname = "Liberty PRIME 2.0 Troubleshooting Bundle - 2023-11-15 13.23.27.zip"
# zipname = "Liberty PRIME 2.0 Troubleshooting Bundle - 2023-09-18 10.05.56.zip"
# zipname = "Liberty PRIME 2.0 Troubleshooting Bundle - 2023-01-13 09.26.42.zip"
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

log_info = dict()
log_info = log(zipname, levels)
# print(log_info)

errors = errorlog(zipname, levels, log_info["serial"])
# print(errors)
st.write(errors)

option = st.selectbox("Pick an error to investigate:", errors["Timestamp"] + " | " + errors["Description"])
# optiontime = datetime.fromisoformat(option.split("|")[0][0:23])
# optiontime = pd.to_datetime(option.split("|")[0][0:23])
optiontime = datetime.fromisoformat(option.split("|")[0][0:23])
error_location = errors.set_index(pd.to_datetime(errors['Timestamp'])).index.get_indexer([optiontime], method='nearest')[0]
print(errors.set_index(pd.to_datetime(errors['Timestamp'])).index.get_indexer([optiontime], method='nearest')[0])
# iloc_idx = errors_timestamp.index.get_indexer([optiontime], method='nearest')

# print (type(errors.Timestamp.iloc[1]))

st.write(errorcontext(zipname, errors, error_location))
# os.system("streamlit run readzip.py")

# errorcontext(zipname, errors, 6)


# for i in range(1,len(errors)):
#
#     errorcontext(zipname, errors, i)
#     print("ERROR NUMBER:", i)
#     print(errors[i-1:i+2])
#
#     k = input("NEXXXXXT:")
