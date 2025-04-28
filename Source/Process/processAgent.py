#!/usr/bin/env python3
#
# updated by ...: Loreto Notarantonio
# Date .........: 28-04-2025 20.36.48
#


import sys; sys.dont_write_bytecode = True
import os
from pathlib import Path
from benedict import benedict
from types import SimpleNamespace
from enum import Enum
import pandas as pd


# --- @Loreto: my lib
import ln_pandasExcel_Class as lnExcel
import lnUtils
import dictUtils
from ln_pandasExcel_Class import workBbookClass, sheetClass



class COLS(Enum):
    Direttore         = 1
    AreaManager       = 2
    ManagerPlus       = 3
    Manager           = 4
    TeamManager       = 5
    Agente            = 6
    Partner           = 7
    Esito_totale      = 8
    Esito_completato  = 9
    Esito_attivazione = 10
    Esito_back        = 11


def setup(gVars: (dict, SimpleNamespace)):
    global gv
    gv=gVars
    gv.logger.caller(__name__)
    gv.excelBook=None
    gv.tmpPath="/tmp/stefanoGirini"
    Path(gv.tmpPath).mkdir(parents=True, exist_ok=True)








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


    def excludeEsito(word: str, exclude_list: list):
        # esito_trimmed = esito.lower().replace(' ', '')

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


    d = gv.myDict()
    for key, value in d_src.items():
        partner  = value["PARTNER"]
        prodotto = value["PRODOTTO"]
        esito    = value["ESITO"]

        if not partner in d:
            d[partner] = gv.myDict()
            d[partner]["totale"] = 0
            d[partner]["confermato"] = 0
            d[partner]["attivazione"] = 0
            d[partner]["back"] = 0
            d[partner]["not_counted"] = 0

        ptr=d[partner]
        gv.logger.debug("processing word: %s", esito)

        esito_trimmed = esito.lower().replace(' ', '')
        if excludeEsito(esito_trimmed, esiti_exclude):
            continue

        if totale_include == "all":
            d[partner]["totale"] += 1

        if includeData(esito_trimmed, confermato_include):
            d[partner]["confermato"] += 1
            continue

        if includeData(esito_trimmed, attivazione_include):
            d[partner]["attivazione"] += 1
            continue

        if includeData(esito_trimmed, back_include):
            d[partner]["back"] += 1
            continue

        d[partner]["not_counted"] += 1
    return d









###########################################################################
#
###########################################################################
def insertAgentInStruct(main_dict: dict, agents: dict):
    # print(agents.keys())
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



#########################################################
# per ogni partner crea un riga
# ritorna list of list
# nella prima riga mettiamo i totali_agente dei vari partner
#########################################################
def calculateResults(agent_data: dict, row: list) -> list:
    new_rows = []
    sunto_agente = row[:]
    totali = 0
    confermati = 0
    attivazione = 0
    back = 0
    for partner_name in agent_data:
        new_row=row[:]
        ptr=agent_data[partner_name]
        data_cols=[partner_name,
                    ptr["totale"],
                    ptr["confermato"],
                    ptr["attivazione"],
                    ptr["back"],
                ]
        totali      += ptr["totale"]
        confermati  += ptr["confermato"]
        attivazione += ptr["attivazione"]
        back        += ptr["back"]

        new_row.extend(data_cols)
        new_rows.append(new_row)
    sunto_agente.extend(["", totali, confermati, attivazione, back])
    new_rows.insert(0, sunto_agente)
    return new_rows




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
