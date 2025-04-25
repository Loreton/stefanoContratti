#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -*- coding: iso-8859-1 -*-

# updated by ...: Loreto Notarantonio
# Date .........: 25-04-2025 16.39.18




import sys; sys.dont_write_bytecode=True
import os
from pathlib import Path

import Source.Main.zipLnLib as ZIP


# -------------------------
# - Load syspath with custom modules paths in modo
# - da poter richiamare facilmente i moduli con il solo nome
# - anche con il progetto zipped
# -------------------------
_my_path=[]
def set_path():
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
        lnLib_zip = f"{prj_dir}/Source/LnLib.zip"
        ZIP.zip_dir_with_extensions(source_dir=f'{prj_dir}/Source/lnLib_links', zip_filename=lnLib_zip, extensions=['.py'] )
        print(lnLib_zip, "has been created")

    _my_path.append(prj_dir)
    _my_path.append(f'{prj_dir}/Source')
    _my_path.append(f'{prj_dir}/Source/Main')
    # _my_path.append(f'{prj_dir}/Source/Modules')
    _my_path.append(f'{prj_dir}/Source/Process')
    # _my_path.append(f'{prj_dir}/Source/lnLib') ## non dovrebbe servire perché ci appoggiamo alla lnLib.zip
    _my_path.append(f'{prj_dir}/Source/LnLib.zip')



    for path in _my_path:
        # print(str(path))
        sys.path.insert(0, str(path))

if not _my_path: set_path()

