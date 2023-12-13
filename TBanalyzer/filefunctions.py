from zipfile import ZipFile, Path
# from datetime import datetime.isoformat
import pandas as pd
import numpy as np
from datetime import datetime, date
import re
from itertools import groupby



log_info = {"instrument" : "", "serial" : "", "version" : "", "date updated" : "Never"}

def findlevels(zipname):
    with ZipFile(zipname) as zip:
        folders = zip.namelist()
        folders_list = pd.DataFrame()
        levels = dict()
        for line in folders:
            if line.endswith('Logs/'):
                levels["logsfolder"] = line
            else:
                levels["logsfolder"] = "Logs/"
            line = pd.Series(line.split('/'))
            folders_list = pd.concat([folders_list,line], axis = 1, ignore_index = 1).replace('', np.nan)
        passby = 0
        for iter in range(1,folders_list.shape[0]):
            name = "level" + str(iter)
            levellist=folders_list.iloc[iter-1,:].drop_duplicates().replace('', np.nan).dropna().tolist()
            # for item in levellist:
            #     print(item)
            #     if "Troubleshooting" in item:
            #         passby = 1
            #         continue
            # if (iter-passby) == 0:
            #     print("JDKL:SJK")
            #     continue
            # name = "level" + str(iter-passby)
            levels[name] = levellist
        # print(levels)
        foundlogs = False
        while (foundlogs == False):
            for item in levels:
                for member in levels[item]:
                    if member == 'Logs':
                        # levels["monthsfolder"] = "level" + str(int(item[5])+1)
                        monthsfolder = "level" + str(int(item[5])+1)
                        errorsfolder = "level" + str(int(item[5])+2)
                        foundlogs = True
                        break

        levels["monthsfolder"] = monthsfolder
        levels["errorsfolder"] = errorsfolder
        levels[levels["monthsfolder"]].sort(key=lambda date: datetime.strptime(date, "%Y-%m"))
        if "Logs" not in levels["logsfolder"]:
            print("Logs folder is missing or invalid zip file, try loading the TB again")
    return levels

def log(zipname, levels):
    with ZipFile(zipname) as zip:
        for month_folder in levels[levels["monthsfolder"]]:
            path = levels["logsfolder"] + month_folder + "/Log.txt"
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
    if 'Errors.txt' not in levels[levels["errorsfolder"]]:
        print("WARNING: No error log found")
    else:
        for month_folder in levels[levels["monthsfolder"]]:
            path = levels["logsfolder"] + month_folder + "/Errors.txt"
            with ZipFile(zipname) as zip:
                try: zip.open(path)
                except: continue
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

def markdown_logtext(line):
    # line = re.sub("[\t ]{2,}", " ", line.decode(encoding="utf-8")).replace('\n', '')
    line =line.decode(encoding="utf-8").replace('\n', '').replace('\r', '')

    line = line.split("|")

    try:
        datetime.fromisoformat(line[0][0:23])
        # line[0] = " `"+line[0]+"`"
        line.remove("INFO")
        line.remove("RunDetails")
        # line[1] = "```" + line[1] + "```"
        # line[1] = "> " + line[1]
    except:

        # line.insert(0, "")

        line[0]



    # line[1] = '|'.join(line[1:]) + "\n"
    # print(line)
    # return line[0:2]
    return ('|'.join(line[1:]))

        # if any(n in line for n in nonverbose):


def errorcontext(zipname, levels, errors, idx, lookback = 200, lookforward = 5, lastoperation = False, verbose = False):
    logtext = ""
    nonverbose = ["ProgressBar", "SKIP ROTARY MOVE COMMAND", "IfThenGoto", "UVReadAndRecordUVAbsorbance"]
    errortime = datetime.fromisoformat(errors.iloc[idx, 0][0:23])

    year = str(errortime.year)
    if len(str(errortime.month)) < 2:
        month = "0" + str(errortime.month)
    else:
        month = str(errortime.month)
    errorfolder = year + "-" + month

    path = levels["logsfolder"] + errorfolder + "/Run/Run"
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
        errordumpline = {"timestamp":datetime(1990,1,1), "line number":0, "last operation":0}
        searchfiles = [errorfile, path + "Detail_0.txt"]
        for item in searchfiles:
            linefile = zip.open(item).readlines()

            for pos, line in enumerate(linefile):
                # print(line)
                try:
                    decoded_line = line.decode(encoding="utf-8")
                    if "|" not in decoded_line:
                        continue
                    else:
                        # try:
                        timestamp = datetime.fromisoformat(decoded_line.split("|")[0][0:23])
                        if "FirmwareVersionNumber:" in decoded_line:
                            errordumpline["timestamp"] = timestamp
                            errordumpline["line number"] = pos
                            errordumpline["verbose count"] = 0
                        elif "OPERATION:" in decoded_line:
                            errordumpline["last operation"] = pos
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
            if lastoperation:
                filelow = errordumpline["last operation"]
            else:
                filelow = errordumpline["line number"]-lookback
            filehigh = errorline["line number"]+1
        else:
            if lastoperation:
                filelow = errordumpline["last operation"]
            else:
                filelow = errorline["line number"]-lookback
            filehigh = errorline["line number"]+lookforward
        # print(len(linefile))
        filelow = np.clip(filelow, 0, len(linefile)-lookforward)
        filehigh = np.clip(filehigh, 0, len(linefile))
        # print(filelow, filehigh)
        # logtext = "| Time | Line |\n| --- | --- |\n"
        logtimes = []
        while filelow < filehigh:
        # for line in linefile[filelow:filehigh]:
            if (any(n in linefile[filelow].decode(encoding="utf-8") for n in nonverbose)):

                if (verbose == False):
                    filelow = filelow + 1
                    filehigh = filehigh + 1
                    filehigh = np.clip(filehigh, 0, len(linefile))
                    continue
                else:
                    logtext = logtext + '\n' + markdown_logtext(linefile[filelow])

                    # markdown_logtext_list = markdown_logtext(linefile[filelow])
                    # logtext = logtext + '\n' + markdown_logtext_list[1]
                    # logtimes.append(markdown_logtext_list[0])

                    filelow = filelow + 1
            else:


                logtext = logtext + '\n' + markdown_logtext(linefile[filelow])

                # markdown_logtext_list = markdown_logtext(linefile[filelow])
                # logtext = logtext + '\n' + markdown_logtext_list[1]
                # logtimes.append(markdown_logtext_list[0])

                filelow = filelow + 1

        if (notfound):
            return ("WARNING: Error not found!")
        else:
            # print(logtext)
            tabs = list()
            # logtext = logtext.split('|')
            # print(logtext)
            logtext = logtext.split('\n')
            logtext = list(filter(('').__ne__, logtext))
            for pos, member in enumerate(logtext):
                # line = line.split("|")
                #
                # for member in line:
                    # print(member)
                # if ("COMMAND" in member) | ("OPERATION" in member):
                groups = groupby(member)
                result = [(label, sum(1 for _ in group)) for label, group in groups]
                # print(result)
                if (result[0][0] == "\t"):
                    tabs.insert(pos, result[0][1])
                else:
                    tabs.insert(pos, 0)
            # print(tabs)
            mintabs = min(list(filter((0).__ne__, tabs)))
            # print(mintabs)
            for pos, member in enumerate(tabs):
                if pos == 0:
                    tabs[pos] = 0
                    continue
                elif member == mintabs:
                    tabs[pos] = 0
                elif (member == 0):
                    tabs[pos] = tabs[pos - 1]
                elif ("COMMAND:" in logtext[pos]) & ("ExecuteOperation" not in logtext[pos]):
                    print(logtext[pos])
                    print(tabs[pos])
                    tabs[pos] = tabs[pos-1]
                else:
                    tabs[pos] = member - mintabs
            print(tabs)
            # print(len(tabs), len(logtext))
            for i in range(len(tabs)):
                logtext[i] = re.sub("[\t ]{2,}", "", logtext[i])
                tabchars = ""
                int = 0
                if tabs[i] == 0:
                    logtext[i] = """---\n
                    """ + logtext[i]
                    # logtimes[i] = """---\n
                    # """ + logtimes[i]
                    tabs[i]
                while int < tabs[i]:
                    tabchars = tabchars + "\t"
                    int = int + 1
                logtext[i] = tabchars + logtext[i] + "\n"
            # logtext[0] = """---\n
            # # """ + logtext[0]




            # print(tabs)
            # print(tabs[8], logtext[8])
            logtext = '\n'.join(logtext)
            # logtimes = '\n'.join(logtimes)
            # return logtimes, logtext
            return logtext
    #         return """Line\n
    #         >FirmwareVersionNumber: 8\n
    # > Counts | Voltage\n
    # > 2012\n
    #     > 2014 | 2.46\n
    # > 2028 | 2.48\n
    # > |\n
    # > |\n
    # > |\n
    # > |\n
    # >**** WAIT FOR LIQUID SENSOR - error: FailedToPrime *****
    # >RETURN FROM ERROR HANDLING, REJOIN STEP: Error: FailedToPrime
    # >ERROR OCCURRED: The PRIME pump did not successfully prime the liquid lines. The liquid sensor (LS1 for Main Wash, LS2 for Deprotection) did not turn on."""
