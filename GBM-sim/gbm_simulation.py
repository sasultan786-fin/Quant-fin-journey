import numpy as np
import matplotlib.pyplot as plt

"""
def start():
    print("This is a stock price simulator which uses GBM simulations. Select one of the following:\n"
    "1. Simulate using own inputs\n"
    "2. Simulate a PSX stock")1
    choice= input("Option: ")
    return choice

choice= start()

if choice== "1":
    S0= float(input("Initial Stock Price: "))
    sigma= float(input("Volatility (Sigma): "))
    r= float(input("Risk-free rate: "))
    time= int(input("Time Period: "))

elif choice== "2":
    print("Choice 2")

"""

def gbm_func(price,r,sigma,dt,z):
    return price*np.exp((r-(1/2)*sigma**2)*dt+sigma*np.sqrt(dt)*z)

#Inputs

S0= 100
sigma= .20
r= .08
time= 1

n= 252 #Time Steps
dt=time/n

#Initialising Grids i.e X and Y Axis
time_grid= np.linspace(0,time,n+1) #X axis for graph
stock_path= np.zeros(n+1) #Stock Path Array

stock_path[0]= S0 #Initial Value is set to Current Stock Price

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
