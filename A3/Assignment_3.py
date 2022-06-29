
from cProfile import label
from pickle import TRUE
from tkinter import Label
import numpy as np
import scipy.special as sc
import scipy.linalg as sl
import matplotlib.pyplot as plt

rows = np.linspace(0,101,101)
columns = np.linspace(1,9,9)


#question 3
try:
   x = np.loadtxt("fitting.dat", dtype='float') #loading data
except OSError:
    print('error occured in opening the file')

                                                                                                  
sigma= np.logspace(-1,-3,9) #generating sigma values
p = np.array([[1.05, -0.105]]).T
time = x[:,0]
data = x[:,1:] #extracting data
   

#question 4
def g(t,A,B):
      return (A*sc.jn(2,t)+B*t) # defining g function for future use

#question 3

y = []
for i in range(len(sigma)):
    y.append(f"$\sigma${i+1}={sigma[i]: .5f}") #for adding the sigma to the graph label
plt.plot(x[:,0], x[:,1:], label=y)
plt.plot(x[:,0],g(x[:,0], 1.05, -0.105), color="k", label='True Value')
plt.legend() 
plt.xlabel("time")
plt.ylabel("f(t)+noise")
plt.title(' f(t) +noise vs time')
plt.show() #plots f(t) +noise vs time graph

 #question 5
# plt.errorbar(x[::5,0],x[::5,1],sigma[0],fmt='ro', label = 'error bar')
# plt.plot(x[:,0],g(x[:,0], 1.05, -0.105), color="k", label = 'true value')
# plt.legend()
# plt.title('stddev error bar')
# plt.show() #stdev error bar graph is plotted

j_t = sc.jn(2,time)
M = np.c_[j_t, time]

#print(p)

result = np.matmul(M, p)
#print(result)

np.array_equal(result, g(time, 1.05, -0.105))
if TRUE:
    print("arrays are equal")
else:
    print("error")

#defining A and B values
A1 = np.linspace(0,2,21)
B1 = np.linspace(-0.2,0,21)


#question 7
E = np.zeros([21,21])
for j in range(len(A1)):
    for k in range(len(B1)):
        for l in range(len(rows)):
            E[j][k] += (x[l][1]- g(x[l][0], A1[j], B1[k]))**2/101 #finding the “mean squared error” between the data (fk) and the assumed model
            

#question 8
cnt=plt.contour(A1,B1,E, levels = 20)
# plt.clabel(cnt)
# plt.xlabel('A')
# plt.ylabel('B')
# plt.title('contourplot of e vs A,B')
# plt.show()#gives us the contourplot of e vs A,B

#question 9
u =sl.lstsq(M, x[:,1] )
print(u) #using lstsq to obtain the best estimate of A and B



# Using scipy.linalg.lstsq to find least squares solution
def lstsq(input):
    return([sl.lstsq(M,input)[0][0], sl.lstsq(M,input)[0][1]])

# Estimate A and B for all sigma values
def manydata():
    error_a = []
    error_b =[]
    for s in sigma:  # Iterating over all sigma values
        est_a = []
        est_b = []
        for i in range(1000): # 1000 data files
            y = np.random.normal(scale=s, size = (101))
            est = lstsq(y+g(x[:,0],1.05,-0.105))
            est_a.append(est[0])
            est_b.append(est[1])
        error_a.append(np.square(np.subtract(1.05,est_a)/1.05).mean())   
        error_b.append(np.square(np.subtract(-0.105,est_b)/-0.105).mean())   # Calculating normalised MSE
 
    return [error_a, error_b]

mse = manydata()


#question 11
# Plot in loglog
# plt.loglog(sigma, mse[0], label = 'A')
# plt.loglog(sigma, mse[1], label = 'B')
# plt.xlabel('sigma')
# plt.ylabel('Normalised MSE Error')
# plt.legend()
# plt.title('Normalised error in estimating A, B over 1000 data files (loglog)')
# plt.show()


#question 10
# Plot in linear
# plt.plot(sigma, mse[0], label = 'A')
# plt.plot(sigma, mse[1], label = 'B')
# plt.xlabel('sigma')
# plt.ylabel('Normalised MSE Error')
# plt.legend()
# plt.title('Normalised error in estimating A, B over 1000 data files (linear)')
# plt.show()

