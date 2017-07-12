import pandas as pd 
import io

ticker = "PFE"
file_obj = open("equityHistorical.json","w")
file_obj.write("  \"" + ticker + "\": [\n")

historicalPricesList = []
colnames = ['Date','Adj Close']
filename = 'CSV/' + ticker + '.csv'
data = pd.read_csv(filename,usecols=colnames)
date = data['Date'].values.tolist()
adj_close = data['Adj Close'].values.tolist()
delimeter = ","
for i in range(0,len(date)) :
    hist_entry = {}
    hist_entry["date"] = date[i]
    hist_entry["value"] = adj_close[i]
    nxtline = "\n"
    if i != (len(date)-1):
        nxtline = delimeter + nxtline
    file_obj.write("    " + str(hist_entry).replace("'","\"") + nxtline)
file_obj.write("  ],")