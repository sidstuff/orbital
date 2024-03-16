#!/usr/bin/env python3

from os import makedirs
from sys import argv
from time import time
from tomllib import load

import numpy as np
from math import factorial
from sympy.physics.hydrogen import R_nl
from scipy.special import lpmv

from matplotlib import pyplot as plt, animation, colormaps
from matplotlib.colors import ListedColormap as lc, LinearSegmentedColormap as lsc, CenteredNorm as cn
from mpl_toolkits.mplot3d import Axes3D

defaults = {

    'n': 1,
    'l': 0,
    'm': 0,

    'dots': 4000,
    'bgcolor': 'black',
    'colormap': "lc(np.vstack((plt.get_cmap('cool')(np.linspace(0,1,256)),plt.get_cmap('spring')(np.linspace(0,1,256)))))",

    'mode': 'draw',

    'elevation': 0,
    'azimuth': 0,
    'format': ['png','webm'],
    'duration': 12,

    'resolution': 1080,
    'mp4codec': 'libx264',
    'webmcodec': 'libvpx-vp9',
    'fps': 30,

    'dotsize': 32,
    'dotshape': 'o',
    'dotalpha': 0.5,
}

try:
    with open('override.conf', mode='rb') as config: defaults.update(load(config))
except: pass

defaults = list(defaults.values())

if len(argv) == 1:         # If no arguments,
    args = [False] * 11    # args is empty.
else:
    args = ['0' if x == 0 else x for x in defaults]    # Stringify 0 so it's not False, which later code interprets as empty.
    for i,x in enumerate(argv[1:]):                    # Remove argv[0], the script name.
        if x != '.':                                   # '.' denotes the default value.
            args[i] = x                                # Store the arguments in args.

def both(cmap):
    arr = cmap(np.linspace(0, 1, 256))
    return lc(np.vstack((arr[::-1], arr)))

def getformat(i):
    if isinstance(args[9], list): return args[9][i]
    else: return args[9]

n = int(args[0] or input("n (default 1) = ") or defaults[0])    # If a value is False, moves onto the next.
l = int(args[1] or input("l (default 0) = ") or defaults[1])    # defaults having a non-string 0 doesn't matter,
m = int(args[2] or input("m (default 0) = ") or defaults[2])    # since it's the last value.

dots = int(args[3] or input("Number of dots (default 4000): ") or defaults[3])
bgcolor = (args[4] or input("Background color (default 'black'): ") or defaults[4]).strip()
colormap = eval(args[5] or input("Change colormap to (optional): ") or defaults[5])
mode = (args[6] or input("View/Draw/Animate [V/D/A] (default Draw): ") or defaults[6]).strip().lower()

if mode in ["view", "v"]:
    mode = 'view'
    size = 640
else:
    size = defaults[11]
    elevation = float(args[7] or input("Elevation in degrees (default 0): ") or defaults[7])
    if mode in ["draw", "d"]:
        mode = 'drawings'
        azimuth = float(args[8] or input("Azimuth in degrees (default 0): ") or defaults[8])
        format = (getformat(0) or input("Format (default PNG): ") or defaults[9][0]).strip().lower()
    else:
        mode = 'animations'
        azimuth = float(args[8] or input("Initial azimuth in degrees (default 0) = ") or defaults[8])
        format = (getformat(1) or input("Format [mp4/webm/gif] (default WebM): ") or defaults[9][1]).strip().lower()
        duration = int(args[10] or input("Duration in sec (default 12): ") or defaults[10])	
        fps = defaults[14]
    makedirs(mode, exist_ok=True)
    name = mode + "/" + str((n, l, m)) + " orbital " + str(dots) + " - " + np.base_repr(int(time()),36) + "." + format

# Probabilities of the spherical coordinates

def p_r(z): return z*z*R_nl(n,l,z)**2

def p_phi(z):
    if m < 0: return np.sin(m*z)    # The square of this will be used as the probability,
    else: return np.cos(m*z)        # the unsquared function will be useful to compute the wavefunction.

def p_theta(z): return np.sin(z)*lpmv(abs(m),l,np.cos(z))**2

r1 = 2.625 * n*n                   # Distance r till which plotted
y_r = n**4 * R_nl(n,n-1,n*n)**2    # Rejection sampling upper bound for p_r

if abs(m) == l: y_theta = (factorial(2*l) / (factorial(l)*2**l))**2    # Rejection sampling upper bound for p_theta
elif abs(m) == 0: y_theta = 2/(np.pi*(l+1/2))
else: y_theta = np.sqrt(abs(m)+1)/(2*l+1) * factorial(l+abs(m))/factorial(l-abs(m))

# Rejection sampling

r = []
i = 0
while i < dots:
    x = np.random.uniform(0, r1)
    y = np.random.uniform(0, y_r)
    if y < p_r(x):
        r.append(x)
        i += 1

phi = []
i = 0
while i < dots:
    x = np.random.uniform(-np.pi, np.pi)
    y = np.random.uniform(0, 1)
    if y < p_phi(x)**2:
        phi.append(x)
        i += 1

theta = []
i = 0
while i < dots:
    x = np.random.uniform(0, np.pi)
    y = np.random.uniform(0, y_theta)
    if y < p_theta(x):
        theta.append(x)
        i += 1

# Unnormalized values of psi for the colormap

psi = [R_nl(n,l,r[i]) * lpmv(abs(m),l,np.cos(theta[i])) * p_phi(phi[i]) for i in range(dots)]

# Conversion to Cartesian coordinates

x = [r[i] * np.sin(theta[i]) * np.cos(phi[i]) for i in range(dots)]
y = [r[i] * np.sin(theta[i]) * np.sin(phi[i]) for i in range(dots)]
z = [r[i] * np.cos(theta[i]) for i in range(dots)]

# Plot

px = 1 / plt.rcParams['figure.dpi']    # Get px in inches
fig = plt.figure(figsize = (size*px, size*px), facecolor = bgcolor)
ax = fig.add_subplot(projection = '3d', aspect = 'equal', xlim = (-r1, r1), ylim = (-r1, r1), zlim = (-r1, r1), facecolor = '#0000'); ax.axis('off')
fig.subplots_adjust(top = 23/18, bottom = -29/90, left = -29/90, right = 23/18)
scat = ax.scatter(x, y, z, c = psi, cmap = colormap, norm = cn(), linewidth = 0, s = defaults[15]*(72*px)**2, marker = defaults[16], alpha = defaults[17])

match mode:
    case 'view': plt.show()
    case 'drawings':
        ax.view_init(elev = elevation, azim = azimuth)
        plt.savefig(name)
    case 'animations':
        def animate(t):
            ax.view_init(elev = elevation, azim = azimuth + 360*t/int(duration*fps))
            return [scat]
        anim = animation.FuncAnimation(fig, animate, frames = int(duration*fps))
        match format:
            case 'mp4': anim.save(name, fps = fps, codec = defaults[12])
            case 'webm': anim.save(name, fps = fps, codec = defaults[13])
            case 'gif': anim.save(name, fps = fps)
