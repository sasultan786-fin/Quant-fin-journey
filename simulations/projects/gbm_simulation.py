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
    mean_ann= daily_mean*252# Historical drift u

    daily_sigma= log_returns.std()
    sigma_ann= daily_sigma*np.sqrt(252)# value of sigma

    S0 = closing_prices.iloc[-1] #Price at the last date

    return mean_ann, sigma_ann, S0

def gbm_func(price,r,sigma,dt,z):
    return price*np.exp((r-(1/2)*sigma**2)*dt+sigma*np.sqrt(dt)*z)

def start():
    print("This is a stock price simulator which uses GBM simulations. Select one of the following:\n"
    "1. Simulate using own inputs\n"
    "2. Simulate a PSX stock\n")
    choice= input("Option: ")
    return choice

choice= start()

if choice== "1":
    S0= float(input("Initial Stock Price: "))
    sigma= float(input("Volatility (Sigma): "))
    time= float(input("Time Period (in Years): "))
    option_type= input("Option Type(call or put): ")
    k= float(input("Strike Price: "))

elif choice== "2":
    while True:
        try:
            input_ticker= input('Please enter the ticker for the stock (e.g UBL.KA for united bank limited): ')
            mu,sigma,S0 = fetch_inputs_stock(input_ticker)
            break
        except:
            print('Invalid Ticker. Please try again.')
    print(f"\nThe current price of the stock is {S0:.2f}\n")
    option_type= input("Option type(call or put): ")
    k= float(input("Strike Price: "))
    time= float(input("Time Period (in Years): "))


r = 0.158# taken from investing.com (https://www.investing.com/rates-bonds/pakistan-1-year-bond-yield)
n= 252 #Time Steps
dt=time/n
m=1000  #Number of Paths

#Initialising Grids i.e X and Y Axis
time_grid= np.linspace(0,time,n) #X axis for graph
stock_path= np.zeros((m,n)) #Stock Path Array
payoff_mat= np.zeros(m)

stock_path[:,0]= float(S0) #Initial Value is set to Current Stock Price

#Main Loop

for i in range(n-1):
    z= np.random.normal(size=m)
    stock_path[:,i+1]= gbm_func(stock_path[:,i],r,sigma,dt,z)


if option_type=='call':
    payoff_mat= np.maximum(stock_path[:,n-1]-k,0)
    payoff= payoff_mat.mean()
elif option_type=='put':
    payoff_mat= np.maximum(k-stock_path[:,n-1],0)
    payoff= payoff_mat.mean()

option_price= payoff*np.exp(-r*(time))

terminal_price= np.mean(stock_path[:,-1])
print("The expected stock price after",time,f"years is {terminal_price:.2f}")
print(f"The price of the {option_type} on the stock is {option_price:.2f}")

# Plotting All Paths

plt.plot(time_grid,stock_path.T)
plt.title("Simulated Stock Price",fontsize=16)
plt.xlabel("Time",fontsize=12)
plt.ylabel("Stock Price",fontsize=12)
plt.grid(True)
plt.show()

