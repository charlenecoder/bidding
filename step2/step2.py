#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author:    Charlene Zhong
@email:     charlenezhong0101@gmail.com
@purpose:   process formated bid from buyer generated in step1,
            adjust profit margin, 
            generate formated bids that can be sent to upstream sellers
@notic:     For file2
            only proces up to 1000 lines
            please make sure the bidding items are in top 1000 lines in file2
@created:   12/08/2014
@updated:   06/05/2018
"""
import csv
import sys
import os
import os.path

#profit margin for different models
#adjust according to market price
p_ip4 = 0.6
p_ip5 = 0.8
p_ip6 = 1.2
p_ip7 = 1.5
p_ip8 = 2.0
p_ipx = 3.0
p_ipad = 1.0
p_other = 0.8
#file1 is the formated bidding file from buyers generated in step1
file1 = None
#file 2 is the bidding file that can be sent to upstream sellers
file2 = None

# print usage
def print_help(program):
    print("Usage: ", program, "file1 file2")
    print("\tfile1 is formated bid from buyers from step1")
    print("\tfile2 is bid need to be generated and sent to upstream sellers")
    print("\tboth file needs to in csv format")
    print("\teg:", program, "formated_bid_from_buyer.csv final_bid_to_seller.csv")
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
    global p_ip4
    global p_ip5
    global p_ip6
    global p_ip7
    global p_ip8
    global p_ipx
    global p_ipad
    global p_other
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
            # only proces up to 1000 lines
            # please make sure the bidding items are in top 1000 lines in file2
            if i > 0 and i < 1000:
                name = row[5]
                #print("name is",name)
                for line in lines:
	            #print(line)
	            #print("line[5]", line[5])
                    # find corresponding model and their profit
                    if line[5] == name:
                        if "iPhone 4" in name:
                            profit = p_ip4
                        elif "iPhone 5" in name:
                            profit = p_ip5
                        elif "iPhone 6" in name:
                            profit = p_ip6
                        elif "iPhone 7" in name:
                            profit = p_ip7
                        elif "iPhone 8" in name:
                            profit = p_ip8
                        elif "iPhone X" in name:
                            profit = p_ipx
                        elif "iPad" in name:
                            profit = p_ipad
                        else:
                            profit = p_other
                        # update price
                        for col in range(8, 24, 2):
                            #print("i=", i, "col=", col)
                            # test if price is valid
                            if isfloat(row[col]) == False:
                                #set to 0
                                line[col] = 0
                            else:
                                price = float(row[col])
                                # leave profit margin only if price is higher than profit
                                # and price is higher than 10
                                if price > profit and price > 10:
                                    line[col] = price - profit
                                # otherwise cut the price to half
                                else:
                                    line[col] = price / 2

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
