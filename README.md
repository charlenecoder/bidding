# bidding
@author:    Charlene Zhong
@E-mail:    charlenezhong0101@gmail.com
bidding processing

The bidding prcess has seven steps, each step process input files and generate results according to different business logic, the source code and test samples are under each folder

step 1

process bidding sheet from buyer, get the price and put it to formated bidding sheet from upstream seller generated result will be used in step2

step 2

process formated bid from buyer generated in step1, adjust profit margin, generate formated bids that can be sent to upstream sellers

step 3

process max bid from supplier, sort the sheet according to file2 so that our interested items are on the top the resulted file2 will be used in step4

step 4

process formated bid from buyer generated in step1, and sorted supplier max file generated in step 3, generate max bids that can be sent to downstream buyers

step 5

process revised bid sent back by downstream buyers, accepted price is marked as red and sorted supplier max file generated in step 3, generate update bids that can be sent to upstream suppliers

step 6 

process both the first and second round of bids from buyer, generate a final buyer's bidding sheet for result processing.

step 7

use the final prices to supplier and from buyer to generate a comparing auction result list
