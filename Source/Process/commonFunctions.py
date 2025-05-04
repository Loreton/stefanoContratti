#!/usr/bin/env python3
#
# updated by ...: Loreto Notarantonio
# Date .........: 04-05-2025 20.07.04
#


import sys; sys.dont_write_bytecode = True
import os
from pathlib import Path
from benedict import benedict
from types import SimpleNamespace
from enum import Enum
import pandas as pd

import  openpyxl
from openpyxl import load_workbook
from openpyxl.styles import PatternFill

# --- @Loreto: my lib
import ln_pandasExcel_Class as lnExcel
import lnUtils
import dictUtils
from ln_pandasExcel_Class import workBbookClass, sheetClass



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
    # gv.excelBook=None
    # gv.tmpPath="/tmp/stefanoGirini"
    # Path(gv.tmpPath).mkdir(parents=True, exist_ok=True)



########### Excel function ----
def prepareTitleRow(index: int):
    # --- @Loreto: prepariamo il titolo
    title_row = gv.colonne_gerarchia[:index]
    for col_name in gv.colonne_dati:
        title_row.append(col_name)
    return title_row



def result_columns():
    # --- aggiungiamo le colonne contenenti i risultati di default (=0)
    default_result_cols = []
    for col_name in gv.colonne_dati:
        default_result_cols.append(0) ### - Valore di default
    default_result_cols[0] = "" ### replace with blank value
    return default_result_cols



def setTitle(ws):
    gray = 'b2b2b2'
    # formatting the header columns, filling red color
    for col in range(1, ws.max_column + 1):
       cell_header = ws.cell(1, col)
       cell_header.fill = PatternFill(start_color=gray, end_color=gray, fill_type="solid") #used hex code for red color


def setColumnSize(ws):
    # Auto-adjust column widths
    for col in ws.columns:
        max_length = 0
        column = col[0].column_letter  # Get the column name (e.g., 'A')
        for cell in col:
            try:
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))
            except:
                pass
        adjusted_width = (max_length + 2)
        ws.column_dimensions[column].width = adjusted_width



############################################################
# cell_range = [ (row1, col1), (row2, col2), ...]
############################################################
def setCellsColor(ws, cells: list, color='ffffa6'):
    # light_yellow_3 = 'ffffa6'
    # my_color = light_yellow_3

    for row, col in cells:
        curr_cell = ws.cell(row, col)
        curr_cell.fill = PatternFill(start_color=color, end_color=color, fill_type="solid") #used hex code for red color





def processAgentList(agent_list: list, partner_column: dict, somma: list):
    for agent_name in agent_list:
        gv.logger.info("    agent: %s", agent_name)
        if agent_data:=gv.agent_results.get(agent_name): # se presente....
            ### --- calcoliamo i valori
            for partner, data in agent_data.items():
                if not partner in partner_column:
                    partner_column[partner] = gv.default_result_cols[1:] ## skip partner name
                    # partner_col_data[partner][0] = partner

                ptr = partner_column[partner]
                ptr[0] += data["totale"]
                ptr[1] += data["confermato"]
                ptr[2] += data["attivazione"]
                ptr[3] += data["back"]
                ptr[4] += data["rid"]

                ### --- aggiorniamo il totale
                somma[0] += data["totale"]
                somma[1] += data["confermato"]
                somma[2] += data["attivazione"]
                somma[3] += data["back"]
                somma[4] += data["rid"]

