#!/usr/bin/env python3

#===============================================
# updated by ...: Loreto Notarantonio
# Date .........: 25-04-2025 16.36.34
#===============================================

import sys; sys.dont_write_bytecode=True
import os


import zipfile
# from io import BytesIO



################################################################
# # Example usage
#       zip_dir_with_extensions(
#           source_dir='my_folder',
#           zip_filename='filtered_files.zip',
#           extensions=['.txt', '.py']  # Only include .txt and .py files
#       )
################################################################
def zip_dir_with_extensions(source_dir, zip_filename, extensions):
    import zipfile
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for foldername, subfolders, filenames in os.walk(source_dir):
            for filename in filenames:
                if any(filename.endswith(ext) for ext in extensions):
                    file_path = os.path.join(foldername, filename)
                    arcname = os.path.relpath(file_path, source_dir)
                    zipf.write(file_path, arcname)



################################################################
# Example usage (da provare ....# @Loreto:  25-04-2025 16:36:15
# if __name__ == '__main__':
#       extract_inner_zip('tools/inner_data.zip', 'output_folder')
################################################################
def extract_inner_zip(inner_zip_path, extract_to):
    # Path to the current running zip/pyz file
    running_zip = sys.argv[0]

    # Open the running .pyz or .zip as a zip file
    with zipfile.ZipFile(running_zip, 'r') as z:
        # Read the inner zip as bytes
        inner_zip_data = z.read(inner_zip_path)

        # Load it into memory as a zip
        with zipfile.ZipFile(io.BytesIO(inner_zip_data)) as inner_zip:
            inner_zip.extractall(extract_to)
            print(f"Extracted {inner_zip_path} to {extract_to}")



################################################################
# # Example usage
################################################################
def extractZip(zipFilename):
    prj_name=zipFilename.parent.stem
    if prj_name in ['bin']:
        prj_name=zipFilename.parent.parent.stem

    extract_dir=Path(f'/tmp/{prj_name}')
    if not extract_dir.exists():
        extract_dir.mkdir(parents=True, exist_ok=True)

    zip_paths=[]
    with zipfile.ZipFile(zipFilename, 'r') as zipObj:
        nameList = zipObj.namelist()
        for fileName in nameList:
            # Check filename endswith csv
            if fileName.endswith('.zip'):
                # Extract a single file from zip
                try:
                    _path=zipObj.extract(fileName, path=extract_dir)
                except OSError:
                    print("ERROR unzippig:", fileName)

                zip_paths.append(_path)

    return zip_paths



################################################################
# # Example usage
################################################################
import re, io
def extractZip_inZip(filename, extract_dir):
    zip_path=[]
    with zipfile.ZipFile(filename, 'r') as zfile:
        for name in zfile.namelist():
            if re.search(r'\.zip$', name) != None:
                zfiledata = io.BytesIO(zfile.read(name))
                _name=Path(name).parts[-1] # get only fname.zip
                _path=write_bytesio_to_file(fname=_name, bytesio=zfiledata, destdir=extract_dir)
                zip_path.append(_path)
                continue
                # extract files in zip2 if necessary
                with zipfile.ZipFile(zfiledata) as zfile2:
                    for name2 in zfile2.namelist():
                        print(name2)

    return zip_path


def write_bytesio_to_file(*, fname, bytesio, destdir):
    """
    Write the contents of the given BytesIO to a file.
    Creates the file or overwrites the if exists
    """
    filepath=Path(destdir).joinpath(fname)
    os.makedirs(destdir,  exist_ok=True)
    with open(filepath, "wb") as fout:
        # Copy the BytesIO stream to the output file
        fout.write(bytesio.getbuffer())
    return filepath