#!/usr/bin/env python3
#
# updated by ...: Loreto Notarantonio
# Date .........: 07-05-2025 18.01.11
#


import sys; sys.dont_write_bytecode = True
import os
from pathlib import Path
from benedict import benedict
from types import SimpleNamespace

import pandas as pd
import  openpyxl
from openpyxl import load_workbook
from openpyxl.styles import PatternFill


# --- @Loreto: my lib
import lnPyExcel_Class as pe
import lnOpenPyXL_Class as pyxl
import lnUtils
import dictUtils
# from ln_pandasExcel_Class import workBbookClass, sheetClass

import commonFunctions
import Sheets



def setup(gVars: (dict, SimpleNamespace)):
    global gv
    gv=gVars
    gv.logger.caller(__name__)
    commonFunctions.setup(gVars=gv)
    Sheets.setup(gVars=gv)



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

    #-----------------------------------------------------------------
    # compara un lista con un'altra.
    # Se un item della search_list contiene BLANK allora viene fatto lo split dell'elemento
    # ...e si fa la comparazione con tutte le parole in AND
    #-----------------------------------------------------------------
    def includeData(source_list: list, search_list: list):
        fConfirmed = False
        for include_value in search_list:
            if ' ' in include_value:
                include_value = include_value.split()
            else:
                include_value = [include_value]

            common_items = [item for item in include_value if item in source_list]
            if len(common_items) == len(include_value):
                gv.logger.debug("including due to: %s", include_value)
                fConfirmed = True
                break

        return fConfirmed

    #-----------------------------------------------------------------
    # compara un lista con un'altra.
    # Se un item della search_list contiene BLANK allora viene fatto lo split dell'elemento
    # ...e si fa la comparazione con tutte le parole in AND
    #-----------------------------------------------------------------
    def excludeData(source_list: list, search_list: list):
        fExcluded = False
        for exclude_value in search_list:
            if ' ' in exclude_value:
                exclude_value = exclude_value.split()
            else:
                exclude_value = [exclude_value]

            common_items = [item for item in exclude_value if item in source_list]
            if len(common_items) == len(exclude_value):
                gv.logger.debug("excluding due to: %s", exclude_value)
                fExcluded = True
                break

        return fExcluded

    #-------------------------------------------------

    esito_exclude     = [v.lower() for v in gv.excel_config.esito_keywords.exclude]
    esito_confermato  = [v.lower() for v in gv.excel_config.esito_keywords.confermato]
    esito_attivazione = [v.lower() for v in gv.excel_config.esito_keywords.attivazione]
    esito_back        = [v.lower() for v in gv.excel_config.esito_keywords.back]

    prodotto_rid      = [v.lower() for v in gv.excel_config.prodotto_keywords.rid]
    prodotto_vas      = [v.lower() for v in gv.excel_config.prodotto_keywords.vas]
    prodotto_sim      = [v.lower() for v in gv.excel_config.prodotto_keywords.sim]
    prodotto_tv       = [v.lower() for v in gv.excel_config.prodotto_keywords.tv]

    d = gv.myDict()
    dc=gv.dataCols

    for key, value in d_src.items():
        xx=''
        partner  = value["PARTNER"]

        ### --- Modifico esoto e prodotto per fare una ricerca affidabile
        prodotto = value["PRODOTTO"].lower()
        prodotto = prodotto.split()

        esito    = value["ESITO"].lower()
        esito    = esito.split()

        if not partner in d:
            ### --- creazione struttura partner
            d[partner] = gv.myDict()
            for item in dc:
                d[partner][item.name] = 0


        ptr=d[partner]
        gv.logger.debug("processing esito: %s", esito)
        gv.logger.debug("processing prodotto: %s", prodotto)

        ### --- tutti i contratti presenti nel foglio
        d[partner][dc.PROCESSATI.name] += 1

        if excludeData(esito, esito_exclude):
            d[partner][dc.EXCLUDED.name] += 1
            continue

        isValid=False
        if includeData(esito, esito_confermato):
            d[partner][dc.CONFERMATI.name] += 1
            isValid=True

        elif includeData(esito, esito_attivazione):
            d[partner][dc.ATTIVAZIONE.name] += 1
            isValid=True

        elif includeData(esito, esito_back):
            d[partner][dc.BACK.name] += 1
            isValid=True

        if isValid:
            d[partner][dc.TOTALE.name] += 1

            ### --- verifichiamo i prodotti
            if includeData(prodotto, prodotto_rid):
                d[partner][dc.RID.name] += 1
            if includeData(prodotto, prodotto_vas):
                d[partner][dc.VAS.name] += 1
            if includeData(prodotto, prodotto_sim):
                d[partner][dc.SIM.name] += 1
            if includeData(prodotto, prodotto_tv):
                d[partner][dc.TV.name] += 1
        else:
            d[partner][dc.SCARTATI.name] += 1

        d[partner][dc.INSERITI.name] = d[partner][dc.SCARTATI.name] + d[partner][dc.TOTALE.name]


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
        gv.logger.info("    compare name: %s", name)
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







################################################################
# Configurazioe dei reservation addresss (config host)
################################################################
def Main(gVars: dict):
    gv.colonne_gerarchia   = gv.excel_config.output_sheet.colonne_gerarchia
    gv.colonne_dati        = gv.excel_config.output_sheet.colonne_dati



    sheet_name                 = gv.excel_config.source_sheet.name
    selected_columns           = gv.excel_config.source_sheet.columns_to_be_extracted
    excel_input_filename       = Path(gv.args.excel_input_filename).resolve()
    excel_output_filename      = Path(gv.args.excel_output_filename).resolve()
    file_agents_data           = Path(gv.working_files.file_agents_data).resolve()
    file_agents_results        = Path(gv.working_files.file_agents_results).resolve()
    file_contratti_preprocess  = Path(gv.working_files.file_contratti_preprocess).resolve()
    file_agenti_discrepanti    = Path(gv.working_files.file_agenti_discrepanti).resolve()



    ### -------------------------------
    ### --- read contracts data
    ### -------------------------------
    gv.peWorkBook  = pe.WorkbookClass(excel_filename=excel_input_filename, logger=gv.logger)
    sh_contratti = gv.peWorkBook.getSheetClass(sheet_name_nr=0)
    dict_contratti = sh_contratti.asDict(usecols=selected_columns)
    dictUtils.toYaml(d=dict_contratti, filepath=file_contratti_preprocess, indent=4, sort_keys=False, stacklevel=0, onEditor=False)


    ### -------------------------------------
    ### --- estrazione dati agenti dal foglio contratti
    ### -------------------------------------
    nomi_agenti = sh_contratti.getColumn(col_name="AGENTE", unique=True, header=False)
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


    # gv.DF = []
    gv.SHEETS = []
    gv.COLOR_CELLS = []

    if len(agents):
        gv.logger.warning("I seguenti agenti sono presenti nel foglio contratti, na non nella struttura")
        for name in agents.keys():
            gv.logger.warning(" - %s", name)
        dictUtils.toYaml(d=agents, filepath=file_agenti_discrepanti, indent=4, sort_keys=False, stacklevel=0, onEditor=False)
        Sheets.agentiNonTrovati(agents=agents)




    ### -------------------------------------
    ### --- creiamo il flatten del mainDict
    ### -------------------------------------
    gv.flatten_data = dictUtils.lnFlatten(gv.struttura_aziendale, separator='#', index=True)
    gv.flatten_keys = list(gv.flatten_data.keys())

    gv.keypaths_list = dictUtils.flatten_keypaths_to_list(gv.flatten_keys, separator="#", item_nrs=6)


    Sheets.create(d=gv.struttura_aziendale, hierarchy_level=gv.HIERARCHY.Direttore)
    Sheets.create(d=gv.struttura_aziendale, hierarchy_level=gv.HIERARCHY.AreaManager)
    Sheets.create(d=gv.struttura_aziendale, hierarchy_level=gv.HIERARCHY.ManagerPlus)
    Sheets.create(d=gv.struttura_aziendale, hierarchy_level=gv.HIERARCHY.Manager)
    Sheets.create(d=gv.struttura_aziendale, hierarchy_level=gv.HIERARCHY.TeamManager)
    Sheets.create(d=gv.struttura_aziendale, hierarchy_level=gv.HIERARCHY.Agente)

    gv.peWorkBook.save(filename=excel_output_filename)




    ### --- aggiustamento col_size e qualche colore
    pyxlWB = pyxl.WorkBookClass(filename=excel_output_filename, logger=gv.logger)
    for sh_name, cell_range in zip(gv.SHEETS, gv.COLOR_CELLS):
        ws = pyxlWB.getSheet(sh_name)
        ws.formattingHeader()
        ws.setColumnCalulatedSize(offset=4)
        if cell_range:
            ws.setCellsColor(cells=cell_range, color='ffffa6')
            ws.setFreezePanes(cell="B2")

    pyxlWB.save()


