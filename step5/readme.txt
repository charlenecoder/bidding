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

Usage:  step5.py file1 file2 file3
	file1 is the revised bid sent back by downstream buyers
	file2 is the sorted supplier max file generated in step 3
	file3 is the updated bids that can be sent to upstream suppliers
	file1 needs to in xls format
	file2 and file3 needs to in csv format
	eg: step5.py revised_buyer_bid.xls sorted_supplier_max.csv updated_bid_to_supplier.csv
