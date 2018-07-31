#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author:    Charlene Zhong
@email:     charlenezhong0101@gmail.com
@purpose:   process revised bid sent back by downstream buyers, 
            accepted price is marked as red
            and sorted supplier max file generated in step 3, 
            generate update bids that can be sent to upstream suppliers
@notic:     For file1
            only proces up to 1000 lines
            please make sure the bidding items are in top 1000 lines in file1
@created:   12/08/2014
@updated:   06/05/2018
"""
import xlrd
import csv
import sys
import os
import os.path

#profit margin for different models
#adjust according to market price
p_ip4 = 0.3
p_ip5 = 0.4
p_ip6 = 0.8
p_ip7 = 1.0
p_ip8 = 2.0
p_ipx = 3.0
p_ipad = 0.6
p_other = 0.5
#file1 is the revised bid sent back by downstream buyers
file1 = None
#file 2 is the sorted supplier max file generated in step 3
file2 = None
#file 3 is the updated bids that can be sent to upstream suppliers
file2 = None
#book object used to open revised buyer bids in xls formate
book = None
#sheet object to open sheet in book
sheet = None

# print usage
def print_help(program):
    print("Usage: ", program, "file1 file2 file3")
    print("\tfile1 is the revised bid sent back by downstream buyers")
    print("\tfile2 is the sorted supplier max file generated in step 3")
    print("\tfile3 is the updated bids that can be sent to upstream suppliers")
    print("\tfile1 needs to in xls format")
    print("\tfile2 and file3 needs to in csv format")
    print("\teg:", program, "revised_buyer_bid.xls sorted_supplier_max.csv updated_bid_to_supplier.csv")
    return None

# parse command line arguments
# validate if the arguments are existing files
def parse_and_validate_arg():
    global file1
    global file2
    global file3
    if len(sys.argv) != 4:
        print_help(sys.argv[0])
        return False
    else:
        file1 = sys.argv[1]
        file2 = sys.argv[2]
        file3 = sys.argv[3]
    path1 = './' + file1
    path2 = './' + file2
    path3 = './' + file3
    if os.path.isfile(path1) == False or os.access(path1, os.R_OK) == False:
        print(file1, "is missing or not readable");
        print_help(sys.argv[0])
        return False
    if os.path.isfile(path2) == False or os.access(path2, os.R_OK) == False:
        print(file2, "is missing or not readable");
        print_help(sys.argv[0])
        return False
    if os.path.isfile(path3) == False or os.access(path3, os.R_OK) == False:
        print(file3, "is missing or not readable");
        print_help(sys.argv[0])
        return False
    print("Get file1:", file1, "file2:", file2, "file3:", file3)
    return True

# check if string is a float
def isfloat(value):
    try:
        float(value)
        return True
    except:
        return False

# check if price is marked as red by buyer in file1
def red(row,col):
    global book
    global sheet

    #print("red input:", row, col)
    xfx = sheet.cell_xf_index(row,col)
    xf = book.xf_list[xfx]
    bgx = xf.background.pattern_colour_index
    if(bgx == 10):
        return True
    else:
        return False

# process file1 file2 and file3, write result back to file3
def process():
    global file1
    global file2
    global file3
    global book
    global sheet
    global p_ip4
    global p_ip5
    global p_ip6
    global p_ip7
    global p_ip8
    global p_ipx
    global p_ipad
    global p_other
    print("Start to process", file1, file2, "and", file3)

    #open workbook file1 sent back by buyer
    book = xlrd.open_workbook(file1, formatting_info=True)
    sheet = book.sheet_by_index(0)

    # open file2 and file3, encoding is added due to encoding error 
    # if the saved csv file is not UTF-8 encoded
    # with error message
    # UnicodeDecodeError: 'utf-8' codec can't decode byte 0xcd in position 3680: invalid continuation byte
    supplier_max = csv.reader(open(file2, 'r', encoding = "ISO-8859-1"))
    update = csv.reader(open(file3,'r',encoding = "ISO-8859-1"))
    profit = None
    orig_price = None
    #load initial update sheet to lists
    lists = list(update)

    #copy all the supplier max price to update
    for i,row in enumerate(supplier_max):
        if i > 0 and i < 1000:
            #print(i, ":", row)
            #print(i, ":", lists[i])
            #error out if Part Name not match
            if(lists[i][5] != row[5]):
                print("Part Name not match on line", i, "in", file2, "and", file3)
                print("In", file2, "it's", row[5])
                print("In", file3, "it's", lists[i][5])
                return None
            for j in range(9, 25, 2):
                if isfloat(row[j]) == False:
                    lists[i][j] = 0
                else:
                    lists[i][j] = float(row[j])

    for row in range(1, 1000):
        for col in range(8, 24, 2):
            thecell = sheet.cell(row, col)
            # if buyer mark it red, we will use upplier max in update
            if red(row, col + 1) == True:
                #print("red:",row,col);
                lists[row][col] = lists[row][col + 1]
            else:
                if thecell.value and float(thecell.value) > 0.0:
                    # get Part Name and set profit
                    name = lists[row][5]
                    # error out if Part Name does not match
                    if name != sheet.cell(row, 5).value:
                        print("Part Name not match on line", row, "in", file1, "and", file3)
                        print("In", file1, "it's", sheet.cell(row, 5).value)
                        print("In", file3, "it's", name)
                        return None
                    if 'iPhone 4' in name:
                        profit = p_ip4
                    elif 'iPhone 5' in name:
                        profit = p_ip5
                    elif 'iPhone 6' in name:
                        profit = p_ip6
                    elif 'iPhone 7' in name:
                        profit = p_ip7
                    elif 'iPhone 8' in name:
                        profit = p_ip8
                    elif 'iPhone X' in name:
                        profit = p_ipx
                    elif 'iPad' in name:
                        profit = p_ipad
                    else:
                        profit = p_other
                    if isfloat(sheet.cell(row,col).value) == False:
                        orig_price = 0
                    else:
                        orig_price = float(sheet.cell(row,col).value)
                    if orig_price > 10:
                        lists[row][col] = orig_price - profit
                    else:
                        lists[row][col] = orig_price - orig_price * 0.33

    #write back to file3
    writer  = csv.writer(open(file3, 'w'))
    writer.writerows(lists)
    print("upload max buyer price to", file3)
    return None

def main():
    #parse and validate arguments
    if parse_and_validate_arg() == False:
        return None
    #process bidding files
    process()
    return None

if __name__ == '__main__':
    main()

