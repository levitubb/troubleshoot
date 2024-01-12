from zipfile import ZipFile
import pandas as pd
import numpy as np
from datetime import datetime
import re
from itertools import groupby

DEFAULT_LOG_INFO = {"instrument": "", "serial": "", "version": "", "date_updated": "Never"}

def find_levels(zip_name):
    """
    Scans the contents of the provided zip file to identify and categorize different levels and folders.

    Args:
        zip_name (str): The name of the zip file.

    Returns:
        dict: Information about the structure of the log files.
    """
    levels = {"log_folder": "Logs/"}
    levels_found = False
    levels_df= pd.DataFrame()
    with ZipFile(zip_name) as zip:
        folders = zip.namelist()

        for line in folders:
            if not levels_found:
                if line.endswith('Logs/'):
                    levels["log_folder"] = line
                    levels_found = True
                else:
                    levels["log_folder"] = "Logs/"

            line_series = pd.Series(line.split('/'))
            levels_df = pd.concat([levels_df, line_series], axis=1, ignore_index=1).replace('', np.nan)

    passby = 0
    for iter in range(1, levels_df.shape[0]):
        name = "level" + str(iter)
        level_list = levels_df.iloc[iter - 1, :].drop_duplicates().replace('', np.nan).dropna().tolist()

        levels[name] = level_list

    found_logs = False
    for item in levels:
        for member in levels[item]:
            if member == 'Logs':
                months_folder = "level" + str(int(item[5]) + 1)
                errors_folder = "level" + str(int(item[5]) + 2)
                found_logs = True
                break

    levels["months_folder"] = months_folder
    levels["errors_folder"] = errors_folder
    levels[levels["months_folder"]].sort(key=lambda date: datetime.strptime(date, "%Y-%m"))

    if "Logs" not in levels["log_folder"]:
        print("Logs folder is missing or invalid zip file, try loading the TB again")

    return levels

def process_log(zip_name, levels):
    """
    Analyzes log entries from a specific month in the zip file.

    Args:
        zip_name (str): The name of the zip file.
        levels (dict): Information about the structure of the log files.

    Returns:
        dict: Updated log information.
    """
    log_info = DEFAULT_LOG_INFO.copy()

    with ZipFile(zip_name) as zip:
        for month_folder in levels[levels["months_folder"]]:
            path = levels["log_folder"] + month_folder + "/Log.txt"

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
                                        log_info["date_updated"] = datetime.fromisoformat(message[0][0:23])

                if "Liberty instrument Connected" in decoded_line:
                    message = decoded_line.split('|')
                    for desc in message:
                        if "Liberty instrument Connected" in desc:
                            message_items = desc.split(' ')
                            for term in message_items:
                                if term.startswith('Serial'):
                                    temp_serial = term.split(":")[1].strip()
                                    if temp_serial == "LB0002":
                                        continue
                                    elif temp_serial == log_info["serial"]:
                                        continue
                                    elif log_info["serial"] == "":
                                        log_info["serial"] = temp_serial
                                    else:
                                        log_info["serial2"] = temp_serial
                                        print("WARNING: multiple serial numbers")

    return log_info

def extract_error_log(zip_name, levels, serial):
    """
    Extracts error log information from the zip file.

    Args:
        zip_name (str): The name of the zip file.
        levels (dict): Information about the structure of the log files.
        serial (str): The serial number.

    Returns:
        pd.DataFrame: DataFrame containing error information.
    """
    errors_df = pd.DataFrame()

    if 'Errors.txt' not in levels[levels["errors_folder"]]:
        print("WARNING: No error log found")
        errors_df = "No Error Log Found"
    else:
        for month_folder in levels[levels["months_folder"]]:
            path = levels["log_folder"] + month_folder + "/Errors.txt"
            with ZipFile(zip_name) as zip:
                try:
                    zip.open(path)
                except:
                    continue

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
                            errors_df = pd.concat([errors_df, pd.Series([message[0], message[3]])], ignore_index=1, axis=1)

        errors_df = errors_df.transpose()
        errors_df["serial"] = serial
        errors_df.columns = ['Timestamp', "Description", "Serial"]

    return errors_df

def errorcontext(zipname, levels, errors, idx, lookback=200, lookforward=5, lastoperation=False, filterflag=False,
                  filtertext=["ProgressBar", "SKIP ROTARY MOVE COMMAND", "IfThenGoto", "UVReadAndRecordUVAbsorbance"], timestamps=False):
    """
    Extracts contextual log information around the specified error index from the zip file.

    Args:
        zipname (str): The name of the zip file.
        levels (dict): Information about the structure of the log files.
        errors (pd.DataFrame): DataFrame containing error information.
        idx (int): Index of the error in the DataFrame.
        lookback (int): Number of lines to look back from the error.
        lookforward (int): Number of lines to look forward from the error.
        lastoperation (bool): Flag to indicate whether to consider the last operation.
        filterflag (bool): Flag to enable filtering log entries based on specific text.
        filtertext (list): List of text patterns for filtering log entries.
        timestamps (bool): Flag to include timestamps in the output.

    Returns:
        str: Contextual log information around the specified error.
    """
    # logtext = "WHATTT??"
    logtext = ""
    errortime = datetime.fromisoformat(errors.iloc[idx, 0][0:23])

    year = str(errortime.year)
    if len(str(errortime.month)) < 2:
        month = "0" + str(errortime.month)
    else:
        month = str(errortime.month)
    errorfolder = year + "-" + month

    path = levels["log_folder"] + errorfolder + "/Run/Run"
    with ZipFile(zipname) as zip:
        df = pd.DataFrame(
            [(zinfo.filename, datetime(*zinfo.date_time), zinfo.file_size) for zinfo in zip.filelist],
            columns=["filename", "date_time", "file_size"],
        )

        runlogfiles = df[df.filename.str.contains(path)]
        errorfile = runlogfiles[runlogfiles.date_time >= errortime].sort_values(by="date_time").iloc[0, 0]

        notfound = True
        errorline = {"timestamp": datetime(1990, 1, 1), "line number": 0}
        errordumpline = {"timestamp": datetime(1990, 1, 1), "line number": 0, "last operation": 0}
        searchfiles = [errorfile, path + "Detail_0.txt"]

        for item in searchfiles:
            linefile = zip.open(item).readlines()
            searchedpath = item
            for pos, line in enumerate(linefile):
                try:
                    decoded_line = line.decode(encoding="utf-8")
                    if "|" not in decoded_line:
                        continue
                    else:
                        timestamp = datetime.fromisoformat(decoded_line.split("|")[0][0:23])
                        if "FirmwareVersionNumber:" in decoded_line:
                            errordumpline["timestamp"] = timestamp
                            errordumpline["line number"] = pos
                            errordumpline["verbose count"] = 0
                        elif "OPERATION:" in decoded_line:
                            errordumpline["last operation"] = pos
                        elif (((timestamp - errortime).seconds) < 1) & (((timestamp - errortime).days) >= 0):
                            print("SEARCHED ERROR:", re.sub("[\t ]{2,}", " ", decoded_line))
                            errorline["timestamp"] = timestamp
                            errorline["line number"] = pos
                            notfound = False
                            break

                except:
                    continue

            if notfound == False:
                break

        if (
            (errorline["line number"] > 0)
            & ((errorline["line number"] - errordumpline["line number"]) > 0)
            & (((errorline["timestamp"] - errordumpline["timestamp"]).seconds) < 5)
        ):
            if lastoperation:
                filelow = errordumpline["last operation"]
            else:
                filelow = errorline["line number"] - lookback
            filehigh = errorline["line number"] + 1
        else:
            if lastoperation:
                filelow = errordumpline["last operation"]
            else:
                filelow = errorline["line number"] - lookback
            filehigh = errorline["line number"] + lookforward

        filelow = np.clip(filelow, 0, len(linefile) - lookforward)
        filehigh = np.clip(filehigh, 0, len(linefile))

        logtimes = []
        while filelow < filehigh:
            try:
                decoded_line = linefile[filelow].decode(encoding="utf-8")
                if any(n in decoded_line for n in filtertext):
                    if filterflag:
                        filelow = filelow + 1
                        filehigh = filehigh + 1
                        filehigh = np.clip(filehigh, 0, len(linefile))
                        continue
                    else:
                        logtime, linetext = markdown_logtext(linefile[filelow])
                        logtext = logtext + '\n' + linetext
                        logtimes.append(logtime)

                        filelow = filelow + 1
                else:
                    logtime, linetext = markdown_logtext(linefile[filelow])
                    logtext = logtext + '\n' + linetext
                    logtimes.append(logtime)
                    filelow = filelow + 1
            except:
                filelow = filelow + 1
                continue
            print("WHATTT??",logtext)

        if notfound:
            return "WARNING: Error not found!"
        else:
            tabs = list()
            logtext = logtext.split('\n')
            logtext = list(filter(('').__ne__, logtext))

            for pos, member in enumerate(logtext):
                groups = groupby(member)
                result = [(label, sum(1 for _ in group)) for label, group in groups]
                if result[0][0] == "\t":
                    tabs.insert(pos, result[0][1])
                else:
                    tabs.insert(pos, 0)

            try:
                mintabs = min(list(filter((0).__ne__, tabs)))
            except:
                mintabs = 0

            for pos, member in enumerate(tabs):
                if pos == 0:
                    tabs[pos] = 0
                elif member == mintabs:
                    tabs[pos] = 0
                elif ((member - tabs[pos - 1]) > 0) & (("ExecuteOperation" in logtext[pos - 1]) | ("OPERATION:" in logtext[pos - 1])):
                    tabs[pos] = tabs[pos - 1] + 1

                elif (member != 0) & ((member - tabs[pos - 1]) < 0):
                    tabs[pos] = tabs[pos - 1] - 1
                elif (member != 0):
                    tabs[pos] = tabs[pos - 1]
                elif (member == 0):
                    tabs[pos] = tabs[pos - 1]

            tabsarray = np.array(tabs)
            B = np.split(tabsarray, np.where(tabsarray[:] == 0)[0][1:])
            tabslength = 0

            maxtabs = 12
            done = False
            while not done:
                for pos, array in enumerate(B):
                    if any(n > maxtabs for n in array):
                        B[pos] = array[array <= maxtabs]
                        B.insert(pos + 1, array[array > maxtabs] - maxtabs - 1)
                        continue
                    done = True

            for pos, array in enumerate(B):
                tabslength = len(B[pos]) + tabslength
                nonzeroarray = array[array > 0]
                if len(nonzeroarray) > 1:
                    if "OPERATION:" in logtext[tabslength - len(B[pos])]:
                        minmember = min(nonzeroarray) - 1
                    else:
                        minmember = min(nonzeroarray)

            tabs = np.hstack(B)

            for i in range(1, len(tabs)):
                logtext[i] = re.sub("[\t ]{2,}", "", logtext[i])
                if logtext[i].startswith("\t"):
                    logtext[i] = logtext[i][1:]

                tabchars = ""
                int = 0
                if (tabs[i] == 0) & (tabs[i - 1] > 0):
                    logtext[i] = """---\n""" + logtext[i]
                else:
                    if timestamps:
                        logtext[i] = """    """ + logtimes[i] + "  " + logtext[i]
                    else:
                        logtext[i] = """    """ + logtext[i]

                while int < tabs[i]:
                    tabchars = tabchars + "\t"
                    int = int + 1
                logtext[i] = tabchars + logtext[i]

            if timestamps:
                logtext[0] = """\n""" + logtimes[0] + re.sub("[\t ]{2,}", " ", logtext[0])
            else:
                logtext[0] = """\n""" + logtext[0]

            logtext[0] = "Searching File: " + str(searchedpath) + """  \n  """ + logtext[0]

            logtext = '\n'.join(logtext)

            return logtext


if __name__ == "__main__":
    # Example usage of the functions
    zip_file_name = "example.zip"
    log_levels = find_levels(zip_file_name)
    log_information = process_log(zip_file_name, log_levels)
    error_data = extract_error_log(zip_file_name, log_levels, log_information["serial"])
    # ... (additional processing or reporting)
