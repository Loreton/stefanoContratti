#!/usr/bin/env python3

import sys; sys.dont_write_bytecode = True
import os

# from pathlib import Path
from benedict import benedict
# from datetime import datetime


# import LnUtils
# import dictUtils
# import File_csv



import pyexcel
import pyexcel_ods3 as ods3
import json



# from pyexcel_ods3 import get_data
###########################################################
#
###########################################################
def getSheetsNames(filename: str):
    book = pyexcel.get_book(file_name=filename)
    sheets = benedict(book.to_dict(), keyattr_enabled=True, keyattr_dynamic=False)
    for name in sheets.keys():
        print(name)

    for name, sheet in sheets.items(): # sheet is a list
        print(name, type(sheet), sheet)
        import pdb; pdb.set_trace();trace=True # by Loreto


###########################################################
#
###########################################################
def getBook(filename: str):
    book = pyexcel.get_book(file_name=filename)
    return book



###########################################################
#
###########################################################
def readSheet(filename: str, sheet_name: str, column_key: str, to_benedict=True):
    # ======================================
    def create_row_dict(row):
        d =dict()
        for col_nr in range(nCols):
            col_name = sheet[0][col_nr]
            d[col_name] = row[col_nr]
        return d
    # ======================================

    book = pyexcel.get_book(file_name=filename)
    sheets = book.to_dict()

    sheet_dict=dict()
    for name, sheet in sheets.items(): # sheet is a list
        if name == sheet_name:
            col_names = sheet[0]  # header row - columns names
            nCols = len(col_names)  # header row - columns names

            # ---- find the main key column
            for index, name in enumerate(col_names):
                if name == column_key:
                    main_key = index
                    break
            else:
                print(f"ERROR: column_key: [{column_key}] NOT found. first column [{col_names[0]}] will be assumed as main key")
                main_key = 0


            # ---- loop trough the sheet and create a dictionary
            for row in range(1, len(sheet)):
                row_name = sheet[row][main_key]  # get col as key_name
                if row_name in ["", "-"]:
                    print(f"[{sheet_name:20}] WARNING: skipping line_nr: [{row}]. key field [{column_key}] has a null value.")
                    continue
                if row_name in sheet_dict.keys():
                    print(f"[{sheet_name:20}] ERROR: key name: [{row_name}] already exists in sheet: [{name}]. It's duplicated key.")
                    sys.exit(1)

                line = sheet[row]
                sheet_dict[row_name] = create_row_dict(row=line)


    print(f"[{sheet_name:20}] valid rows: {len(sheet_dict)}")
    if to_benedict:
        sheet_dict=benedict(sheet_dict, keyattr_enabled=True, keyattr_dynamic=False)
        # print(sheet_dict.to_yaml())
    return sheet_dict





def exportExcelDB(filename: str):
    sheet_dict = readSheet(filename, "devices",             column_key="name")
    to_csv(sheet_dict,  filepath="/tmp/devices.csv")

    # sheet_dict = readSheet(filename, "tasmotaProperties",   column_key="device_name")
    # sheet_dict = readSheet(filename, "telegramBots",        column_key="bot_name")
    # sheet_dict = readSheet(filename, "mqttBrokers",         column_key="broker_name")
    # sheet_dict = readSheet(filename, "virtual_servers",     column_key="rule_name")



if __name__ == '__main__':
    filename = os.path.expandvars("${HOME}/lnProfile/devicesDB/devicesDB_D20241110.ods")
    filename = os.path.expandvars("${HOME}/lnProfile/devicesDB/DevicesV002/devicesDB.ods")
    # getSheetsNames(filename)
    sheet_dict = readSheet(filename, "devices",             column_key="name")
    sheet_dict = readSheet(filename, "tasmotaProperties",   column_key="device_name")
    sheet_dict = readSheet(filename, "telegramBots",        column_key="bot_name")
    sheet_dict = readSheet(filename, "mqttBrokers",         column_key="broker_name")
    sheet_dict = readSheet(filename, "virtual_servers",     column_key="rule_name")

    # sheet_dict=benedict(sheet_dict, keyattr_enabled=True, keyattr_dynamic=False)
