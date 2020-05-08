import numpy as np
import matplotlib.pyplot as plt

# Initial magnetization
Magx = np.asarray([1, 0, 0])
Magy = np.asarray([0, 1, 0])
Magz = np.asarray([0, 0, 1])

# Rotation matrices in the rotating framework
def xrot(phi):
    # Rotation around the x axis
    Rx = np.asarray([[1, 0, 0], [0, np.cos(phi), -np.sin(phi)], [0, np.sin(phi), np.cos(phi)]])
    return Rx

def yrot(phi):
    # Rotation around the y axis
    Ry = np.asarray([[np.cos(phi), 0, np.sin(phi)], [0, 1, 0], [-np.sin(phi), 0, np.cos(phi)]])
    return Ry

def zrot(phi):
    # Rotation around the z axis
    Rz = np.asarray([[np.cos(phi), -np.sin(phi), 0], [np.sin(phi), np.cos(phi), 0], [0, 0, 1]])
    return Rz

def throt(M, phi, theta):
    # Rotation about a transverse axis defined by y=x*tg(theta)
    Rth = np.dot((np.dot(zrot(theta), xrot(phi))), zrot(-theta))
    return Rth

# Free precession
def freeprecess(dt, T1, T2, df):
    '''Function simulates free precession and decay
%	over a time interval dt, given relaxation times T1 and T2
%	and off-resonance df.  Times in ms, off-resonance in Hz.'''
    phi = 2 * np.pi * df * dt/1000 #angle every 1ms
    Afp = np.dot(np.asarray([[np.exp(-dt / T2), 0, 0], [0, np.exp(-dt / T2), 0], [0, 0, np.exp(-dt / T1)]]),
                 zrot(phi))#
    Bfp = np.transpose(np.asarray([0, 0, (1 - np.exp(-dt / T1))]))
    return Afp, Bfp

def HahnSeq(TS, offfreq, Tref):
    # Hahn Spin-Echo sequence of a single spin
    M0 = np.dot(yrot(np.pi / 2), Magz)  # first excitation
    dt = 1  # 1ms delta time
    T = TS  # total duration
    df = offfreq  # off-resonance (Hz)
    T1 = 600  # ms
    T2 = 100  # ms
    Tp = Tref  # Refocusing pulse time
    timesteps = np.arange(1, T)
    M1 = np.zeros((len(timesteps) + 1, 3))
    M1[0] = M0
    PreState = M0
    PulseCount = 0
    np.set_printoptions(formatter={'float': lambda x: "{0:0.6f}".format(x)})
    for i in timesteps:
        if i % Tp == 0 and PulseCount == 0:
            M1[i] = np.dot(xrot(np.pi), M1[i - 1])
            PreState = np.dot(xrot(np.pi), M1[i - 1])
            PulseCount += Tp
            # print(PreState)
            # input('')
        else:
            a, b = freeprecess(i - PulseCount, T1, T2, df)
            M1[i] = np.dot(a, PreState) + b
            # print(PreState)
            # input('')
    return M1

#Hahn spin echo of multiple spins
timesteps = 1000 #ms
Nesp = 100  # Number of spins
Freqs = np.random.uniform(-10, 10, Nesp)  # Spins off-resonance frequencies
Data = np.zeros((len(Freqs),timesteps,3))
Signal = np.zeros((timesteps,3))
for i in range(len(Freqs)):
    Data[i] = HahnSeq(timesteps, Freqs[i], Tref=50)
    Signal += Data[i]

fig, ax = plt.subplots()
ax.plot(range((timesteps)), Signal[:,0]/np.max(Signal),'k', label= "Mx" )
#ax.plot(range((timesteps)), abs(Signal[:,1])/np.max(Signal),'r', label= "My" )
ax.plot(range((timesteps)), Signal[:,2]/np.max(Signal),'--b', label= "Mz" )
ax.set_xlabel("time (ms)")
ax.set_ylabel("Normalized Magnetization")
ax.legend()
plt.show()
