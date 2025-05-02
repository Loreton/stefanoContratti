#!/usr/bin/env python3
#
# updated by ...: Loreto Notarantonio
# Date .........: 02-05-2025 09.21.55
#


import sys; sys.dont_write_bytecode = True
import os
from pathlib import Path
from benedict import benedict
from types import SimpleNamespace

import pandas as pd


# --- @Loreto: my lib
import ln_pandasExcel_Class as lnExcel
import lnUtils
import dictUtils
from ln_pandasExcel_Class import workBbookClass, sheetClass
import processAgent
import sheetAgent
import sheetTeamManager



def setup(gVars: (dict, SimpleNamespace)):
    global gv
    gv=gVars
    gv.logger.caller(__name__)
    gv.excelBook=None
    gv.tmpPath="/tmp/stefanoGirini"
    Path(gv.tmpPath).mkdir(parents=True, exist_ok=True)

    # sheetAgent.sheetAgent.setup(gVars=gv)
    processAgent.setup(gVars=gv)









#########################################################
# per ogni partner crea un riga
# ritorna list of list
# nella prima riga mettiamo i totali_agente dei vari partner
#########################################################
def calculateAgentResults(agent_data: dict, row: list) -> list:
    new_rows = []
    sunto_agente = row[:]
    totali = 0
    confermati = 0
    attivazione = 0
    back = 0
    rid = 0
    for partner_name in agent_data:
        new_row=row[:]
        ptr=agent_data[partner_name]
        data_cols=[partner_name,
                    ptr["totale"],
                    ptr["confermato"],
                    ptr["attivazione"],
                    ptr["back"],
                    ptr["rid"],
                ]
        totali      += ptr["totale"]
        confermati  += ptr["confermato"]
        attivazione += ptr["attivazione"]
        back        += ptr["back"]
        rid         += ptr["rid"]

        new_row.extend(data_cols)
        new_rows.append(new_row)
    sunto_agente.extend(["", totali, confermati, attivazione, back, rid])
    new_rows.insert(0, sunto_agente)
    return new_rows






################################################################
# Configurazioe dei reservation addresss (config host)
################################################################
def Main(gVars: dict):
    excel_filename             = gv.args.input_excel_filename
    agenti_excel_filename      = gv.args.output_agenti_filename
    sheet_name                 = gv.excel_config.source_sheet.name
    selected_columns           = gv.excel_config.source_sheet.columns_to_be_extracted
    file_agents_data           = gv.working_files.file_agents_data
    file_agents_results        = gv.working_files.file_agents_results
    file_contratti_preprocess  = gv.working_files.file_contratti_preprocess
    file_agenti_discrepanti   = gv.working_files.file_agenti_discrepanti

    ### -------------------------------
    ### --- read contracts data
    ### -------------------------------
    gv.workBook  = workBbookClass(excel_filename=excel_filename, logger=gv.logger)
    sh_contratti = sheetClass(wbClass=gv.workBook, sheet_name_nr=0)
    dict_contratti = sh_contratti.asDict(usecols=selected_columns, use_benedict=True)
    dictUtils.toYaml(d=dict_contratti, filepath=file_contratti_preprocess, indent=4, sort_keys=False, stacklevel=0, onEditor=False)


    ### -------------------------------------
    ### --- estrazione dati agenti dal foglio contratti
    ### -------------------------------------
    nomi_agenti = sh_contratti.readColumn(col_name="AGENTE", unique=True)
    gv.logger.info("nomi agenti: %s", nomi_agenti)


    ### -------------------------------------
    ### --- processiamo i contratti per ogni agente
    ### -------------------------------------
    agents = processAgent.retrieveContracts(contract_dict=dict_contratti, lista_agenti=nomi_agenti )

    ### -------------------------------------
    ### --- creazione due dict (che salviamo su yaml file)
    ### --- per eventuale verifica di un corretto calcolo
    ### --- gv.agents_results sarà utile per il calcolo ai livelli superiori.
    ### -------------------------------------
    d_data = gv.myDict()
    gv.agent_results = gv.myDict()
    for name in agents:
        d_data[name]=agents[name]["data"]
        gv.agent_results[name]=agents[name]["results"]

    dictUtils.toYaml(d=d_data, filepath=file_agents_data, indent=4, sort_keys=False, stacklevel=0, onEditor=False)
    dictUtils.toYaml(d=gv.agent_results, filepath=file_agents_results, indent=4, sort_keys=False, stacklevel=0, onEditor=False)

    ### -------------------------------------
    ### --- inseriamo gli agenti nella struttura globale
    ### --- gli agenti inseriti verranno rimossi dagli agenti trovati
    ### --- in modo che se avanzano segnaliamo l'incongruenza
    ### -------------------------------------
    processAgent.insertAgentInStruct(main_dict=gv.struttura_aziendale, agents=agents)
    if len(agents):
        gv.logger.warning("I seguenti agenti sono presenti nel foglio contratti, na non nella struttura")
        for name in agents.keys():
            gv.logger.warning(" - %s", name)
        dictUtils.toYaml(d=agents, filepath=file_agenti_discrepanti, indent=4, sort_keys=False, stacklevel=0, onEditor=False)


    ### -------------------------------------
    ### --- creiamo il flatten del mainDict
    ### -------------------------------------
    gv.flatten_data = dictUtils.lnFlatten(gv.struttura_aziendale, separator='#', index=True)
    gv.flatten_keys = list(gv.flatten_data.keys())
    for item in gv.flatten_data: gv.logger.debug(item)


    # sheetAgent.createSheet(d=gv.struttura_aziendale, calculateAgentResultsCB=calculateAgentResults)
    sheetTeamManager.createSheet(d=gv.struttura_aziendale, calculateAgentResultsCB=calculateAgentResults)


