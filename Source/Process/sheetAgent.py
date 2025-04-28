#!/usr/bin/env python3
#
# updated by ...: Loreto Notarantonio
# Date .........: 28-04-2025 20.27.20
#


import sys; sys.dont_write_bytecode = True
import os
from pathlib import Path
from benedict import benedict
from types import SimpleNamespace
from enum import Enum
import pandas as pd

import ln_pandasExcel_Class as lnExcel


import lnUtils
import dictUtils
from ln_pandasExcel_Class import workBbookClass, sheetClass
# import xlwt

sq="'"
dq='"'

def setup(gVars: (dict, SimpleNamespace)):
    global gv
    gv=gVars
    gv.logger.caller(__name__)
    gv.excelBook=None
    gv.tmpPath="/tmp/stefanoGirini"
    Path(gv.tmpPath).mkdir(parents=True, exist_ok=True)






#################################################################
#
#################################################################
def sheetAgent(d: dict):
    colonne_gerarchia = gv.excel_config.output_sheet.colonne_gerarchia
    colonne_dati      = gv.excel_config.output_sheet.colonne_dati

    sh_index          = COLS.Agente.value
    sh_name           = COLS.Agente.name
    # sheet_name        = colonne_gerarchia[sheet_index]
    separator         = '#'
    flatten_data      = dictUtils.lnFlatten(gv.struttura_aziendale, separator = separator, index = True)
    flatten_keys      = list(flatten_data.keys())

    ## catturiamo tutti i records fino al livello di agent creando dei keypath
    keypaths = dictUtils.chunckList(flatten_keys, item_nrs=sh_index, separator=separator)
    records = lnUtils.removeListOfListDuplicates(list_of_lists=keypaths, keep_order=True)

    df = myDict()

    ### --- remove_empty_array items (columns_data)
    # sheet_rows = [row for row in rows_data if not all(a == '-' for a in row)]
    # for item in sheet_rows: gv.logger.debug(item)
    ### ---

    ### --- find row where director changes in modo da inserire una riga di separazione
    ### --- da sviluppare
    # row_separator = [index for index, row in enumerate(sheet_rows) if all(a != '-' for a in row)]
    ### ---


    # --- aggiungiamo le colonne contenenti i risultati di default (=0)
    # default_result_cols = []
    default_result_cols = [""]
    # --- @Loreto: prepariamo il titolo
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
            new_row=AGENT.calculateAgentResults(agent_data=agent_data, row=row)
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


