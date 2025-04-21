#!/usr/bin/env python3
#
# updated by ...: Loreto Notarantonio
# Date .........: 21-04-2025 09.18.50
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
    gv.tmpPath="/tmp/stefanoGG"
    Path(gv.tmpPath).mkdir(parents=True, exist_ok=True)





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
def processAgente1(sheet_name: str, nome_agente: str):
    data = sheet_name.selectRecords(col_name="AGENTE", evaluation_string=f' in ["{nome_agente}"] ', use_benedict=False)
    d = dict()

    ### - creazione agente dictionary
    for key, value in data.items():
        contract_id = value.pop("SPEEDY_CTR_ID")
        # value.pop("AGENTE")
        d[contract_id] = value

    return benedict(d, keyattr_enabled=True, keyattr_dynamic=False)



################################################################
# Configurazioe dei reservation addresss (config host)
################################################################
def processAgente(d_src: dict, nome_agente: str):
    d = dict()

    ### - creazione agente dictionary
    for key, value in d_src.items():
        if value["AGENTE"] == nome_agente:
            contract_id = value.pop("SPEEDY_CTR_ID")
            # value.pop("AGENTE")
            d[contract_id] = value

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
    # d_contratti.py()
    dictUtils.toYaml(d=d_contratti, filepath=f"{gv.tmpPath}/stefanoGG.yaml", indent=4, sort_keys=False, stacklevel=0, onEditor=False)





    nomi_agenti = ["Mirko Mazzoni", "Emanuela Luciano"]
    agents = benedict(keyattr_enabled=True, keyattr_dynamic=False)

    for agent_name in nomi_agenti:
        gv.logger.info("processing agent: %s", agent_name)
        agents[agent_name] = processAgente(d_src=d_contratti, nome_agente=agent_name)
        gv.logger.info("    found records: %s ", len(agents[agent_name].keys()))

        ### save yaml to file
        yaml_filename = f"{gv.tmpPath}/{agent_name.replace(' ', '_')}.yaml"
        dictUtils.toYaml(d=agents[agent_name], title=agent_name, filepath=yaml_filename, indent=4, sort_keys=False, stacklevel=0, onEditor=False)

