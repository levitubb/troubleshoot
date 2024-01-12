from filefunctions import *
import os
import streamlit as st
import numpy as np

# zipname = "Liberty PRIME 2.0 Troubleshooting Bundle - 2023-11-15 13.23.27.zip"
# zipname = "Liberty PRIME 2.0 Troubleshooting Bundle - 2023-09-18 10.05.56.zip"
# zipname = "Liberty PRIME 2.0 Troubleshooting Bundle - 2023-01-13 09.26.42.zip"
# zipname = "C:/Users/lt259/Desktop/Liberty PRIME 2.0 Troubleshooting Bundle - 2023-11-21 10.32.48.zip"
# zipname = "C:/Users/lt259/Desktop/Liberty Blue 2.0 Troubleshooting Bundle - 2023-12-06 09.18.31.zip"
def TBanalyzer():
    st.set_page_config(layout = "wide")
    hide_streamlit_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    # save = open("save.txt", "r")
    # saveread = save.readlines()
    # save.close()
    # print(saveread)
    # try:
    #     zipname = saveread[0]
    # except:
    #     zipname = ""
    zipname = ""

    zipname = st.file_uploader("Pick a Troubleshooting Bundle Zip File...", type = ".zip")
    if zipname is None:
        st.session_state["upload_state"] = "Upload a file first!"

    if (zipname != "") & (zipname != None):
    # if 0:
        # st.text("TB Location: " + zipname)
        levels = find_levels(zipname)
        # print(levels)

        log_info = process_log(zipname, levels)
        # print(log_info)

        errors = extract_error_log(zipname, levels, log_info["serial"])
        if type(errors) == str:
            st.write("Your TB file does not show any errors, please upload a different file to be analyzed.")
        else:

            st.markdown(":blue[__Software Version:__ " + log_info["version"] + "\t|\t__Date Updated:__ " + str(log_info["date_updated"])[0:19]+" ]")
            "---"
            # col2 = st.write("Date Updated: " + str(log_info["date updated"]))
            st.subheader("Errors Detected:")
            st.dataframe(errors, width = 1200, height = 300, use_container_width = True)



            option = st.selectbox("Pick an error to investigate:", errors["Timestamp"] + " | " + errors["Description"])
            optiontime = datetime.fromisoformat(option.split("|")[0][0:23])
            print(errors.set_index(pd.to_datetime(errors['Timestamp'])).sort_index().index.get_indexer([optiontime], method='nearest')[0])
            error_location = errors.set_index(pd.to_datetime(errors['Timestamp'])).sort_index().index.get_indexer([optiontime], method='nearest')[0]

            col1, col2, col3= st.columns([1,2,2])
            lastoperation = col1.checkbox("Start logs from most recent Operation", value = True)
            filterflag = col1.checkbox("Filter Text", value = True)
            timestamps = col1.checkbox("Timestamps", value = False)
            if filterflag:
                filtertext = col2.text_area("Text to filter", """ProgressBar
SKIP ROTARY MOVE COMMAND
IfThenGoto
UVReadAndRecordUVAbsorbance""", height = 125)
                filtertext = filtertext.split("\n")
            else:
                filtertext = []
            # coll1, coll2 = st.columns([1, 3])

            if not lastoperation:
                lookback = col3.number_input("How many lines to load before the error?", min_value = 0, value = 20)
                lookforward = col3.number_input("How many lines to load after the error?", min_value = -500, value = 5)
                # logtimes, logtext = errorcontext(zipname, levels, errors, error_location, lookback, lookforward, verbose=verbose)
                # coll1.markdown(logtimes)
                # coll2.markdown(logtext)

                st.markdown(errorcontext(zipname, levels, errors, error_location, lookback, lookforward, filterflag=filterflag, filtertext = filtertext, timestamps=timestamps))
            else:
                # logtimes, logtext = errorcontext(zipname, levels, errors, error_location, lastoperation = lastoperation, verbose=verbose)
                # coll1.markdown(logtimes)
                # coll2.markdown(logtext)

                st.markdown(errorcontext(zipname, levels, errors, error_location, lastoperation = lastoperation, filterflag=filterflag, filtertext = filtertext, timestamps=timestamps))



if __name__ == "__main__":
    TBanalyzer()
