#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -*- coding: iso-8859-1 -*-

# updated by ...: Loreto Notarantonio
# Date .........: 09-06-2025 08.05.14

import sys; sys.dont_write_bytecode=True
import os
from benedict import benedict
from pathlib import Path
# import pandas as pd
from enum import Enum



#=======================================
# - Project modules
#=======================================
project_log_levels={
    "notset":   0,
    "trace":    5,
    "debug":    10,
    "caller":   17,
    "function": 18,
    "notify":   19,
    "info":     20,
    "warning":  30,
    "error":    40,
    "critical": 50,
}

# os.environ['Loader_modules']="csv ini yaml json"
import  Source
from    ColoredLogger import setColoredLogger, testLogger

from    ParseInput import ParseInput
import  prepare_gVars
import  mainProcess
import  FileLoader

class dataCols(Enum):
    PROCESSATI     = 0
    EXCLUDED       = 1
    INSERITI       = 2
    SCARTATI       = 3
    TOTALE         = 4
    CONFERMATI     = 5
    ATTIVAZIONE    = 6
    BACK           = 7
    RID            = 8
    RID_percent    = 9
    VAS            = 10
    VAS_percent    = 11
    SIM            = 12
    TV             = 13

class HIERARCHY(Enum):
    Direttore         = 1
    AreaManager       = 2
    ManagerPlus       = 3
    Manager           = 4
    TeamManager       = 5
    Agente            = 6




# def isAgentInContract(ag: str):
#     from itertools import permutations
#     # lista = [1, 2, 3, 4]
#     lista=["Franco Cosimino", "Giuliano Yabandeh Jahromi", "Luigi Amato Euroma2 Pm"]
#     if ag in lista:
#         return True

#     tk = ag.split()
#     combinazioni = list(permutations(tk, len(tk)))
#     for item in combinazioni:
#         name=' '.join(item)
#         if name in lista:
#             print(name)


    # print(combinaziqoni)


    # for i in range(len(tk)):
    #     name = tk[i:] + tk[0]


    '''
    import itertools

    lista = ['a', 'b', 'c', 'd']

    # Tutte le combinazioni di lunghezza 1 a 4
    tutte_combinazioni = []
    for r in range(1, len(lista)+1):
        tutte_combinazioni.extend(itertools.combinations(lista, r))

    for c in tutte_combinazioni:
        print(c)
    '''


    # _list=["Franco Cosimino", "Giuliano Yabandeh Jahromi", "Luigi Amato Euroma2 Pm"]


# -------------------------------
# ----- Load configuration data
# -------------------------------
def readConfig():
    global gv
    gv.exit_on_config_file_not_found = True
    config_file=f"{prj_name}_config.yaml"

    unresolved_fileout=f"{gv.tmp_dir}/full_config.yaml"
    if not (full_config:=FileLoader.loadConfigurationData(config_file=config_file, save_yaml_on_file=unresolved_fileout, set_system_variables=False) ):
        logger.error("Configuration data error")
        sys.exit(1)

    gv.excel_config         = full_config.pop("excel") ### extrai la parte sqlite
    gv.struttura_aziendale  = full_config.pop("StrutturaAziendale") ### extrai la parte sqlite
    gv.working_files        = full_config.pop("working_files") ### extrai la parte sqlite
    # gv.COLS = COLS
    gv.HIERARCHY = HIERARCHY
    gv.dataCols   = dataCols
    # gv.output_sheet         = full_config.pop("output_sheet") ### extrai la parte sqlite


#######################################################
#
#######################################################
if __name__ == '__main__':
    global gv

    # isAgentInContract("Loreto notarantonio")
    # isAgentInContract("Luigi Amato Pm Euroma2")
    # sys.exit()
    prj_name = "stefanoContratti"

    # ----------------------------
    # ----- logging
    # ----------------------------
    __ln_version__=f"{prj_name} version: V2025-06-09_080514"
    args=ParseInput(__ln_version__)
    excelFilename = Path(os.path.expandvars(args.excel_input_filename))

    logger=setColoredLogger(logger_name=prj_name,
                            console_logger_level=args.log_console_level,
                            file_logger_level="critical",
                            logging_dir=None, # no filehandler
                            threads=False,
                            create_logging_dir=False,
                            prj_log_levels=project_log_levels)


    testLogger(logger)

    logger.info('------- Starting -----------')
    logger.warning(__ln_version__)

    if not excelFilename.exists():
        logger.warning("file: %s doesn't exists", excelFilename)
        #sys.exit(1)

    # ----------------------------
    # ----- prepare global project variables
    # ----------------------------
    gv=prepare_gVars.setMainVars(logger=logger, input_args=args, prj_name=prj_name, search_paths=["conf", "links_conf"])


    readConfig()

    # mainProcess.testExcel(gVars=gv)
    # sys.exit()



    mainProcess.Main(gVars=gv)

    sys.exit()

