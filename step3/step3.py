#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author:    Charlene Zhong
@email:     charlenezhong0101@gmail.com
@purpose:   process max bid from supplier, sort the sheet according to file2
            so that our interested items are on the top
            the resulted file2 will be used in step4
@notic:     For file1
            only proces up to 1400 lines
@created:   12/08/2014
@updated:   06/05/2018
"""
import csv
import sys
import os
import os.path

#file1 is the file with max bidding price sent from supplier
file1 = None
#file 2 is the sorted sheet has our interest items on top
file2 = None

# print usage
def print_help(program):
    print("Usage: ", program, "file1 file2")
    print("\tfile1 is the file with max bidding price sent from supplier")
    print("\tfile2 is the sorted sheet has our interest items on top")
    print("\tboth file needs to in csv format")
    print("\tthe resulted file2 will be used in step4")
    print("\teg:", program, "supplier_max.csv sorted_supplier_max.csv")
    return None

# parse command line arguments
# validate if the arguments are existing files
def parse_and_validate_arg():
    global file1
    global file2
    if len(sys.argv) != 3:
        print_help(sys.argv[0])
        return False
    else:
        file1 = sys.argv[1]
        file2 = sys.argv[2]
    path1 = './' + file1
    path2 = './' + file2
    if os.path.isfile(path1) == False or os.access(path1, os.R_OK) == False:
        print(file1, "is missing or not readable");
        print_help(sys.argv[0])
        return False
    if os.path.isfile(path2) == False or os.access(path2, os.R_OK) == False:
        print(file2, "is missing or not readable");
        print_help(sys.argv[0])
        return False
    print("Get file1:", file1, "file2:", file2)
    return True

# check if string is a float
def isfloat(value):
    try:
        float(value)
        return True
    except:
        return False

# process file1 and file2, write result back to file2
def process():
    global file1
    global file2
    cnumber = None
    cname = None
    cstart = None

    print("Start to process", file1, "and", file2)
    # open file1 and file2, encoding is added due to encoding error 
    # if the saved csv file is not UTF-8 encoded
    # with error message
    # UnicodeDecodeError: 'utf-8' codec can't decode byte 0xcd in position 3680: invalid continuation byte
    with open(file1, 'r', encoding = "ISO-8859-1") as fd1, open(file2, 'r', encoding = "ISO-8859-1") as fd2:
        reader1 = csv.reader(fd1)
        reader2 = csv.reader(fd2)
        # put file2 in lists
        lines = list(reader2)
        #print(lines)

        # read each line in file1
        # save index in i, each line in row
        for i, row in enumerate(reader1):
            #print(i,row)
            # header line
            if i == 0:
                # get Part number, Part Name and start column of price
                # incase the supplier's sheet is out of order
                for j in range(0,len(row)):
                    name = row[j]
                    if name == "Part Number":
                        cnumber = j
                    elif name == "Part Name":
                        cname = j
                    elif name == "Max of grade a-yyy":
                        cstart = j
                #print(i, row, cnumber, cname, cstart)
            # start from second line, the first line is header
            # only proces up to 1400 lines
            if i > 0 and i < 1400:
                name = row[cname]
                #print(i,"name is",name)
                for line in lines:
                    #print(line)
                    #print("line[5]", line[5], "line[4]", line[4])
                    # Part name needs to match
                    if line[5] == name:
                        # for iPhone and iPad
                        if "iPhone" in name or "iPad" in name:
                            #print(line)
                            #print(row[cstart + col - 9])
                            for col in range(9, 25, 2):
                                line[col] = row[cstart + col - 9]
                                #print(row[cstart + col - 9])
                        # other devices need to match Part Number
                        else:
                            if row[cnumber] == line[4]:
                                for col in range(9, 25, 2):
                                    line[col] = row[cstart + col - 9]
    #write back to file2
    writer  = csv.writer(open(file2, 'w'))
    writer.writerows(lines)
    print("upload sorted max price to", file2)
    return None

def main():
    #parse and validate arguments
    if parse_and_validate_arg() == False:
        return None
    #process max price files
    process()
    return None

if __name__ == '__main__':
    main()
