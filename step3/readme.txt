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

Usage:  step3.py file1 file2
	file1 is the file with max bidding price sent from supplier
	file2 is the sorted sheet has our interest items on top
	both file needs to in csv format
	the resulted file2 will be used in step4
	eg: step3.py supplier_max.csv sorted_supplier_max.csv
