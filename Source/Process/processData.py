#!/usr/bin/env python3
#
# updated by ...: Loreto Notarantonio
# Date .........: 26-04-2025 21.21.43
#


import sys; sys.dont_write_bytecode = True
import os
from pathlib import Path
from benedict import benedict
from types import SimpleNamespace
from enum import Enum
import pandas as pd

import ln_pandasExcel_Class as lnExcel


class COLS(Enum):
    Agente            = 1
    Partner           = 2
    Esito_totale      = 3
    Esito_completato  = 4
    Esito_attivazione = 5
    Esito_back        = 6

import lnUtils
import dictUtils
from ln_pandasExcel_Class import workBbookClass, sheetClass
# import xlwt

sq="'"
dq='"'

def setup(gVars: (dict, SimpleNamespace)):
    global gv
    gv=gVars
    gv.logger.caller(__name__)
    gv.excelBook=None
    gv.tmpPath="/tmp/stefanoG"
    Path(gv.tmpPath).mkdir(parents=True, exist_ok=True)



# ################################################################
# # array is list
# ################################################################
# def areAllItemEmpy(array: list):
#     x=0
#     # empty = [x+1 for ele in array if ele=='']
#     for ele in array:
#         if ele == '':
#             x += 1

#     if x==len(array):
#         # gv.logger.info("all string empty in list")
#         return True
#     return False


# ################################################################
# # array is list of list
# ################################################################
# def remove_empty_arrays(lol: list):
#     result = [row for row in lol if not all(a is '' for a in row)]

#     import pdb; pdb.set_trace() # by Loreto
#     _array = array[:]
#     for index, item in enumerate(reversed(array)):
#         if areAllItemEmpy(item):
#             del array[index]




###########################################
### read devices from excel file
### - portiamo la struttura in flatten
###########################################
def testExcel(gVars: dict):
    excel_filename        = gv.args.input_excel_filename
    agenti_excel_filename = gv.args.output_agenti_filename
    sheet_name            = gv.excel_config.source_sheet.name
    selected_columns      = gv.excel_config.source_sheet.columns_to_be_extracted
    colonne_gerarchia     = gv.excel_config.output_sheet.colonne_gerarchia
    colonne_dati          = gv.excel_config.output_sheet.colonne_dati

    if False:
        ### benedict flatten
        flat_data = gv.struttura_aziendale.flatten(separator="#")
        gv.logger.info("")
        index=0
        for k, v in flat_data.items():
            index+=1
            gv.logger.info(f"{index:04} - {k}: {v}")
        gv.logger.info("")

    if True:
        ### loreto flatten
        separator='#'

        ### dictionary flatten
        flatten_data = dictUtils.lnFlatten(gv.struttura_aziendale, separator=separator, index=True)
        for item in flatten_data:
            gv.logger.info(item)

        import pdb; pdb.set_trace() # by Loreto
        # flatten_data = dict(sorted(flatten_data.items()))

        ### prendi le colonne fino al TeamManager
        for i in range(0, len(colonne_gerarchia)):
            sheet_name=colonne_gerarchia[i]
            columns_data = dictUtils.flatten_keypaths_to_list(list(flatten_data.keys()), item_nrs=i+1, remove_enpty_array=True)
            for item in columns_data:
                gv.logger.info(item)
            gv.logger.info("")
            # import pdb; pdb.set_trace() # by Loreto
            # remove_empty_array items (columns_data)
            # result = [row for row in columns_data if not all(a is '' for a in row)]
            result=columns_data
            for item in result:
                gv.logger.info(item)
            gv.logger.info("")
            # index   = [ 'row 1', 'row 2'],     # row name se serve (index = True in to_excel())
            df = pd.DataFrame(
                    columns = colonne_gerarchia[:i+1],
                    data    = result
                )


            lnExcel.addSheets(filename=gv.args.output_agenti_filename, sheets=[sheet_name], dataFrames=[df], sheet_exists="replace", mode='a')
            lnExcel.setColumnSize(file_path=gv.args.output_agenti_filename, sheetname=sheet_name)

        import pdb; pdb.set_trace() # by Loreto

        # for k, v in flatten_data.items():
        #     index+=1
        #     cur_row=k.split(separator)
        #     for i, col in enumerate(cur_row):
        #         if col == prev_row[i]:
        #             cur_row[i]='\t\t'
        #     gv.logger.info(index, cur_row)
        #     prev_row = cur_row
            # for col in cur_row:
            #     gv.logger.info(index, '\t', col)



            # k_list=k.split(separator)

        import pdb; pdb.set_trace() # by Loreto
        gv.logger.info("")
        # import pdb; pdb.set_trace() # by Loreto

        ### cerchiamo di creare la truttura su excel
        prev_key=''
        work_key=''
        sep="#"
        for index, kp in enumerate(kpaths):
            work_key=kp
            if work_key.startswith(prev_key):
                work_key.replace(prev_key, ' ')
            gv.logger.info(f"{index:04} - {work_key}")

            prev_key=kp


    if False:
        kpaths = gv.struttura_aziendale.keypaths(indexes=False, sort=True)
        gv.logger.info("")
        index=0
        for kp in kpaths:
            index+=1
            gv.logger.info(f"{index:04} - {kp}")
        gv.logger.info("")


        ### cerchiamo di creare la truttura su excel
        prev_key=''
        work_key=''
        sep="#"
        for index, kp in enumerate(kpaths):
            work_key=kp
            if work_key.startswith(prev_key):
                work_key.replace(prev_key, ' ')
            gv.logger.info(f"{index:04} - {work_key}")

            prev_key=kp

    gv.logger.info("")

    import pdb; pdb.set_trace() # by Loreto


    gv.logger.info(flat_data)


    ### --- lettura sheet contratti da excel
    wb_contratti = workBbookClass(excel_filename=excel_filename, logger=gv.logger)
    sh_contratti = sheetClass(wbClass=wb_contratti, sheet_name_nr=0)
    dict_contratti = sh_contratti.asDict(usecols=selected_columns, use_benedict=True)
    dictUtils.toYaml(d=dict_contratti, filepath=f"{gv.tmpPath}/stefanoG.yaml", indent=4, sort_keys=False, stacklevel=0, onEditor=False)


    db_flat_data = dict_contratti.flatten(separator="#")
    gv.logger.info(db_flat_data)
    sys.exit(1)








################################################################
# Configurazioe dei reservation addresss (config host)
################################################################
def processAgente(d_src: dict, nome_agente: str):
    d = dict()

    ### - creazione agente dictionary
    for key, value in d_src.items():
        if value["AGENTE"] == nome_agente:
            contract_id = value.pop("SPEEDY_CTR_ID")
            # value.pop("AGENTE")
            d[contract_id] = value

    return benedict(d, keyattr_enabled=True, keyattr_dynamic=False)

################################################################
#    partners:
#        Eni:
#            totale:
#            confermati:
#            back:
#            attivazione:
#
################################################################
def partnerPerAgente(d_src: dict):
    # d = dict()
    d = benedict(keyattr_enabled=True, keyattr_dynamic=False)

    # ----------------------------------------
    # - valori di include/exclude
    # ----------------------------------------
    esiti               = gv.excel_config.esiti
    totale_include      = esiti.totale.include

    esiti_exclude       = []
    for value in esiti.exclude:
        esiti_exclude.append(value.lower().replace(' ', ''))

    confermato_include = []
    for value in esiti.confermato.include:
        confermato_include.append(value.lower().replace(' ', ''))

    attivazione_include = []
    for value in esiti.attivazione.include:
        attivazione_include.append(value.lower().replace(' ', ''))

    back_include = []
    for value in esiti.back.include:
        back_include.append(value.lower().replace(' ', ''))



    for key, value in d_src.items():
        partner  = value["PARTNER"]
        prodotto = value["PRODOTTO"]
        esito    = value["ESITO"]

        if not partner in d:
            d[partner] = benedict(keyattr_enabled=True, keyattr_dynamic=False)
            d[partner]["totale"] = 0
            d[partner]["confermato"] = 0
            d[partner]["attivazione"] = 0
            d[partner]["back"] = 0

        ptr=d[partner]

        ### - exclude unwante esito words
        gv.logger.info("processing esito: %s", esito)
        esito_trimmed = esito.lower().replace(' ', '')

        fExcluded = False
        for excl_value in esiti_exclude:
            if excl_value in esito_trimmed:
                fExcluded = True
                break

        if fExcluded:
            gv.logger.warning("excluding due to: %s", excl_value)
            continue

        if totale_include == "all":
            d[partner]["totale"] += 1

        ### - confermato
        fConfirmed = False
        for include_value in confermato_include:
            if include_value in esito_trimmed:
                d[partner]["confermato"] += 1
                fConfirmed = True
                break

        if fConfirmed:
            continue

        ### - attivazione
        fAttivazione = False
        for include_value in attivazione_include:
            if include_value in esito_trimmed:
                d[partner]["attivazione"] += 1
                fAttivazione = True
                break


        if fAttivazione:
            continue

        ### - attivazione
        fBack = False
        for include_value in back_include:
            if include_value in esito_trimmed:
                d[partner]["back"] += 1
                fBack = True
                break

        if fBack:
            continue


    return d


################################################################
# Configurazioe dei reservation addresss (config host)
################################################################
def processExcelFile(gVars: dict):
    excel_filename        = gv.args.input_excel_filename
    agenti_excel_filename = gv.args.output_agenti_filename
    sheet_name            = gv.excel_config.sheet.name
    selected_columns      = gv.excel_config.sheet.valid_columns
    # dict_main_key      = gv.excel_config.sheet.dict_main_key



    ### -------------------------------
    ### --- get my contracts list
    ### -------------------------------
    contratti_xls = lnExcel_Class(excel_filename=excel_filename, logger=gv.logger)
    d_contratti  = contratti_xls.getSheet(0, usecols=None, convert_to="dict")
    dictUtils.toYaml(d=d_contratti, filepath=f"{gv.tmpPath}/stefanoGG.yaml", indent=4, sort_keys=False, stacklevel=0, onEditor=False)
    import pdb; pdb.set_trace() # by Loreto





    ### -------------------------------------
    ### --- estrazione dati per ogni agente
    ### -------------------------------------
    ### --- lista agenti
    nomi_agenti = sh_contratti.columnValueList(col_name="AGENTE")
    gv.logger.info("nomi agenti: %s", nomi_agenti)

    agents = benedict(keyattr_enabled=True, keyattr_dynamic=False)
    d_excel_out = benedict(keyattr_enabled=True, keyattr_dynamic=False)

    for agent_name in nomi_agenti:
        gv.logger.info("processing agent: %s", agent_name)
        agents[agent_name] = processAgente(d_src=d_contratti, nome_agente=agent_name)
        gv.logger.info("    found records: %s ", len(agents[agent_name].keys()))

        ### save yaml to file
        yaml_filename = f"{gv.tmpPath}/{agent_name.replace(' ', '_')}.yaml"
        dictUtils.toYaml(d=agents[agent_name], title=agent_name, filepath=yaml_filename, indent=4, sort_keys=False, stacklevel=0, onEditor=False)

        agent_result = partnerPerAgente(d_src=agents[agent_name])
        # agent_result.py()


        # for key, value in agent_result.items():
        #     shAgentiAddLine(agent_name=agent_name, partner=key, data=value)
        # import pdb; pdb.set_trace() # by Loreto
        shAgentiAddLine(agent_name=agent_name, data=agent_result)

    # shAgentiAddLine(agent_name=agent_name, filename="/tmp/prova01.xls")
    shAgentiAddLine(agent_name=agent_name, filename=agenti_excel_filename)

