"""
A wrapper class for gspread in order to write effectively to a spreadsheet (google drive).
The following functionalities are supported:
 1) reading a single cell from a spreadsheet (function read_value)
 2) writing in a single cell (function write_value)
 3) reading the values of a range of cells (function readrange)

 Copyright (C) 2014,2015 Grigorios G. Chrysos
 available under the terms of the Apache License, Version 2.0
 """

import sys
import json
from oauth2client.client import SignedJwtAssertionCredentials
import gspread
from gspread import SpreadsheetNotFound, WorksheetNotFound

class Spreadsheets:

    def login(self):
        scope = ['https://spreadsheets.google.com/feeds']
        try:
            credentials = SignedJwtAssertionCredentials(self.json_key['client_email'], self.json_key['private_key'], scope)
            self.gc = gspread.authorize(credentials)
        except:
            raise ValueError('Confirm that your credentials work fine.')

    def __init__(self, json_path):
        try:
            import gspread
        except ImportError:
            raise ImportError('You should install gspread first to use the functionalities of the class.')
        self.json = json_path
        try:
            self.json_key = json.load(open(json_path))
        except:
            raise ImportError('Check that the path of the json exists.')
        self.login()
        self.spreadsheet = None
        self.wks = None

    def get_spr(self, name_spr):
        self.login()
        try:
            self.spreadsheet = self.gc.open(name_spr)
        except SpreadsheetNotFound:
            raise SpreadsheetNotFound('Ensure that you have shared the shpreadsheet with the developer mail. '
                                      'If that is already done, then probably the spreasheet does not exist.')
        return self.spreadsheet

    def get_worksheet(self, name_spr, name_wks, create_wks=True):
        spreadsheet = self.get_spr(name_spr)
        try:
            self.wks = spreadsheet.worksheet(name_wks)
        except WorksheetNotFound:                     # in case it does not exist, the worksheet is created
            if create_wks:
                self.wks = spreadsheet.add_worksheet(title=name_wks, rows="220", cols="90")
            else:
                print('The worksheet does not exist.')
                return -1  # dummy value
        return self.wks

    def _check_wks_existence(self, name_spr='', name_wks='', create_wks=True):
        if self.wks is None:
            tr = self.get_worksheet(name_spr, name_wks, create_wks=create_wks)
        else:
            self.login()

    def read_value(self, row, col, name_spr='', name_wks=''):
        """
         Reads and returns a value from a cell.
         :param row:            Row to read the data from.
         :param col:            Column to read the data from.
         :param name_spr:       (Optional) name_spr in case there is no previous access to this spreadsheet from this instance.
         :param name_wks:       (Optional) name_spr in case there is no previous access to this worksheet from this instance.
         :return:
        """
        self._check_wks_existence(name_spr, name_wks, create_wks=False)
        try:
            val = self.wks.cell(row, col).value
        except:
            raise ValueError('Potentially row or column are out of bounds.')
        return val

    def write_value(self, row, col, msg, name_spr='', name_wks=''):
        """
         Writes a value to a cell.
         :param row:            Row to write the data to.
         :param col:            Column to write the data to.
         :param msg:            Message that will be written.
         :param name_spr:       (Optional) name_spr in case there is no previous access to this spreadsheet from this instance.
         :param name_wks:       (Optional) name_spr in case there is no previous access to this worksheet from this instance.
         :return:
        """
        self._check_wks_existence(name_spr, name_wks, create_wks=True)
        cell = form_cell(col, row)
        self.wks.update_acell(cell, msg)
        return 1

    def readrange(self, row, row_end, col, col_end, name_spr='', name_wks=''):
        """
         Reads a range of cells and returns their values.
         :param row:            Starting row to read.
         :param row_end:        Ending row.
         :param col:            Starting column.
         :param col_end:        Ending column.
         :param name_spr:       (Optional) name_spr in case there is no previous access to this spreadsheet from this instance.
         :param name_wks:       (Optional) name_spr in case there is no previous access to this worksheet from this instance.
         :return:
        """
        if (row_end < row) | (col_end < col):
            raise ValueError('Mistake with the range values.')
        self._check_wks_existence(name_spr, name_wks, create_wks=False)
        cell_1 = form_cell(col, row)
        cell_2 = form_cell(col_end, row_end)
        try:
            val = self.wks.range(cell_1 + ':' + cell_2)
        except:
            raise ValueError('Potentially row or column are out of bounds.')
        return val

def form_cell(col, row):
    """Auxiliary function for creating a cell in the format that gspread requires (e.g. from (7,9) -> \'G9\')"""
    cell = chr(96 + col)
    if col > 26:                      # in case col>26, then it is in the form of AA, AB, ...
        first_term = col/26
        col -= first_term*26
        cell = chr(96 + first_term) + chr(96 + col)
    cell = cell.upper() + str(row)
    return cell


# def make_backup(name_spr, uid, pass1, backup_name='Copy' ):
#     """This function creates a copy/backup of an existing spreadsheet. """
#
#     sp = login_find_spreadsheet(name_spr, uid, pass1, 'False')
#     try:
#         import gdata.docs.client
#     except:
#         raise ImportError('Package gdata does not exist, cannot create backup')
#     docs_client = gdata.docs.client.DocsClient()
#     docs_client.ClientLogin(uid, pass1,'any')
#     base_resource = docs_client.GetResourceById(sp.id)
#     docs_client.copy_resource(base_resource, backup_name)



def check_nr_args(args1, requested_nr, func):
    # checks whether the number of arguments is sufficient.
    if args1 != requested_nr:
        raise RuntimeError("The requested number of arguments is not met in the call of " + func + ".")

# call from terminal with full argument list:
if __name__ == '__main__':
    args = len(sys.argv)
    if args < 2:
        print("Not enough arguments for selecting an option in " + sys.argv[0])
        raise Exception()
    option = int(sys.argv[1])
    sp = Spreadsheets(sys.argv[2])
    if option == 1:
        check_nr_args(args, 8, 'write_value')
        val = sp.write_value(int(sys.argv[3]), int(sys.argv[4]), sys.argv[5], sys.argv[6], sys.argv[7])
        # writeInSpreadsheet(sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5]), sys.argv[6], sys.argv[7], sys.argv[8])
        # val = 0  # dummy value
    elif option == 2:
        check_nr_args(args, 7, 'read_value')
        val = sp.read_value(int(sys.argv[3]), int(sys.argv[4]), sys.argv[5], sys.argv[6])
    elif option == 3:
        check_nr_args(args, 9, 'readrange')
        val = sp.readrange(int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]),
                           sys.argv[7], sys.argv[8])
    else:
        val = 0
        raise Exception('Invalid option.')
    print(val)
