#!/usr/bin/env python3
#
# updated by ...: Loreto Notarantonio
# Date .........: 02-05-2025 16.08.07
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







#################################################################
#
#################################################################
def createSheet(d: dict, calculateAgentResultsCB):
    colonne_gerarchia   = gv.excel_config.output_sheet.colonne_gerarchia
    colonne_dati        = gv.excel_config.output_sheet.colonne_dati

    sh_index          = gv.COLS.TeamManager.value
    sh_name           = gv.COLS.TeamManager.name

    separator         = '#'

    ## catturiamo tutti i records fino al livello di agent creando dei keypath
    keypaths = dictUtils.chunckList(gv.flatten_keys, item_nrs=sh_index, separator=separator)

    ### --- remove_empty_array items (columns_data)
    records = lnUtils.removeListOfListDuplicates(list_of_lists=keypaths, keep_order=True)




    # --- aggiungiamo le colonne contenenti i risultati di default (=0)
    default_result_cols = [""]
    # --- @Loreto: prepariamo il titolo
    title_row = colonne_gerarchia[:sh_index]
    inx=0
    for col_name in colonne_dati:
        title_row.append(col_name)
        if inx > 0:
            default_result_cols.append(0) ### - Valore di default
        inx+=1



    # -------------------------------------------------------------------------------------
    # --- @Loreto: riempiamo le colonne dati con il valori agente
    #--- creiamo un dictionary con key=partner
    # --- {
    # ---   "edison": [0,0,0,0,0], somma dei vaori dei singoli agenti
    # ---   "....":   [0,0,0,0,0]
    # ---   }
    # --- con questi dati andrò a creare delle righe sotto il Team Manager
    # -------------------------------------------------------------------------------------
    sheet_rows = []

    for index in range(len(records)):
        tm_somma=default_result_cols[1:] ### conterrà la somma dei vari partner
        partner_col_data = gv.myDict()
        row=records[index]
        gv.logger.info("analysing data for teamManager %s:", row[-1])
        agent_list = d[row] ### - lista degli agenti sotto questo teamManager

        for agent_name in agent_list:
            gv.logger.info("    agent: %s", agent_name)
            if agent_data:=gv.agent_results.get(agent_name): # se presente....
                ### --- calcoliamo i valori
                for partner, data in agent_data.items():
                    if not partner in partner_col_data:
                        partner_col_data[partner] = default_result_cols[1:] ## skip partner name
                        # partner_col_data[partner][0] = partner

                    ptr = partner_col_data[partner]
                    ptr[0] += data["totale"]
                    ptr[1] += data["confermato"]
                    ptr[2] += data["attivazione"]
                    ptr[3] += data["back"]
                    ptr[4] += data["rid"]

                    ### --- aggiorniamo il totale
                    tm_somma[0] += data["totale"]
                    tm_somma[1] += data["confermato"]
                    tm_somma[2] += data["attivazione"]
                    tm_somma[3] += data["back"]
                    tm_somma[4] += data["rid"]

                ### --- fine partner
            ### --- fine agent


        ### --- riga con i totali per teamManager
        new_row = row[:]
        new_row.append('')
        new_row.extend(tm_somma)
        sheet_rows.append(new_row)

        if partner_col_data:
            for partner, data in partner_col_data.items():
                gv.logger.notify("    agent data has been found")
                new_row = row[:]
                new_row.append(partner)
                new_row.extend(data)
                sheet_rows.append(new_row)
        else:
            gv.logger.warning("    NO agent data found")
            new_row=row[:]
            new_row.extend(default_result_cols)
            sheet_rows.append(new_row)


    # --- @Loreto:  eliminiamo le celle che hanno valore == cella superire
    rows_data = dictUtils.compact_list(data=sheet_rows, max_items=sh_index, replace_str='-')

    ### - creiamo il dataFrame
    df = gv.myDict()
    df = pd.DataFrame(
            # columns = colonne_gerarchia[:inx+1],
            columns = title_row,
            data    = rows_data
        )


    lnExcel.addSheet(filename=gv.args.output_agenti_filename, sheets=[sh_name], dataFrames=[df], sheet_exists="replace", mode='a')
    lnExcel.setColumnSize(file_path=gv.args.output_agenti_filename, sheetname=sh_name)




