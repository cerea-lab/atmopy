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
import datetime
import os, sys
sys.path.insert(0, os.path.split(os.path.dirname(os.path.abspath(__file__)))[0])
import talos, observation, ensemble, measure
sys.path.pop(0)


def compute_stat(sim, obs, measures, dates = None, stations = None, period =
                 None, stations_out = None):
    """
    Computes a set of statistical measures for one simulation or for a set of
    simulations.

    @type sim: list of list of 1D-array, or list of 1D-array.
    @param sim: The list (indexed by simulations) of lists (indexed by
    stations) of simulated concentrations, or the list (indexed by stations)
    of simulated concentrations.
    @type obs: list of 1D-array
    @param obs: The list (indexed by stations) of observed concentrations.
    @type dates: list of list of datetime, or list of datetime
    @param dates: The list (indexed by stations) of list of dates at which the
    data is defined. Both observations and simulated data (of every ensemble)
    are assumed to be designed at the same dates. 'dates' may also be a list
    of datetime in case there is a single station. If 'dates' is set to None,
    all dates are included.
    @type stations: list of Station, or Station
    @param stations: The station(s) at which the concentrations are given. If
    it is set to None, all stations will be included.
    @type period: 2-tuple of datetime, or datetime, or string
    @param period: The period where to select the concentrations (bounds
    included). A single date may be provided. If 'period' is set to None, all
    input dates are included.
    @type stations_out: list of Station, or Station, or string
    @param stations_out: The station(s) at which the concentrations are
    selected. If 'stations_out' is set to None, all input dates are included.

    @rtype: dict of array
    @return: The statistical measures are a key of the output dictionary. Each
    value is a 1D-array (indexed by simulations).
    """

    ### Initializations.

    if isinstance(sim[0], NumArray):
        sim = (sim, )

    if isinstance(dates[0], datetime.datetime) \
           or isinstance(dates[0], datetime.date):
        dates = (dates, )
    elif dates == None:
        dates = [range(len(x)) for x in obs]
        period = None
    if isinstance(period, datetime.datetime) \
           or isinstance(period, datetime.date):
        period = (period, period)
    elif period == None:
        period = (min([x[0] for x in dates]), max([x[-1] for x in dates]))

    if isinstance(stations, observation.Station):
        stations = (stations, )
    elif stations == None:
        stations = range(len(obs))
        stations_out = None
    if stations_out == None:
        stations_out = stations

    Nsim = len(sim)

    # Functions to be applied.
    functions = talos.get_module_functions(measure, 2, measures)

    ### Statistics.

    stat_all = dict(zip(functions, [[] for f in functions]))

    s, o = ensemble.collect(sim, obs, dates, stations, period, stations_out)
    for i in range(Nsim):
        for f, r in zip(functions,
                        talos.apply_module_functions(measure, (s[i], o),
                                                     measures)[1]):
            stat_all[f].append(r)

    # To arrays.
    for k in stat_all.keys():
        stat_all[k] = array(stat_all[k])

    return stat_all


def compute_stat_step(dates, sim, obs, obs_type, measures, stations = None,
                      period = None, stations_out = None, ratio = 0.):
    """
    Computes a set of statistical measures for one simulation or for a set of
    simulations, and for all time step.

    @type dates: list of list of datetime, or list of datetime
    @param dates: The list (indexed by stations) of list of dates at which the
    data is defined. Both observations and simulated data (of every ensemble)
    are assumed to be designed at the same dates. 'dates' may also be a list
    of datetime in case there is a single station.
    @type sim: list of list of 1D-array, or list of 1D-array.
    @param sim: The list (indexed by simulations) of lists (indexed by
    stations) of simulated concentrations, or the list (indexed by stations)
    of simulated concentrations.
    @type obs: list of 1D-array
    @param obs: The list (indexed by stations) of observed concentrations.
    @type obs_type: string
    @param obs_type: The type of the concentrations: "hourly" or "peak".
    @type stations: list of Station, or Station
    @param stations: The station(s) at which the concentrations are given. If
    it is set to None, all stations will be included.
    @type period: 2-tuple of datetime, or datetime, or string
    @param period: The period where to select the concentrations (bounds
    included). A single date may be provided. If 'period' is set to None, all
    input dates are included.
    @type stations_out: list of Station, or Station, or string
    @param stations_out: The station(s) at which the concentrations are
    selected. If 'stations_out' is set to None, all input dates are included.
    @type ratio: float
    @param ratio: Minimum ratio of the number of available observations (per
    step) and the number of stations. A step at which the actual ratio is
    below this minimum is discarded.

    @rtype: (list of datetime, dict of array)
    @return: The statistical measures are a key of the output dictionary. Each
    value is a (simulation x step)-array. The dates associated with the steps
    with enough measurements are returned in a list.
    """

    ### Initializations.

    if isinstance(sim[0], NumArray):
        sim = (sim, )

    if obs_type != "hourly" and obs_type != "peak":
        raise Exception, "Concentrations must be hourly concentrations" \
              + " or peaks."
    
    if isinstance(period, datetime.datetime) \
           or isinstance(period, datetime.date):
        period = (period, period)
    elif period == None:
        period = (min([x[0] for x in dates]), max([x[-1] for x in dates]))

    Nsim = len(sim)
    Nstations = len(sim[0])

    # Functions to be applied.
    functions = talos.get_module_functions(measure, 2, measures)

    ### Statistics.

    # List of all steps.
    start_date = period[0]
    end_date = period[1]
    if obs_type == "hourly":
        range_delta = datetime.timedelta(0, 3600)
        Nsteps = (end_date - start_date).seconds / 3600 + 1
    else:
        start_date = observation.midnight(start_date)
        end_date = observation.midnight(end_date)
        range_delta = datetime.timedelta(1)
        Nsteps = (end_date - start_date).days + 1
    range_dates = [start_date + x * range_delta for x in range(Nsteps)]

    stat_step = dict(zip(functions,
                         [[[] for i in range(Nsim)] for f in functions]))

    output_dates = []
    for date in range_dates:
        s, o = ensemble.collect(sim, obs, dates, stations, date, stations_out)
        # Enough observations?
        if float(len(o)) / float(Nstations) < ratio:
            continue
        output_dates.append(date)
        for i in range(Nsim):
            for f, r in zip(functions,
                            talos.apply_module_functions(measure, (s[i], o),
                                                         measures)[1]):
                stat_step[f][i].append(r)

    # To arrays.
    for k in stat_step.keys():
        stat_step[k] = array(stat_step[k])

    return output_dates, stat_step


def compute_stat_station(sim, obs, measures, dates = None, stations = None,
                         period = None, stations_out = None):
    """
    Computes a set of statistical measures for one simulation or for a set of
    simulations, at given stations.

    @type sim: list of list of 1D-array, or list of 1D-array.
    @param sim: The list (indexed by simulations) of lists (indexed by
    stations) of simulated concentrations, or the list (indexed by stations)
    of simulated concentrations.
    @type obs: list of 1D-array
    @param obs: The list (indexed by stations) of observed concentrations.
    @type dates: list of list of datetime, or list of datetime
    @param dates: The list (indexed by stations) of list of dates at which the
    data is defined. Both observations and simulated data (of every ensemble)
    are assumed to be designed at the same dates. 'dates' may also be a list
    of datetime in case there is a single station. If 'dates' is set to None,
    all dates are included.
    @type stations: list of Station, or Station
    @param stations: The station(s) at which the concentrations are given. If
    it is set to None, all stations will be included.
    @type period: 2-tuple of datetime, or datetime, or string
    @param period: The period where to select the concentrations (bounds
    included). A single date may be provided. If 'period' is set to None, all
    input dates are included.
    @type stations_out: list of Station, or Station, or string
    @param stations_out: The station(s) at which the concentrations are
    selected. If 'stations_out' is set to None, all input dates are included.

    @rtype: dict of array
    @return: The statistical measures are a key of the output dictionary. Each
    value is a (simulation x station)-array.
    """

    ### Initializations.

    if isinstance(sim[0], NumArray):
        sim = (sim, )

    if isinstance(stations, observation.Station):
        stations = (stations, )
    elif stations == None:
        stations = range(len(obs))
        stations_out = None
    if stations_out == None:
        stations_out = stations

    Nsim = len(sim)

    # Functions to be applied.
    functions = talos.get_module_functions(measure, 2, measures)

    ### Statistics.

    stat_station = dict(zip(functions,
                            [[[] for i in range(Nsim)] for f in functions]))

    for station in stations_out:
        s, o = \
           ensemble.collect(sim, obs, dates, stations, period, station)
        for i in range(Nsim):
            for f, r in zip(functions,
                            talos.apply_module_functions(measure, (s[i], o),
                                                         measures)[1]):
                stat_station[f][i].append(r)

    # To arrays.
    for k in stat_station.keys():
        stat_station[k] = array(stat_station[k])

    return stat_station
