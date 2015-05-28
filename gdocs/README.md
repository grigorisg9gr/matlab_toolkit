# Google Spreadsheets MATLAB API
This is a package that allows you to modify a spreadsheet with the new Google Sheets directly from MATLAB. 


Installation: 
1) Download the files
Install [gspread](https://github.com/burnash/gspread) and the rest dependencies. 
More specifically you can use pip: 
pip install PyOpenSSL==0.13 # [reasoning](https://github.com/pyca/cryptography/issues/693#issuecomment-41106090) , and [this](https://github.com/conda/conda-build/issues/61).
pip install --upgrade oauth2client
pip install --upgrade gspread


2) Provide the json file as instructed [here](http://gspread.readthedocs.org/en/latest/oauth2.html) and the path of installation in modify_gdocs.m

3) Create the spreadsheet you want to modify, read if it doesn't exist. 



Apart from the MATLAB API, it can be used as an API for accessing and modifying the google drive documents from python. The functions of modify_drive.py can be used in python scripts for this purpose. 



