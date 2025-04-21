#!/usr/bin/env python3
#
# updated by ...: Loreto Notarantonio
# Date .........: 21-04-2025 08.52.16
#


import sys; sys.dont_write_bytecode = True
import os
# from datetime import datetime
from pathlib import Path
from benedict import benedict
# import shlex
# import re
# import csv
from types import SimpleNamespace


# from subprocessLN import scp_get #, run_sh_get_output, ssh_runCommand, scp_put
import lnUtils
import dictUtils
import ln_Excel_Class as lnExcel
# import openwrtUtils


sq="'"
dq='"'

def setup(gVars: (dict, SimpleNamespace)):
    global gv
    gv=gVars
    gv.logger.caller(__name__)
    gv.excelBook=None





###########################################
### read devices from excel file
###########################################
def readExcelSheet(excel_filename: str, sheet_name: str):
    if not gv.excelBook:
        gv.excelBook = lnExcel.lnExcelBook_Class(excel_filename=excel_filename, logger=gv.logger )

    return gv.excelBook.getSheet(sheet_name=sheet_name)







################################################################
# Configurazioe dei reservation addresss (config host)
################################################################
def processAgente(sheet_name: str, agente: str):
    data = sheet_name.selectRecords(col_name="AGENTE", evaluation_string=f' in ["{agente}"] ', use_benedict=False)
    d = dict()
    d[agente] = dict()
    ptr = d[agente]

    ### - creazione agente dictionary
    for key, value in data.items():
        contract_id = value.pop("SPEEDY_CTR_ID")
        value.pop("AGENTE")
        d[agente][contract_id] = value

    return benedict(d, keyattr_enabled=True, keyattr_dynamic=False)


################################################################
# Configurazioe dei reservation addresss (config host)
################################################################
def processFile(gVars: dict):
    excel_filename     = gv.args.excel_filename
    sheet_name         = gv.excel_config.sheet.name
    filtered_columns   = gv.excel_config.sheet.valid_columns
    dict_main_key      = gv.excel_config.sheet.dict_main_key

    ### --- get my contracts list
    sh_contratti = readExcelSheet(excel_filename=excel_filename, sheet_name="Contratti")
    d_contratti  = sh_contratti.asDict(dict_main_key=None, filtered_columns=filtered_columns, use_benedict=True)
    d_contratti.py()




    agent_name="Mirko Mazzoni"
    agente = processAgente(sheet_name=sh_contratti, agente=agent_name)
    agente.py()
    # import pdb; pdb.set_trace() # by Loreto
