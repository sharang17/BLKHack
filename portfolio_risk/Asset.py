import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import newton

print("Start Program....Loading Data From Data Base")
#class of equtiy, which can return the risk of specific date
# and return the return of a certain period
return_table=pd.read_csv("return_table.csv")
STORM_Single_Risk_Table=pd.read_csv("STORM_single_risk.csv")
#get tickers
tickers=list(return_table)[0:(len(list(return_table))-1)]
dates=STORM_Single_Risk_Table.ix[:,"Date"]
#This dates vector is used to convert to specific date that we want
#storm risk Matrix is a table with only numbers we need
STORM_Risk_Matrix=pd.read_csv('STORM_Risk/12_30_2016_Storm_Risk.csv').ix[:,tickers]
STORM_Risk_Matrix=STORM_Risk_Matrix.as_matrix()
print("All Data is loaded")
#function to transfer ticker to index within our
def Get_Ticker_Index(ticker):
    index=tickers.index(ticker)
    return(index)

#function that we would use to find the correct weight
def target_risk_func(risk,portfolio):
    return(portfolio.get_rick()-risk)

#function we use to find optimal weight
def get_optimal_weight(initial_guess,target_risk,portfolio,index):
    portfolio._equity_weight[index]=initial_guess



class Equity(object):
    def __init__(self,ticker):
        #read what security need from ticker
        self._ticker=ticker
        #return and risk series also have Date
        self.risk_series=STORM_Single_Risk_Table.ix[:,[ticker,"Date"]]
        self.return_series=return_table.ix[:,[ticker,"Date"]]

    #date has the forma DD/MM/YYYY, note that there is no 0 before each number.
    # is 7/1/2016, not 07/01/2016
    def Get_Risk(self,date,all):
        #return the risk of a specific date or whole sequence of risk
        if all:
            return(np.sqrt(self.risk_series.ix[:,self._ticker]*52))
        else:
            #risk decomposition
            risk_total=self.risk_series.loc[self.risk_series["Date"]==date]
            #convert to a table
            risk_single=list(np.sqrt(risk_total.ix[:,self._ticker]*52))[0]
            return(risk_single)

    def Get_Return(self,start_date,end_date,all):
        #get return of time serie of stock
        if all:
            return(list(self.return_series.ix[:,self._ticker]))
        else:
            #all date is a pandas series
            all_date=self.return_series["Date"]
            first_index=all_date[all_date==start_date].index[0]
            second_index=all_date[all_date==end_date].index[0]
            temp_return=self.return_series.ix[first_index:(second_index),self._ticker]
            #return the result as list
            return(list(temp_return))

#class for child portfolio
class Child_Portfolio(object):
    #weight should be an 11 dimensional vector
    def __init__(self,equity_weight,ticker):
        self._equity_weight=equity_weight
        self._ticker=ticker
    def get_risk(self):
        #get risk of today
        temp_risk=np.dot(self._equity_weight,STORM_Risk_Matrix)
        final_risk=np.dot(temp_risk,self._equity_weight.transpose())
        return(np.sqrt(final_risk*52))
    def get_historical_risk(self):
        print("ha")
    def adjust_weight(self,new_weight):
        self._equity_weight=new_weight



if __name__ == "__main__":
    weight=np.array([0.25,0.25,0.25,0.25,0,0,0,0,0,0,0])
    test_port=Child_Portfolio(weight,"Tech")
    ticker="AAPL"

    get_optimal_weight(0.3,0.1,test_port,0)
    print(test_port._equity_weight)
    #print(STORM_Risk_Table[0,0])