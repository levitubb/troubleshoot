from filefunctions import *
import tkinter
from tkinter import filedialog
import os
import streamlit as st
import numpy as np


# zipname = "Liberty PRIME 2.0 Troubleshooting Bundle - 2023-11-15 13.23.27.zip"
# zipname = "Liberty PRIME 2.0 Troubleshooting Bundle - 2023-09-18 10.05.56.zip"
# zipname = "Liberty PRIME 2.0 Troubleshooting Bundle - 2023-01-13 09.26.42.zip"
# zipname = "C:/Users/lt259/Desktop/Liberty PRIME 2.0 Troubleshooting Bundle - 2023-11-21 10.32.48.zip"
# zipname = "C:/Users/lt259/Desktop/Liberty Blue 2.0 Troubleshooting Bundle - 2023-12-06 09.18.31.zip"
def readzip():
    st.set_page_config(layout = "wide")

    root = tkinter.Tk()
    root.withdraw() #use to hide tkinter window
    root.wm_attributes('-topmost', 1)
    save = open("save.txt", "r")
    saveread = save.readlines()
    save.close()
    print(saveread)
    try:
        zipname = saveread[0]
    except:
        zipname = ""



    def search_for_file_path():
        currdir = os.getcwd()
        tempdir = filedialog.askopenfilename(parent=root, initialdir=currdir, title='Please select a directory')
        if len(tempdir) > 0:
            print ("You chose: %s" % tempdir)
        return tempdir

    # zipname = search_for_file_path()

    if st.button("Pick a TB to analyze"):
        zipname = search_for_file_path()
        print("ZIPNAME", zipname)
        save = open("save.txt", "w")
        save.write(zipname)
        save.close()
        print ("\nfile_path_variable = ", zipname)


    if zipname != "":
        st.text("TB Location: " + zipname)
        levels = findlevels(zipname)
        # print(levels)

        log_info = log(zipname, levels)
        # print(log_info)

        errors = errorlog(zipname, levels, log_info["serial"])
        # print(errors)

        st.write(errors)


        option = st.selectbox("Pick an error to investigate:", errors["Timestamp"] + " | " + errors["Description"])
        optiontime = datetime.fromisoformat(option.split("|")[0][0:23])
        error_location = errors.set_index(pd.to_datetime(errors['Timestamp'])).index.get_indexer([optiontime], method='nearest')[0]

        col1, col2, col3= st.columns(3)
        lastoperation = col1.checkbox("Start logs from most recent Operation", value = True)
        verbose = col1.checkbox("Verbose")
        if not lastoperation:
            lookback = col2.number_input("How many lines to load before the error?", min_value = 0, value = 20)
            lookforward = col3.number_input("How many lines to load after the error?", min_value = 0, value = 5)
            st.write(errorcontext(zipname, errors, error_location, lookback, lookforward, verbose=verbose))
        else:
            st.write(errorcontext(zipname, errors, error_location, lastoperation = lastoperation, verbose=verbose))



if __name__ == "__main__":
    readzip()
