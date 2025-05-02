#!/usr/bin/env python3
#
# updated by ...: Loreto Notarantonio
# Date .........: 02-05-2025 09.03.14
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






def somma_livello(d, livello_attuale=1, livello_target=6):
    if livello_attuale == livello_target:
        # Se siamo al livello target, sommiamo i valori (che devono essere numeri)
        return sum(v for v in d.values() if isinstance(v, (int, float)))

    # Se non siamo ancora al livello target, ricorriamo nei sotto-dizionari
    somma = 0
    for k, v in d.items():
        if isinstance(v, dict):
            risultato = somma_livello(d=v, livello_attuale=livello_attuale+1, livello_target=livello_target)
            somma += risultato
            # Memorizziamo la somma nel dizionario corrente, se serve
            d[k]['_somma'] = risultato
    return somma




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
