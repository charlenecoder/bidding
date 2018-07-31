#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author:    Charlene Zhong
@E-mail:    charlenezhong0101@gmail.com
@purpose:   use the final prices to supplier and from buyer to 
            generate a comparing auction result list
@created:   05/18/2015
@updated:   06/16/2018
"""
import csv
import sys
import xlrd
import os
import os.path

file1 = None
file2 = None
file3 = None
book1 = None
revise = None
book2 = None
buyer_final = None
book2 = None
buyer_final = None

# print usage information
def Print_help(program):
    print("Usage:", program, "file file2 file3")
    print("\tfile1 is the updated bids send to the supplier generated in step5")
    print("\tfile2 is the final bids from the buyer generated in step6")
    print("\tfile3 is the biding result from supplier and to buyer")
    print("\tfile1 and file2 needs to be xls format")
    print("\tfile3 needs to be csv format")
    print("\teg:", program, "updated_bid_to_supplier.xls buyer_final_price.xls  biding_result.csv")
    return None

# validate if the files are existing and readable
def parse_argv():
    global file1
    global file2
    global file3

    if len(sys.argv) != 4:
        Print_help(sys.argv[0])
        return False
    else:
        file1 = sys.argv[1]
        file2 = sys.argv[2]
        file3 = sys.argv[3]

    path1 = './'+file1
    path2 = './'+file2
    path3 = './'+file3

    if os.path.isfile(path1) == False or os.access(path1, os.R_OK) == False:
        print(file1, "is missing or not readable")
        Print_help(sys.argv[0])
        return False
    if os.path.isfile(path2) == False or os.access(path2, os.R_OK) == False:
        print(file2,"is missing or not readable")
        Print_help(sys.argv[0])
        return False
    if os.path.isfile(path3) == False or os.access(path3, os.R_OK) == False:
        print(file3, "is missing or not readable")
        Print_help(sys.argv[0])
        return False

def process():
    global file1
    global file2
    global file3
    global book1
    global revise
    global book2
    global buyer_final
    print("start to process:",file1,file2,file3)

    # open file1
    book1 = xlrd.open_workbook(file1)
    revise = book1.sheet_by_index(0)

    # open file2
    book2 = xlrd.open_workbook(file2)
    buyer_final = book2.sheet_by_index(0)

    # open file3
    outfile = csv.reader(open(file3,'r', encoding = "ISO-8859_1"))
    lists = list(outfile)

    # retrive final buyer's price and final auction price to the supplier 
    # according to the auction result and generate a compare list 
    for index in range(2, len(lists)):
        for row in range(1,1000):
            name = revise.cell(row, 5).value
            if name in lists[index][1]:
                for i in range(0, 8):
                    # print("row", row, "i", i, "col", 8 + i * 2, revise.cell(row, 8 + i * 2).value)
                    lists[index][3 + i * 3] = float(revise.cell(row, 8 + i * 2).value)
    
    for index in range(2, len(lists)):
        for row in range(1,1000):
            name = buyer_final.cell(row, 5).value
            if len(name) > 3 and name in lists[index][1]:
                for i in range(0, 8):
                    lists[index][4 + i * 3] = float(buyer_final.cell(row, 8 + i * 2).value)
    # save the data from lists to file3
    writer = csv.writer(open(file3,'w'))
    writer.writerows(lists)
    print("upload sorted max price to", file3)
    return None

def main():
    if parse_argv() == False:
        return None
    process()
    return None
if __name__ == '__main__':
    main()
