#!/usr/bin/env python3
#
# updated by ...: Loreto Notarantonio
# Date .........: 28-04-2025 10.47.59
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
    gv.tmpPath="/tmp/stefanoGirini"
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
'''
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

        # import pdb; pdb.set_trace() # by Loreto
        # flatten_data = dict(sorted(flatten_data.items()))

        ### prendi le colonne fino al TeamManager
        for i in range(0, len(colonne_gerarchia)):
            sheet_name=colonne_gerarchia[i]
            rows_data = dictUtils.flatten_keypaths_to_list(list(flatten_data.keys()), item_nrs=i+1, remove_enpty_array=True)
            for item in rows_data:
                gv.logger.info(item)
            gv.logger.info("")
            # import pdb; pdb.set_trace() # by Loreto

            ### --- remove_empty_array items (columns_data)
            result = [row for row in rows_data if not all(a == '-' for a in row)]
            ### --- insert bleank row if all cols have a value
            end_of_director = [xxx for index, row in enumerate(rows_data) if not all(a != '-' for a in row)]
            import pdb; pdb.set_trace() # by Loreto

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

'''






################################################################
# Configurazioe dei reservation addresss (config host)
################################################################
def retrieveAgentData(d_src: dict, nome_agente: str):
    d = myDict()

    ### - creazione agente dictionary
    for key, value in d_src.items():
        if value["AGENTE"] == nome_agente:
            contract_id = value.pop("SPEEDY_CTR_ID")
            # value.pop("AGENTE")
            d[contract_id] = value

    return d

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
    esiti               = gv.excel_config.esito_keywords
    totale_include      = gv.excel_config.esito_keywords.totale.include

    # ----------------------------------------
    # - valori di include/exclude
    # ----------------------------------------

    # --- remove blanks
    esiti_exclude       = [v.lower().replace(' ', '') for v in esiti.exclude]
    confermato_include  = [v.lower().replace(' ', '') for v in esiti.confermato.include]
    attivazione_include = [v.lower().replace(' ', '') for v in esiti.attivazione.include]
    back_include        = [v.lower().replace(' ', '') for v in esiti.back.include]


    d = myDict()
    for key, value in d_src.items():
        partner  = value["PARTNER"]
        prodotto = value["PRODOTTO"]
        esito    = value["ESITO"]

        if not partner in d:
            d[partner] = myDict()
            d[partner]["totale"] = 0
            d[partner]["confermato"] = 0
            d[partner]["attivazione"] = 0
            d[partner]["back"] = 0

        ptr=d[partner]

        ### - exclude unwante esito words
        gv.logger.debug("processing esito: %s", esito)
        esito_trimmed = esito.lower().replace(' ', '')

        fExcluded = False
        for excl_value in esiti_exclude:
            if excl_value in esito_trimmed:
                fExcluded = True
                break

        if fExcluded:
            gv.logger.debug("excluding due to: %s", excl_value)
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




def myDict(use_benedict: bool=True):
    if use_benedict:
        return benedict(keyattr_enabled=True, keyattr_dynamic=False)
    return dict()





###########################################################################
#
###########################################################################
def insertAgentInStruct(main_dict: dict, agents: dict):
    print(agents.keys())
    separator = '.'
    key_paths = main_dict.keypaths(gv.struttura_aziendale)

    fLoreto = True
    fBenedict = not fLoreto

    if fLoreto:
        flatten_data = dictUtils.lnFlatten(main_dict, separator=separator, index=False)
        agent_col=5
        for item in flatten_data:
            keypath = item.split(separator)
            if len(keypath) >= agent_col:  ### colonna Agent
                agent_name = keypath[-1]
                if agent_name in agents.keys():
                    gv.logger.info("adding %s results data", agent_name)
                    this_agent = agents.pop(agent_name)
                    # print(agents.keys())
                    agent_results=this_agent["results"]
                    if isinstance(agent_results, dict):
                        main_dict[keypath] = agent_results ### sfrutto la capacita di benedict per puntare ad un keypath


    if fBenedict: # --- uso il jkypaths di benedict....
        agent_col=6
        for item in key_paths:
            keypath = item.split(separator)
            if len(keypath) >= agent_col:  ### colonna Agent
                agent_name = keypath[-1]
                if agent_name in agents.keys():
                    this_agent= agents.pop(agent_name)
                    gv.logger.info("adding %s results data", agent_name)
                    agent_results=this_agent["results"]
                    if isinstance(agent_results, dict):
                        main_dict[keypath] = agent_results ### sfrutto la capacita di benedict per puntare ad un keypath

    dictUtils.toYaml(d=main_dict, filepath=f"{gv.tmpPath}/strutturaAziendaleWithAgentResuls.yaml", indent=4, sort_keys=False, stacklevel=0, onEditor=False)



###################################################################
# creazine dei dataFrames per i vari fogli
# da tenere in considerazione i dati degli agenti:
# il partner sarà una colonna e conterrà tante righe quanti sono per ogni agente.
# Es:
#   Agent Name:
#       Eni:
#           totale: 17
#           confermato: 16
#           attivazione: 0
#           back: 0
#       Enel:
#           totale: 17
#           confermato: 17
#           attivazione: 0
#           back: 0
###################################################################
def createStructForExcel(agents: dict):
    colonne_gerarchia = gv.excel_config.output_sheet.colonne_gerarchia
    colonne_dati      = gv.excel_config.output_sheet.colonne_dati
    separator='#'

    ### --- aggiungiamo i dati dei risultati per gli agenti trovai
    insertAgentInStruct(gv.struttura_aziendale, agents)
    if len(agents):
        gv.logger.warning("Alcuni agenti non sono presenti nella struttura ma sono presenti nel risultati dei contratti")
        for name in agents.keys():
            gv.logger.warning(" - %s", name)


    flatten_data = dictUtils.lnFlatten(gv.struttura_aziendale, separator=separator, index=True)
    for item in flatten_data: gv.logger.debug(item)



    # --- @Loreto:  creaimao le strutture per i fogli excel
    sheet = myDict()
    for inx, sheet_name in enumerate(colonne_gerarchia):
        sheet[sheet_name] = myDict()
        sheet[sheet_name]["df"] = myDict()

        # --- filter all the columns limiting item per row (item_nrs)
        rows_data = dictUtils.flatten_keypaths_to_list(list(flatten_data.keys()), item_nrs=inx+1, remove_enpty_array=True)
        for item in rows_data: gv.logger.debug(item)
        ### ---


        ### --- remove_empty_array items (columns_data)
        sheet_rows = [row for row in rows_data if not all(a == '-' for a in row)]
        for item in sheet_rows: gv.logger.debug(item)
        ### ---

        ### --- find row where director changes in modo da inserire una riga di separazione
        ### --- da sviluppare
        row_separator = [index for index, row in enumerate(sheet_rows) if all(a != '-' for a in row)]
        ### ---


        # --- aggiungiamo le colonne contenenti i risultati
        result_cols = []
        title_row = colonne_gerarchia[:inx+1]
        for col_name in colonne_dati:
            title_row.append(col_name)
            result_cols.append(0)

        for index in range(len(sheet_rows)):
            sheet_rows[index].extend(result_cols)
        # ---

        ### - creiamo il dataFrame
        sheet[sheet_name]["df"] = pd.DataFrame(
                # columns = colonne_gerarchia[:inx+1],
                columns = title_row,
                data    = sheet_rows
            )


        if True:
            df = sheet[sheet_name]["df"]
            lnExcel.addSheet(filename=gv.args.output_agenti_filename, sheets=[sheet_name], dataFrames=[df], sheet_exists="replace", mode='a')
            lnExcel.setColumnSize(file_path=gv.args.output_agenti_filename, sheetname=sheet_name)

    import pdb; pdb.set_trace() # by Loreto



### -------------------------------------
### --- processiamo i contratti per ogni agente
### -------------------------------------
def agentContracts(contract_dict: dict, list_agenti: list):
    fDEBUG_SAVE_TO_YAML = False
    d = myDict()
    for name in list_agenti:
        gv.logger.info("processing agent: %s", name)
        d[name] = myDict()

        ### -----------------------------
        d[name]["data"] = retrieveAgentData(d_src=contract_dict, nome_agente=name)
        gv.logger.info("    found records: %s ", len(d[name]["data"].keys()))
        if fDEBUG_SAVE_TO_YAML:
            agent_filename = f"{gv.tmpPath}/{name.replace(' ', '_')}_data.yaml"
            dictUtils.toYaml(d=d[name]["data"], title=name, filepath=agent_filename, indent=4, sort_keys=False, stacklevel=0, onEditor=False)


        ### -----------------------------
        d[name]["results"] = partnerPerAgente(d_src=d[name]["data"])
        ag_results=d[name]["results"]
        gv.logger.info("    found partners: %s ", len(ag_results.keys()))
        if fDEBUG_SAVE_TO_YAML:
            result_filename = f"{gv.tmpPath}/{name.replace(' ', '_')}_results.yaml"
            dictUtils.toYaml(d=ag_results, title=name, filepath=result_filename, indent=4, sort_keys=False, stacklevel=0, onEditor=False)

    return d



################################################################
# Configurazioe dei reservation addresss (config host)
################################################################
def Main(gVars: dict):
    excel_filename        = gv.args.input_excel_filename
    agenti_excel_filename = gv.args.output_agenti_filename
    sheet_name            = gv.excel_config.source_sheet.name
    selected_columns      = gv.excel_config.source_sheet.columns_to_be_extracted



    ### -------------------------------
    ### --- read contracts data
    ### -------------------------------
    ### --- lettura sheet contratti da excel
    gv.workBook  = workBbookClass(excel_filename=excel_filename, logger=gv.logger)
    sh_contratti = sheetClass(wbClass=gv.workBook, sheet_name_nr=0)
    dict_contratti = sh_contratti.asDict(usecols=selected_columns, use_benedict=True)
    dictUtils.toYaml(d=dict_contratti, filepath=f"{gv.tmpPath}/stefanoG.yaml", indent=4, sort_keys=False, stacklevel=0, onEditor=False)





    ### -------------------------------------
    ### --- estrazione dati agenti dal foglio contratti
    ### -------------------------------------
    nomi_agenti = sh_contratti.readColumn(col_name="AGENTE", unique=True)
    gv.logger.info("nomi agenti: %s", nomi_agenti)


    ### -------------------------------------
    ### --- processiamo i contratti per ogni agente
    ### -------------------------------------
    agent = agentContracts(contract_dict=dict_contratti, list_agenti=nomi_agenti )
    '''
    agent = myDict()
    for name in nomi_agenti:
        gv.logger.info("processing agent: %s", name)
        agent[name] = myDict()

        ### -----------------------------
        agent[name]["data"] = retrieveAgentData(d_src=dict_contratti, nome_agente=name)
        gv.logger.info("    found records: %s ", len(agent[name]["data"].keys()))
        if fDEBUG_SAVE_TO_YAML:
            agent_filename = f"{gv.tmpPath}/{name.replace(' ', '_')}_data.yaml"
            dictUtils.toYaml(d=agent[name]["data"], title=name, filepath=agent_filename, indent=4, sort_keys=False, stacklevel=0, onEditor=False)


        ### -----------------------------
        agent[name]["results"] = partnerPerAgente(d_src=agent[name]["data"])
        ag_results=agent[name]["results"]
        gv.logger.info("    found partners: %s ", len(ag_results.keys()))
        if fDEBUG_SAVE_TO_YAML:
            result_filename = f"{gv.tmpPath}/{name.replace(' ', '_')}_results.yaml"
            dictUtils.toYaml(d=ag_results, title=name, filepath=result_filename, indent=4, sort_keys=False, stacklevel=0, onEditor=False)
    '''



    # --- prepare Excel structure
    createStructForExcel(agents=agent)

