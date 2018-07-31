#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author:    Charlene Zhong
@email:     charlenezhong0101@gmail.com
@purpose:   process bidding sheet from buyer, 
            get the price and put it to formated bidding sheet from upstream seller
            generated result will be used in step2
@created:   12/08/2014
@updated:   06/05/2018
"""
import csv
import sys
import os
import os.path

#file1 is the bidding file from buyers
file1 = None
#file 2 is the bidding file that have format needed for upstream supplier
file2 = None
#max possible price, incase there is typo
max_price = 1000

# print usage
def print_help(program):
    print("Usage: ", program, "file1 file2")
    print("\tfile1 is the original bid from buyers")
    print("\tfile2 is the formated bidding sheet from upstream seller")
    print("\tboth file needs to in csv format")
    print("\teg:", program, "orig_bid_from_buyer.csv formatted_buyer_bid.csv")
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
    global max_price
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
            # start from second line, the first line is header
            if i > 0:
                name = row[0]
	        #print("name is",name)
                for line in lines:
                    #print(line)
                    #print("line[5]", line[5])
                    # find corresponding model
                    if line[5] == name:
                        # upload buyer's first round bidding
                        for col in range(2,10):
                            #print(row[col])
                            # test if price is valid
                            if isfloat(row[col]) == False:
                                #set to 0
                                line[2*(col-2)+8] = 0
                            else:
                                price = float(row[col])
                                # if price is too high, might be typo
                                if price > max_price:
                                    print("price in", file1, "row", i, "col", end = " ")
                                    print(col, "is", price, "bigger than max", max_price)
                                    return None;
                                # check if it's for iPad or iPhone
                                if "iPad" in name or "iPhone" in name:
                                    if price > 0:
                                        line[2*(col-2)+8] = price
                                    else:
                                        if row[1] == line[4] and price > 0:
                                            line[2*(col-2)+8] = price
    #write back to file2
    writer  = csv.writer(open(file2, 'w'))
    writer.writerows(lines)
    print("upload bidding price to", file2)
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
