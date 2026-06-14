import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd
from datetime import datetime
import time

#--------------------------------------------------------------------------------------------------------------------------
#Output Print Function
#--------------------------------------------------------------------------------------------------------------------------

def print_summary_statistics():

    s0= float(input("Please enter the current Stock price for option value: "))

    s0= 250
    value_index= np.argmin(np.abs(price_grid-s0))
    option_val= v_mat[value_index,0]

    print("\n===============================================" )
    print("Model Summary Statistics:\n" \
        "---------------------------------------------" )
    time.sleep(1)

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

#--------------------------------------------------------------------------------------------------------------------------
#Plotting Functions
#--------------------------------------------------------------------------------------------------------------------------

def plot_option_value(price_grid, v_mat):
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

#--------------------------------------------------------------------------------------------------------------------------
#Assign Boundary Conditions:
#--------------------------------------------------------------------------------------------------------------------------

def assign_boundary_conditions(v_mat):
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

#--------------------------------------------------------------------------------------------------------------------------
#Implicit Scheme:
#--------------------------------------------------------------------------------------------------------------------------

def implicit_scheme():
    v_mat= np.zeros((i,k))
    assign_boundary_conditions(v_mat)
    kmat= np.zeros((i-2,i-2))
    rhs=np.zeros((i-2))
    upper_c=0
    lower_a=0
    for x in range(i-2):
        n= x+1
        a= (-.5*n**2*sigma**2+.5*n*r)*dt
        b= 1+(n**2*sigma**2+r)*dt
        c= (-.5*n**2*sigma**2-.5*n*r)*dt
        if x>0:
            kmat[x,x-1]=a
        elif x==0:
            lower_a=a
        kmat[x,x]=b
        if x<i-3:
            kmat[x,x+1]=c
        elif x==i-3:
            upper_c=c

    for l in range(k-1,0,-1):
        rhs= v_mat[1:-1,l].copy()
        rhs[0] -= lower_a*v_mat[0,l]
        rhs[-1] -= upper_c*v_mat[-1,l]

        v_mat[1:-1,l-1]= np.linalg.solve(kmat,rhs)
    return v_mat

#--------------------------------------------------------------------------------------------------------------------------
#Explicit Scheme Matrix Method
#--------------------------------------------------------------------------------------------------------------------------

def explicit_scheme_matrix():
    emat=np.zeros((i-2,i))
    for x in range(i-2):
        n= x+1
        A= ((.5)*(n**2)*(sigma**2)-.5*(n)*(r))*dt
        emat[x,x]=A
        B= 1-((n**2)*sigma**2+r)*dt
        emat[x,x+1]=B
        C= ((.5)*(n**2)*(sigma**2)+.5*(n)*(r))*dt
        emat[x,x+2]=C

    print(emat[-1,:])

    for l in range(k-1,0,-1):
        v_mat[1:-1,l-1]= emat @ v_mat[:,l]

    print(v_mat[:,-1])
        
    print(v_mat[:-10,k-2])
    return v_mat

#--------------------------------------------------------------------------------------------------------------------------
#Excplicit Scheme Manual Recursion Method grid style
#--------------------------------------------------------------------------------------------------------------------------

def explicit_scheme_manual():
    v_mat = np.zeros((i,k))
    assign_boundary_conditions(v_mat, price_grid, time_grid, o_type, o_style, s_max, e, r)
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
    return v_mat

#--------------------------------------------------------------------------------------------------------------------------
#Crank Nicholson
#--------------------------------------------------------------------------------------------------------------------------

def crank_nicholson():
    v_mat = np.zeros((i,k))
    assign_boundary_conditions(v_mat, price_grid, time_grid, o_type, o_style, s_max, e, r)
    cnmat= np.zeros((i-2,i-2))
    I = np.eye(i-2)
    A_lower=0
    C_upper=0

    for x in range(i-2):
        n=x+1
        A= 1/4*dt*(sigma**2*n**2-r*n)
        if x==0:
            A_lower=A
        elif x>0:
            cnmat[x,x-1]= A
        B= -1/2*dt*(sigma**2*n**2+r)
        cnmat[x,x]= B
        C= 1/4*dt*(sigma**2*n**2+r*n)
        if x<i-3:
            cnmat[x,x+1]=C
        elif x==i-3:
            C_upper= C
    matr= I+cnmat.copy()
    matl= I-cnmat.copy()
    for l in range(k-1,0,-1):
        rhs= (matr) @ v_mat[1:-1,l].copy()
        rhs[0] += A_lower*v_mat[0,l-1] + A_lower*v_mat[0,l]
        rhs[-1] += C_upper*v_mat[-1,l-1] + C_upper*v_mat[-1,l]
        v_mat[1:-1,l-1]=np.linalg.solve(matl,rhs)
    return v_mat

#--------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------

#Running the model

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

time_grid= np.linspace(0,t,k)
price_grid= np.linspace(0,s_max,i)

v_mat= implicit_scheme()
print_summary_statistics()
plot_option_value(price_grid, v_mat)
