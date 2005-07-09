# Copyright (C) 2005 CEREA
#     Author: Vincent Picavet
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


import numarray
import datetime


def get_filesize(filename):
    """Gets a file's size.
    Returns integer"""
    fileSize = 0
    try:
        f = open(filename, "r", 0)
        try:
            f.seek(0,2)
            fileSize = f.tell()
        finally:
            f.close()
    except IOError:
        pass
    return fileSize


def get_timesteps(filename, recordLength):
    """Gets number of timsteps in a file given its
    record length (in Bytes).
    Returns integer."""
    ts = 0
    if (recordLength != 0):
        ts = get_filesize / recordLength
    return ts


def load_binary(filename, shape, type = 'f4'):
    """Loads a binary file into an array using specified shape.
    Returns numarray."""
    return numarray.fromfile(filename, type, shape)


def load_binary_first_level(filename, shape, type = 'f4'):
    """Loads a binary file into an array using specified 3D shape for
    X, Y and T dimensions (a time sequence of planes).
    If the given binary file is a 4D file (XYZT), the plane Z = 1 is
    extracted.
    """
    res = []
    zsize = get_filesize(filename) \
            / (numerictypes.getType(type).bytes * shape[0] \
               * shape[1] * shape[2])
    if zsize != 1:
        res = load_binary(filename, shape, type)
    else:
        newshape = list(shape)
        newshape.insert(1, zsize)
        # Use temp array to be sure that memory is freed
        temp = load_binary(filename, newshape, type)
        res = temp[:,1,:,:]
        del temp
    return res


def save_binary(arrayToSave, filename, type = 'f4'):
    """Saves a numarray in a binary file using specified type."""
    numarray.array(arrayToSave, type = type).tofile(filename)
