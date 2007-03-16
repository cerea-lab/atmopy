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
#     http://www.enpc.fr/cerea/polyphemus/atmopy.html


from numpy import *
import scipy.stats.stats


def pdf(data, Nbins = 200, val = None):
    """
    Computes an approximation of the probability density function. The range
    of data (minimum to maximum) is split into bins of constant length and a
    probability is computed for each bin.

    @type data: numpy.array
    @param data: Data whose probability density function is sought.
    @type Nbins: integer
    @param Nbins: The number of bins.
    @type val: numpy.array
    @param val: Values at which the probability density function should be
    evaluated. Contiguous values are assumed to be at a fixed distance d, and
    output densities are representative of the interval ]val[i] - d/2, val[i]
    + d/2]. If 'val' is None, the bins are automatically adapted. If 'val' is
    not None, 'Nbins' is discarded.

    @rtype: 1D numpy.array, 1D numpy.array
    @return: The middle values of the bins and the array of probabilities
    associated with each bin. The mean of this array multiplied by the data
    range (maximum minus minimum) is equal to one.
    """
    data = sort(ravel(data))

    if val is not None:
        delta = float(val[1] - val[0])
        bins = arange(len(val) + 1, dtype = 'd') * delta \
               + val[0] - 0.5 * delta
        res = searchsorted(data, bins)
        return val, (res[1:] - res[:-1]) / (delta * float(len(data)))

    # Bins.
    Nbins = float(Nbins)
    delta = (data[-1] - data[0]) / Nbins
    bins = arange(Nbins + 1., dtype = 'd') * delta + data[0]
    bins[0] = data[0] - delta   # So that all elements are counted.
    bins[-1] = data[-1] + delta   # So that all elements are counted.
    
    res = searchsorted(data, bins)

    return arange(data[0] + delta / 2., data[-1], delta), \
           (res[1:] - res[:-1]) / (data[-1] - data[0]) \
           / float(len(data)) * Nbins


def cdf(data):
    """
    Returns the cumulative density function.

    @type data: numpy.array
    @param data: Data whose cumulative density function is sought.

    @rtype: (1D numpy.array, 1D numpy.array)
    @return: The data values and the cumulative densities associated with
    them.
    """
    data = sort(ravel(data))
    return data, (arange(len(data), dtype = 'd') + 1.) / float(len(data))
