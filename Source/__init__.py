#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -*- coding: iso-8859-1 -*-

# updated by ...: Loreto Notarantonio
# Date .........: 08-06-2025 20.08.02




import sys; sys.dont_write_bytecode=True
import os
from pathlib import Path

import Source.preMain.zipLnLib as ZIP


# -------------------------
# - Load syspath with custom modules paths in modo
# - da poter richiamare facilmente i moduli con il solo nome
# - anche con il progetto zipped
# -------------------------
_my_path=[]

def set_path():

    no_lnlib_zip=False
    if "--nolnlibzip" in sys.argv:
        sys.argv.remove("--nolnlibzip")
        no_lnlib_zip=True


    script_name=Path(sys.argv[0]).resolve()

    if script_name.suffix == '.zip': # sono all'interno dello zip
        _my_path.append(script_name.parent.parent)
        prj_dir=script_name # ... nome dello zip_file
        lnLib_zip = f"{prj_dir}/Source/LnLib.zip"
        _my_path.extend(ZIP.extractZip(script_name)) # extract lnLib.zip from project.zip file and get its path
    else:
        prj_dir=script_name.parent # nome della prj directory
        _my_path.append(script_name.parent)

        ### creiamo lnLib.zip per avere i moduli aggiornati al momento

        import socket
        hostname = socket.gethostname()
        if hostname.lower() in ["asusp2520l"]:
            lnLib_zip = f"{prj_dir}/Source/LnLib.zip"
            ZIP.zip_dir_with_extensions(source_dir=f'{prj_dir}/Source/lnLib_links', zip_filename=lnLib_zip, extensions=['.py'] )
            print(lnLib_zip, "has been created")

    _my_path.append(prj_dir)
    _my_path.append(f'{prj_dir}/Source')
    _my_path.append(f'{prj_dir}/Source/preMain')
    _my_path.append(f'{prj_dir}/Source/Main')
    if no_lnlib_zip:
        _my_path.append(f'{prj_dir}/Source/lnLib_links') ## non dovrebbe servire perché ci appoggiamo alla lnLib.zip
    else:
        _my_path.append(f'{prj_dir}/Source/LnLib.zip')



    for path in _my_path:
        # print(str(path))
        sys.path.insert(0, str(path))

if not _my_path: set_path()

