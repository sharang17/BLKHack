import json
import collections
import io

try:
    to_unicode = unicode
except NameError:
    to_unicode = str
stockName = ["s1","s2","s3","s4","s5"]
stockTicker = ["t1","t2","t3","t4","t5"]
stocksAndBonds = {}
stockInformationList = []
for x in range (0,len(stockName)) :
    stockInfo = collections.OrderedDict();
    stockInfo["name"] = stockName[x]
    stockInfo["ticker"] = stockName[x]
    stockInfo["value"] = stockName[x]
    stockInfo["coefficient"] = stockName[x]
    stockInfo["risk"] = stockName[x]
    stockInformationList.append(stockInfo)
stocksAndBonds["stocks"] = stockInformationList
stocksAndBonds["bonds"] = []
with io.open('StocksViaBonds.json', 'w', encoding='utf8') as outfile:
    str_ = json.dumps(stocksAndBonds,
                      indent=4, sort_keys=False,
                      separators=(',', ': '), ensure_ascii=False)
    outfile.write(to_unicode(str_))