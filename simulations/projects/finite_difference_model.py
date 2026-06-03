import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd
from datetime import datetime
#Option Call
sigma= .20 #Volatility
e= 300 #Exercise Price 
r= .10 #RFR

#Creating Grid
k=1000 #Time Steps
i=100 #stock Steps 


time= 2
s_max= 400
dt= time/k

time_grid= np.linspace(0,time,k)
price_grid= np.linspace(0,s_max,i)

v_mat= np.zeros((i,k))

#Boundary Condition
v_mat[:,-1]= np.maximum(price_grid-e,0) #Final Condition
v_mat[0,:] = 0 #Lower Boundary
for n in range(k):
    tau= time- time_grid[n]
    v_mat[-1,n]= s_max - e*np.exp(-r*tau)


for t in range(k-1,0,-1):
    for n in range(1,i-1):
        A= ((.5)*(n**2)*(sigma**2)-.5*(n)*(r))*dt
        B= 1- ((n**2)*sigma**2-r)*dt
        C= ((.5)*(n**2)*(sigma**2)+.5*(n)*(r))*dt
        v_mat[n,t-1]= A*v_mat[n-1,t]+B*v_mat[n,t]+C*v_mat[n+1,t]

np.set_printoptions(precision=2)

print(price_grid)
print(v_mat)

print ("-------------------")
print(v_mat[:,-1])
print(np.maximum(price_grid-e,0))
plt.plot(price_grid, v_mat[:,0])
plt.xlabel("Stock Price")
plt.ylabel("Option Value")
plt.title("Option Value at t=0")
plt.grid(True)
plt.show()