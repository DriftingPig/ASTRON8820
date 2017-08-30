#! /usr/bin/python
# program for running scipy integration routines
# from ipython, call as "%run si.py llim ulim"
# to time performance, use "%timeit -n 4 %run si.py llim ulim"

import sys
import numpy as np
import scipy.integrate as si

tolerance=1.e-6		# require convergence to this fractional error

llim=float(sys.argv[1])
ulim=float(sys.argv[2])

def integrand(x):
    return((np.sin(x)/x)**2)
#   return(1./(x+1./x))

value=si.quad(integrand,llim,ulim,epsrel=tolerance,limit=200)
print 'si.quad gives ',value

#value=si.romberg(integrand,llim,ulim,rtol=tolerance,divmax=20)
#print 'si.romberg gives ',value

