#!/usr/bin/env python33
# -*- coding: utf-8 -*-
# -*- coding: iso-8859-1 -*-

# updated by ...: Loreto Notarantonio
# Date .........: 26-04-2025 21.25.33

import sys
import os
from pathlib import Path



##############################################################
# - Parse Input
##############################################################
def ParseInput(version: str):
    # global base_device_db_dir
    # base_device_db_dir = Path(db_dir)
    logger_levels=['trace', 'debug', 'notify', 'info', 'function', "caller", 'warning', 'error', 'critical']
    # table_list=["devices", "telegramBots", "tasmotaProperties", "mqttBrokers", "virtual_servers"]
    # server_list=["archerc6", "archerc20", "lnpi22", "lnpi23"]

    # base_device_db_dir=os.path.expandvars("${HOME}/lnProfile/devicesDB")


    def common_options(subp):
        # -- add common options to all subparsers
            help_color='white'
            ### --- mi serve per avere la entry negli args e creare poi la entry "product"
            # subp.add_argument('--{0}'.format(name), action='store_true', default=True)

            subp.add_argument('--go',            action='store_true', help='specify if command must be executed. (default: %(default)s)\n\n')
            subp.add_argument('--display-args',  action='store_true', help='Display arguments (default: %(default)s)\n\n')
            subp.add_argument('--editor',        action='store_true', help='display generated files on editor. (default: %(default)s)\n\n')
            subp.add_argument('--test',          action='store_true', help='skip remote access (default: %(default)s)\n\n')


            subp.add_argument( "--log-console-level",
                                    metavar='<optional>',
                                    type=str.lower,
                                    required=False,
                                    default='notify',
                                    choices=logger_levels,
                                    nargs="?", # just one entry
                                    help=f"""set console logger level:
                                            {logger_levels}
                                            \n\n""".replace('  ', '')
                                )




    # -----------------------------
    import argparse
    if len(sys.argv) == 1:
        sys.argv.append('-h')

    parser = argparse.ArgumentParser(description='tst programma per Stefano')
    parser.add_argument('--version', action='version', version=version)
    # subparsers = parser.add_subparsers(title="required positional arguments")



    # ==================
    # sqlite load_from_file
    # ==================
    # load_parser.add_argument('--create-table', action='store_true', help='create/replace  table name')
    parser.add_argument('--input-excel-filename', default=None, required=True,
        help='filename containing records to be loaded. (default: %(default)s)\n')
    parser.add_argument('--output-agenti-filename', default=None, required=True,
        help='filename containing records to be loaded. (default: %(default)s)\n')



    # - common options
    common_options(parser)

    args = parser.parse_args()

    if args.display_args:
        import json
        json_data = json.dumps(vars(args), indent=4, sort_keys=True)
        print('input arguments: {json_data}'.format(**locals()))
        sys.exit(0)


    return  args



