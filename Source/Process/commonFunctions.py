#!/usr/bin/env python3
#
# updated by ...: Loreto Notarantonio
# Date .........: 04-05-2025 09.20.13
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
    # gv.excelBook=None
    # gv.tmpPath="/tmp/stefanoGirini"
    # Path(gv.tmpPath).mkdir(parents=True, exist_ok=True)







