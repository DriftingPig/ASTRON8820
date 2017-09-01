"""
integrate_sub.py -- subroutine functions for numerical integration
  integrate_driver does adaptive stepping and can be called with euler,
    trapzd, or midpoint as the underlying method
"""

import numpy as np

def integrate_driver(func,integrator,a,b,tolerance,nstepmax,verbose):
    """
    Integrate a function func() using the specified integrator routine
    integrator = euler, euler_loop, trapzd, or midpoint
    a = lower limit of integration
    b = upper limit of integration
    tolerance = fractional convergence required for integral
    nstepmax = maximum number of steps allowed
    verbose = 1 -> write individual iterations to "iterations.out"

    Number of steps starts at 4 and doubles until convergence or nstep>nstepmax
    """
    if (verbose):
        f=open("iterations.out","a")
    nstep=4
    oldint=0.0    
    integral=integrator(func,a,b,nstep)
    #integral_simpson=integral
    while ((np.fabs(oldint/integral-1.0) > tolerance) and (2*nstep<nstepmax)):
        oldint=integral
        nstep*=2
	integral=integrator(func,a,b,nstep)
        integral_simpson=4*integral/3.0-oldint/3.0
        if (verbose):
	    hstep=(b-a)/nstep
            outstring="%8d %.8g %.8g\n" % (nstep,hstep,integral)
            f.write(outstring)
    
    if (verbose):
        f.close()
    if (np.fabs(oldint/integral-1.0) > tolerance):
        print "Warning, fractional convergence is only ", \
	  np.fabs(oldint/integral-1.0)
    return [integral, nstep]

def euler_loop(func,a,b,nstep):#euler
    """
    Evaluate [\int_a^b func(x) dx] using Euler rule with nstep steps
    Use loop analogous to C or fortran
    """
    hstep=(b-a)/nstep
    y=a                                
    integral=func(y)*hstep
    for i in xrange(nstep-1):
        y+=hstep
        integral+=func(y)*hstep
    return(integral)

def euler(func,a,b,nstep):#trapezoidal
    """ 
    Evaluate [\int_a^b func(x) dx] using Euler rule with nstep steps
    Use numpy array operations
    """
    hstep=(b-a)/nstep
    y=a                                
    integral=0.5*hstep*(func(a)+func(b))
    for i in xrange(nstep-1):
        y+=hstep
        integral+=func(y)*hstep
    return(integral)

def simpson(func,a,b,nstep):
    hstep=(b-a)/nstep
    y=a
    integral=hstep*func(a)/3.0+hstep*func(b)/3.0
    flag=0
    for i in xrange(nstep-1):
        y+=hstep
        if(flag):
           integral+=hstep*func(y)*2.0/3.0
           flag=0
        else:
           integral+=hstep*func(y)*4.0/3.0
           flag=1
    return integral

def midpoint(func,a,b,nstep):
    hstep=(b-a)/nstep
    y=a+hstep/2.0
    integral=func(y)*hstep
    for i in xrange(nstep-1):
        y+=hstep
        integral+=func(y)*hstep
    return(integral)

