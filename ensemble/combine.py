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
import scipy.stats.stats


def collect(sim, obs, dates = None, stations = None, period = None,
            stations_out = None):
    """
    Collects data (observations and simulated concentrations) over a given
    period and at a given set of stations.

    @type sim: list of list of 1D-array, or list of 1D-array.
    @param sim: The list (indexed by simulations) of lists (indexed by
    stations) of simulated concentrations, or the list (indexed by stations)
    of simulated concentrations.
    @type obs: list of 1D-array
    @param obs: The list (indexed by stations) of observed concentrations.
    @type dates: list of list of datetime
    @param dates: The list (indexed by stations) of list of dates at which the
    data is defined. Both observations and simulated data (of every ensemble)
    are assumed to be designed at the same dates.
    @type stations: list of Station
    @param stations: The stations at which the concentrations are given.
    @type period: 2-tuple of datetime, or datetime, or list of datetime
    @param period: The period where to select the concentrations (bounds
    included). A single date may be provided. If a list is provided, the
    period is defined by the first and the last dates in the list.
    @type stations_out: list of Station, or Station
    @param stations_out: The station(s) at which the concentrations are
    selected.

    @rtype: (1D-array, 2D-array)
    @return: The observed concentrations in a 1D-array and the corresponding
    simulated concentrations in a 2D-array (simulations x concentrations).
    """
    # Initializations.
    if isinstance(sim[0], NumArray):
        sim = (sim, )

    if dates == None:
        dates = [range(len(x)) for x in obs]
        period = None
    elif isinstance(dates[0], datetime.datetime) \
             or isinstance(dates[0], datetime.date):
        dates = (dates, )
    if period == None:
        period = (min([x[0] for x in dates]), max([x[-1] for x in dates]))
    elif isinstance(period, datetime.datetime) \
             or isinstance(period, datetime.date):
        period = (period, period)
    elif len(period) == 1:
        period = (period[0], period[0])
    elif len(period) > 2:
        period = (period[0], period[-1])

    if stations == None:
        stations = range(len(obs))
        stations_out = None
    elif isinstance(stations, observation.Station) \
             or isinstance(stations, str) \
             or isinstance(stations, int):
        stations = (stations, )
    if stations_out == None:
        stations_out = stations
    elif isinstance(stations_out, observation.Station) \
           or isinstance(stations_out, str) \
           or isinstance(stations_out, int):
        stations_out = (stations_out, )

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


def m_mean(sim):
    """
    Returns the mean of an ensemble.

    @type sim: 2D-array
    @param sim: The simulated concentrations are a 2D-array, (simulation x
    concentrations).

    @rtype: 1D-array
    @return: The mean of the simulations.
    """
    return array(scipy.stats.stats.mean(sim, 0))


def m_median(sim):
    """
    Returns the median of an ensemble.

    @type sim: 2D-array
    @param sim: The simulated concentrations are a 2D-array, (simulation x
    concentrations).

    @rtype: 1D-array
    @return: The median of the simulations.
    """
    return array(scipy.stats.stats.median(sim, 0))


def combine_step(dates, sim, coeff_dates, coeff_step):
    """
    Combines the simulated concentrations based on coefficients provided for
    each date. The same coefficients are applied to all stations.

    @type dates: list of list of datetime
    @param dates: The list (indexed by stations) of the list of dates at which
    the concentrations are defined.
    @type sim: list of list of 1D-array, or list of 1D-array.
    @param sim: The list (indexed by simulations) of lists (indexed by
    stations) of simulated concentrations, or the list (indexed by stations)
    of simulated concentrations.
    @type coeff_dates: list of datetime
    @param coeff_dates: The dates at which the coefficients in 'coeff_step'
    are defined.
    @type coeff_step: list of array
    @param coeff_step: The coefficients of the linear combination. They are
    stored in a list (indexed by dates) of 1D-arrays of coefficients. The
    first combination is associated with the earliest date of 'dates' and the
    last combination is associated with the latest date of 'dates'.

    @rtype: list of array
    @return: The ensemble based on the linear combination. It is returned in a
    list (indexed by stations) of 1D-arrays (that contain the time series).
    """
    # Initializations.
    if isinstance(sim[0], NumArray):
        sim = (sim, )

    if isinstance(dates[0], datetime.datetime) \
           or isinstance(dates[0], datetime.date):
        dates = (dates, )

    Nsim = len(sim)
    Nstations = len(sim[0])
    Ndates = len(coeff_dates)

    output_sim = [[] for i in range(Nstations)]

    # Combining.
    for istation in range(Nstations):
        icoeff = 0
        for idate in range(len(dates[istation])):
            # Corresponding index in 'coeff_dates' and 'coeff_step'.
            while icoeff < Ndates \
                      and coeff_dates[icoeff] != dates[istation][idate]:
                icoeff += 1
            if icoeff == Ndates:
                raise Exception, "Unable to find coefficients for date " \
                      + str(dates[istation][idate]) + "."
            # Concentrations of the ensemble.
            data = array([sim[i][istation][idate] for i in range(Nsim)])
            # Combination.
            output_sim[istation].append((coeff_step[icoeff] * data).sum())
        output_sim[istation] = array(output_sim[istation])

    return output_sim


def combine_step_unbiased(dates, sim, obs, coeff_dates, coeff_step):
    """
    Combines the simulated concentrations based on coefficients provided for
    each date. The same coefficients are applied to all stations so that the
    overall field is unbiased. At each step, the formula is: output_s =
    <obs>_s + sum_i coeff_step_i (sim_{s, i} - <sim_i>_s), where s stands for
    station and i is the simulation index.

    @type dates: list of list of datetime
    @param dates: The list (indexed by stations) of the list of dates at which
    the concentrations are defined.
    @type sim: list of list of 1D-array, or list of 1D-array.
    @param sim: The list (indexed by simulations) of lists (indexed by
    stations) of simulated concentrations, or the list (indexed by stations)
    of simulated concentrations.
    @type obs: list of 1D-array
    @param obs: The list (indexed by stations) of observed concentrations.
    @type coeff_dates: list of datetime
    @param coeff_dates: The dates at which the coefficients in 'coeff_step'
    are defined.
    @type coeff_step: list of array
    @param coeff_step: The coefficients of the linear combination. They are
    stored in a list (indexed by dates) of 1D-arrays of coefficients. The
    first combination is associated with the earliest date of 'dates' and the
    last combination is associated with the latest date of 'dates'.

    @rtype: list of array
    @return: The ensemble based on the linear combination. It is returned in a
    list (indexed by stations) of 1D-arrays (that contain the time series).
    """
    # Initializations.
    if isinstance(sim[0], NumArray):
        sim = (sim, )

    if isinstance(dates[0], datetime.datetime) \
           or isinstance(dates[0], datetime.date):
        dates = (dates, )

    Nsim = len(sim)
    Nstations = len(sim[0])
    Ndates = len(coeff_dates)

    # Initializes the ensemble.
    output_sim = [[] for i in range(Nstations)]

    # Time indices for all stations.
    date_index = [0 for i in range(Nstations)]

    # Combining.
    for idate in range(len(coeff_dates)):
        # New indices.
        for i in range(Nstations):
            while date_index[i] < len(dates[i]) \
                      and dates[i][date_index[i]] < coeff_dates[idate]:
                date_index[i] += 1
        # Computing the means for the current step.
        obs_mean = []
        sim_mean = [[] for j in range(Nsim)]
        for i in range(Nstations):
            if date_index[i] < len(dates[i]) \
                   and dates[i][date_index[i]] == coeff_dates[idate]:
                obs_mean.append(obs[i][date_index[i]])
                for j in range(Nsim):
                    sim_mean[j].append(sim[j][i][date_index[i]])
        if len(obs_mean) == 0:   # Empty step.
            continue
        obs_mean = array(obs_mean).mean()
        for j in range(Nsim):
            sim_mean[j] = array(sim_mean[j]).mean()
        # Computes the ensemble value.
        for i in range(Nstations):
            if date_index[i] < len(dates[i]) \
                   and dates[i][date_index[i]] == coeff_dates[idate]:
                ens = obs_mean
                for j in range(Nsim):
                    ens += coeff_step[idate][j] * (sim[j][i][date_index[i]]
                                                   - sim_mean[j])
                output_sim[i].append(ens)

    for istation in range(Nstations):
        output_sim[istation] = array(output_sim[istation])

    return output_sim


def combine_station_step(dates, sim, coeff_dates, coeff_station_step):
    """
    Combines the simulated concentrations based on coefficients provided for
    each date and for each station.

    @type dates: list of list of datetime
    @param dates: The list (indexed by stations) of the list of dates at which
    the concentrations are defined.
    @type sim: list of list of 1D-array, or list of 1D-array.
    @param sim: The list (indexed by simulations) of lists (indexed by
    stations) of simulated concentrations, or the list (indexed by stations)
    of simulated concentrations.
    @type coeff_dates: list of list of datetime
    @param coeff_dates: The dates at which the coefficients in
    'coeff_station_step' are defined.
    @type coeff_step: list of list of array
    @param coeff_step: The coefficients of the linear combination. They are
    stored in a list (indexed by stations) of list (indexed by dates) of
    1D-arrays of coefficients. The first combination is associated with the
    earliest date of 'dates' and the last combination is associated with the
    latest date of 'dates'.

    @rtype: list of array
    @return: The ensemble based on the linear combination. It is returned in a
    list (indexed by stations) of 1D-arrays (that contain the time series).
    """
    # Initializations.
    if isinstance(sim[0], NumArray):
        sim = (sim, )

    if isinstance(dates[0], datetime.datetime) \
           or isinstance(dates[0], datetime.date):
        dates = (dates, )

    Nsim = len(sim)
    Nstations = len(sim[0])

    output_sim = [[] for i in range(Nstations)]

    # Combining.
    for istation in range(Nstations):
        icoeff = 0
        Ndates = len(coeff_dates[istation])
        for idate in range(len(dates[istation])):
            # Corresponding index in 'coeff_dates' and 'coeff_step'.
            while icoeff < Ndates \
                      and coeff_dates[istation][icoeff] \
                      != dates[istation][idate]:
                icoeff += 1
            if icoeff == Ndates:
                raise Exception, "Unable to find coefficients for date " \
                      + str(dates[istation][idate]) + "."
            # Concentrations of the ensemble.
            data = array([sim[i][istation][idate] for i in range(Nsim)])
            # Combination.
            output_sim[istation].append((coeff_step[istation][icoeff]
                                         * data).sum())
        output_sim[istation] = array(output_sim[istation])

    return output_sim
