import gspread
import sys
# grigoris, 24 July 2014:
# all functions of editing of spreadsheets can be called from another python script.
# Also, they can be called from the terminal with arguments as argv.
# There are the following options:
#   1) readFromSpreadsheet          read a single cell from a spreadsheet
#   2) writeInSpreadsheet           write in a single cell
#   3) readrange                    read the values of a range of cells

# Copyright (C) 2014 Grigorios G. Chrysos
# available under the terms of the Apache License, Version 2.0

# for functions login_find_spreadsheet, form_cell, readFromSpreadsheet, writeInSpreadsheet, readrange
# the input values are:
    # Input:
    # name_spr          name of the spreadsheet
    # name_wks          name of the worksheet
    # row               row that it will be written
    # col               column (in number) that it will be written
    # ms                the message that will be written
    # uid               used id (or e-mail) for login in drive
    # pass1             password for drive

def login_find_spreadsheet(name_spr, uid, pass1, create_sp = 'True'):
    # grigoris, 24 July 2014: This function makes the login to drive and tracks the spreadsheet.
    # if anything goes wrong, it raises and exception.

    # Login with your Google account
    try:
        gc = gspread.login(uid, pass1)
    except:
        print "Identification with google drive failed"
        raise Exception("Identification with google drive failed")

    # Open a spreadsheet or create it if it doesn't exist
    try:
        spreadsheet = gc.open(name_spr)
    except:
        #print "No such spreadsheet with name " + name_spr
        #raise Exception()
	if create_sp=='False': 
	    raise Exception('The spreadsheet does not exist')
	try:
	    import gdata.docs.client
	except:
	    raise Exception('The spreadsheet does not exist and'+
		'gdata is not installed, so it cannot be created')
	print('The gdoc did not exist and is created')
	docs_client = gdata.docs.client.DocsClient()
	docs_client.ClientLogin(uid, pass1,'any')
	document = gdata.docs.data.Resource(type='spreadsheet', 
			title=name_spr)
	resource = docs_client.CreateResource(document)
	full_id = resource.resource_id.text # returned by gdata
	gs_id = full_id[len('spreadsheet:'):] 
	spreadsheet = gc.open_by_key(gs_id)
    return spreadsheet


def form_cell(col, row):
    # form the cell (row, col) in the expected format (eg 'G9')
    cell = chr(96 + col)
    if col > 26:                      # in case col>26, then it is in the form of AA, AB, ...
        first_term = col/26
        col = col - first_term*26
        cell = chr(96 + first_term) + chr(96 + col)
    cell = cell.upper() + str(row)
    return cell


def readFromSpreadsheet(name_spr, name_wks, row, col, uid, pass1):
    # grigoris, 24 July 2014: This function reads a message from a cell.

    spreadsheet = login_find_spreadsheet(name_spr, uid, pass1)
    try:
        wks = spreadsheet.worksheet(name_wks)
    except:                     # in case it does not exist, we create this worksheet
        print "No such worksheet with name " + name_wks

    try:
        val = wks.cell(row, col).value
    except:
        print "Potentially row or column are out of bounds."
        raise Exception()
    return val


def writeInSpreadsheet(name_spr, name_wks, row, col, msg, uid, pass1):
    # grigoris, 24 July 2014: This function writes in a spreadsheet a message.
    # If the worksheet does not exist, it creates it.

    spreadsheet = login_find_spreadsheet(name_spr, uid, pass1)
    try:
        wks = spreadsheet.worksheet(name_wks)
    except:                     # in case it does not exist, we create this worksheet
        wks = spreadsheet.add_worksheet(title=name_wks, rows="70", cols="70")

    cell = form_cell(col, row)

    # write in the worksheet
    try:
        wks.update_acell(cell, msg)
    except:
        print "Potentially row or column are out of bounds."
        raise Exception()


def readrange(name_spr, name_wks, row, row_end, col, col_end, uid, pass1):
    # grigoris, 24 July 2014: This function reads a message from a range of cells
    if (row_end < row) | (col_end < col):
        print "Mistake with the range values."
        raise Exception()
    spreadsheet = login_find_spreadsheet(name_spr, uid, pass1)
    try:
        wks = spreadsheet.worksheet(name_wks)
    except:                     # in case it does not exist, we create this worksheet
        print "No such worksheet with name " + name_wks
    cell_1 = form_cell(col, row)
    cell_2 = form_cell(col_end, row_end)
    try:
        val = wks.range(cell_1 + ':' + cell_2)
    except:
        print "Potentially row or column are out of bounds."
        raise Exception()
    return val


def make_backup(name_spr, uid, pass1, backup_name = 'Copy' ):
    # grigoris, 16/12/2014: This function creates a copy/backup of the existing name_spr spreadsheet
    sp = login_find_spreadsheet(name_spr,uid,pass1,'False')
    try:
	import gdata.docs.client
    except:
	raise Exception('Package gdata does not exist, cannot create backup')
    docs_client = gdata.docs.client.DocsClient()
    docs_client.ClientLogin(uid, pass1,'any')
    base_resource = docs_client.GetResourceById(sp.id)
    docs_client.copy_resource(base_resource, backup_name)


# example call through another python script or in terminal with no arguments
#writeInSpreadsheet("python_test", "Sheet2", 11, 14,11, 'your_mail@gmail.com', 'pass' )
#print readFromSpreadsheet("python_test", "Sheet2", 11, 14, 'your_mail@gmail.com', 'pass' )

def check_nr_args(args, requested_nr, func):
    # checks whether the number of arguments is sufficient
    if args != requested_nr:
        print "The requested number of arguments is not met in the call of " + func + "."
        raise Exception()

# call from terminal with full argument list:
if __name__ == '__main__':
    args = len(sys.argv)
    if args < 2:
        print "Not enough arguments for selecting an option in " + sys.argv[0]
        raise Exception()
    option = int(sys.argv[1])
    if option == 1:
        check_nr_args(args, 9, 'writeInSpreadsheet')
        writeInSpreadsheet(sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5]), sys.argv[6], sys.argv[7], sys.argv[8])
        val = 0  # dummy value
    elif option == 2:
        check_nr_args(args, 8, 'readFromSpreadsheet')
        val = readFromSpreadsheet(sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5]), sys.argv[6], sys.argv[7])
    elif option == 3:
        check_nr_args(args, 10, 'readrange')
        val = readrange(sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]),
                                  int(sys.argv[7]), sys.argv[8], sys.argv[9])
    else:
        print "Invalid option."
        val = 0
        raise Exception()
    print val
