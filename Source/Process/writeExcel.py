#!/usr/bin/env python3
#
# updated by ...: Loreto Notarantonio
# Date .........: 21-04-2025 19.03.09
#


import sys; sys.dont_write_bytecode = True
import os
# from datetime import datetime
# from pathlib import Path
# from benedict import benedict


# Import workbook to write data from xlwt
# from xlwt import Workbook
import xlwt


def addLine(data, sheet_name):


def writeExcel(data, filename, sheet_name):
    # Create an object of the workbook
    excel = xlwt.Workbook()

    # Add sheet in workbook
    sheet = excel.add_sheet(sheet_name)

    for row, value in enumerate(data):
        sheet.write(row, 0, value["name"])
        sheet.write(row, 1, value["age"])
        sheet.write(row, 2, value["country"])

    # Now save the excel
    excel.save(filename)



if __name__ == '__main__':

    writeExcel(data=my_data, filename="/tmp/my_excel.xls", sheet_name="laura")