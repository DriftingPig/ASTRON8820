#!/usr/bin/python2.7
from integrate_sub_starter import *
import sys
class distance:
      def __init__(self,omega=0.3,H0=67):
            self.om = float(omega)
            self.h0=float(H0)
            self.c=299792.458
            self.ol=1.0-self.om
            self.tolerance=1.e-6 
            self.nstepmax=9e8  
            self.verbose=1
      
      def cosmos_integrand(self,z):
          return((self.om*(1.0+z)**3+self.ol)**(-0.5))

      def dc(self,z):
          return (self.c/self.h0)*integrate_driver(self.cosmos_integrand,simpson,0.0,z,self.tolerance,self.nstepmax,self.verbose)

if __name__=='__main__':
     d=distance()
     Z=sys.argv[1]
     print d.dc(float(Z))
     
