import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd
from datetime import datetime


def IR_model(rate,kappa,theta,sigma,dt,z,model_type):
    if model_type== 1 or model_type== 2:
        return rate+kappa*(theta-rate)*dt+sigma*np.sqrt(dt)*z
    elif model_type== 3:
        return rate+kappa*(theta-rate)*dt+sigma*np.sqrt(dt)*np.sqrt(np.maximum(rate,0))*z

print('This is a model that simulates interest rates.')
print('\n Please select the type of Model Simulated:\n' \
'1.OU Process\n' \
'2.Vasicek\n' \
'3.CIR \n')
model_type= int(input("Model Type: "))

print("Please enter the following inputs:\n")
kappa= float(input("Speed of reversion (Kappa): "))
sigma= float(input("Volatility(Sigma): "))
r0= float(input("Initial Interest Rate(R0): "))
t= float(input("Enter Time Period: "))

n= int(input("Enter the number of time steps: "))
m= int(input("Enter the number of total simulations: "))

if model_type!= 1:
    theta= float(input("Long Term Mean(Theta): "))
else:
    theta=0

dt=t/n

time_grid= np.linspace(0,t,n)
rate_path= np.zeros((m,n))

rate_path[:,0]= r0 #Setting the first data point to R0

for i in range(n-1):
    z= np.random.normal(size=m)
    rate_path[:,i+1]=IR_model(rate_path[:,i],kappa,theta,sigma,dt,z,model_type)

path_num= int(input("Please Enter the number of Paths to display in the graph: "))
plt.plot(time_grid,rate_path[path_num,:].T)
plt.title("Simulated Stock Price",fontsize=16)
plt.xlabel("Time",fontsize=12)
plt.ylabel("Stock Price",fontsize=12)
plt.grid(True)
plt.show()