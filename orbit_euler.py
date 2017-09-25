#! /usr/bin/python
# orbit_euler.py -- integrate an orbit via Euler's method (bad), fixed timestep
# orbit_euler.py  xinit yinit xdotinit ydotinit tstep tmax pot_type [qh]
#   xinit, yinit = initial x and y positions
#   xdotinit, ydotinit = initial x and y velocities
#   tstep = timestep
#   tmax = maximum time; integration will stop here
#   pot_type = 1 -> Kepler, Phi(r) = -1/r
#              2 -> Harmonic Oscillator, Phi(x,y) = x**2/2 + y**2/2q**2
#   [qh] = flattening of H.O. potential (default is 1.0)
# 
# Note that output spacing is controlled by in-file parameter dt
# For harmonic oscillator potential, shape is controlled by in-file parameter qh

import sys
import numpy as np

dtout=0.02		# time spacing of outputs
qh=1.0			# default flattening of harmonic oscillator potential

xinit=float(sys.argv[1])
yinit=float(sys.argv[2])
xdotinit=float(sys.argv[3])
ydotinit=float(sys.argv[4])
tstep=float(sys.argv[5])
tmax=float(sys.argv[6])
pot_type=int(sys.argv[7])

if (pot_type != 1 and pot_type !=2):
    raise ValueError("Potential argument must be 1 (Kepler) or 2 (H.O.)")

if (pot_type == 2):
    if (len(sys.argv)>7):
        qh=float(sys.argv[8])

def accelerate(pot,x,y):
    """
    Compute acceleration of a particle 
    pot = 1 for Kepler, 2 for H.O.
    x, y = particle position
    returns accelerations xdd, ydd
    """

    if (pot==1):
        r=np.sqrt(x**2+y**2)
        xdd= -x/r**3
        ydd= -y/r**3
    elif (pot==2):
        # up to you to fill in the next two lines
        xdd=0#TODO 
        ydd=0 
    else:
        raise ValueError ("Invalid potential type")

    return([xdd,ydd])

def potential(pot,x,y):
    """
    Compute potential energy (per unit mass)
    pot = 1 for Kepler, 2 for H.O.
    x, y = particle position
    returns potential phi
    """

    if (pot==1):
        phi=-1/np.sqrt(x**2+y**2)
    elif (pot==2):
        # up to you to fill in the next line
        phi=0#TODO
    else:
        raise ValueError ("Invalid potential type")

    return(phi)

t=0.0
x=xinit
y=yinit
xdot=xdotinit
ydot=ydotinit
e0=potential(pot_type,x,y)+0.5*(xdot**2+ydot**2)
de=0
print '%8.5f %7.3f %7.3f %8.2f %8.2f %7.4e' % (t,x,y,xdot,ydot,de)
tnext=dtout

while (t<tmax):

    xdd,ydd = accelerate(pot_type,x,y)
    x+=xdot*tstep
    y+=ydot*tstep
    xdot+=xdd*tstep
    ydot+=ydd*tstep
    t+=tstep

    if (t>=tnext):
        energy=potential(pot_type,x,y)+0.5*(xdot**2+ydot**2)
        de=(energy-e0)/np.abs(e0)
        print '%8.5f %7.3f %7.3f %8.2f %8.2f %7.4e' % (t,x,y,xdot,ydot,de)
        tnext+=dtout
