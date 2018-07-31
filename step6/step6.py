#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author:    Charlene Zhong
@email:     charlenezhong0101@gmail.com
@purpose:   process both the first and second round of bids from buyer, 
            generate a final buyer's bidding sheet for result processing
@notic:     For file2
            only proces up to 1000 lines
@created:   03/21/2015
@updated:   06/08/2018
"""
import csv
import sys
import xlrd
import os
import os.path

file1 = None
file2 = None
book = None
sheet = None
Max_price = 1000

# print usage
def print_help(program):
    print("Usage:", program, "file1 file2")
    print("\tfile1 is the revised bid with matched max prices highlited in red from buyer")
    print("\tfile2 is the generated aggregated final bids from buyer")
    print("\teg:", program,"revised_buyer_bid.xls buyer_final_price.csv")
    return None

# parse command line arguments
# validate if the arguments are existing and accesable files
def parse_arg():
    global file1
    global file2
    if len(sys.argv) != 3:
        print_help(sys.argv[0])
        return False
    else:
        file1 = sys.argv[1]
        file2 = sys.argv[2]

    path1='./'+file1
    path2='./'+file2
    if os.path.isfile(path1) ==False or os.access(path1, os.R_OK) == False:
        print(file1, "is missing or not readable")
        print_help(sys.argv[0])
        return False
    if os.path.isfile(file2) == False or os.access(path2, os.R_OK) == False:
        print(file2, "is missing or not readable")
        print_help(sys.argv[0])
        return False

# check if price is marked as red by buyer in file1
def red(row, col):
    global book
    global sheet
    xfx = sheet.cell_xf_index(row, col)
    xf = book.xf_list[xfx]
    bgx = xf.background.pattern_colour_index
    if(bgx == 10):
        return True
    else:
        return False

# process file1 and file2, return result to file2
def process():
    global file1
    global file2
    global book
    global sheet
    print("Start to process:", file1, file2)

    # open and read file1 with format
    book = xlrd.open_workbook(file1, formatting_info=True)
    sheet = book.sheet_by_index(0)

    # open file2, encoding is added due to encoding error 
    # if the saved csv file is not UTF-8 encoded
    # with error message
    # UnicodeDecodeError: 'utf-8' codec can't decode byte 0xcd in position 3680: invalid continuation byte
    with open(file2,'r', encoding = "ISO-8859-1") as fd2:
        reader2 = csv.reader(fd2)
        # put file2 in list
        lists = list(reader2)

        for row in range(1,1000):
            for col in range(8,24,2):
                # check if the cell is matched max price with red colour by buyer
                thecell = sheet.cell(row,col)
                if red(row, col + 1) == True:
                    # if the price is red colored, use the price as final price from buyer and transfer to list
                    lists[row][col] = sheet.cell(row,col + 1).value
                else:
                    # if the price is not red colored, use the original price from buyer and transfer to list
                    lists[row][col] = sheet.cell(row,col).value

    # transfer the price from list to file2
    writer = csv.writer(open(file2, 'w'))
    writer.writerows(lists)
    print("save buyer final bids to", file2)
    return None

def main():
    if parse_arg() == False:
        return None
    process()
    return None

if __name__ == '__main__':
    main()
