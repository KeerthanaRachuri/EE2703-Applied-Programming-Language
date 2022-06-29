#                                            ASSIGNMENT 6 
#                                         LAPLACE TRANSFORMS
#                                      RACHURI KEERTHANA EE20B102
from pylab import *
import scipy.signal as sp

# calculating x(t) for decay 0.5
p11 = poly1d([1,0.5])
p21 = polymul([1,1,2.5],[1,0,2.25])
X1 = sp.lti(p11,p21)
t1,x1 = sp.impulse(X1,None,linspace(0,50,500))


# calculating x(t) for decay 0.05
p12 = poly1d([1,0.05])
p22 = polymul([1,0.1,2.2525],[1,0,2.25])
X2 = sp.lti(p12,p22)
t2,x2 = sp.impulse(X2,None,linspace(0,50,500))

# simulating the function 
H = sp.lti([1],[1,0,2.25])
print(H)
for w in arange(1.4,1.6,0.05):
	t = linspace(0,50,500)
	f = cos(w*t)*exp(-0.05*t)
	t,x,svec = sp.lsim(H,f,t)

# x(t) for various frequencies vs time.
	figure(2)
	plot(t,x,label='w = ' + str(w))
	title("x(t) for different frequencies")
	xlabel(r'$t\rightarrow$')
	ylabel(r'$x(t)\rightarrow$')
	legend(loc = 'upper left')
	grid(True)

# Finding x(t) and y(t)
t4 = linspace(0,20,500)
X4 = sp.lti([1,0,2],[1,0,3,0])
Y4 = sp.lti([2],[1,0,3,0])	
t4,x4 = sp.impulse(X4,None,t4)
t4,y4 = sp.impulse(Y4,None,t4)

# Bode plot for H5
temp = poly1d([1e-12,1e-4,1])
H5 = sp.lti([1],temp)
w,S,phi = H5.bode()

#finds the output for the filter function
t6 = arange(0,25e-3,1e-7)
vi = cos(1e3*t6) - cos(1e6*t6)
t6,vo,svec = sp.lsim(H5,vi,t6)

# plots

# x(t) vs t for decay 0.5
figure(0)
plot(t1,x1)
title("The solution x(t) for Q.1")
xlabel(r'$t\rightarrow$')
ylabel(r'$x(t)\rightarrow$')
grid(True)

# x(t) vs t for decay 0.05
figure(1)
plot(t2,x2)
title("The solution x(t) for Q.2")
xlabel(r'$t\rightarrow$')
ylabel(r'$x(t)\rightarrow$')
grid(True)

#  x(t) and y(t) vs t 
figure(3)
plot(t4,x4,label='x(t)')
plot(t4,y4,label='y(t)')
title("x(t) and y(t)")
xlabel(r'$t\rightarrow$')
ylabel(r'$functions\rightarrow$')
legend(loc = 'upper right')
grid(True)

# The magnitude bode plot 
figure(4)
semilogx(w,S)
title("Magnitude Bode plot")
xlabel(r'$\omega\rightarrow$')
ylabel(r'$20\log|H(j\omega)|\rightarrow$')
grid(True)

# The phase bode plot 
figure(5)
semilogx(w,phi)
title("Phase Bode plot")
xlabel(r'$\omega\rightarrow$')
ylabel(r'$\angle H(j\omega)\rightarrow$')
grid(True)

# The plot of Vo(t) vs t for large time interval.
figure(6)
plot(t6,vo)
title("The Output Voltage for large time interval")
xlabel(r'$t\rightarrow$')
ylabel(r'$V_o(t)\rightarrow$')
grid(True)

# The plot of Vo(t) vs t for small time interval.
figure(7)
plot(t6[0:300],vo[0:300])
title("The Output Voltage for small time interval")
xlabel(r'$t\rightarrow$')
ylabel(r'$V_o(t)\rightarrow$')
grid(True)

show()
