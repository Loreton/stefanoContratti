#!/usr/bin/env python3
#
# updated by ...: Loreto Notarantonio
# Date .........: 04-05-2025 09.23.05
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


this=sys.modules[__name__]

import ln_pandasExcel_Class as lnExcel
import lnUtils
import dictUtils
from ln_pandasExcel_Class import workBbookClass, sheetClass
# import xlwt


def setup(gVars: (dict, SimpleNamespace)):
    global gv
    gv=gVars
    gv.logger.caller(__name__)
    # gv.excelBook=None





#################################################################
#
#################################################################
def prepareSheet(d: dict, level: int, sh_name: str):
    colonne_gerarchia   = gv.excel_config.output_sheet.colonne_gerarchia
    colonne_dati        = gv.excel_config.output_sheet.colonne_dati


    separator         = '#'

    ## catturiamo tutti i records fino al livello di agent creando dei keypath
    keypaths = dictUtils.chunckList(gv.flatten_keys, item_nrs=level, separator=separator)

    ### --- remove_empty_array items (columns_data)
    records = lnUtils.removeListOfListDuplicates(list_of_lists=keypaths, keep_order=True)

    import pdb; pdb.set_trace() # by Loreto



