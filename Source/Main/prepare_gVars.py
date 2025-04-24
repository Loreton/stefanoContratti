#!/usr/bin/env python3

#===============================================
# updated by ...: Loreto Notarantonio
# Date .........: 24-04-2025 15.33.28
#===============================================

import sys; sys.dont_write_bytecode=True
import os

from    datetime import datetime, timedelta
import platform
import socket
from pathlib import Path
from benedict import benedict


def setMainVars(logger, prj_name, input_args, type: str=None, search_paths: list=["conf"]):
    global gv



    gv=benedict(keyattr_enabled = True, keyattr_dynamic = False) # copy all input args to gv

    # gv=gVars
    # ----- basic variables
    gv.logger               = logger
    gv.args                 = vars(input_args)
    gv.OpSys: str           = platform.system()
    gv.prj_name: str        = prj_name
    gv.search_paths: list   = search_paths
    gv.date_time: str       = datetime.now().strftime("%Y%m%d_%H%M")
    gv.YYMMDD: str          = datetime.now().strftime("%Y%m%d")
    gv.time: str            = datetime.now().strftime("%H%M%S")
    gv.HHMMSS: str          = datetime.now().strftime("%H%M%S")
    gv.HHMM: str            = datetime.now().strftime("%H%M")
    gv.date:      str       = datetime.now().strftime("%Y%m%d")
    gv.now: str             = datetime.now().strftime("%d-%m-%Y_%H:%M")
    gv.script_path          = Path(sys.argv[0]).resolve()
    gv.tmp_dir              = f"/tmp/{prj_name}"
    gv.hostname             = socket.gethostname().split()[0]

    gv.dry_run              =  not gv.args.go
    gv.run_env              =  "prod" if gv.args.go else "dry_run"
    gv.fExecute             =  gv.args.go


    # - set env variables
    os.environ['DATE_TIME'] = gv.date_time
    os.environ['DATE']      = gv.date
    os.environ['TIME']      = gv.time
    os.environ['HHMM']      = gv.HHMM
    os.environ['HOST_NAME'] = gv.hostname

    import FileLoader;       FileLoader.setup(gVars=gv)
    import lnUtils;          lnUtils.setup(gVars=gv)
    import subprocessLN;     subprocessLN.setup(gVars=gv)
    import dictUtils;        dictUtils.setup(gVars=gv)
    # import checkDuplicates;  checkDuplicates.setup(gVars=gv)
    # import ln_Excel_Class;   ln_Excel_Class.setup(gVars=gv)
    # import openwrtUtils;     openwrtUtils.setup(gVars=gv)
    import processData;     processData.setup(gVars=gv)


    return gv




def setExtraVars():
    return
