import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd
from datetime import datetime
import time

def IR_model(rate,kappa,theta,sigma,dt,z,model_type):
    if model_type== 1 or model_type== 2:
        return rate+kappa*(theta-rate)*dt+sigma*np.sqrt(dt)*z
    elif model_type== 3:
        return rate+kappa*(theta-rate)*dt+sigma*np.sqrt(dt)*np.sqrt(np.maximum(rate,0))*z
    
def model_name(model_type):
    if model_type==1:
        return "OU Process"
    elif model_type==2:
        return "Vasicek"
    elif model_type==3:
        return "CIR"
def model_stats(terminal_values):
    avg_rate= terminal_values.mean()
    min_rate= terminal_values.min()
    max_rate= terminal_values.max()
    dev_rate= terminal_values.std()
    return avg_rate,min_rate,max_rate,dev_rate

def plot_graph(x_axis,y_axis,paths_num=1,title="",x_title="",y_title=""):
    plt.plot(x_axis,y_axis[:path_num,:].T)
    plt.title(title,fontsize=16)
    plt.xlabel(x_title,fontsize=12)
    plt.ylabel(y_title,fontsize=12)
    plt.grid(True)
    plt.show()

def print_summary_stats(inputs,outputs):
    print("===============================================" )
    print("Model Summary Statistics:\n" \
    "---------------------------------------------\n" \
    f"Model: {model_name(model_type)} \n" \
    f"Initial Rate: {r0}\n" \
    f"Long Run Mean: {theta} \n" \
    f"Volatility: {sigma}\n" \
    f"Mean Reversion Speed: {kappa}\n" \
    "---------------------------------------------\n" \
    "Simulation Results\n"\
    "---------------------------------------------\n" \
    f"Average Terminal Rate: {outputs[0]:.2f}\n" \
    f"Minimum Terminal Rate: {outputs[1]:.2f}\n" \
    f"Maximum Terminal Rate: {outputs[2]:.2f}\n" \
    f"Terminal Rate Deviation: {outputs[3]:.2f}\n" \
    "\n" \
    "===============================================" )

print('This is a model that simulates interest rates.')
print('\n Please select the type of Model Simulated:\n' \
'1.OU Process\n' \
'2.Vasicek\n' \
'3.CIR \n' \
'4.Simulate all three models side by side')
model_type= int(input("Model Type: "))

print("\nPlease enter the following inputs(in decimals):\n")
time.sleep(1)
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

#Main Engine

if model_type!=4:
    rate_path= np.zeros((m,n))
    rate_path[:,0]= r0 #Setting the first data point to R0
    for i in range(n-1):
        z= np.random.normal(size=m)
        rate_path[:,i+1]=IR_model(rate_path[:,i],kappa,theta,sigma,dt,z,model_type)

    avg_rate,min_rate,max_rate,dev_rate= model_stats(rate_path[:,-1])

    print("\n===============================================" )
    print("Model Summary Statistics:\n" \
    "---------------------------------------------" )
    time.sleep(1)

    print(f"Model: {model_name(model_type)} \n" \
    f"Initial Rate: {r0*100:.2f}%\n" \
    f"Long Run Mean: {theta*100:.2f}%\n" \
    f"Volatility: {sigma*100:.2f}%\n" \
    f"Mean Reversion Speed: {kappa:.2f}\n" \
    "---------------------------------------------")
    time.sleep(2)
    print("Simulation Results\n"\
    "---------------------------------------------\n" \
    f"Average Terminal Rate: {avg_rate*100:.2f}%\n" \
    f"Minimum Terminal Rate: {min_rate*100:.2f}%\n" \
    f"Maximum Terminal Rate: {max_rate*100:.2f}%\n" \
    f"Terminal Rate Deviation: {dev_rate*100:.2f}%\n" \
    "===============================================" )

    time.sleep(2)
    path_num= int(input("Please Enter the number of Paths to display in the graph: "))
    plot_graph(time_grid,rate_path,path_num,"Interest Rate Model", "Time", "Interest Rates")

else:

    rate_path= np.zeros((3,m,n)) # 0 index for OU, 1 index for Vasicek and 2 index for CIR
    rate_path[:,:,0]= r0 #Setting the first data point to R0

    for i in range(n-1):
        z= np.random.normal(size=m)
        rate_path[0,:,i+1]=IR_model(rate_path[0,:,i],kappa,0,sigma,dt,z,1)
        rate_path[1,:,i+1]=IR_model(rate_path[1,:,i],kappa,theta,sigma,dt,z,2)
        rate_path[2,:,i+1]=IR_model(rate_path[2,:,i],kappa,theta,sigma,dt,z,3)
    path_num= int(input("Please enter the number of paths in each plot: "))
    fig, axes = plt.subplots(1,3, figsize=(18,6))
    for p in range(path_num):
        axes[0].plot(time_grid,rate_path[0,p,:])
        axes[1].plot(time_grid,rate_path[1,p,:])
        axes[2].plot(time_grid,rate_path[2,p,:])

    axes[0].grid(True)
    axes[1].grid(True)
    axes[2].grid(True)
    axes[0].set_title("OU Process")
    axes[1].set_title("Vasicek Model")
    axes[2].set_title("CIR Model")
    for ax in axes:
        ax.set_xlabel("Time")
        ax.set_ylabel("Interest Rate")
    plt.tight_layout()
    plt.show()