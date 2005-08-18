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


from numarray import *
import scipy.stats.stats


def pdf(data, Nbins = 200):
    """
    Computes an approximation of the probability density function. The range
    of data (minimum to maximum) is split into bins of constant length and a
    probability is computed for each bin.

    @type data: numarray.array
    @param data: Data whose probability density function is sought.
    @type Nbins: integer
    @param Nbins: The number of bins.

    @rtype: 1D numarray.array
    @return: The array of probabilities associated with each bin. The mean of
    this array multiplied by the data range (maximum minus minimum) is equal
    to one.
    """
    Nbins = float(Nbins)
    data = sort(ravel(data))
    delta = (data[-1] - data[0]) / Nbins
    bins = arange(Nbins + 1., typecode = 'f') * delta + data[0]
    bins[0] = data[0] - delta   # So that all elements are counted.
    bins[-1] = data[-1] + delta   # So that all elements are counted.
    
    res = searchsorted(data, bins)

    return arange(data[0] + delta / 2., data[-1], delta), \
           (res[1:] - res[:-1]) / (data[-1] - data[0]) \
           / float(len(data)) * Nbins


def cdf(data):
    """
    Returns the cumulative density function.

    @type Nbins: integer
    @param Nbins: The number of bins.

    @rtype: (1D numarray.array, 1D numarray.array)
    @return: The data values and the cumulative densities associated with
    them.
    """
    data = sort(ravel(data))
    return data, (arange(len(data), typecode = 'f') + 1.) / float(len(data))
