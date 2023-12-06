from zipfile import ZipFile, Path
# from datetime import datetime.isoformat
import pandas as pd
import numpy as np
from datetime import datetime, date
import re



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
                                        log_info["date updated"] = datetime.fromisoformat(message[0][0:23])

                if "Liberty instrument Connected" in decoded_line:
                    message = decoded_line.split('|')
                    for desc in message:
                        if "Liberty instrument Connected" in desc:
                            message_items = desc.split(' ')
                            for term in message_items:
                                if term.startswith('Serial'):
                                    tempserial = term.split(":")[1].strip()
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


def errorlog(zipname, levels, serial):
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
    errors["serial"] = serial
    errors.columns = ['Timestamp', "Description", "Serial"]
    # print (type(errors.Timestamp.iloc[1]))
    return errors

def errorcontext(zipname, errors, idx, lookback = 15, lookforward = 5):
    logtext = ""
    errortime = datetime.fromisoformat(errors.iloc[idx, 0][0:23])

    year = str(errortime.year)
    if len(str(errortime.month)) < 2:
        month = "0" + str(errortime.month)
    else:
        month = str(errortime.month)
    errorfolder = year + "-" + month

    path = "Logs/" + errorfolder + "/Run/Run"
    with ZipFile(zipname) as zip:
        df = pd.DataFrame(
        [(zinfo.filename, datetime(*zinfo.date_time), zinfo.file_size) for zinfo in zip.filelist],
        columns=["filename", "date_time", "file_size"],)
        # print(df)
        runlogfiles = df[df.filename.str.contains(path)] #filter out only "Rundetail_XX.txt" files
        errorfile = runlogfiles[runlogfiles.date_time >=errortime].sort_values(by="date_time").iloc[0,0] #remove the files that were updated prior to the datetime of the error in question
        # print("Run Log:", errorfile)
        notfound = True
        errorline = {"timestamp":datetime(1990,1,1), "line number":0}
        errordumpline = {"timestamp":datetime(1990,1,1), "line number":0}
        searchfiles = [errorfile, path + "Detail_0.txt"]
        for item in searchfiles:
            linefile = zip.open(item).readlines()

            for pos, line in enumerate(linefile):
                try:
                    decoded_line = line.decode(encoding="utf-8")
                    if "|" not in decoded_line:
                        # if "RegulatorFirmwareVersionNumber" in decoded_line:
                        #     errordumpline = pos
                        continue
                    else:
                        # try:
                        timestamp = datetime.fromisoformat(decoded_line.split("|")[0][0:23])
                        if "FirmwareVersionNumber:" in decoded_line:
                            errordumpline["timestamp"] = timestamp
                            errordumpline["line number"] = pos
                        elif (((timestamp - errortime).seconds) < 1) & (((timestamp - errortime).days) >= 0):
                            print("SEARCHED ERROR:",re.sub("[\t ]{2,}", " ", decoded_line))
                            errorline["timestamp"] = timestamp
                            errorline["line number"] = pos
                            notfound = False
                            # print(item,"\n")
                            break
                        # except:
                        #     continue
                except:
                    continue #added due to error trying to decode "0xb0" byte in some random RunDetail log
            if (notfound == False):
                    break
        if ((errorline["line number"] > 0) & ((errorline["line number"]-errordumpline["line number"]) > 0) & (((errorline["timestamp"] - errordumpline["timestamp"]).seconds) < 5)):
            for line in linefile[errordumpline["line number"]-lookback:errorline["line number"]+1]:
                line = re.sub("[\t ]{2,}", " ", line.decode(encoding="utf-8")).replace('\n', '')
                logtext = logtext + "\n" + line
                # logtext = logtext + line
                # print(logtext)
                # print(line.decode(encoding="utf-8").replace('\t', '').replace('\n', ''))
        else:
            for line in linefile[errorline["line number"]-lookback:errorline["line number"]+lookforward]:
                line = re.sub("[\t ]{2,}", " ", line.decode(encoding="utf-8")).replace('\n', '')
                logtext = logtext + "\n" + line
                # logtext = logtext + line
        # print(logtext)
                # print(line.decode(encoding="utf-8").replace('\t', '').replace('\n', ''))
        return logtext
        # for line in zip.open(path + "Detail_0.txt"):
        #     decoded_line = line.decode(encoding="utf-8")
        #     if "|" not in decoded_line:
        #         continue
        #     else:
        #         # print(decoded_line)
        #         try:
        #             timestamp = datetime.fromisoformat(decoded_line.split("|")[0][0:23])
        #             if ((timestamp - errortime).seconds) < 1:
        #                 print(decoded_line)
        #                 print("Error found in RunDetail 0")
        #                 notfound = False
        #                 break
        #         except:
        #             continue
        if (notfound):
            print("WARNING: Error not found!")

        # print(df["date_time"].iloc[20]>errortime)
