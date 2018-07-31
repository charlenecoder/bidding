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

Usage:  step4.py file1 file2 file3
	file1 is formated bid from buyers from step1
	file2 is the sorted supplier max file generated in step 3
	file3 is the updated buyer max price that will be sent to downstream buyer
	all the file needs to in csv format
	eg: step4.py formated_buyer_bid.csv sorted_supplier_max.csv max_bid_to_buyer.csv
