#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -*- coding: iso-8859-1 -*-

# updated by ...: Loreto Notarantonio
# Date .........: 25-04-2025 18.07.17

import sys; sys.dont_write_bytecode=True
import os
from benedict import benedict
from pathlib import Path
import pandas as pd




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
import  FileLoader
import  processData



# -------------------------------
# ----- Load configuration data
# -------------------------------
def readConfig():
    global gv
    config_file=f"{prj_name}_config.yaml"

    unresolved_fileout=f"{gv.tmp_dir}/unresolved_full_config.yaml"
    if not (full_config:=FileLoader.loadConfigurationData(config_file=config_file, save_yaml_on_file=unresolved_fileout) ):
        logger.error("Configuration data error")

    gv.excel_config         = full_config.pop("excel") ### extrai la parte sqlite
    gv.struttura_aziendale  = full_config.pop("StrutturaAziendale") ### extrai la parte sqlite
    # gv.output_sheet         = full_config.pop("output_sheet") ### extrai la parte sqlite



#######################################################
#
#######################################################
if __name__ == '__main__':
    global gv

    prj_name = "stefanoG"

    # ----------------------------
    # ----- logging
    # ----------------------------
    __ln_version__=f"{prj_name} version: V2025-04-25_180717"
    args=ParseInput(__ln_version__)
    excelFilename = Path(os.path.expandvars(args.input_excel_filename))

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
        logger.error("file: %s doesn't exists", excelFilename)
        sys.exit(1)

    # ----------------------------
    # ----- prepare global project variables
    # ----------------------------
    gv=prepare_gVars.setMainVars(logger=logger, input_args=args, prj_name=prj_name, search_paths=["conf", "links_conf"])


    readConfig()

    processData.testExcel(gVars=gv)
    sys.exit()



    processData.processExcelFile(gVars=gv)

    sys.exit()

