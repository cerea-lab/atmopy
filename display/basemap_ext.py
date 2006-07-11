# Copyright (C) 2005 CEREA
#     Author: Vivien Mallet
#
# CEREA (http://www.enpc.fr/cerea/) is a joint laboratory of
# ENPC (http://www.enpc.fr/) and EDF R&D (http://www.edf.fr/).
#
# This file is part of AtmoPy package.
# AtmoPy is a tool for data processing and visualization in atmospheric
# sciences.
#
# AtmoPy is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# AtmoPy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License (file ``license'') for more details.
#
# For more information, please see the AtmoPy home page:
#     http://www.enpc.fr/cerea/atmopy/


from pylab import *
from numarray import *
try:
    from matplotlib.toolkits.basemap import Basemap
except:
    pass
import sys, os
sys.path.insert(0, os.path.split(os.path.dirname(os.path.abspath(__file__)))[0])
import talos
sys.path.pop(0)


def getm(config, cbar = True):
    """
    Generates a map with Basemap.

    @type config: Config or string
    @param config: The configuration or the configuration file.
    @type cbar: Boolean
    @param cbar: True is there is a colormap, false otherwise.

    @rtype: Basemap
    @return: The map.
    """
    if isinstance(config, str):
        config = talos.Config(config)
    m = Basemap(projection = 'cyl',
                llcrnrlon = config.x_min - config.Delta_x / 2.,
                llcrnrlat = config.y_min - config.Delta_y / 2.,
                urcrnrlon = config.x_min + config.Delta_x / 2. +
                config.Delta_x * float(config.Nx),
                urcrnrlat = config.y_min + config.Delta_y / 2. +
                config.Delta_y * float(config.Ny), resolution = 'l',
                suppress_ticks = False)
    fig_num = get_current_fig_manager().num
    xsize = rcParams['figure.figsize'][0]
    fig = figure(num = fig_num)
    if cbar:
        ax = fig.add_axes([0.1, 0.1, 0.75, 0.75])
        axes(ax)
        axes([0.875, 0.1, 0.05, 0.75])
    else:
        ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
        axes(ax)
    return m


def getd(config, filename = "", Nt = None, Nz = None, Ny = None, Nx = None):
    """
    Reads data from a binary file.

    @type config: Config or string
    @param config: The configuration or the configuration file.
    @type filename: string
    @param filename: The file to be loaded. If filename is empty, then the
    file from 'config' is loaded.

    @rtype: numarray.array
    @return: The data.
    """
    if isinstance(config, str):
        config = talos.Config(config)
    if filename == "":
        filename = config.input_file

    import os
    if Nx is None:
        Nx = config.Nx
    if Ny is None:
        Ny = config.Ny
    if Nz is None:
        Nz = config.Nz
    if Nt is None:
        Nt = config.Nt

    if Nx == 0:
        Nx = int(os.stat(filename)[6] / 4) / Ny / Nz / Nt
    if Ny == 0:
        Ny = int(os.stat(filename)[6] / 4) / Nx / Nz / Nt
    if Nz == 0:
        Nz = int(os.stat(filename)[6] / 4) / Nx / Ny / Nt
    if Nt == 0:
        Nt = int(os.stat(filename)[6] / 4) / Nx / Ny / Nz
        
    return fromfile(filename, type = 'f', shape = [Nt, Nz, Ny, Nx])


def getmd(config, cbar = True):
    """
    Reads data from a binary file and generates the corresponding map.

    @type config: Config or string
    @param config: The configuration or the configuration file.
    @type cbar: Boolean
    @param cbar: True is there is a colormap, false otherwise.

    @rtype: (Basemap, numarray.array)
    @return: The map and the data.
    """
    return (getm(config), getd(config))


def disp(map, data):
    """
    Displays a 2D array on a given map.

    @type map: Basemap
    @param map: The map on which data is displayed.
    @type data: 2D numarray.array
    @param data: Data (2D) to be displayed.
    """
    # If the figure is empty, sets new axes.
    if len(gcf().axes) == 0:
        xsize = rcParams['figure.figsize'][0]
        fig_num = get_current_fig_manager().num
        fig = figure(num = fig_num)
        ax = fig.add_axes([0.1, 0.1, 0.75, 0.75])
        axes(ax)
        axes([0.875, 0.1, 0.05, 0.75])

    # Clears current image.
    gcf().axes[0].clear()
    axes(gcf().axes[0])
    map.imshow(data)
    map.drawcountries()
    map.drawcoastlines()

    # Colorbar.
    if len(gcf().axes) > 1:
        gcf().axes[1].clear()
        cax = gcf().axes[1]
        colorbar(cax = cax)
    

def cbar():
    """
    Displays a colorbar.
    """
    if len(gcf().axes) > 1:
        gcf().axes[1].clear()
        cax = gcf().axes[1]
    else:
        cax = axes([0.875, 0.1, 0.05, 0.75])
    colorbar(cax = cax)
