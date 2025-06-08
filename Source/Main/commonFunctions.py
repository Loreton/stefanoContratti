#!/usr/bin/env python3
#
# updated by ...: Loreto Notarantonio
# Date .........: 19-05-2025 20.18.39
#


import sys; sys.dont_write_bytecode = True
import os
from pathlib import Path
# from benedict import benedict
from types import SimpleNamespace
from enum import Enum
# import pandas as pd

# import  openpyxl
# from openpyxl import load_workbook
# from openpyxl.styles import PatternFill

# --- @Loreto: my lib
# import ln_pandasExcel_Class as lnExcel
# import lnUtils
# import dictUtils
# from ln_pandasExcel_Class import workBbookClass, sheetClass




def setup(gVars: (dict, SimpleNamespace)):
    global gv
    gv=gVars
    gv.logger.caller(__name__)





########### Excel function ----
def prepareTitleRow(index: int):
    # --- @Loreto: prepariamo il titolo
    title_row = gv.colonne_gerarchia[:index]
    title_row.append("Partner")
    for col in gv.dataCols:
        title_row.append(col.name)
    return title_row



def result_columns():
    # --- aggiungiamo le colonne contenenti i risultati di default (=0)
    default_result_cols = []
    for col in gv.dataCols:
        default_result_cols.append(0) ### - Valore di default
    return default_result_cols






def partnerData(agent_data: dict, partner_column: dict, somma: list):
    dc = gv.dataCols
    for partner, data in agent_data.items():
        if not partner in partner_column:
            partner_column[partner] = result_columns() ## skip partner name

        ptr = partner_column[partner]


        ptr[dc.PROCESSATI.value] += data[dc.PROCESSATI.name]
        ptr[dc.EXCLUDED.value] += data[dc.EXCLUDED.name]
        ptr[dc.INSERITI.value] += data[dc.INSERITI.name]
        ptr[dc.SCARTATI.value] += data[dc.SCARTATI.name]
        ptr[dc.TOTALE.value] += data[dc.TOTALE.name]
        ptr[dc.CONFERMATI.value] += data[dc.CONFERMATI.name]
        ptr[dc.ATTIVAZIONE.value] += data[dc.ATTIVAZIONE.name]
        ptr[dc.BACK.value] += data[dc.BACK.name]
        ptr[dc.RID.value] += data[dc.RID.name]
        ptr[dc.VAS.value] += data[dc.VAS.name]
        ptr[dc.SIM.value] += data[dc.SIM.name]
        ptr[dc.TV.value] += data[dc.TV.name]

        # rid:x=totale:100 --> x = rid*100/totale
        try:
            if  ptr[dc.RID.value] > 0 and ptr[dc.TOTALE.value] > 0:
                ptr[dc.RID_percent.value] = ptr[dc.RID.value] / ptr[dc.TOTALE.value]
            if  ptr[dc.VAS.value] > 0 and ptr[dc.TOTALE.value] > 0:
                ptr[dc.VAS_percent.value] = ptr[dc.VAS.value] / ptr[dc.TOTALE.value]
        except (Exception) as e:
            print(e)
            import pdb; pdb.set_trace() # by Loreto

        somma[dc.PROCESSATI.value] += data[dc.PROCESSATI.name]
        somma[dc.EXCLUDED.value] += data[dc.EXCLUDED.name]
        somma[dc.INSERITI.value] += data[dc.INSERITI.name]
        somma[dc.SCARTATI.value] += data[dc.SCARTATI.name]
        somma[dc.TOTALE.value] += data[dc.TOTALE.name]
        somma[dc.CONFERMATI.value] += data[dc.CONFERMATI.name]
        somma[dc.ATTIVAZIONE.value] += data[dc.ATTIVAZIONE.name]
        somma[dc.BACK.value] += data[dc.BACK.name]
        somma[dc.RID.value] += data[dc.RID.name]
        somma[dc.VAS.value] += data[dc.VAS.name]
        somma[dc.SIM.value] += data[dc.SIM.name]
        somma[dc.TV.value] += data[dc.TV.name]

        if  somma[dc.RID.value] > 0 and somma[dc.TOTALE.value] > 0:
            somma[dc.RID_percent.value] = somma[dc.RID.value] / somma[dc.TOTALE.value]
        if  somma[dc.VAS.value] > 0 and somma[dc.TOTALE.value] > 0:
            somma[dc.VAS_percent.value] = somma[dc.VAS.value] / somma[dc.TOTALE.value]


