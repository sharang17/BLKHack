import pandas as pd
import numpy as np
import json
import collections
import io

Names=pd.read_csv("MainPortfolio.csv")
stockName=list(Names.ix[:,"Company Name"])
stockTicker=list(Names.ix[:,"Ticker"])
Date="12/30/2016"
Stock_Price= pd.read_csv("MainPortfolioPrice.csv")
#print(Stock_Price)
select_column=Stock_Price["Date"] == Date
Stock_Price=Stock_Price.loc[select_column].ix[:,stockTicker].values[0]

#get risk

Stock_Risk=pd.read_csv("STORM_Single_Risk.csv")
select_column=Stock_Risk["Date"] == Date
Stock_Risk=Stock_Risk.loc[select_column].ix[:,stockTicker].values[0]
Stock_Risk=np.sqrt(Stock_Risk*52)*100

Stock_Coefficient=pd.read_csv("r3000_beta_adj.csv")
Stock_Coefficient=Stock_Coefficient.ix[:,stockTicker+["Date"]]
select_column=Stock_Coefficient["Date"] == Date
Stock_Coefficient=Stock_Coefficient.loc[select_column].ix[:,stockTicker].values[0]






try:
    to_unicode = unicode
except NameError:
    to_unicode = str

stocksAndBonds = {}
stockInformationList = []
for x in range (0,len(stockName)) :
    stockInfo = collections.OrderedDict();
    stockInfo["name"] = stockName[x]
    stockInfo["ticker"] = stockTicker[x]
    stockInfo["value"] = Stock_Price[x]
    stockInfo["coefficient"] = Stock_Coefficient[x]
    stockInfo["risk"] = Stock_Risk[x]
    stockInformationList.append(stockInfo)
stocksAndBonds["stocks"] = stockInformationList
stocksAndBonds["bonds"] = []
with io.open('StocksViaBonds.json', 'w', encoding='utf8') as outfile:
    str_ = json.dumps(stocksAndBonds,
                      indent=4, sort_keys=False,
                      separators=(',', ': '), ensure_ascii=False)
    outfile.write(to_unicode(str_))