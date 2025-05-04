#!/usr/bin/env python3
#
# updated by ...: Loreto Notarantonio
# Date .........: 04-05-2025 08.50.09
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






def somma_livello(d, livello_attuale=1, livello_target=6):
    if livello_attuale == livello_target:
        # Se siamo al livello target, sommiamo i valori (che devono essere numeri)
        return sum(v for v in d.values() if isinstance(v, (int, float)))

    # Se non siamo ancora al livello target, ricorriamo nei sotto-dizionari
    somma = 0
    for k, v in d.items():
        if isinstance(v, dict):
            risultato = somma_livello(d=v, livello_attuale=livello_attuale+1, livello_target=livello_target)
            somma += risultato
            # Memorizziamo la somma nel dizionario corrente, se serve
            d[k]['_somma'] = risultato
    return somma







