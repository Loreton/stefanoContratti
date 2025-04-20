#!/usr/bin/env python3
#
# updated by ...: Loreto Notarantonio
# Date .........: 20-04-2025 21.16.47
#


import sys; sys.dont_write_bytecode = True
import os
# from datetime import datetime
from pathlib import Path
from benedict import benedict
# import shlex
# import re
# import csv
from types import SimpleNamespace


# from subprocessLN import scp_get #, run_sh_get_output, ssh_runCommand, scp_put
import lnUtils
import dictUtils
import ln_Excel_Class as lnExcel
# import openwrtUtils


sq="'"
dq='"'

def setup(gVars: (dict, SimpleNamespace)):
    global gv
    gv=gVars
    gv.logger.caller(__name__)






###########################################
### read devices from excel file
###########################################
def readExcelSheet(filename: str, sheet_name: str, dict_main_key: str, filtered_columns: list=[]):
    excelBook = lnExcel.lnExcelBook_Class(excel_filename=filename, logger=gv.logger )
    sheet = excelBook.getSheet(sheet_name=sheet_name)
    # contratti = sheet.asList()
    # contratti = sheet.asDict(dict_main_key=dict_main_key, use_benedict=True)
    contratti = sheet.asDict(dict_main_key=None, filtered_columns=filtered_columns, use_benedict=True)
    return contratti






################################################################
# Configurazioe dei reservation addresss (config host)
################################################################
def processFile(gVars: dict):
    excel_filename     = gv.args.excel_filename
    sheet_name         = gv.excel_config.sheet.name
    filtered_columns   = gv.excel_config.sheet.valid_columns
    dict_main_key      = gv.excel_config.sheet.dict_main_key

#     ### --- retrieve remote file
#     new_openwrt_data, host_domain_dict=getRemoteData(remote_file, retrieved_file)

    # ### --- get my devices list
    contratti=readExcelSheet(filename=excel_filename, sheet_name=sheet_name, dict_main_key=dict_main_key, filtered_columns=filtered_columns)
    import pdb; pdb.set_trace() # by Loreto
#     ip_devices = devices.selectRecords(col_name="ip", evaluation_string=' not in ["null", "", "-"] ')

#     ### ----------------------------------
#     ### merging current retrieved file with new definitions
#     ### ----------------------------------
#     dictUtils.toYaml(d=host_domain_dict, filepath="/tmp/host_domain_dict_before_merge.yaml", indent=4, sort_keys=False, stacklevel=0, onEditor=False)
#     host_domain_dict=merge_data(target_data=host_domain_dict, new_rec=ip_devices)
#     dictUtils.toYaml(d=host_domain_dict, filepath="/tmp/host_domain_dict_after_merge.yaml", indent=4, sort_keys=False, stacklevel=0, onEditor=False)


#     ### ----------------------------------
#     ### convert dict to openwrt format
#     ### ----------------------------------
#     new_openwrt_data.extend(openwrtUtils.dictToSection(d=host_domain_dict["hosts"], section_type="host"))
#     new_openwrt_data.extend(openwrtUtils.dictToSection(d=host_domain_dict["domains"], section_type="domain"))
#     new_openwrt_data=lnUtils.remove_extra_blank_lines(data=new_openwrt_data)

#     ### ----------------------------------
#     ### write autogen file
#     ### ----------------------------------
#     lnUtils.dataToFile(filepath=autogen_file, data=new_openwrt_data, replace=True, onEditor=False)
#     if gv.args.editor:
#         os.system(f"/usr/bin/subl {retrieved_file} {autogen_file}")


#     TAB=" "*5

#     ### ----------------------------------
#     ### - create a list of hosts record (BLANK separator) for script
#     ### ----------------------------------
#     rec_type="host"

#     _format = "{:<30} {:<20} {:<20} {:<20} {:<10} {} "
#     fields = _format.format("<name>",  "<ip>",  "<mac>", "<leasetime>",  "<dns>", "<rec_tyoe>")
#     host_output=["# " + fields]
#     host_output.append("# " + "-"*100)
#     for key, record in host_domain_dict["hosts"].items():
#         if gv.openwrt_version == "22_03":
#             mac=record["mac"]
#             dns="1"
#         else:
#             mac=record["mac"][0]
#             dns=""

#         host_output.append(f"  {_format}".format(record["name"], record["ip"], mac, record["leasetime"], dns, rec_type))
#     lnUtils.dataToFile(data=host_output, filepath=gv.hosts_list, replace=True, write_datetime=True, onEditor=False)


#     rec_type="domain"
#     _format = "{:<30} {:<30} {} "
#     fields = _format.format("<name>",  "<ip>", "<rec_tyoe>")
#     domain_output=["# " + fields]
#     domain_output.append("# " + "-"*70)

#     for key, record in host_domain_dict["domains"].items():
#         domain_output.append(f"  {_format}".format(record["name"], record["ip"], rec_type))
#     lnUtils.dataToFile(data=domain_output, filepath=gv.domains_list, replace=True, write_datetime=True, onEditor=False)


