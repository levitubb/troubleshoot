from zipfile import ZipFile, Path
# from datetime import datetime.isoformat
import pandas as pd
import numpy as np
from datetime import datetime, date



log_info = {"instrument" : "", "serial" : "", "version" : "", "date updated" : "Never"}

def findlevels(zipname):
    with ZipFile(zipname) as zip:
        folders = zip.namelist()
        folders_list = pd.DataFrame()
        levels = dict()
        for line in folders:
            line = pd.Series(line.split('/'))
            folders_list = pd.concat([folders_list,line], axis = 1, ignore_index = 1).replace('', np.nan)
        for iter in range(1,folders_list.shape[0]):
            name = "level" + str(iter)
            levels[name]=folders_list.iloc[iter-1,:].drop_duplicates().replace('', np.nan).dropna().tolist()
        levels["level2"].sort(key=lambda date: datetime.strptime(date, "%Y-%m"))
        if "Logs" not in levels["level1"]:
            print("Logs folder is missing or invalid zip file, try loading the TB again")
    return levels

def log(zipname, levels):
    with ZipFile(zipname) as zip:
        for month_folder in levels["level2"]:
            path = "Logs/" + month_folder + "/Log.txt"
            for line in zip.open(path):
                decoded_line = line.decode(encoding="utf-8")
                if "APPLICATION STARTUP" in decoded_line:
                    message = decoded_line.split('|')
                    for desc in message:
                        if "APPLICATION STARTUP" in desc:
                            message_items = desc.split(' ')
                            if log_info["instrument"] == '':
                                log_info["instrument"] = ' '.join(message_items[2:5])
                            elif log_info["instrument"] != ' '.join(message_items[2:5]):
                                print("WARNING: multiple instruments detected")
                            for term in message_items:
                                if term.startswith('v'):
                                    if term.strip('v') == log_info["version"]:
                                        continue
                                    elif log_info["version"] == "":
                                        log_info["version"] = term.strip('v')
                                    else:
                                        log_info["version"] = term.strip('v')
                                        # print(message[0][0:23])
                                        log_info["date updated"] = datetime.fromisoformat(message[0][0:23])
                                        # print(log_info["date updated"])
                if "Liberty instrument Connected" in decoded_line:
                    message = decoded_line.split('|')
                    for desc in message:
                        if "Liberty instrument Connected" in desc:
                            message_items = desc.split(' ')
                            for term in message_items:
                                if term.startswith('Serial'):
                                    tempserial = term.split(":")[1].strip()#term.strip('SerialNumber:')#.strip()
                                    if tempserial == "LB0002":
                                        continue
                                    elif tempserial == log_info["serial"]:
                                        continue
                                    elif log_info["serial"] == "":
                                        log_info["serial"] = tempserial
                                    else:
                                        log_info["serial2"] = tempserial
                                        print("WARNING: multiple serial numbers")
        return log_info


def errorlog(zipname, levels):
    errors = pd.DataFrame()
    if 'Errors.txt' not in levels["level3"]:
        print("WARNING: No error log found")
    else:
        for month_folder in levels["level2"]:
            path = "Logs/" + month_folder + "/Errors.txt"
            with ZipFile(zipname) as zip:
                for line in zip.open(path):
                    decoded_line = line.decode(encoding="utf-8")
                    if "|" not in decoded_line:
                        continue
                    else:
                        message = decoded_line.split("|")
                        if '"' not in message[3]:
                            continue
                        else:
                            message[3] = message[3].split('"')[1]
                            errors = pd.concat([errors, pd.Series([message[0], message[3]])], ignore_index = 1, axis = 1)
    errors = errors.transpose()
    return errors

def errorcontext(zipname, errors, idx):
    errortime = datetime.fromisoformat(errors.iloc[idx, 0][0:23])
    errorfolder = str(errortime.year) + "-" + str(errortime.month)
    print(type(errortime))
    path = "/Logs/" + errorfolder + "/Run/"
    with ZipFile(zipname) as zip:
            df = pd.DataFrame(
            [(zinfo.filename, zinfo.date_time, zinfo.file_size) for zinfo in zip.filelist],
            columns=["filename", "date_time", "file_size"],)
            print(type(df["date_time"].sort_values().iloc[3]))
            print(df["date_time"].iloc[3]>errortime)
