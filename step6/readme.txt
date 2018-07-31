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

Usage: step6.py file1 file2
	file1 is the revised bid with matched max prices highlited in red from buyer
	file2 is the generated aggregated final bids from buyer
	eg: step6.py revised_buyer_bid.xls buyer_final_price.csv
