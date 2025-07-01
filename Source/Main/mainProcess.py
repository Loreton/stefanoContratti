#!/usr/bin/env python3
#
# updated by ...: Loreto Notarantonio
# Date .........: 01-07-2025 16.40.52
#


import sys; sys.dont_write_bytecode = True
import os
from pathlib import Path
from benedict import benedict
from types import SimpleNamespace

# import pandas as pd
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
# Per ogni agente presente nella struttura gerarchinca
#   andiamo a prelevare i relativi rsultati dai contratti
# Ho notato che alcuni nomi sono presenti
###########################################################################
def insertAgentInStruct(main_dict: dict, agent_contracts: dict):
    from itertools import permutations
    ## --- per comodità salviamo la list degli agenti usato nella subfunction
    agenti_in_contratto = [x for x in agent_contracts.keys()]

    #--------------------------------------------------
    def agentInContract(ag: str):
        # ag = ag.lower()
        # print(len(lista))
        # lista=["Franco Cosimino", "Giuliano Yabandeh Jahromi", "Luigi Amato Euroma2 Pm"]
        if ag in agenti_in_contratto:
            return True

        tk = ag.split()
        combinazioni = list(permutations(tk, len(tk)))
        for item in combinazioni:
            name=' '.join(item)
            print(f"checking {name}  --- {ag}")
            if name in agenti_in_contratto:
                print("name modified: ", name)
                return True
        else:
            print(ag)
            import pdb; pdb.set_trace() # by Loreto

        return False

    #--------------------------------------------------

    file_contratti_dettagliati = gv.working_files.contratti_dettagliati
    separator = '.'
    # key_paths = main_dict.keypaths(gv.struttura_aziendale)
    # import pdb; pdb.set_trace() # by Loreto


    flatten_data = dictUtils.lnFlatten(main_dict, separator=separator, index=False)
    agent_col=5
    for item in flatten_data:
        keypath = item.split(separator)
        if len(keypath) >= agent_col:  ### colonna Agent
            agent_name = keypath[-1]
            if agent_name in agent_contracts.keys():
                gv.logger.info("adding %s results data", agent_name)
                this_agent = agent_contracts.pop(agent_name)
                agent_results=this_agent["results"]
                if isinstance(agent_results, dict):
                    main_dict[keypath] = agent_results ### sfrutto la capacita di benedict per puntare ad un keypath
            else:
                gv.agents_not_in_contracts.append(agent_name) # --- @Loreto:  01-07-2025 15:55:18

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
            gv.logger.info(f"Agente: {nome_agente} found")
            break
    else:
        gv.logger.error(f"Agente: {nome_agente} NOT found in contracts")

    return d



### ##########################################################
### --- processiamo i contratti per ogni agente
### provvediamo anche ad aggiustare il nome:
###     -. eliminando extra BLANKs
###     -. convertendo "o'" in "ò"
###
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
def retrieveContractsForAgent(contract_dict: dict, lista_agenti: list):
    fDEBUG_SAVE_TO_YAML = False
    d = gv.myDict()
    for name in lista_agenti:
        gv.logger.info("processing agent: %s", name)
        name = name.replace("o'", "ò").replace("-", " ")
        name = lnUtils.remove_extra_blanks(data=name)
        gv.logger.info("    modified name: %s", name)
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



    ### -------------------------------
    ### --- identifichiamo i nomi dei vai file
    ### -------------------------------
    sheet_name                 = gv.excel_config.source_sheet.name
    selected_columns           = gv.excel_config.source_sheet.columns_to_be_extracted
    excel_input_filename       = Path(gv.args.excel_input_filename).resolve()
    excel_output_filename      = Path(gv.args.excel_output_filename).resolve()
    file_agents_data           = Path(gv.working_files.agents_data).resolve()
    file_struttura_aziendale   = Path(gv.working_files.agents_data).resolve()
    file_agents_results        = Path(gv.working_files.agents_results).resolve()
    file_contratti_preprocess  = Path(gv.working_files.contratti_preprocess).resolve()
    file_agenti_discrepanti    = Path(gv.working_files.agenti_discrepanti).resolve()
    file_struttura_aziendale    = Path(gv.working_files.struttura_aziendale).resolve()

    dictUtils.toYaml(d=gv.struttura_aziendale, filepath=file_struttura_aziendale, indent=4, sort_keys=False, stacklevel=0, onEditor=False)
    gv.agents_not_in_contracts = []
    # --- @Loreto:  01-07-2025 estrarre un file con i nomi agenti per confrontarli con quelli sul foglio excel


    ### -------------------------------
    ### --- read contracts data from excel
    ### --- and create a dictionary with selected columns
    ### -------------------------------
    gv.peWorkBook  = pe.WorkbookClass(excel_filename=excel_input_filename, logger=gv.logger)
    sh_contratti = gv.peWorkBook.getSheetClass(sheet_name_nr=0)
    dict_contratti = sh_contratti.asDict(usecols=selected_columns)
    dictUtils.toYaml(d=dict_contratti, filepath=file_contratti_preprocess, indent=4, sort_keys=False, stacklevel=0, onEditor=False)


    ### -------------------------------------
    ### --- normalizzazione dei nomi nei contratti # --- @Loreto:  01-07-2025 15:54:09
    ### -------------------------------------
    nomi_agenti=[]
    for k, v in dict_contratti.items():
        cur_name = v["AGENTE"]
        new_name = cur_name.replace("o'", "ò").replace("-", " ")
        new_name = lnUtils.remove_extra_blanks(data=new_name)
        if not new_name == cur_name:
            v["AGENTE"] = new_name
            gv.logger.warning(f"modified name: from {cur_name} to: {new_name}")
            cur_name = v["AGENTE"]

        if not cur_name in nomi_agenti:
            nomi_agenti.append(cur_name)


    gv.logger.info("nomi agenti: %s", nomi_agenti)


    ### -------------------------------------
    ### --- processiamo i contratti per ogni agente
    ### --- estrazione dati agenti dal foglio contratti
    ### -------------------------------------
    agent_contracts = retrieveContractsForAgent(contract_dict=dict_contratti, lista_agenti=nomi_agenti )

    ### -------------------------------------
    ### --- creazione due dict (che salviamo su yaml file)
    ### --- per eventuale verifica di un corretto calcolo
    ### --- d_data              con i dati deti prelevati dai contratti
    ### --- gv.agents_results   con i risultati dei dati processati
    ### -------------------------------------
    d_data = gv.myDict()
    gv.agent_results = gv.myDict()
    for name in agent_contracts:
        d_data[name]=agent_contracts[name]["data"]
        gv.agent_results[name]=agent_contracts[name]["results"]

    dictUtils.toYaml(d=d_data, filepath=file_agents_data, indent=4, sort_keys=False, stacklevel=0, onEditor=False)
    dictUtils.toYaml(d=gv.agent_results, filepath=file_agents_results, indent=4, sort_keys=False, stacklevel=0, onEditor=False)

    ### -------------------------------------
    ### --- inseriamo gli agenti nella struttura globale
    ### --- gli agenti inseriti verranno rimossi dagli agent_contracts
    ### --- tutti quelli trovati nei contratti ma non presenti in struttura andranno in uno sheet dedicato
    ### -------------------------------------
    insertAgentInStruct(main_dict=gv.struttura_aziendale, agent_contracts=agent_contracts)


    # gv.DF = []
    gv.SHEETS = []
    gv.COLOR_CELLS = []



    ### -------------------------------------
    ### --- creiamo il flatten del mainDict
    ### -------------------------------------
    gv.flatten_data = dictUtils.lnFlatten(gv.struttura_aziendale, separator='#', index=True)
    gv.flatten_keys = list(gv.flatten_data.keys())
    gv.keypaths_list = dictUtils.flatten_keypaths_to_list(gv.flatten_keys, separator="#", item_nrs=6)


    ### -------------------------------------
    ### --- creiamo gli sheets
    ### -------------------------------------
    Sheets.create(d=gv.struttura_aziendale, hierarchy_level=gv.HIERARCHY.Direttore)
    Sheets.create(d=gv.struttura_aziendale, hierarchy_level=gv.HIERARCHY.AreaManager)
    Sheets.create(d=gv.struttura_aziendale, hierarchy_level=gv.HIERARCHY.ManagerPlus)
    Sheets.create(d=gv.struttura_aziendale, hierarchy_level=gv.HIERARCHY.Manager)
    Sheets.create(d=gv.struttura_aziendale, hierarchy_level=gv.HIERARCHY.TeamManager)
    Sheets.create(d=gv.struttura_aziendale, hierarchy_level=gv.HIERARCHY.Agente)


    ### -------------------------------------
    ### --- creiamo gli sheets anche per agenti non trovati
    ### -------------------------------------
    if len(agent_contracts):
        Sheets.agentiNonTrovati(agents=agent_contracts, sh_name="Unsresolved_Contracts_Agents", descr="I seguenti agenti sono presenti nel foglio contratti, na non nella struttura")

    if len(gv.agents_not_in_contracts):
        Sheets.agentiNonTrovati(agents=gv.agents_not_in_contracts, sh_name="Orphans_Hierarchy_Agents", descr="I seguenti agenti sono presenti nella struttura ma non nel foglio contratti")


    ### -------------------------------------
    ### --- chiudiamo file excel
    ### -------------------------------------
    gv.peWorkBook.save(filename=str(excel_output_filename))




    ### -------------------------------------
    ### --- riapriamo ed aggiustamento col_size e qualche colore
    ### -------------------------------------
    pyxlWB = pyxl.WorkBookClass(filename=excel_output_filename, logger=gv.logger)
    for sh_name, cell_range in zip(gv.SHEETS, gv.COLOR_CELLS):
        ws = pyxlWB.getSheet(sh_name)
        ws.formattingHeader()
        ws.setColumnCalulatedSize(offset=4)
        if cell_range:
            ws.setCellsColor(cells=cell_range, color='ffffa6')
            ws.setFreezePanes(cell="B2")

        ws.setColumnPercent(row_range=range(2, ws.getRows()), col_name=gv.dataCols.RID_percent.name)
        ws.setColumnPercent(row_range=range(2, ws.getRows()), col_name=gv.dataCols.VAS_percent.name)

    pyxlWB.save()



    ### -------------------------------------
    ### --- Solo come debug per assicurarci che non abbiamo mancato qualche agente
    ### -------------------------------------
    for name in gv.agents_not_in_contracts:
        if name in agent_contracts.keys():
            gv.logger.error(" - %s --- COME MAI????", name)
    for name in agent_contracts.keys():
        if name in gv.agents_not_in_contracts:
            gv.logger.error(" - %s --- COME MAI????", name)
        # else:
        #     gv.logger.info(" - %s --- ok", name)


