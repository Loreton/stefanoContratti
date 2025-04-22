#!/usr/bin/env python3
#
# updated by ...: Loreto Notarantonio
# Date .........: 21-04-2025 19.02.02
#


import sys; sys.dont_write_bytecode = True
import os


import pandas



class lnExcel_Class():

    def __init__(self, excel_filename, logger):
        self.logger=logger
        # self.use_benedict=use_benedict
        self.filename=os.path.expandvars(excel_filename)

        self.xls = pandas.ExcelFile(filename)



        df1 = pd.read_excel(xls, 'Sheet1')
        df2 = pd.read_excel(xls, 'Sheet2')






if __name__ == '__main__':
    # import pdb; pdb.set_trace() # by Loreto
    excel_data_df = pandas.read_excel('/tmp/prova01.xls', sheet_name='Agenti')
    print(excel_data_df)
    columns = excel_data_df.columns.ravel()
    print(columns)
    print('Excel Sheet to Dict:', excel_data_df.to_dict(orient='records'))
    # print('Excel Sheet to JSON:', excel_data_df.to_json(orient='records'))
    # print('Excel Sheet to CSV:\n', excel_data_df.to_csv(index=False))

    # print whole sheet data