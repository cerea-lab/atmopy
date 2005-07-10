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


def remove_lowest(dates, data1, data2, mini):
    """ Removes values of data1, data2 and dates where data1 values
    are lower than the given minimum.
    Returns arrays for data1 and data2, list for dates."""
    condition = (data1 > mini)
    for i in range(len(condition)-1, -1, -1):
        if condition[i] == 0:
            dates.pop(i)
    return dates, data1[numarray.where(condition)], \
           data2[numarray.where(condition)]


def remove_highest(dates, data1, data2, maxi):
    """ Removes values of data1, data2 and dates where data1 values
    are higher than the given maximum.
    Returns arrays for data1 and data2, list for dates."""
    condition = (data1 < maxi)
    for i in range(len(condition)-1, -1, -1):
        if condition[i] == 0:
            dates.pop(i)
    return dates, data1[numarray.where(condition)], \
           data2[numarray.where(condition)]
