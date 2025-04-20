#!/usr/bin/env python3

import sys; sys.dont_write_bytecode = True
import os

from pathlib import Path
from benedict import benedict

## project modules
import  FileLoader
import  File_json
import  File_csv
import  File_yaml

import dictUtils
import copy


def setup(gVars):
    global gv
    gv=gVars
    gv.logger.caller(__name__)

###########################################################
#
###########################################################
def Main(gVars: dict, sqlite_config: dict, input_file: str, exit_on_duplicates=False):
    global gv
    gv=gVars

    # db_filepath=Path(sqlite_config.db_filepath)
    # table_name=sqlite_config.table_name

    # table_struct=sqlite_config.tables[table_name]

    # input_file = Path(sqlite_config.input_file)
    # file_suffix = input_file.suffix
    # fSublime=False



    input_file=Path(sqlite_config.source_dir) / "devices.csv"
    if not input_file.is_file():
        print(f"    Please enter one of the files [source dir: {sqlite_config.source_dir}]\n")
        os.system(f"ls  {sqlite_config.source_dir}")
        print()
        sys.exit(1)




    all_records = File_csv.load_csv(filepath=input_file, dict_pri_key="name")

    #---------------------------------------------
    #- check ip
    #---------------------------------------------
    gv.logger.info("-"*60)
    gv.logger.info("check duplicated ip")
    # gv.logger.info("-"*60)
    records = copy.deepcopy(all_records)
    keys = list(records.keys())
    # for name in keys:
    #     record=records[name]
    #     if "ip" in record and record.ip in ["null", '-']:
    #         gv.logger.debug("skipping record: %s  ip: %s", name, record.ip)
    #         records.pop(name)
    devices_sorted_by_ip = records.sort_by_key_name(sort_key_name="ip", check_duplicates=True, return_keylist=False, exit_on_duplicates=exit_on_duplicates)


    #---------------------------------------------
    #- check mac
    #---------------------------------------------
    gv.logger.info("-"*60)
    gv.logger.info("check duplicated mac")
    # gv.logger.info("-"*60)
    records = copy.deepcopy(all_records)
    keys = list(records.keys())
    # for name in keys:
    #     record=records[name]
    #     if "mac" in record and record.mac in ["null", '-']:
    #         gv.logger.debug("skipping record: %s  mac: %s", name, record.mac)
    #         records.pop(name)

    devices_sorted_by_mac = records.sort_by_key_name(sort_key_name="mac", check_duplicates=True, return_keylist=False, exit_on_duplicates=exit_on_duplicates)


