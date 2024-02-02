# An AI classifer and spending tracker for Singapore Bank statements 



This is a tracker that lets you automatically format and classify transactions in bank statement. You can then pivot and create charts as you like to track. 

### Steps to use:

1.download csv files from Standard chartered, UOB and DBS banks and copy them to the folder /bankfiles

2. run the batch file run.bat

3. on a successful run, the formatted and classified transactions will be updated in masteretl.csv

### Optional: 

4. copy the records in masteretl.csv to 'financial tracker 2.0.xlsm' sheet 'expenses'

5. edit the 'head' column in expenses to reflect your desired classifications. 

6. uncomment the training code block in predhead.py to train a new model on your classifications


This project arose out of my need to track my expenses across multiple banks with aligned classifications. 
I  trained the included model on about 18 months of records that I had cleaned and classified. The model predicts the heads with about 92% accuracy. For example, it will reliably classify a transaction saying NTUC F/P as groceries. (NTUC fairprice is a singaporean supermarket chain). Fixing the remaining errors is usually not too onerous. 
I have not been successful in getting beyond 92% accuracy, mainly because there is some ambiguity in the transaction descriptions. Adding in other features only seems to lower the accuracy. 




