#!/usr/bin/env python3
#
# updated by ...: Loreto Notarantonio
# Date .........: 22-04-2025 18.23.43
#


import sys; sys.dont_write_bytecode = True
import os


import pandas as pd
from pathlib import Path


import yaml

data = '''
    - name: Alice
      age: 28
      city: New York
    - name: Bob
      age: 24
      city: Los Angeles
    - name: Carol
      age: 31
      city: Chicago
'''

def readYamlFile(filename: str):
    # Convert YAML string to a Python list of dictionaries
    filepath=Path(filename).resolve()
    with filepath.open(mode="r") as f:
        content=f.read() # single string

    if content:
        gv.logger.info("File: %s loaded", filepath)
    else:
        gv.logger.error("File: %s not found in paths: %s", filename, _paths)
        if gv.exit_on_config_file_not_found:
            sys.exit(1)
        return None


    content=os.path.expandvars(content)
    data_list= yaml.load(content, Loader=yaml.FullLoader)
    # data_list = yaml.safe_load(data)

    # data_list = yaml.load(content, Loader=yaml.FullLoader)

    # Create a Pandas DataFrame from the data
    df = pd.DataFrame(data_list)

    # Print the original DataFrame
    print("Original DataFrame:")
    print(df)

    # Perform some data manipulations
    # df["age_group"] = pd.cut(df["age"], bins=[20, 30, 40], labels=["20-30", "30-40"])

    # Print the DataFrame after adding the 'age_group' column
    # print("DataFrame with Age Groups:")
    # print(df)


if __name__ == '__main__':
    readYamlFile("/media/loreto/LnDisk_SD_ext4/Filu/GIT-REPO/Python/stefanoG/conf/stefanoG_config.yaml")

    # import pdb; pdb.set_trace() # by Loreto
    # excel_data_df = pandas.read_excel('/tmp/prova01.xls', sheet_name='Agenti')
    # print(excel_data_df)
    # columns = excel_data_df.columns.ravel()
    # print(columns)
    # print('Excel Sheet to Dict:', excel_data_df.to_dict(orient='records'))
    # print('Excel Sheet to JSON:', excel_data_df.to_json(orient='records'))
    # print('Excel Sheet to CSV:\n', excel_data_df.to_csv(index=False))

    # print whole sheet data