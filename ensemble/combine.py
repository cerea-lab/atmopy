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


import datetime
import sys, os
sys.path.insert(0, os.path.split(os.path.dirname(os.path.abspath(__file__)))[0])
import observation
sys.path.pop(0)
from numarray import *
import scipy.linalg


def collect(dates, stations, sim, obs, period, stations_out):
    """
    Collects data (observations and simulated concentrations) over a given
    period and at a given set of stations.

    @type dates: list of list of datetime
    @param dates: The list (indexed by stations) of list of dates at which the
    data is defined. Both observations and simulated data (of every ensemble)
    are assumed to be designed at the same dates.
    @type stations: list of Station
    @param stations: The stations at which the concentrations are given.
    @type sim: list of list of 1D-array
    @param sim: The list (indexed by simulations) of lists (indexed by
    stations) of simulated concentrations.
    @type obs: list of 1D-array
    @param obs: The list (indexed by stations) of observed concentrations.
    @type period: 2-tuple of datetime
    @param period: The period where to select the concentrations (bounds
    included).
    @type stations_out: list of Station, or Station
    @param stations_out: The station(s) at which the concentrations are
    selected.

    @rtype: (1D-array, 2D-array)
    @return: The observed concentrations in a 1D-array and the corresponding
    simulated concentrations in a 2D-array (simulations x concentrations).
    """
    if isinstance(stations_out, observation.Station):
        stations_out = (stations_out, )   # Now it is a sequence.
    
    # Output arrays.
    out_obs = []
    out_sim = [[] for i in range(len(sim))]
    
    for istation in range(len(stations)):
        if stations[istation] in stations_out:
            # Searches for the first date in the considered period.
            i = 0
            while i < len(dates[istation]) and dates[istation][i] < period[0]:
                i += 1
            while i < len(dates[istation]) \
                      and dates[istation][i] <= period[1]:
                # Observations.
                out_obs.append(obs[istation][i])
                # Simulations.
                for isim in range(len(sim)):
                    out_sim[isim].append(sim[isim][istation][i])
                i += 1

    return array(out_sim), array(out_obs)


def w_least_squares(sim, obs):
    """
    Solves a least square problem in order to optimally combine
    simulations. It minimizes (sim^T alpha - obs)^2.

    @type sim: 2D-array
    @param sim: The simulated concentrations are a 2D-array, (simulation x
    concentrations).
    @type obs: 1D-array
    @param obs: Observations (or any other target).

    @rtype: 1D-array
    @return: The coefficients (or weights) 'alpha' of the linear combination.
    """
    return matrixmultiply(scipy.linalg.inv(matrixmultiply(sim,
                                                          transpose(sim))),
                          matrixmultiply(sim, obs))


def m_least_squares(sim, obs):
    """
    Returns the optimal model in the least-square sense. It minimizes (sim^T
    alpha - obs)^2 and returns 'sim^T alpha'.

    @type sim: 2D-array
    @param sim: The simulated concentrations are a 2D-array, (simulation x
    concentrations).
    @type obs: 1D-array
    @param obs: Observations (or any other target).
    
    @rtype: 1D-array
    @return: The linear combination 'sim^T alpha'.
    """
    return matrixmultiply(transpose(sim), w_least_squares(sim, obs))


def w_unbiased_least_squares(sim, obs):
    """
    Solves a least square problem in order to optimally combine
    simulations with the constraint to be unbiased. It minimizes ((sim^T -
    <sim^T>) alpha + <obs> - obs)^2.

    @type sim: 2D-array
    @param sim: The simulated concentrations are a 2D-array, (simulation x
    concentrations).
    @type obs: 1D-array
    @param obs: Observations (or any other target).

    @rtype: 1D-array
    @return: The coefficients (or weights) 'alpha' of the linear unbiased
    combination.

    @note: This is also the superensemble coefficients.
    """
    obs = obs - obs.mean()
    sim = array([x - x.mean() for x in sim])
    return w_least_squares(sim, obs)


def m_unbiased_least_squares(sim, obs):
    """
    Returns the optimal model in the least-square sense with the constraint to
    be unbiased. It minimizes ((sim^T - <sim^T>) alpha + <obs> - obs)^2.

    @type sim: 2D-array
    @param sim: The simulated concentrations are a 2D-array, (simulation x
    concentrations).
    @type obs: 1D-array
    @param obs: Observations (or any other target).

    @rtype: 1D-array
    @return: The linear combination '(sim^T - <sim^T>) alpha + <obs>'.

    @note: This is also the superensemble combination.
    """
    obs_mean = obs.mean()
    obs = obs - obs_mean
    sim = array([x - x.mean() for x in sim])
    return matrixmultiply(transpose(sim), w_least_squares(sim, obs)) \
           + obs_mean
