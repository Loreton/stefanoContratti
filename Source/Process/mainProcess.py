#!/usr/bin/env python3
#
# updated by ...: Loreto Notarantonio
# Date .........: 04-05-2025 09.22.02
#


import sys; sys.dont_write_bytecode = True
import os
from pathlib import Path
from benedict import benedict
from types import SimpleNamespace

import pandas as pd


# --- @Loreto: my lib
import ln_pandasExcel_Class as lnExcel
import lnUtils
import dictUtils
from ln_pandasExcel_Class import workBbookClass, sheetClass
# import processAgent
import sheetAgent
import sheetTeamManager
import sheetManagers



def setup(gVars: (dict, SimpleNamespace)):
    global gv
    gv=gVars
    gv.logger.caller(__name__)
    # gv.excelBook=None
    # gv.tmpPath="/tmp/stefanoGirini"
    # Path(gv.tmpPath).mkdir(parents=True, exist_ok=True)

    sheetAgent.setup(gVars=gv)
    sheetTeamManager.setup(gVars=gv)
    sheetManagers.setup(gVars=gv)




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
    #-------------------------------------------------
    def includeData(word: str, include_list: list):
        fConfirmed = False
        for include_value in include_list:
            if include_value in word:
                fConfirmed = True
                break

        return fConfirmed


    def excludeData(word: str, exclude_list: list):
        fExcluded = False
        for excl_value in exclude_list:
            if excl_value in word:
                gv.logger.debug("excluding due to: %s", excl_value)
                fExcluded = True
                break

        return fExcluded
    #-------------------------------------------------


    esiti               = gv.excel_config.esito_keywords
    totale_include      = gv.excel_config.esito_keywords.totale.include

    # ----------------------------------------
    # - valori di include/exclude
    # ----------------------------------------

    # --- remove blanks inside item's list
    esiti_exclude       = [v.lower().replace(' ', '') for v in esiti.exclude]
    confermato_include  = [v.lower().replace(' ', '') for v in esiti.confermato.include]
    attivazione_include = [v.lower().replace(' ', '') for v in esiti.attivazione.include]
    back_include        = [v.lower().replace(' ', '') for v in esiti.back.include]
    rid_include         = [v.lower().replace(' ', '') for v in esiti.rid.include]


    d = gv.myDict()
    for key, value in d_src.items():
        partner  = value["PARTNER"]
        prodotto = value["PRODOTTO"].lower().replace(' ', '')
        esito    = value["ESITO"].lower().replace(' ', '')

        if not partner in d:
            d[partner] = gv.myDict()
            d[partner]["totale"] = 0
            d[partner]["confermato"] = 0
            d[partner]["attivazione"] = 0
            d[partner]["back"] = 0
            d[partner]["discarded"] = 0
            d[partner]["excluded"] = 0
            d[partner]["rid"] = 0

        ptr=d[partner]
        gv.logger.debug("processing word: %s", esito)
        # esito = esito.lower().replace(' ', '')
        # prodotto_trimmed = prodotto.lower().replace(' ', '')

        if excludeData(esito, esiti_exclude):
            d[partner]["excluded"] += 1
            continue

        if totale_include == "all":
            d[partner]["totale"] += 1

        if includeData(prodotto, rid_include):
            d[partner]["rid"] += 1 # non deve uscire

        if includeData(esito, confermato_include):
            d[partner]["confermato"] += 1
            continue

        if includeData(esito, attivazione_include):
            d[partner]["attivazione"] += 1
            continue

        if includeData(esito, back_include):
            d[partner]["back"] += 1
            continue

        d[partner]["discarded"] += 1
    return d









###########################################################################
#
###########################################################################
def insertAgentInStruct(main_dict: dict, agents: dict):
    # print(agents.keys())
    file_contratti_dettagliati = gv.working_files.file_contratti_dettagliati
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
                    agent_results=this_agent["results"]
                    if isinstance(agent_results, dict):
                        main_dict[keypath] = agent_results ### sfrutto la capacita di benedict per puntare ad un keypath


    dictUtils.toYaml(d=main_dict, filepath=file_contratti_dettagliati, indent=4, sort_keys=False, stacklevel=0, onEditor=False)





################################################################
# Configurazioe dei reservation addresss (config host)
################################################################
def retrieveAgentData(d_src: dict, nome_agente: str):
    d = gv.myDict()

    ### - creazione agente dictionary
    for key, value in d_src.items():
        if value["AGENTE"] == nome_agente:
            contract_id = value.pop("SPEEDY_CTR_ID")
            # value.pop("AGENTE")
            d[contract_id] = value

    return d



### ##########################################################
### --- processiamo i contratti per ogni agente
### crea una struct:
###     agent_name:
###         partner1:
###             totale: 38
###             confermato: 10
###             attivazione: 0
###             back: 1
###         partner2:
###             ...:
### ##########################################################
def retrieveContracts(contract_dict: dict, lista_agenti: list):
    fDEBUG_SAVE_TO_YAML = False
    d = gv.myDict()
    for name in lista_agenti:
        gv.logger.info("processing agent: %s", name)
        name = name.replace("o'", "ò").replace("-", " ")
        name = lnUtils.remove_extra_blanks(data=name)
        d[name] = gv.myDict()

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




#########################################################
# per ogni partner crea un riga
# ritorna list of list
# nella prima riga mettiamo i totali_agente dei vari partner
#########################################################
def calculateAgentResults(agent_data: dict, row: list) -> list:
    new_rows = []
    sunto_agente = row[:]
    totali = 0
    confermati = 0
    attivazione = 0
    back = 0
    rid = 0
    for partner_name in agent_data:
        new_row=row[:]
        ptr=agent_data[partner_name]
        data_cols=[partner_name,
                    ptr["totale"],
                    ptr["confermato"],
                    ptr["attivazione"],
                    ptr["back"],
                    ptr["rid"],
                ]
        totali      += ptr["totale"]
        confermati  += ptr["confermato"]
        attivazione += ptr["attivazione"]
        back        += ptr["back"]
        rid         += ptr["rid"]

        new_row.extend(data_cols)
        new_rows.append(new_row)
    sunto_agente.extend(["", totali, confermati, attivazione, back, rid])
    new_rows.insert(0, sunto_agente)
    return new_rows






################################################################
# Configurazioe dei reservation addresss (config host)
################################################################
def Main(gVars: dict):
    excel_filename             = gv.args.input_excel_filename
    agenti_excel_filename      = gv.args.output_agenti_filename
    sheet_name                 = gv.excel_config.source_sheet.name
    selected_columns           = gv.excel_config.source_sheet.columns_to_be_extracted
    file_agents_data           = gv.working_files.file_agents_data
    file_agents_results        = gv.working_files.file_agents_results
    file_contratti_preprocess  = gv.working_files.file_contratti_preprocess
    file_agenti_discrepanti   = gv.working_files.file_agenti_discrepanti

    ### -------------------------------
    ### --- read contracts data
    ### -------------------------------
    gv.workBook  = workBbookClass(excel_filename=excel_filename, logger=gv.logger)
    sh_contratti = sheetClass(wbClass=gv.workBook, sheet_name_nr=0)
    dict_contratti = sh_contratti.asDict(usecols=selected_columns, use_benedict=True)
    dictUtils.toYaml(d=dict_contratti, filepath=file_contratti_preprocess, indent=4, sort_keys=False, stacklevel=0, onEditor=False)


    ### -------------------------------------
    ### --- estrazione dati agenti dal foglio contratti
    ### -------------------------------------
    nomi_agenti = sh_contratti.readColumn(col_name="AGENTE", unique=True)
    gv.logger.info("nomi agenti: %s", nomi_agenti)


    ### -------------------------------------
    ### --- processiamo i contratti per ogni agente
    ### -------------------------------------
    agents = retrieveContracts(contract_dict=dict_contratti, lista_agenti=nomi_agenti )

    ### -------------------------------------
    ### --- creazione due dict (che salviamo su yaml file)
    ### --- per eventuale verifica di un corretto calcolo
    ### --- gv.agents_results sarà utile per il calcolo ai livelli superiori.
    ### -------------------------------------
    d_data = gv.myDict()
    gv.agent_results = gv.myDict()
    for name in agents:
        d_data[name]=agents[name]["data"]
        gv.agent_results[name]=agents[name]["results"]

    dictUtils.toYaml(d=d_data, filepath=file_agents_data, indent=4, sort_keys=False, stacklevel=0, onEditor=False)
    dictUtils.toYaml(d=gv.agent_results, filepath=file_agents_results, indent=4, sort_keys=False, stacklevel=0, onEditor=False)

    ### -------------------------------------
    ### --- inseriamo gli agenti nella struttura globale
    ### --- gli agenti inseriti verranno rimossi dagli agenti trovati
    ### --- in modo che se avanzano segnaliamo l'incongruenza
    ### -------------------------------------
    insertAgentInStruct(main_dict=gv.struttura_aziendale, agents=agents)
    if len(agents):
        gv.logger.warning("I seguenti agenti sono presenti nel foglio contratti, na non nella struttura")
        for name in agents.keys():
            gv.logger.warning(" - %s", name)
        dictUtils.toYaml(d=agents, filepath=file_agenti_discrepanti, indent=4, sort_keys=False, stacklevel=0, onEditor=False)


    ### -------------------------------------
    ### --- creiamo il flatten del mainDict
    ### -------------------------------------
    gv.flatten_data = dictUtils.lnFlatten(gv.struttura_aziendale, separator='#', index=True)
    gv.flatten_keys = list(gv.flatten_data.keys())
    for item in gv.flatten_data: gv.logger.debug(item)

    '''
    sheetAgent.createSheet(d=gv.struttura_aziendale, calculateAgentResultsCB=calculateAgentResults)
    sheetTeamManager.createSheet(d=gv.struttura_aziendale, calculateAgentResultsCB=calculateAgentResults)
    '''
    sheetTeamManager.prepareSheet(d=gv.struttura_aziendale, level=v.COLS.Manager.value, sh_name=gv.COLS.Manager.name)


