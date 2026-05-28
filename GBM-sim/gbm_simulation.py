import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd
from datetime import datetime

def fetch_inputs_stock(ticker):

    today = datetime.today().strftime('%Y-%m-%d')
    data = yf.download(ticker,start='2023-01-01', end=today)
    closing_prices= data['Close'].squeeze()
    date=data.index

    log_returns= np.log(closing_prices/closing_prices.shift(1))
    log_returns = log_returns.dropna()
    daily_mean= log_returns.mean()
    mean_ann= daily_mean*252# historical drift u

    daily_sigma= log_returns.std()
    sigma_ann= daily_sigma*np.sqrt(252)# value of sigma

    S0 = closing_prices.iloc[-1] #Price at the last date

    return mean_ann, sigma_ann, S0
 
def gbm_func(price,r,sigma,dt,z):
    return price*np.exp((r-(1/2)*sigma**2)*dt+sigma*np.sqrt(dt)*z)

def start():
    print("This is a stock price simulator which uses GBM simulations. Select one of the following:\n"
    "1. Simulate using own inputs\n"
    "2. Simulate a PSX stock")
    choice= input("Option: ")
    return choice

choice= start()

if choice== "1":
    S0= float(input("Initial Stock Price: "))
    sigma= float(input("Volatility (Sigma): "))
    r= float(input("Risk-free rate: "))
    time= int(input("Time Period: "))

elif choice== "2":
    while True:
        try:
            input_ticker= input('Please enter the ticker for the stock (e.g UBL.KA for united bank limited): ')
            r,sigma,S0 = fetch_inputs_stock(input_ticker)
            break
        except:
            print('Invalid Ticker. Please try again.')
    time= int(input("Time Period: "))

n= 252 #Time Steps
dt=time/n

#Initialising Grids i.e X and Y Axis
time_grid= np.linspace(0,time,n+1) #X axis for graph
stock_path= np.zeros(n+1) #Stock Path Array

stock_path[0]= float(S0) #Initial Value is set to Current Stock Price

#Main Loop

for i in range(n):
    z= np.random.normal()
    stock_path[i+1]= gbm_func(stock_path[i],r,sigma,dt,z)

# Making Plot
plt.plot(time_grid,stock_path)
plt.title("Simulated Stock Price",fontsize=16)
plt.xlabel("Time",fontsize=12)
plt.ylabel("Stock Price",fontsize=12)
plt.grid(True)
plt.show()

