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

Usage:  step2.py file1 file2
	file1 is formated bid from buyers from step1
	file2 is bid need to be generated and sent to upstream sellers
	both file needs to in csv format
	eg: step2.py formated_bid_from_buyer.csv final_bid_to_seller.csv
