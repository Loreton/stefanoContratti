#!/usr/bin/env python3
#
# updated by ...: Loreto Notarantonio
# Date .........: 22-04-2025 19.40.07
#


import sys; sys.dont_write_bytecode = True
import os
from pathlib import Path
from benedict import benedict
from types import SimpleNamespace
from enum import Enum

class COLS(Enum):
    Agente            = 1
    Partner           = 2
    Esito_totale      = 3
    Esito_completato  = 4
    Esito_attivazione = 5
    Esito_back        = 6

# from subprocessLN import scp_get #, run_sh_get_output, ssh_runCommand, scp_put
import lnUtils
import dictUtils
# import ln_Excel_Class as lnExcel
from lnPandasExcel_Class import lnExcel_Class
import xlwt

sq="'"
dq='"'

def setup(gVars: (dict, SimpleNamespace)):
    global gv
    gv=gVars
    gv.logger.caller(__name__)
    gv.excelBook=None
    gv.tmpPath="/tmp/stefanoG"
    Path(gv.tmpPath).mkdir(parents=True, exist_ok=True)




# Add sheet in workbook
excelOutput = xlwt.Workbook()
sh_agenti = excelOutput.add_sheet("Agenti")
sh_agenti_rows = 0



#########################################################
#       sample of data
#            Edison:
#                totale: 38
#                confermato: 10
#                attivazione: 0
#                back: 1
#            Edison Business:
#                totale: 2
#                confermato: 0
#                attivazione: 0
#                back: 0
#########################################################
def shAgentiAddLine(agent_name, data: dict={}, filename: str=None):
    global sh_agenti_rows, sh_agenti, excelOutput

    # Now save the excel
    if filename:
        excelOutput.save(filename)
        return

    if sh_agenti_rows==0:
        sh_agenti.write(sh_agenti_rows , COLS.Agente.value            , COLS.Agente.name)
        sh_agenti.write(sh_agenti_rows , COLS.Partner.value           , COLS.Partner.name)
        sh_agenti.write(sh_agenti_rows , COLS.Esito_totale.value      , COLS.Esito_totale.name)
        sh_agenti.write(sh_agenti_rows , COLS.Esito_completato.value  , COLS.Esito_completato.name)
        sh_agenti.write(sh_agenti_rows , COLS.Esito_attivazione.value , COLS.Esito_attivazione.name)
        sh_agenti.write(sh_agenti_rows , COLS.Esito_back.value        , COLS.Esito_back.name)
        sh_agenti_rows += 1

    for partner, esiti in data.items():
        sh_agenti_rows += 1
        sh_agenti.write(sh_agenti_rows , COLS.Agente.value            , agent_name)
        sh_agenti.write(sh_agenti_rows , COLS.Partner.value           , partner)
        sh_agenti.write(sh_agenti_rows , COLS.Esito_totale.value      , esiti["totale"])
        sh_agenti.write(sh_agenti_rows , COLS.Esito_completato.value  , esiti["confermato"])
        sh_agenti.write(sh_agenti_rows , COLS.Esito_attivazione.value , esiti["attivazione"])
        sh_agenti.write(sh_agenti_rows , COLS.Esito_back.value        , esiti["back"])







def writeExcel(data, filename, sheet_name):
    # Create an object of the workbook

    for row, value in enumerate(data):
        sheet.write(row, 0, value["name"])
        sheet.write(row, 1, value["age"])
        sheet.write(row, 2, value["country"])

    # Now save the excel
    excel.save(filename)






###########################################
### read devices from excel file
###########################################
# def readExcelSheet(excel_filename: str, sheet_name: str):
#     if not gv.excelBook:
#         gv.excelBook = lnExcel.lnExcelBook_Class(excel_filename=excel_filename, logger=gv.logger )

#     return gv.excelBook.getSheet(sheet_name=sheet_name)







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
#    partners:
#        Eni:
#            totale:
#            confermati:
#            back:
#            attivazione:
#
################################################################
def partnerPerAgente(d_src: dict):
    # d = dict()
    d = benedict(keyattr_enabled=True, keyattr_dynamic=False)

    # ----------------------------------------
    # - valori di include/exclude
    # ----------------------------------------
    esiti               = gv.excel_config.esiti
    totale_include      = esiti.totale.include

    esiti_exclude       = []
    for value in esiti.exclude:
        esiti_exclude.append(value.lower().replace(' ', ''))

    confermato_include = []
    for value in esiti.confermato.include:
        confermato_include.append(value.lower().replace(' ', ''))

    attivazione_include = []
    for value in esiti.attivazione.include:
        attivazione_include.append(value.lower().replace(' ', ''))

    back_include = []
    for value in esiti.back.include:
        back_include.append(value.lower().replace(' ', ''))



    for key, value in d_src.items():
        partner  = value["PARTNER"]
        prodotto = value["PRODOTTO"]
        esito    = value["ESITO"]

        if not partner in d:
            d[partner] = benedict(keyattr_enabled=True, keyattr_dynamic=False)
            d[partner]["totale"] = 0
            d[partner]["confermato"] = 0
            d[partner]["attivazione"] = 0
            d[partner]["back"] = 0

        ptr=d[partner]

        ### - exclude unwante esito words
        gv.logger.info("processing esito: %s", esito)
        esito_trimmed = esito.lower().replace(' ', '')

        fExcluded = False
        for excl_value in esiti_exclude:
            if excl_value in esito_trimmed:
                fExcluded = True
                break

        if fExcluded:
            gv.logger.warning("excluding due to: %s", excl_value)
            continue

        if totale_include == "all":
            d[partner]["totale"] += 1

        ### - confermato
        fConfirmed = False
        for include_value in confermato_include:
            if include_value in esito_trimmed:
                d[partner]["confermato"] += 1
                fConfirmed = True
                break

        if fConfirmed:
            continue

        ### - attivazione
        fAttivazione = False
        for include_value in attivazione_include:
            if include_value in esito_trimmed:
                d[partner]["attivazione"] += 1
                fAttivazione = True
                break


        if fAttivazione:
            continue

        ### - attivazione
        fBack = False
        for include_value in back_include:
            if include_value in esito_trimmed:
                d[partner]["back"] += 1
                fBack = True
                break

        if fBack:
            continue


    return d


################################################################
# Configurazioe dei reservation addresss (config host)
################################################################
def processExcelFile(gVars: dict):
    excel_filename        = gv.args.input_excel_filename
    agenti_excel_filename = gv.args.output_agenti_filename
    sheet_name            = gv.excel_config.sheet.name
    filtered_columns      = gv.excel_config.sheet.valid_columns
    # dict_main_key      = gv.excel_config.sheet.dict_main_key



    ### -------------------------------
    ### --- get my contracts list
    ### -------------------------------
    contratti_xls = lnExcel_Class(excel_filename=excel_filename, logger=gv.logger)
    d_contratti  = contratti_xls.getSheet(0, usecols=None, convert_to="dict")
    dictUtils.toYaml(d=d_contratti, filepath=f"{gv.tmpPath}/stefanoGG.yaml", indent=4, sort_keys=False, stacklevel=0, onEditor=False)
    import pdb; pdb.set_trace() # by Loreto





    ### -------------------------------------
    ### --- estrazione dati per ogni agente
    ### -------------------------------------
    ### --- lista agenti
    nomi_agenti = sh_contratti.columnValueList(col_name="AGENTE")
    gv.logger.info("nomi agenti: %s", nomi_agenti)

    agents = benedict(keyattr_enabled=True, keyattr_dynamic=False)
    d_excel_out = benedict(keyattr_enabled=True, keyattr_dynamic=False)

    for agent_name in nomi_agenti:
        gv.logger.info("processing agent: %s", agent_name)
        agents[agent_name] = processAgente(d_src=d_contratti, nome_agente=agent_name)
        gv.logger.info("    found records: %s ", len(agents[agent_name].keys()))

        ### save yaml to file
        yaml_filename = f"{gv.tmpPath}/{agent_name.replace(' ', '_')}.yaml"
        dictUtils.toYaml(d=agents[agent_name], title=agent_name, filepath=yaml_filename, indent=4, sort_keys=False, stacklevel=0, onEditor=False)

        agent_result = partnerPerAgente(d_src=agents[agent_name])
        # agent_result.py()


        # for key, value in agent_result.items():
        #     shAgentiAddLine(agent_name=agent_name, partner=key, data=value)
        # import pdb; pdb.set_trace() # by Loreto
        shAgentiAddLine(agent_name=agent_name, data=agent_result)

    # shAgentiAddLine(agent_name=agent_name, filename="/tmp/prova01.xls")
    shAgentiAddLine(agent_name=agent_name, filename=agenti_excel_filename)

