#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author:    Charlene Zhong
@email:     charlenezhong0101@gmail.com
@purpose:   process formated bid from buyer generated in step1,
            and sorted supplier max file generated in step 3, 
            generate max bids that can be sent to downstream buyers
@notic:     For file1
            only proces up to 1000 lines
            please make sure the bidding items are in top 1000 lines in file1
@created:   12/08/2014
@updated:   06/05/2018
"""
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
#file1 is the formated bidding file from buyers generated in step1
file1 = None
#file 2 is the sorted supplier max file generated in step 3
file2 = None
#file 3 is the updated buyer max price that will be sent to downstream buyer
file2 = None

# print usage
def print_help(program):
    print("Usage: ", program, "file1 file2 file3")
    print("\tfile1 is formated bid from buyers from step1")
    print("\tfile2 is the sorted supplier max file generated in step 3")
    print("\tfile3 is the updated buyer max price that will be sent to downstream buyer")
    print("\tall the file needs to in csv format")
    print("\teg:", program, "formated_buyer_bid.csv sorted_supplier_max.csv max_bid_to_buyer.csv")
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

# process file1 file2 and file3, write result back to file3
def process():
    global file1
    global file2
    global file3
    global p_ip4
    global p_ip5
    global p_ip6
    global p_ip7
    global p_ip8
    global p_ipx
    global p_ipad
    global p_other
    print("Start to process", file1, file2, "and", file3)

    # open file1 file 2 and file3, encoding is added due to encoding error 
    # if the saved csv file is not UTF-8 encoded
    # with error message
    # UnicodeDecodeError: 'utf-8' codec can't decode byte 0xcd in position 3680: invalid continuation byte
    with open(file1, 'r', encoding = "ISO-8859-1") as fd1, open(file2, 'r', encoding = "ISO-8859-1") as fd2, open(file3, 'r', encoding = "ISO-8859-1") as fd3:
        buyer_bids = csv.reader(fd1)
        sorted_supplier_max = csv.reader(fd2)
        to_buyer_max = csv.reader(fd3)
        # put file2 and file3 in lists
        lines = list(to_buyer_max)
        supplier_max = list(sorted_supplier_max)
        #print(lines)

        # read each line in file1
        # save index in i, each line in row
        for i, row in enumerate(buyer_bids):
            #print(i,row)
            # find model and their profit
            name = row[5]
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

            # start from second line, the first line is header
            # only proces up to 1000 lines
            # please make sure the bidding items are in top 1000 lines in file1
            if i > 0 and i < 1000:
                #print("name is",name)
                #for line in lines:
	            #print(line)
	            #print("line[5]", line[5])
                # Part Name needs to match
                if lines[i][5] == name and supplier_max[i][5] == name:
                    for col in range(8, 24, 2):
                        # copy original buyer's price back
                        if isfloat(row[col]) == False:
                            price = 0
                        else:
                            price = float(row[col])
                        if price > 0:
                            lines[i][col] = price
                    for col in range(9, 25, 2):
                        if isfloat(supplier_max[i][col]) == False:
                            price = 0
                        else:
                            price = float(supplier_max[i][col])
                        if isfloat(row[col - 1]) == False:
                            bid = 0
                        else:
                            bid = float(row[col - 1])
                        # if buyer's bid already higher than supplier's max + profit
                        # set max to buyer's bidding price
                        if bid >= price + profit:
                            lines[i][col] = bid
                        # otherwise set max price to supplier's max price + profit
                        else:
                            lines[i][col] = price + profit
                else:
                    # Part Name not match, Error out
                    print("Error happen in line", i, "name is different in col 6")
                    print("In file", file1, "is:", name)
                    print("In file", file3, "is:", lines[i][5])
                    print("In file", file2, "is:", supplier_max[i][5])
                    return None;

    #write back to file3
    writer  = csv.writer(open(file3, 'w'))
    writer.writerows(lines)
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
