#!/usr/bin/python
# the path in the line above should point to the location of the python
# executable; having this as the first line allows the script to be
# run directly provided you make it executable by chmod +x integrate.py
"""
integrate.py -- main program for running integration functions
  The integrand is defined in the function integrand() below.
  The integration functions themselves are in the file integrate_sub.py.
  Can be called from shell as integrate.py a b	  [see comment above]
    where a and b are the limits of integration 
  Can be called from ipython as '%run integrate.py a b'
"""

import math
import numpy as np		# may be used in integrand
import sys			# needed for command line reads below
from subprocess import call	# to allow a shell call to rename file

# import the integration functions, two different cases
from integrate_sub_starter import *

# define several control variables
nstepmax=9e8    	# maximum number of allowed integration steps
tolerance=1.e-6 	# require convergence to this fractional error
verbose=1		# write iterations to output files

def integrand(z):
    return((0.3*(1+z)**3+0.7)**(-0.5))

# read the integration limits from the command line
a=float(sys.argv[1])
b=float(sys.argv[2])

[value, nc]=integrate_driver(integrand,simpson,a,b,tolerance,nstepmax,verbose)
#[value, nc]=integrate_driver(integrand,euler,a,b,tolerance,nstepmax,verbose)
print 'Euler Integration Converged to ',value,' in ',nc,' steps'
#if (verbose):
#    call(["mv","iterations.out","euler.out"])

#[value, nc]=integrate_driver(integrand,trapzd,a,b,tolerance,nstepmax,verbose)
#print 'Trapezoidal Integration Converged to ',value,' in ',nc,' steps'
#if (verbose):
#    call(["mv","iterations.out","trapzd.out"])

#[value, nc]=integrate_driver(integrand,midpoint,a,b,tolerance,nstepmax,verbose)
#print 'Midpoint Rule Integration Converged to ',value,' in ',nc,' steps'
#if (verbose):
#    call(["mv","iterations.out","midpoint.out"])

#[value, nc]=simpson_driver(integrand,a,b,tolerance,nstepmax,verbose)
#print 'Simpson Rule Integration Converged to ',value,' in ',nc,' steps'
#if (verbose):
#    call(["mv","iterations.out","simpson.out"])
 
