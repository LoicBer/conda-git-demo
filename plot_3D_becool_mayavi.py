#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import numpy as np
from mayavi import mlab
from tvtk.api import tvtk # python wrappers for the C++ vtk ecosystem

import matplotlib.pyplot as plt

#import matplotlib.colors as mcol
#from mpl_toolkits.mplot3d import Axes3D
#from matplotlib.cbook import get_sample_data
#from matplotlib import cm
#import cv2


import sys
import os

sys.path.append('/home/lesigne/BECOOL/PROG/STRAT2_new/UTILS')

from BECOOL_util import *
import lecture_BCL




def auto_sphere(image_file):
    '''
    Tracer le globe terrestre
    '''
    # create a figure window (and scene)
    fig = mlab.figure(size=(600, 600))

    # load and map the texture
    img = tvtk.JPEGReader()
    img.file_name = image_file
    texture = tvtk.Texture(input_connection=img.output_port, interpolate=1)
    # (interpolate for a less raster appearance when zoomed in)

    # use a TexturedSphereSource, a.k.a. getting our hands dirty
    R = 0.8
    Nrad = 180

    # create the sphere source with a given radius and angular resolution
    sphere = tvtk.TexturedSphereSource(radius=R, theta_resolution=Nrad,
                                       phi_resolution=Nrad)

    # assemble rest of the pipeline, assign texture    
    sphere_mapper = tvtk.PolyDataMapper(input_connection=sphere.output_port)
    sphere_actor = tvtk.Actor(mapper=sphere_mapper, texture=texture)
    fig.scene.add_actor(sphere_actor)


# répertoire des bichiers BCL
REP_BCL = '/home/lesigne/BECOOL/DATABASE/Strateole2/ST2_C1_02_STR1/pr2_brut_ascii'
liste_tot = sorted([X for X in os.listdir(REP_BCL) if 'mli2_' in X])

# liste des premières mesures de chaque nuit:
liste_par_jours = liste_adjacents(liste_tot,dt.timedelta(hours=5))
liste_jours = [X[0] for X in liste_par_jours]

distance = np.arange(0.015,30.730,0.015)

lat=[]
lon=[]
dates=[]
data=[]

# lecture fichiers
for liste in liste_par_jours[:2]:
        for BCL in liste[:]:
                print('lecture fichier :',BCL)
                profil = lecture_BCL.fichier(os.path.join(REP_BCL,BCL),0,1)
                lat.append(profil.lat)
                lon.append(profil.lon)
                dates.append(BCL_name2datetime(BCL))
                data.append(profil.donnees[:1333,1])
        lat.append(lat[-1])
        lon.append(lon[-1])
        data.append(np.nan * data[-1])
        
data = np.array(data)
lat = np.array(lat)
lon = np.array(lon)
print('*****************************************************')
print('len(lat):',len(lat))
print('len(lon):',len(lon))
print('data.shape:',data.shape)

#z = np.tile(np.arange(data.shape[1],0,-1),(data.shape[0],1))
#z = np.transpose(z)
#print('z.shape:',z.shape)

# limites en dynamique pour affichage
# percentiles
pmin=1
pmax=99
# limites
dmin = np.nanpercentile(np.log10(data),pmin)
dmax = np.nanpercentile(np.log10(data),pmax)

#data = (data-dmin)/(dmax-dmin)

# create colormap according to x-value (can use any 50x50 array)
color_dimension = np.log10(data) # change to desired fourth dimension

print('mini:',dmin)
print('maxi:',dmax)

# coordonnees spheriques vers cartesiennes
# Create a sphere
pi = np.pi
cos = np.cos
sin = np.sin
#phi, theta = np.mgrid[0:pi:101j, 0:2 * pi:101j]
r=1
x = r * cos(np.deg2rad(180+lon)) * cos(np.deg2rad(lat))
y = r * sin(np.deg2rad(180+lon)) * cos(np.deg2rad(lat))
z = r * sin(np.deg2rad(lat))



image_file = 'blue_marble_spherical.jpg'
auto_sphere(image_file)
mlab.plot3d(x, y, z, np.arange(len(lat)), tube_radius=0.025, colormap='Spectral')
mlab.show()

