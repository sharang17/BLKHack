import  numpy as np
import pandas as pd

#function to convert data set to our main portfolio
def generate_Main_Port():
    price_data =pd.read_csv("r3000_price_update.csv")
    price_data= price_data.dropna(axis =1)
    main_portfolio=pd.read_csv("MainPortfolio.csv")
    ticker=main_portfolio.loc[:,"Ticker"]
    ticker=["Date"]+list(ticker)
    main_portfolio_price=price_data.loc[:,ticker]
    print(main_portfolio_price.cov())
    main_portfolio_price.to_csv("MainPortfolioPrice.csv",index=False)
    # tickers= list(price_data.columns)
    # tickers=tickers[1:len(tickers)]
    # dates=price_data.loc[:,"Date"]
    # price_data.to_csv("r3000_price_update.csv")
    # for i in range(len(dates)-104):
    #     np.cov(price_data[i:i+104,["APPL",""]])
    # print(dates)


def Generate_STORM_Risk():

    #price data is price and date data
    price_data =pd.read_csv("MainPortfolioPrice.csv")
    #price table only consists of price data
    price_table=price_data.ix[:,1:len(list(price_data))]
    tickers=list(price_table)
    return_table=np.log(price_table)
    return_table=return_table.diff()
    print(return_table)
    #first row in return is NULL
    return_table=pd.DataFrame(return_table.dropna())


    # #return dates is when return could be calcualted
    dates=price_data.loc[:,"Date"]
    return_dates=list(dates[1:])
    #save return table to csv
    return_table["Date"]=return_dates
    return_table.to_csv("return_table.csv",index=False)
    return_table.reset_index(inplace=True,drop=True)
    #delete date column for return table
    return_table = return_table.drop("Date", 1)
    start=0
    period=153
    for i in range(start,len(return_dates)-period):
        temp_date=return_dates[i+period].replace("/","_")
        file_name=temp_date+"_Storm_Risk.csv"
        return_table.ix[i:i+period+1,:].cov().to_csv("STORM_Risk/"+file_name)

def Generate_STOMR_Single_Risk():
    Generate_STORM_Risk()
    price_data=pd.read_csv("MainPortfolioPrice.csv")
    return_table=pd.read_csv("return_table.csv")
    #delete date column for covariancce calculation
    return_table = return_table.drop("Date", 1)
    price_table=price_data.ix[:,1:len(list(price_data))]


    dates=price_data.loc[:,"Date"]
    return_dates=list(dates[1:])
    risk_list=[]
    start=0
    period=153

    #Note that here I am calculating variance, result table is
    # table for variance not sd
    for i in range(start,len(return_dates)-period):
        temp_risk_table=return_table.ix[i:i+period+1,:].cov()
        temp_risk_diagnoal =  np.diagonal(temp_risk_table)
        risk_list.append(temp_risk_diagnoal)

    single_risk_table=pd.DataFrame(risk_list)
    single_risk_table["Date"]=list(return_dates[153:])
    #print(len(list(return_dates[153:])))
    #print(return_dates[153+1])
    #print(single_risk_table)
    name_var=list(price_table)+["Date"]
    single_risk_table.columns =name_var
    single_risk_table.to_csv("STORM_single_risk.csv",index=False)

if __name__ == "__main__":
    Generate_STORM_Risk()