# Copyright (C) 2005-2007, ENPC - INRIA - EDF R&D
#     Author(s): Vivien Mallet
#
# This file is part of AtmoPy library, a tool for data processing and
# visualization in atmospheric sciences.
#
# AtmoPy is developed in the INRIA - ENPC joint project-team CLIME and in
# the ENPC - EDF R&D joint laboratory CEREA.
#
# AtmoPy is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# AtmoPy is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# For more information, visit the AtmoPy home page:
#     http://cerea.enpc.fr/polyphemus/atmopy.html


from pylab import *
from numpy import *
try:
    from matplotlib.toolkits.basemap import Basemap
except:
    pass
import sys, os
sys.path.insert(0,
                os.path.split(os.path.dirname(os.path.abspath(__file__)))[0])
import talos
sys.path.pop(0)


def getm(config = None, y_min = None, x_min = None,
         Delta_y = None, Delta_x = None, Ny = None, Nx = None, cbar = True,
         open_figure = True, resolution = 'l', area_thresh = 1000):
    """
    Generates a map with Basemap.

    @type config: Config or string
    @param config: The configuration or the configuration file.
    @type cbar: Boolean
    @param cbar: True if there is a colormap, false otherwise.
    @type open_figure: Boolean
    @param open_figure: Should a figure be opened?

    @rtype: Basemap
    @return: The map.
    """
    if isinstance(config, str):
        config = talos.Config(config)

    if x_min is None:
        x_min = config.x_min
    if y_min is None:
        y_min = config.y_min
    if Delta_x is None:
        Delta_x = config.Delta_x
    if Delta_y is None:
        Delta_y = config.Delta_y
    if Nx is None:
        Nx = config.Nx
    if Ny is None:
        Ny = config.Ny

    m = Basemap(projection = 'cyl',
                llcrnrlon = x_min - Delta_x / 2.,
                llcrnrlat = y_min - Delta_y / 2.,
                urcrnrlon = x_min + Delta_x / 2. + Delta_x * float(Nx - 1),
                urcrnrlat = y_min + Delta_y / 2. + Delta_y * float(Ny - 1),
                resolution = resolution, suppress_ticks = False,
                area_thresh = area_thresh)
    if open_figure:
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


def getd(config = None, filename = "", Nt = None,
         Nz = None, Ny = None, Nx = None):
    """
    Reads data from a binary file.

    @type config: Config or string
    @param config: The configuration or the configuration file.
    @type filename: string
    @param filename: The file to be loaded. If filename is empty, then the
    file from 'config' is loaded.
    @type Nt: integer.
    @param Nt: The number of time steps in the file to be loaded. If it is not
    given, it is read in 'config'.
    @type Nz: integer.
    @param Nz: The number of levels in the file to be loaded. If it is not
    given, it is read in 'config'.
    @type Ny: integer.
    @param Ny: The number of space steps along y in the file to be loaded. If
    it is not given, it is read in 'config'.
    @type Nx: integer.
    @param Nx: The number of space steps along xin the file to be loaded. If
    it is not given, it is read in 'config'.

    @rtype: numpy.array
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
        
    length = 1
    for l in [Nt, Nz, Ny, Nx]:
        length *= l
    d = fromfile(filename, 'f', length)
    d.shape = (Nt, Nz, Ny, Nx)
    return d.astype('f8')


def getmd(config, cbar = True):
    """
    Reads data from a binary file and generates the corresponding map.

    @type config: Config or string
    @param config: The configuration or the configuration file.
    @type cbar: Boolean
    @param cbar: True is there is a colormap, false otherwise.

    @rtype: (Basemap, numpy.array)
    @return: The map and the data.
    """
    return (getm(config), getd(config))


def disp(map, data, **kwargs):
    """
    Displays a 2D array on a given map.

    @type map: Basemap
    @param map: The map on which data is displayed.
    @type data: 2D numpy.array
    @param data: Data (2D) to be displayed.
    """
    if data.ndim != 2:
        raise Exception, "Function \"disp\" proceeds with 2D data," \
              + " but input data has " + str(data.ndim) + " dimension(s)."

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
    map.imshow(data, **kwargs)
    map.drawcountries()
    map.drawcoastlines()

    # Colorbar.
    if len(gcf().axes) > 1:
        gcf().axes[1].clear()
        cax = gcf().axes[1]
        colorbar(cax = cax)
    

def dispcf(map, data, V = None, **kwargs):
    """
    Displays a 2D array on a given map with filled contours.

    @type map: Basemap
    @param map: The map on which data is displayed.
    @type data: 2D numpy.array
    @param data: Data (2D) to be displayed.
    @type V: integer, list or 1D numpy.array
    @param V: The number of levels or the list of thresholds for the contours.
    """
    if data.ndim != 2:
        raise Exception, "Function \"dispcf\" proceeds with 2D data," \
              + " but input data has " + str(data.ndim) + " dimension(s)."
    
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

    xrange, yrange = map.makegrid(data.shape[1], data.shape[0])
    if kwargs.has_key("colors"):
        V = len(kwargs["colors"]) - 1
    if V is None:
        map.contourf(xrange, yrange, data, **kwargs)
    else:
        map.contourf(xrange, yrange, data, V, **kwargs)
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
