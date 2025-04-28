#!/usr/bin/env python3
#
# updated by ...: Loreto Notarantonio
# Date .........: 28-04-2025 20.41.58
#


import sys; sys.dont_write_bytecode = True
import os
from pathlib import Path
from benedict import benedict
from types import SimpleNamespace
from enum import Enum
import pandas as pd


# --- @Loreto: my lib
import ln_pandasExcel_Class as lnExcel
import lnUtils
import dictUtils
from ln_pandasExcel_Class import workBbookClass, sheetClass
import processAgent
import sheetAgent


class COLS(Enum):
    Direttore         = 1
    AreaManager       = 2
    ManagerPlus       = 3
    Manager           = 4
    TeamManager       = 5
    Agente            = 6
    Partner           = 7
    Esito_totale      = 8
    Esito_completato  = 9
    Esito_attivazione = 10
    Esito_back        = 11


def setup(gVars: (dict, SimpleNamespace)):
    global gv
    gv=gVars
    gv.logger.caller(__name__)
    gv.excelBook=None
    gv.tmpPath="/tmp/stefanoGirini"
    Path(gv.tmpPath).mkdir(parents=True, exist_ok=True)

    # sheetAgent.sheetAgent.setup(gVars=gv)
    processAgent.setup(gVars=gv)




#################################################################
#
#################################################################
def sheetAgent(d: dict):
    colonne_gerarchia = gv.excel_config.output_sheet.colonne_gerarchia
    colonne_dati      = gv.excel_config.output_sheet.colonne_dati

    sh_index          = COLS.Agente.value
    sh_name           = COLS.Agente.name
    separator         = '#'
    flatten_data      = dictUtils.lnFlatten(gv.struttura_aziendale, separator = separator, index = True)
    flatten_keys      = list(flatten_data.keys())

    ## catturiamo tutti i records fino al livello di agent creando dei keypath
    keypaths = dictUtils.chunckList(flatten_keys, item_nrs=sh_index, separator=separator)

    ### --- remove_empty_array items (columns_data)
    records = lnUtils.removeListOfListDuplicates(list_of_lists=keypaths, keep_order=True)



    ### --- find row where director changes in modo da inserire una riga di separazione
    ### --- da sviluppare
    # row_separator = [index for index, row in enumerate(sheet_rows) if all(a != '-' for a in row)]
    ### ---


    # --- @Loreto: prepariamo il titolo
    default_result_cols = [""]
    title_row = colonne_gerarchia[:sh_index]
    inx=0
    for col_name in colonne_dati:
        title_row.append(col_name)
        if inx > 0:
            default_result_cols.append(0) ### - Valore di default
        inx+=1



    # --- @Loreto: riempiamo le colonne dati con il valori agente
    sheet_rows = []
    for index in range(len(records)):
        row=records[index]
        agent_data = d[row]
        if agent_data:
            new_row=processAgent.calculateResults(agent_data=agent_data, row=row)
            # print(new_row)
            sheet_rows.extend(new_row)
        else:
            new_row=row[:]
            new_row.extend(default_result_cols)
            sheet_rows.append(new_row)
    # ---

    # --- @Loreto:  eliminiamo le celle che hanno valore == cella superire
    rows_data = dictUtils.compact_list(data=sheet_rows, max_items=sh_index, replace_str='-')
    # for i, item in enumerate(rows_data): gv.logger.info("%s . %s", i, item)

    ### - creiamo il dataFrame
    df = pd.DataFrame(
            # columns = colonne_gerarchia[:inx+1],
            columns = title_row,
            data    = rows_data
        )


    lnExcel.addSheet(filename=gv.args.output_agenti_filename, sheets=[sh_name], dataFrames=[df], sheet_exists="replace", mode='a')
    lnExcel.setColumnSize(file_path=gv.args.output_agenti_filename, sheetname=sh_name)


    import pdb; pdb.set_trace() # by Loreto
    ...







################################################################
# Configurazioe dei reservation addresss (config host)
################################################################
def Main(gVars: dict):
    excel_filename        = gv.args.input_excel_filename
    agenti_excel_filename = gv.args.output_agenti_filename
    sheet_name            = gv.excel_config.source_sheet.name
    selected_columns      = gv.excel_config.source_sheet.columns_to_be_extracted



    ### -------------------------------
    ### --- read contracts data
    ### -------------------------------
    gv.workBook  = workBbookClass(excel_filename=excel_filename, logger=gv.logger)
    sh_contratti = sheetClass(wbClass=gv.workBook, sheet_name_nr=0)
    dict_contratti = sh_contratti.asDict(usecols=selected_columns, use_benedict=True)
    dictUtils.toYaml(d=dict_contratti, filepath=f"{gv.tmpPath}/stefanoG.yaml", indent=4, sort_keys=False, stacklevel=0, onEditor=False)



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
    ### --- inseriamo gli agenti nella struttura globale
    ### --- gli agenti inseriti verranno rimossi dagli agenti trovati
    ### --- in modo che se avanzano segnaliamo l'incongruenza
    ### -------------------------------------
    processAgent.insertAgentInStruct(main_dict=gv.struttura_aziendale, agents=agents)
    if len(agents):
        gv.logger.warning("I seguenti agenti sono presenti nel foglio contratti, na non nella struttura")
        for name in agents.keys():
            gv.logger.warning(" - %s", name)


    flatten_data = dictUtils.lnFlatten(gv.struttura_aziendale, separator='#', index=True)
    for item in flatten_data: gv.logger.debug(item)


    sheetAgent(d=gv.struttura_aziendale)


    # --- prepare Excel structure
    # createStructForExcel(agents=agent)

