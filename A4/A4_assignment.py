import math
import numpy as np
import pylab
from scipy.integrate import quad

# Function exp(x)
def exp(x):
    return np.exp(x)

# Function cos(cos(x))
def coscos(x):
    return np.cos(np.cos(x))

function={'exp(x)':exp,'cos(cos(x))':coscos}
# Function to Find Fourier Coefficient
def findingCoeff(n,func):
    coeff=np.zeros(n)                                         # Constructing A Array Filled With Zeros
    fourier=function[func]
    a=lambda x,k:fourier(x)*np.cos(k*x)                             # Cosine Function
    b=lambda x,k:fourier(x)*np.sin(k*x)                             # Sine Function
    coeff[0]=quad(fourier,0,2*np.pi)[0]/(2*np.pi)             # DC Coefficient
    for i in range(1,n,2):
        coeff[i]=quad(a,0,2*np.pi,args=((i+1)/2))[0]/np.pi    # Sine Coefficient
    for i in range(2,n,2):
        coeff[i]=quad(b,0,2*np.pi,args=(i/2))[0]/np.pi        # Cosine Coefficient
    return coeff

xActual=np.linspace(-2*np.pi,4*np.pi,300)       #  Evenly Spaced Numbers array over A Specified Interval
xExpected=np.linspace(0,2*np.pi,100)            # Constructing An Array Of Evenly Spaced Numbers Over A Specified Interval
xExpected=np.tile(xExpected,3)                  # Constructing An Array By Repeating xExpected Three Times


#true value and fourier comparision of exp(x)
pylab.figure(figsize=(7,6))                                         # Creating A New Figure
pylab.semilogy(xActual,exp(xActual),'-r',label='Actual')            # Making A Plot With Log Scaling On The y-axis
pylab.semilogy(xActual,exp(xExpected),'--g',label='Periodic')       # Making A Plot With Log Scaling On The y-axis
pylab.xlabel(r'x$\rightarrow$',fontsize=15)                         # Setting The Label For The x-axis
pylab.ylabel(r'$e^{x}\rightarrow$',fontsize=15)                     # Setting The Label For The y-axis
pylab.legend(loc='upper right')                                     # Placing A Legend On The Top Right Corner Of The Graph
pylab.grid(True)                                                    # Displaying The Grid
pylab.show()                                                        # Displaying The Figure


#cos(cos(x)) in linear scale
pylab.figure(figsize=(7,6))                                         # Creating A New Figure
pylab.plot(xActual,coscos(xActual),'-r',label='Actual')             # Ploting y vs x As Lines And Markers
pylab.plot(xActual,coscos(xExpected),'--g',label='Periodic')        # Ploting y vs x As Lines And Markers
pylab.xlabel(r'x$\rightarrow$',fontsize=15)                         # Setting The Label For The x-axis
pylab.ylabel(r'$\cos(\cos(x))\rightarrow$',fontsize=15)             # Setting The Label For The y-axis
pylab.legend(loc='upper right')                                     # Placing A Legend On The Top Right Corner Of The Graph
pylab.grid(True)                                                    # Displaying The Grid
pylab.show()                                                        # Displaying The Figure

coefficientExp=findingCoeff(51,'exp(x)')                 # Fourier Coefficients of exp(x)
coefficientCosCos=findingCoeff(51,'cos(cos(x))')         # Fourier Coefficients of cos(cos(x))


#Fourier Coefficients of f(x) by direct integration in loglog scale
pylab.figure(figsize=(7,6))                                         # Creating A New Figure
pylab.loglog(range(51),np.abs(coefficientExp),'ro')                 # Making A Plot With Log Scaling On Both The Axis
pylab.xlabel(r'n$\rightarrow$',fontsize=15)                         # Setting The Label For The x-axis
pylab.ylabel(r'Coefficient Magnitude$\rightarrow$',fontsize=15)     # Setting The Label For The y-axis
pylab.title('Fourier Coefficients Of $e^{x}$',fontsize=15)          # Setting Title Of The Graph
pylab.grid(True)                                                    # Displaying The Grid
pylab.show()                                                        # Displaying The Figure


#Fourier Coefficients of f(x) by direct integration in semilog scale
pylab.figure(figsize=(7,6))                                         # Creating A New Figure
pylab.semilogy(range(51),np.abs(coefficientExp),'ro')               # Making A Plot With Log Scaling On The y-axis
pylab.xlabel(r'n$\rightarrow$',fontsize=15)                         # Setting The Label For The x-axis
pylab.ylabel(r'Coefficient Magnitude$\rightarrow$',fontsize=15)     # Setting The Label For The y-axis
pylab.title('Fourier Coefficients Of $e^{x}$',fontsize=15)          # Setting Title Of The Graph
pylab.grid(True)                                                    # Displaying The Grid
pylab.show()                                                        # Displaying The Figure

#Fourier Coefficients of g(x) by direct integration in loglog scale
pylab.figure(figsize=(7,6))                                         # Creating A New Figure
pylab.loglog(range(51),np.abs(coefficientCosCos),'ro')              # Making A Plot With Log Scaling On Both The Axis
pylab.xlabel(r'n$\rightarrow$',fontsize=15)                         # Setting The Label For The x-axis
pylab.ylabel(r'Coefficient Magnitude$\rightarrow$',fontsize=15)     # Setting The Label For The y-axis
pylab.title('Fourier Coefficients Of $cos(cos(x))$',fontsize=15)    # Setting Title Of The Graph
pylab.grid(True)                                                    # Displaying The Grid
pylab.show()                                                        # Displaying The Figure

#Fourier Coefficients of g(x) by direct integration in semilog scale
pylab.figure(figsize=(7,6))                                         # Creating A New Figure
pylab.semilogy(range(51),np.abs(coefficientCosCos),'ro')            # Making A Plot With Log Scaling On Both The Axis
pylab.xlabel(r'n$\rightarrow$',fontsize=15)                         # Setting The Label For The x-axis
pylab.ylabel(r'Coefficient Magnitude$\rightarrow$',fontsize=15)     # Setting The Label For The y-axis
pylab.title('Fourier Coefficients Of $cos(cos(x))$',fontsize=15)    # Setting Title Of The Graph
pylab.grid(True)                                                    # Displaying The Grid
pylab.show()                                                        # Displaying The Figure

x=np.linspace(0,2*np.pi,400)
A=np.zeros((400,51))
A[:,0]=1
for k in range(1,26):
    A[:,2*k-1]=np.cos(k*x)
    A[:,2*k]=np.sin(k*x) 
bExp=exp(x)  
bCosCos=coscos(x)
cExp=np.linalg.lstsq(A,bExp,rcond=-1)[0]
cCosCos=np.linalg.lstsq(A,bCosCos,rcond=-1)[0]




pylab.loglog(range(51),np.abs(cExp),'go',label='Estimated Value')           # Making A Plot With Log Scaling On Both The Axis
pylab.loglog(range(51),np.abs(coefficientExp),'ro',label='True Value')      # Making A Plot With Log Scaling On Both The Axis
pylab.xlabel(r'n$\rightarrow$',fontsize=15)                                 # Setting The Label For The x-axis
pylab.ylabel(r'$Coefficient\rightarrow$',fontsize=15)                       # Setting The Label For The y-axis
pylab.legend(loc='upper right')                                             # Placing A Legend On The Top Right Corner Of The Graph
pylab.title('Fourier Coefficients Of $e^{x}$',fontsize=15)                  # Setting Title Of The Graph
pylab.grid(True)                                                            # Displaying The Grid
pylab.show()                                                                # Displaying The Figure


pylab.semilogy(range(51),np.abs(cExp),'go',label='Estimated Value')         # Making A Plot With Log Scaling On The y-axis
pylab.semilogy(range(51),np.abs(coefficientExp),'ro',label='True Value')    # Making A Plot With Log Scaling On The y-axis
pylab.xlabel(r'n$\rightarrow$',fontsize=15)                                 # Setting The Label For The x-axis
pylab.ylabel(r'$Coefficient\rightarrow$',fontsize=15)                       # Setting The Label For The y-axis
pylab.legend(loc='upper right')                                             # Placing A Legend On The Top Right Corner Of The Graph
pylab.title('Fourier Coefficients Of $e^{x}$',fontsize=15)                  # Setting Title Of The Graph
pylab.grid(True)                                                            # Displaying The Grid
pylab.show()                                                                # Displaying The Figure

#loglog Plot of cos(cos(x))
pylab.loglog(range(51),np.abs(cCosCos),'go',label='Estimated Value')        # Making A Plot With Log Scaling On Both The Axis
pylab.loglog(range(51),np.abs(coefficientCosCos),'ro',label='True Value')   # Making A Plot With Log Scaling On Both The Axis
pylab.xlabel(r'n$\rightarrow$',fontsize=15)                                 # Setting The Label For The x-axis
pylab.ylabel(r'$Coefficient\rightarrow$',fontsize=15)                       # Setting The Label For The y-axis
pylab.legend(loc='upper right')                                             # Placing A Legend On The Top Right Corner Of The Graph
pylab.title('Fourier Coefficients Of $cos(cos(x))$',fontsize=15)            # Setting Title Of The Graph
pylab.grid(True)                                                            # Displaying The Grid
pylab.show()                                                                # Displaying The Figure


#semilog plot of cos(cos(x))
pylab.semilogy(range(51),np.abs(cCosCos),'go',label='Estimated Value')      # Making A Plot With Log Scaling On The y-axis
pylab.semilogy(range(51),np.abs(coefficientCosCos),'ro',label='True Value') # Making A Plot With Log Scaling On The y-axis
pylab.xlabel(r'n$\rightarrow$',fontsize=15)                                 # Setting The Label For The x-axis
pylab.ylabel(r'$Coefficient\rightarrow$',fontsize=15)                       # Setting The Label For The y-axis
pylab.legend(loc='upper right')                                             # Placing A Legend On The Top Right Corner Of The Graph
pylab.title('Fourier Coefficients Of $cos(cos(x))$',fontsize=15)            # Setting Title Of The Graph
pylab.grid(True)                                                            # Displaying The Grid
pylab.show()                                                                # Displaying The Figure

deviationExp=abs(coefficientExp-cExp)
deviationCosCos=abs(coefficientCosCos-cCosCos)
maxDeviationExp=np.max(deviationExp)
maxDeviationCosCos=np.max(deviationCosCos)
print(maxDeviationExp)
print(maxDeviationCosCos)

#original and reconstructed function from fourier coefficients for e^x
approxExp=np.matmul(A,cExp)                                     # Matrix Product Of Two Arrays
pylab.semilogy(x,approxExp,'go',label="Approx value")           # Making A Plot With Log Scaling On The y-axis
pylab.semilogy(x,exp(x),'-r',label='True value')                # Making A Plot With Log Scaling On The y-axis
pylab.xlabel(r'n$\rightarrow$',fontsize=15)                     # Setting The Label For The x-axis
pylab.ylabel(r'$e^{x}\rightarrow$',fontsize=15)                 # Setting The Label For The y-axis
pylab.legend(loc='upper right')                                 # Placing A Legend On The Top Right Corner Of The Graph
pylab.grid(True)                                                # Displaying The Grid
pylab.show()                                                    # Displaying The Figure

#original and reconstructed function from fourier coefficients for cos(cos(x))
approxCosCos=np.matmul(A,cCosCos)                               # Matrix Product Of Two Arrays
pylab.plot(x,approxCosCos,'go',label="Approx value")            # Ploting y vs x As Lines And Markers
pylab.plot(x,coscos(x),'-r',label='True value')                 # Ploting y vs x As Lines And Markers
pylab.xlabel(r'n$\rightarrow$',fontsize=15)                     # Setting The Label For The x-axis
pylab.ylabel(r'$\cos(\cos(x))\rightarrow$',fontsize=15)         # Setting The Label For The y-axis
pylab.legend(loc='upper left')                                  # Placing A Legend On The Top Right Corner Of The Graph
pylab.grid(True)                                                # Displaying The Grid
pylab.show()                                                    # Displaying The Figure