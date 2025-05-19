#!/usr/bin/env python3
#
# updated by ...: Loreto Notarantonio
# Date .........: 19-05-2025 17.00.40
#


import sys; sys.dont_write_bytecode = True
import os
from pathlib import Path
from benedict import benedict
from types import SimpleNamespace
from enum import Enum
# import pandas as pd

# import  openpyxl
# from openpyxl import load_workbook
# from openpyxl.styles import PatternFill
# from pprint import pprint as pp

this=sys.modules[__name__]

# import ln_pandasExcel_Class as lnExcel
import lnUtils
import dictUtils
# from ln_pandasExcel_Class import workBbookClass, sheetClass
import commonFunctions


def setup(gVars: (dict, SimpleNamespace)):
    global gv
    gv=gVars
    gv.logger.caller(__name__)






#################################################################
#
#################################################################
def processAgentList(agent_list: list, partner_column: dict, somma: list):
    for agent_name in agent_list:
        gv.logger.info("    agent: %s", agent_name)
        if agent_data:=gv.agent_results.get(agent_name): # se presente....
            commonFunctions.partnerData(agent_data=agent_data, partner_column=partner_column, somma=somma)
        else:
            pass
            # import pdb; pdb.set_trace() # by Loreto




#################################################################
#
#################################################################
# def create(d: dict, level: int, sh_name: str):
def create(d: dict, hierarchy_level):
    level = hierarchy_level.value
    sh_name = hierarchy_level.name

    ## catturiamo tutti i records fino al livello di agent creando dei keypath
    keypaths = dictUtils.chunckList(gv.keypaths_list, item_nrs=level)

    ### --- remove duplicate entries
    hier_keypaths = lnUtils.removeListOfListDuplicates(list_of_lists=keypaths, keep_order=True)


    ### --- create title row
    title_row = commonFunctions.prepareTitleRow(index=level)


    # -------------------------------------------------------------------------------------
    # --- creazione delle colonne da partenr in poi (con i dati dei contratti)
    #--- creiamo un dictionary con key=partner
    # --- {
    # ---   "edison": [0,0,0,0,0], somma dei vaori dei singoli agenti
    # ---   "....":   [0,0,0,0,0]
    # ---   }
    # --- con questi dati andrò a creare delle righe sotto il Team Manager
    # -------------------------------------------------------------------------------------
    sheet_rows = [] # righe del foglio excel
    row_to_be_colored = [] # da evidenziare
    target_level = gv.HIERARCHY.Agente.value - (level+1)

    for index in range(len(hier_keypaths)):
        partner_col_data = gv.myDict()

        tm_somma=commonFunctions.result_columns() ### conterrà la somma dei vari partner

        this_level_kp=hier_keypaths[index] ## riga corrente

        manager_name=this_level_kp[-1]
        gv.logger.info("analysing data for %s %s:", sh_name, manager_name)

        if d_data := d[this_level_kp]:
            if target_level < 0: ### siamo a livello di Agente. non dobbiamo raggrupparli
                commonFunctions.partnerData(agent_data=d_data, partner_column=partner_col_data, somma=tm_somma)
            else:
                agent_list = dictUtils.get_keys_at_level(d_data, target_level=target_level, current_level=0)
                gv.logger.info("analysing data for Agents: %s:", agent_list)

                ### --- aggiunge tutte le rige dei partner sommati per i relativi agenti
                this.processAgentList(agent_list=agent_list, partner_column=partner_col_data, somma=tm_somma)

            new_row = this_level_kp[:]

            ### --- riga con i totali per teamManager
            new_row.append('Summary')
            new_row.extend(tm_somma)
            sheet_rows.append(new_row)
            row_to_be_colored.append(len(sheet_rows)+1) ### aggiungere il titolo

            if partner_col_data:
                for partner, data in partner_col_data.items():
                    gv.logger.debug("    agent data has been found")
                    new_row = this_level_kp[:]
                    new_row.append(partner)
                    new_row.extend(data)
                    sheet_rows.append(new_row)
            else:
                gv.logger.debug("NO agent data found")


    # --- @Loreto:  eliminiamo le celle che hanno valore == cella superire
    rows_data = dictUtils.compact_list(data=sheet_rows, max_items=level, replace_str='-')
    gv.peWorkBook.addSheet(sheet_name=sh_name, col_names=title_row, data_rows=rows_data, replace=True)



    ### --- crea il range di celle da colorare
    cell_range=[]
    for col in range(level, len(title_row)+1):
        row_cells = [(row, col) for row in row_to_be_colored]
        cell_range.extend(row_cells)

    gv.COLOR_CELLS.append(cell_range)
    gv.SHEETS.append(sh_name)





#######################################################################
#
#######################################################################
def agentiNonTrovati(agents: list):
    ### - creiamo il dataFrame
    sh_name = "Unsresolved_Agents"
    title_row = ["Agents_not_present_in_Structure"]
    rows_data = []
    for agent_name in list(agents.keys()):
        rows_data.append([agent_name])

    gv.peWorkBook.addSheet(sheet_name=sh_name, col_names=title_row, data_rows=rows_data, replace=True)

    # gv.DF.append(df)
    gv.SHEETS.append(sh_name)
    gv.COLOR_CELLS.append(None)
