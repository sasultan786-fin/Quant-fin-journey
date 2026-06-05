import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd
from datetime import datetime
import time
''''
print("This is a finite difference Option price calculator. Please enter the following inputs: ")
time.sleep(1)

while True:
    sigma= float(input("Volatility (Sigma): "))
    e= float(input("Strike Price (E): "))
    r= float(input("Risk free rate(r): "))
    k= int(input("Time steps(k): "))
    i= int(input("Stock Steps(i): "))
    t= int(input("Time: "))
    s_max= 1.5*e
    o_type= input("Option Type(Call/Put): ").lower()
    o_style= input("Option_Style(European/American): ").lower()
    dt= t/k
    stability_test= 1/(sigma**2*i**2)
    if dt>stability_test:
        time.sleep(1)
        print("Unstable parameters chosen!\n" \
        f"Current dt= {dt:.6f}\n"\
        f"Suggested maximum dt= {stability_test:.6f}\n"\
        "Please choose finer discretization.")
        continue
    break
'''

#Option Call
sigma= .20 #Volatility
e= 300 #Exercise Price 
r= .10 #RFR
o_type= "call"
k=2000 #Time Steps
i=50 #stock Steps 
t= 2
dt= t/k
s_max= 400
o_style= "american"
#Creating Grid
time_grid= np.linspace(0,t,k)
price_grid= np.linspace(0,s_max,i)
v_mat= np.zeros((i,k))

#Boundary Condition Option Type Call
if o_type=="call":
    v_mat[:,-1]= np.maximum(price_grid-e,0) #Final Condition
    v_mat[0,:] = 0 #Lower Boundary
    if o_style=="european":
        for n in range(k):
            tau= t- time_grid[n]
            v_mat[-1,n]= s_max - e*np.exp(-r*tau)
    elif o_style=="american":
        v_mat[-1,:]= s_max- e
elif o_type=="put":
    v_mat[:,-1]= np.maximum(e-price_grid,0) #Final Condition
    v_mat[-1,:] = 0 #Upper Boundary
    if o_style=="european":
        for n in range(k):
            tau= t- time_grid[n]#Lower Boundary
            v_mat[0,n]= e*np.exp(-r*tau)
    elif o_style=="american":
        v_mat[0,:] = e


for l in range(k-1,0,-1):
    for x in range(1,i-1):
        A= ((.5)*(x**2)*(sigma**2)-.5*(x)*(r))*dt
        B= 1-((x**2)*sigma**2+r)*dt
        C= ((.5)*(x**2)*(sigma**2)+.5*(x)*(r))*dt
        if o_style=="european":
            v_mat[x,l-1]= A*v_mat[x-1,l]+B*v_mat[x,l]+C*v_mat[x+1,l]
        elif o_style=="american":
            contin_val= A*v_mat[x-1,l]+B*v_mat[x,l]+C*v_mat[x+1,l]
            if o_type=="call":
                exercise_val= np.maximum(price_grid[x]-e,0)
            elif o_type=="put":
                exercise_val= np.maximum(e- price_grid[x],0)
            v_mat[x,l-1]= np.maximum(contin_val,exercise_val)


'''
s0= float(input("Please enter the current Stock price for option value: "))
'''
s0= 250
value_index= np.argmin(np.abs(price_grid-s0))
option_val= v_mat[value_index,0]

print("\n===============================================" )
print("Model Summary Statistics:\n" \
    "---------------------------------------------" )
time.sleep(1)
''''
print(f"Option Type: {o_type} \n" \
f"Current Stock Price: {s0}\n" \
f"Strike Price: {e}\n" \
f"Volatility: {sigma*100:.2f}%\n" \
f"Risk Free Rate: {r*100:.2f}%\n" \
f"Time to Maturity: {t}\n" \
    "---------------------------------------------")
time.sleep(2)
print("Finite Difference Option Price\n"\
"---------------------------------------------\n" \

f"Option Value: {option_val:.2f}\n" \
"===============================================" )

'''
np.set_printoptions(precision=2)

print ("-------------------")

print(v_mat[:10,-1])   # maturity
print(v_mat[:10,-2])   # first backward step

print(v_mat[:10,0])
print(price_grid[:10])

plt.plot(price_grid, v_mat[:,0])
plt.xlabel("Stock Price")
plt.ylabel("Option Value")
plt.title("Option Value at t=0")
plt.grid(True)
plt.show()

plt.plot(price_grid, v_mat[:,-1], label="Payoff at Maturity")
plt.plot(price_grid, v_mat[:,0], label="Option Value Today")
plt.legend()
plt.grid(True)
plt.show()
