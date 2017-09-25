import matplotlib.pyplot as plt
import numpy as np

class filelist:
    def __init__(self,ydot):
        self.eul01='kep.ydot'+str(ydot)+'.eul.dt0.01'
        self.leap01='kep.ydot'+str(ydot)+'.leap.dt0.01'
        self.eul0001='kep.ydot'+str(ydot)+'.eul.dt0.0001'
        self.leap0001='kep.ydot'+str(ydot)+'.leap.dt0.0001'
class axis_setting:
    def __init__(self):
        self.x1=-1.5
        self.y1=-1.5
        self.x2=1.5
        self.y2=1.5
'''
'kep.ydot0.2.eul.dt0.0001'
'kep.ydot0.2.eul.dt0.01'
'kep.ydot0.2.leap.dt0.0001'
'kep.ydot0.2.leap.dt0.01'
'kep.ydot0.5.eul.dt0.0001'
'kep.ydot0.5.eul.dt0.01'
'kep.ydot0.5.leap.dt0.0001'
'kep.ydot0.5.leap.dt0.01'
'kep.ydot1.eul.dt0.0001'
'kep.ydot1.eul.dt0.01'
'kep.ydot1.leap.dt0.0001'
'kep.ydot1.leap.dt0.01'
'''

def orbit_plot(data,color0,label0):
    #Plot the orbits
    legend, =plt.plot(data[1],data[2],color=color0,label=label0)
    return legend
    
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


def plotstyle():
    plt.tick_params(axis='x', labelsize=12)
    plt.tick_params(axis='y', labelsize=12)
    plt.rc('axes', titlesize=12)
    
def orbit_plot_all(ydot=0.2):
    #Plot the orbits for the two methods and two integration steps. 
    dat = filelist(ydot)
    euler01 = np.loadtxt(dat.eul01).transpose()
    leap01 = np.loadtxt(dat.leap01).transpose()
    euler0001 = np.loadtxt(dat.eul0001).transpose()
    leap0001 = np.loadtxt(dat.leap0001).transpose()
    euler_dt01= orbit_plot(euler01,'r',label0='euler dt=0.01')
    leap_dt01=orbit_plot(leap01,'g',label0='leap dt=0.01')
    euler_dt0001= orbit_plot(euler0001,'b',label0='euler dt=0.0001')
    leap_dt0001= orbit_plot(leap0001,'k',label0='leap dt=0.0001')
    plt.legend(handles=[euler_dt01, leap_dt01,euler_dt0001,leap_dt0001])
    plt.title('euler and leapfrog method for ydot='+str(ydot))
    plotstyle()
    plt.xlabel('AU')
    plt.ylabel('AU') 
    ast=axis_setting()
    plt.axis((ast.x1,ast.x2,ast.y1,ast.y2))
    import matplotlib.backends.backend_pdf as pp
    with pp.PdfPages('./output/eul_leap_ydot'+str(ydot)+'.pdf') as pdf:
        pdf.savefig()
    plt.show()
    plt.clf()
    return True



def energy_check(ydot=0.2):
    dat = filelist(ydot)
    eul01 = np.loadtxt(dat.eul01).transpose()
    leap01 = np.loadtxt(dat.leap01).transpose()
    eul0001 = np.loadtxt(dat.eul0001).transpose()
    leap0001 = np.loadtxt(dat.leap0001).transpose()
    
    eul01_phi = potential(1,eul01[1],eul01[2])
    eul01_e = eul01_phi+0.5*eul01[3]*eul01[3]+0.5*eul01[4]*eul01[4]

    leap01_phi = potential(1,leap01[1],leap01[2])
    leap01_e = leap01_phi+0.5*leap01[3]*leap01[3]+0.5*leap01[4]*leap01[4]     
    
    eul0001_phi = potential(1,eul0001[1],eul0001[2])
    eul0001_e = eul0001_phi+0.5*eul0001[3]*eul0001[3]+0.5*eul0001[4]*eul0001[4]
    
    leap0001_phi = potential(1,leap0001[1],leap0001[2])
    leap0001_e = leap0001_phi+0.5*leap0001[3]*leap0001[3]+0.5*leap0001[4]*leap0001[4]
    
    plt.clf()
    plotstyle()
    #lgd_eul01, = plt.plot(eul01[0],eul01_e,'r',label='euler dt=0.01')
    #lgd_leap01, = plt.plot(leap01[0],leap01_e,'g',label = 'leap frog dt=0.01')
    lgd_eul0001, = plt.plot(eul0001[0],eul0001_e,'b',label = 'euler dt=0.0001')
    lgd_leap0001, = plt.plot(leap0001[0],leap0001_e,'k', label = 'leap frog dt=0.0001')
    #plt.legend(handles=[lgd_eul01, lgd_leap01,lgd_eul0001,lgd_leap0001])
    plt.legend(handles=[lgd_eul0001,lgd_leap0001])
    plt.xlabel('time/yr')
    plt.ylabel('energy')
    plt.title('energy for ydot='+str(ydot))
    import matplotlib.backends.backend_pdf as pp
    with pp.PdfPages('./output/eul_leap_e_two'+str(ydot)+'.pdf') as pdf:
        pdf.savefig()
    plt.show()
    plt.clf()
    return True

def angular_momentum_check(ydot):
    dat = filelist(ydot)
    eul01 = np.loadtxt(dat.eul01).transpose()
    leap01 = np.loadtxt(dat.leap01).transpose()
    eul0001 = np.loadtxt(dat.eul0001).transpose()
    leap0001 = np.loadtxt(dat.leap0001).transpose()
    
    eul01_phi = potential(1,eul01[1],eul01[2])
    eul01_am = eul01[1]*eul01[3]+eul01[2]*eul01[4]

    leap01_phi = potential(1,leap01[1],leap01[2])
    leap01_am = leap01[1]*leap01[3]+leap01[2]*leap01[4]     
    
    eul0001_phi = potential(1,eul0001[1],eul0001[2])
    eul0001_am = eul0001[1]*eul0001[3]+eul0001[2]*eul0001[4]
    
    leap0001_phi = potential(1,leap0001[1],leap0001[2])
    leap0001_am = leap0001[1]*leap0001[3]+leap0001[2]*leap0001[4]
    
    plt.clf()
    plotstyle()
    #lgd_eul01, = plt.plot(eul01[0],eul01_am,'r',label='euler dt=0.01')
    #lgd_leap01, = plt.plot(leap01[0],leap01_am,'g',label = 'leap frog dt=0.01')
    lgd_eul0001, = plt.plot(eul0001[0],eul0001_am,'b',label = 'euler dt=0.0001')
    lgd_leap0001, = plt.plot(leap0001[0],leap0001_am,'k', label = 'leap frog dt=0.0001')
    #plt.legend(handles=[lgd_eul01, lgd_leap01,lgd_eul0001,lgd_leap0001])
    plt.legend(handles=[lgd_eul0001,lgd_leap0001])
    plt.xlabel('time/yr')
    plt.ylabel('angular momentum')
    plt.title('angualr momentum for ydot='+str(ydot))
    import matplotlib.backends.backend_pdf as pp
    with pp.PdfPages('./output/eul_leap_am_two'+str(ydot)+'.pdf') as pdf:
        pdf.savefig()
    plt.show()
    plt.clf()
    return True

def r_check(ydot):
    dat = filelist(ydot)
    eul01 = np.loadtxt(dat.eul01).transpose()
    leap01 = np.loadtxt(dat.leap01).transpose()
    eul0001 = np.loadtxt(dat.eul0001).transpose()
    leap0001 = np.loadtxt(dat.leap0001).transpose()
    
    eul01_r = np.sqrt(eul01[1]*eul01[1]+eul01[2]*eul01[2])

    leap01_r = np.sqrt(leap01[1]*leap01[1]+leap01[2]*leap01[2])     
    
    eul0001_r = np.sqrt(eul0001[1]*eul0001[1]+eul0001[2]*eul0001[2])
    
    leap0001_r = np.sqrt(leap0001[1]*leap0001[1]+leap0001[2]*leap0001[2])
    
    plt.clf()
    #plotstyle()
    lgd_eul01, = plt.plot(eul01[0],eul01_r,'r',label='euler dt=0.01')
    lgd_leap01, = plt.plot(leap01[0],leap01_r,'g',label = 'leap frog dt=0.01')
    lgd_eul0001, = plt.plot(eul0001[0],eul0001_r,'b',label = 'euler dt=0.0001')
    lgd_leap0001, = plt.plot(leap0001[0],leap0001_r,'k', label = 'leap frog dt=0.0001')
    plt.legend(handles=[lgd_eul01, lgd_leap01,lgd_eul0001,lgd_leap0001])
    plt.xlabel('time/yr')
    plt.ylabel('distance')
    plt.title('distance for ydot='+str(ydot))
    import matplotlib.backends.backend_pdf as pp
    with pp.PdfPages('./output/eul_leap_r'+str(ydot)+'.pdf') as pdf:
        pdf.savefig()
    plt.show()
    plt.clf()
    return True

    

    