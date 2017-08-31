"""
integrate_sub.py -- subroutine functions for numerical integration
  integrate_driver does adaptive stepping and can be called with euler,
    trapzd, or midpoint as the underlying method
"""

import numpy as np

def integrate_driver(func,integrator,a,b,tolerance,nstepmax,verbose,integrator_name):
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
    from matplotlib.backends.backend_pdf import PdfPages
    fp = open('./output/'+integrator_name+'.txt','w')
    if (verbose):
        f=open("iterations.out","w")
    nstep=4
    oldint=0.0    
    integral=integrator(func,a,b,nstep)
    #integral_simpson=integral
    while ((np.fabs(oldint/integral-1.0) > tolerance) and (2*nstep<nstepmax)):
        fp.write(str(nstep)+'\t'+str(np.fabs(oldint/integral-1.0))+'\n')
        oldint=integral
        nstep*=2
	integral=integrator(func,a,b,nstep)
        #integral_simpson=4*integral/3.0-oldint/3.0
        if (verbose):
	    hstep=(b-a)/nstep
            outstring="%8d %.8g %.8g\n" % (nstep,hstep,integral)
            f.write(outstring)
    fp.write(str(nstep)+'\t'+str(np.fabs(oldint/integral-1.0))+'\n')
    fp.close()
    fq = np.loadtxt('./output/'+integrator_name+'.txt').transpose()
    from matplotlib import pyplot as plt
    with PdfPages('./output/'+integrator_name+'.pdf') as pdf:
         plt.loglog(fq[0],fq[1])
         plt.xlabel('nsteps')
         plt.ylabel('error')
         plt.title(integrator_name)
         pdf.savefig()
    
    if (verbose):
        f.close()
    if (np.fabs(oldint/integral-1.0) > tolerance):
        print "Warning, fractional convergence is only ", \
	  np.fabs(oldint/integral-1.0)
    return [integral, nstep]

def euler_loop(func,a,b,nstep):
    """
    Evaluate [\int_a^b func(x) dx] using Euler rule with nstep steps
    Use loop analogous to C or fortran
    """
    hstep=(b-a)/nstep
    y=a                                
    integral=0.5*hstep*(func(a)+func(b))
    for i in xrange(nstep-1):
        y+=hstep
        integral+=func(y)*hstep
    return(integral)

def euler(func,a,b,nstep):
    """ 
    Evaluate [\int_a^b func(x) dx] using Euler rule with nstep steps
    Use numpy array operations
    """
    hstep=(b-a)/nstep
    x=np.linspace(a+hstep,b-hstep,nstep-1)
    y=func(x)*hstep
    return (np.sum(y)+0.5*hstep*(func(a)+func(b)))

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
