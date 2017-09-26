import numpy as np
tstep = 0.0001
dtout = 0.02
e0=0
Energy=0
de=0
tmax=20.0
t=0
class object:
    def __init__(self,m,x0,yd,xd=0,y0=0,xdd=0,ydd=0,potl=0):
        self.mass = m
        self.ydot = yd
        self.xdot = xd
        self.x = x0
        self.y = y0
        self.xdd = xdd
        self.ydd = ydd
        self.pot = potl
        
star = object(1,0,0)
planet = object(0.1,1,1)
moon = object(0.01,1.05,1.64388)

fstar = open('./output/Q3/star_m'+str(star.mass)+'_x'+str(star.x)+'_ydot'+str(star.ydot)+'.txt','w+')
fmoon = open('./output/Q3/moon_m'+str(moon.mass)+'_x'+str(moon.x)+'_ydot'+str(moon.ydot)+'.txt','w+')
fplanet = open('./output/Q3/planet_m'+str(planet.mass)+'_x'+str(planet.x)+'_ydot'+str(planet.ydot)+'.txt','w+')

#center of mass, assuming xdot=0 in all cases
ydot_com = -(star.mass*star.ydot+planet.mass*planet.ydot+moon.mass*moon.ydot)/(star.mass+planet.mass+moon.mass)

star.ydot+=ydot_com
planet.ydot+=ydot_com
moon.ydot+=ydot_com

#potential on obj1 by obj2
def potential(obj1,obj2):
        pot = -obj2.mass*obj1.mass/np.sqrt((obj1.x-obj2.x)**2+(obj1.y-obj2.y)**2)
        return pot/2.0

def potential_loop(obj1,obj2):
        x1 = obj1.x+obj1.xdot*tstep/2.0
        y1 = obj1.y+obj1.ydot*tstep/2.0
        x2 = obj2.x+obj2.xdot*tstep/2.0
        y2 = obj2.y+obj2.ydot*tstep/2.0
        pot = -obj2.mass*obj1.mass/np.sqrt((x1-x2)**2+(y1-y2)**2)
        return pot/2.0    
#acceleration on obj1 by obj2
def accelerate(obj1,obj2):
        r=np.sqrt((obj1.x-obj2.x)**2+(obj1.y-obj2.y)**2)
        acc_x = -obj2.mass*(obj1.x-obj2.x)/r**3
        acc_y = -obj2.mass*(obj1.y-obj2.y)/r**3
        return acc_x,acc_y

star.pot = potential(star,moon)+potential(star,planet)
moon.pot = potential(moon,star)+potential(moon,planet)
planet.pot = potential(planet,moon)+potential(planet,star)

#xdd,ydd
xdd01,ydd01 = accelerate(star,moon)
xdd02,ydd02 = accelerate(star,planet)
star.xdd = xdd01+xdd02
star.ydd = ydd01+ydd02
#star.xdd,star.ydd = accelerate(star,moon)+acceterate(star,planet)
xdd01,ydd01 = accelerate(planet,moon)
xdd02,ydd02 = accelerate(planet,star)
planet.xdd = xdd01+xdd02
planet.ydd = ydd01+ydd02
#planet.xdd,planet.ydd = accelerate(planet,moon)+accelerate(planet,star)
xdd01,ydd01 = accelerate(moon,planet)
xdd02,ydd02 = accelerate(moon,star)
moon.xdd = xdd01+xdd02
moon.ydd = ydd01+ydd02
#moon.xdd,planet.ydd = accelerate(moon,planet)+accelerate(moon,star)

def k_energy(obj):
    return 0.5*obj.mass*(obj.xdot**2+obj.ydot**2)

def energy():
    return star.pot+moon.pot+planet.pot+k_energy(star)+k_energy(moon)+k_energy(planet)

e0 = energy()
'''
print moon.pot
print planet.pot
print star.pot
print k_energy(star)
print k_energy(moon)
print k_energy(planet)
print accelerate(moon,star)
print accelerate(planet,star)
print e0
'''

star.xdot+=star.xdd*tstep/2.0
star.ydot+=star.ydd*tstep/2.0
moon.xdot+=moon.xdd*tstep/2.0
moon.ydot+=moon.ydd*tstep/2.0
planet.xdot+=planet.ydd*tstep/2.0
planet.ydot+=planet.ydd*tstep/2.0


tnext=dtout
#print 'star:'+str(star.x)+' '+str(star.y)+' '+str(star.xdot)+' '+str(star.ydot)+' '+str(star.xdd)+' '+str(star.ydd)+'\n'
#print 'moon:'+str(moon.x)+' '+str(moon.y)+' '+str(moon.xdot)+' '+str(moon.ydot)+' '+str(moon.xdd)+' '+str(moon.ydd)+'\n'
#print 'planet:'+str(planet.x)+' '+str(planet.y)+' '+str(planet.xdot)+' '+str(planet.ydot)+' '+str(planet.xdd)+' '+str(planet.ydd)+'\n'
flag=1
while(t<tmax):
    #x
    star.x+=star.xdot*tstep
    moon.x+=moon.xdot*tstep
    planet.x+=planet.xdot*tstep
    #y
    star.y+=star.ydot*tstep
    moon.y+=moon.ydot*tstep
    planet.y+=planet.ydot*tstep

    #xdd,ydd
    xdd01,ydd01 = accelerate(star,moon)
    xdd02,ydd02 = accelerate(star,planet)
    star.xdd = xdd01+xdd02
    star.ydd = ydd01+ydd02
    #star.xdd,star.ydd = accelerate(star,moon)+acceterate(star,planet)
    xdd01,ydd01 = accelerate(planet,moon)
    xdd02,ydd02 = accelerate(planet,star)
    planet.xdd = xdd01+xdd02
    planet.ydd = ydd01+ydd02
    #planet.xdd,planet.ydd = accelerate(planet,moon)+accelerate(planet,star)
    xdd01,ydd01 = accelerate(moon,planet)
    xdd02,ydd02 = accelerate(moon,star)
    moon.xdd = xdd01+xdd02
    moon.ydd = ydd01+ydd02
    #  moon.xdd,planet.ydd = accelerate(moon,planet)+accelerate(moon,star)
    #xdot,ydot
    star.xdot+=star.xdd*tstep
    star.ydot+=star.ydd*tstep
    moon.xdot+=moon.xdd*tstep
    moon.ydot+=moon.ydd*tstep
    planet.xdot+=planet.ydd*tstep
    planet.ydot+=planet.ydd*tstep
    #t
    t+=tstep
    
    if (t>=tnext):
        #pot
        star.pot = potential_loop(star,moon)+potential_loop(star,planet)
        moon.pot = potential_loop(moon,star)+potential_loop(moon,planet)
        planet.pot = potential_loop(planet,moon)+potential_loop(planet,star)
        Energy=energy()
        de=(Energy-e0)/np.abs(e0)
        fstar.write('%8.5f %7.3f %7.3f %8.2f %8.2f %7.4e %7.3f %7.3f\n' % (t,star.x+star.xdot*tstep/2.0,star.y+star.ydot*tstep/2.0,star.xdot,star.ydot,de,star.xdd,star.ydd))
        fmoon.write('%8.5f %7.3f %7.3f %8.2f %8.2f %7.4e %7.3f %7.3f\n' % (t,moon.x+moon.xdot*tstep/2.0,moon.y+moon.ydot*tstep/2.0,moon.xdot,moon.ydot,de,moon.xdd,moon.ydd))
        fplanet.write('%8.5f %7.3f %7.3f %8.2f %8.2f %7.4e %7.3f %7.3f\n' % (t,planet.x+planet.xdot*tstep/2.0,planet.y+planet.ydot*tstep/2.0,planet.xdot,planet.ydot,de,planet.xdd,planet.ydd))
        tnext+=dtout
        flag=0
        #print moon.pot
        #print planet.pot
        #print star.pot
        #print k_energy(star)
        #print k_energy(moon)
        #print k_energy(planet)
        #print accelerate(moon,star)
        #print accelerate(planet,star)
        #print e0
        #print de
        #print '\n'
        
        
    #elif flag:

        #print 'moon: %8.5f %10.6f %10.6f %8.2f %8.2f %7.4f %7.3f %7.3f' % (t,moon.x+moon.xdot*tstep/2.0,moon.y+moon.ydot*tstep/2.0,moon.xdot,moon.ydot,de,moon.xdd,moon.ydd)
        #print 'planet: %8.5f %10.6f %10.6f %8.2f %8.2f %7.4f %7.3f %7.3f\n' % (t,planet.x+planet.xdot*tstep/2.0,planet.y+planet.ydot*tstep/2.0,planet.xdot,planet.ydot,de,planet.xdd,planet.ydd)
           
          
        
fstar.close()
fmoon.close()
fplanet.close()
        