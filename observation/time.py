# Copyright (C) 2005 CEREA
#     Authors: Vincent Picavet, Vivien Mallet
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


class Period:
    """Stores a time period."""
    start = datetime.datetime(1,1,1)
    end = datetime.datetime(1,1,1,1)

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __str__(self):
        """ Returns Period's presentation."""
        return str(self.start) + " -> " + str(self.end)


def get_period(dates):
    """ Returns the period containing all dates in dates. dates
    is sorted.
    Returns Period.
    """
    return Period(dates[0], dates[-1])


def get_periods(start, end, length=datetime.timedelta(1), \
                interperiod = datetime.timedelta(0), \
                fit_last = False):
    """ Returns a list of periods of given length (except last period
    if fit_last is True), beginning at given start date, ending
    at given end date, and with an interperiod time between them.
    By default, interperiod is null and length of period is one day.
    Returns list of Period."""
    periods = []
    if length != datetime.timedelta(0):
        in_period = False
        last_current = start
        current = start + length
        while current <= end:
            if in_period == True:

                last_current = current
                current = current + length
                in_period = not in_period
            else:
                periods.append(Period(last_current, current))
                last_current = current
                current = current + interperiod
                in_period = not in_period
        if not in_period and fit_last and last_current != end:
            periods.append(Period(last_current,end))
    return periods


def split_into_days(dates, data):
    """Returns a list of arrays which store the values
    for each day."""
    if len(data) != len(dates):
        raise ValueError, "Data and dates are not of the same length."

    if len(data) == 0:
        return [numarray.array([])], [[]]
    
    output_data = [[data[0]]]
    output_dates = [[dates[0]]]

    day = dates[0].date()
    for i in range(1, len(dates)):
        if dates[i].date() == day:
            output_data[-1].append(data[i])
            output_dates[-1].append(dates[i])
        else:
            output_data.append([data[i]])
            output_dates.append([dates[i]])
            day = dates[i].date()

    return output_dates, map(lambda x: numarray.array(x), output_data)


def mask_for_common_days(sim_dates, simulated, obs_dates, obs):
    """ Creates masks for simulated data and observation data
    corresponding to data of common dates.
    Returns numarrays masks for simulated data and observation data.
    """
    if len(simulated) != len(sim_dates) or len(obs) != len(obs_dates):
        print len(simulated), len(sim_dates), len(obs), len(obs_dates)
        raise ValueError, "Incompatible dimensions!"

    # Dates.
    sim_dates_float = list(sim_dates)
    map(lambda x: float(x.toordinal()) + float(x.hour) / 24., sim_dates_float)
    obs_dates_float = list(obs_dates)
    map(lambda x: float(x.toordinal()) + float(x.hour) / 24., obs_dates_float)

    # Selection.
    sim_condition = numarray.zeros(len(simulated))
    obs_condition = numarray.zeros(len(obs))

    # Selects the common days.
    j = 0
    for i in range(len(sim_dates_float)):
        while j < len(obs_dates_float) \
                  and obs_dates_float[j] < sim_dates_float[i]:
            j += 1
        if j == len(obs_dates_float):
            break
        if obs_dates_float[j] == sim_dates_float[i]:
           sim_condition[i] = 1
           obs_condition[j] = 1

    return sim_condition, obs_condition


def apply_mask_for_common_days(sim_dates, simulated, obs_dates, obs, \
                               mask_sim, mask_obs):
    """ Applies a mask returned by mask_for_common_days on
    simulated and observation data, and gets corresponding dates.
    Returns numarray for simulated and observations, list of datetime
    for dates.
    """
    if len(simulated) != len(sim_dates) or len(obs) != len(obs_dates):
        print len(simulated), len(sim_dates), len(obs), len(obs_dates)
        raise ValueError, "Incompatible dimensions!"

    common_dates = []
    # Selects the common days.
    for i in mask_sim:
        common_dates.append(sim_dates[i])

    return common_dates, simulated[numarray.where(mask_sim)], \
           obs[numarray.where(mask_obs)]


def restrict_to_common_dates(sim_dates, simulated, obs_dates, obs):
    """ Removes items from data and dates to keep only
    dates and corresponding data which are both in observations and
    simulated.
    Returns Arrays for simulated and observations, list of datetime
    for dates."""

    if len(simulated) != len(sim_dates) or len(obs) != len(obs_dates):
        print len(simulated), len(sim_dates), len(obs), len(obs_dates)
        raise ValueError, "Incompatible dimensions!"

    dates = list(sim_dates)
    sim_condition = numarray.zeros(len(simulated))
    obs_condition = numarray.zeros(len(obs))
    
    for i in range(len(dates)):
       try:
           ind = obs_dates.index(dates[i])
           sim_condition[i] = 1
           obs_condition[ind] = 1
       except ValueError:
           pass

    # print len(sim_condition)-1, range(len(sim_condition)-1, -1, -1), dates
    for i in range(len(sim_condition)-1, -1, -1):
        if sim_condition[i] == 0:
            dates.pop(i)

    return dates, simulated[numarray.where(sim_condition)], \
           obs[numarray.where(obs_condition)]


def restrict_to_common_days(sim_dates, simulated, obs_dates, obs):
    """ Removes items from data and dates to keep only
    daily data which are both in observations and
    simulated. Dates lists and data have to be sorted (by increasing
    time).
    Returns Arrays for simulated and observations, list of datetime
    for dates."""

    if len(simulated) != len(sim_dates) or len(obs) != len(obs_dates):
        print len(simulated), len(sim_dates), len(obs), len(obs_dates)
        raise ValueError, "Incompatible dimensions!"

    # Dates.
    sim_dates_iso = list(sim_dates)
    map(lambda x: x.date().isoformat(), sim_dates_iso)
    obs_dates_iso = list(obs_dates)
    map(lambda x: x.date().isoformat(), obs_dates_iso)

    # Selection.
    sim_condition = numarray.zeros(len(simulated))
    obs_condition = numarray.zeros(len(obs))

   # Gets the start date index for observations.
    obs_start = 0
    while(obs_dates_iso[obs_start] < sim_dates_iso[0]):
        obs_start = obs_start + 1

    common_dates = []
    old_ind = 0
    # Loops over observation dates and mark indices of matching dates.
    for i in range(obs_start, len(obs_dates_iso)):
        ind = old_ind
        while(sim_dates_iso[ind] < obs_dates_iso[i] \
              and ind < len(sim_dates_iso) - 1 ):
            ind = ind + 1
        if sim_dates_iso[ind] == obs_dates_iso[i]:
            sim_condition[ind] = 1
            obs_condition[i] = 1
            old_ind = ind
            common_dates.append(sim_dates[ind])
        else:
            old_ind = ind - 1

    return common_dates, simulated[numarray.where(sim_condition)], \
           obs[numarray.where(obs_condition)]


def restrict_to_common_days2(sim_dates, simulated, obs_dates, obs):
    """ Removes items from data and dates to keep only
    daily data which are both in observations and
    simulated.
    Returns Arrays for simulated and observations, list of datetime
    for dates."""

    if len(simulated) != len(sim_dates) or len(obs) != len(obs_dates):
        print len(simulated), len(sim_dates), len(obs), len(obs_dates)
        raise ValueError, "Incompatible dimensions!"

    # Dates.
    sim_dates_iso = list(sim_dates)
    map(lambda x: x.date().isoformat(), sim_dates_iso)
    obs_dates_iso = list(obs_dates)
    map(lambda x: x.date().isoformat(), obs_dates_iso)

    # Selection.
    sim_condition = numarray.zeros(len(simulated))
    obs_condition = numarray.zeros(len(obs))
    
    # Selects the common days.
    for i in range(len(sim_dates_iso)):
       try:
           ind = obs_dates_iso.index(sim_dates_iso[i])
           sim_condition[i] = 1
           obs_condition[ind] = 1
       except ValueError:
           pass

    # Extracts the common dates.
    common_dates = sim_dates
    for i in range(len(sim_condition)-1, -1, -1):
        if sim_condition[i] == 0:
            common_dates.pop(i)

    return common_dates, simulated[numarray.where(sim_condition)], \
           obs[numarray.where(obs_condition)]


def restrict_to_period(dates, data, period_date, end_date = None):
    """
    Returns data and associated dates within a given period.

    @type dates: list of datetime
    @param dates: The dates associated with data.
    @type data: array
    @param data: Array of data.
    @type period_date: Period, list of datetime, or datetime
    @param period_date: Defines:
    0. a period (Period object);
    1. a period through its bounds (list of datetime);
    2. the first date of the selected period.
    @type end_date: datetime
    @param end_date: the last date of the selected period (if not provided by
    'period_date').

    @rtype: (list of datetime, array)
    @return: The dates and data over the selected period.
    """
    condition = numarray.zeros(len(dates))
    if isinstance(period_date, Period):
        start_date = period_date.start
        end_date = period_date.end
    elif isinstance(period_date, (list, tuple)):
        start_date = period_date[0]
        end_date = period_date[-1]
    else:
        start_date = period_date
    istart = 0
    while istart < len(dates) and dates[istart] < start_date: istart += 1
    if istart == len(dates):
        return dates[:], data[:]
    iend = istart + 1
    while iend < len(dates) and dates[iend] <= end_date: iend += 1
    return dates[istart:(iend-1)], data[istart:(iend-1)]


def midnight(date):
    """Move to midnight in the current day. Midnight is assumed to be
    the beginning of the day."""
    return date - datetime.timedelta(0, 3600 * date.hour \
                                     + 60 * date.minute + date.second, \
                                     date.microsecond)


def timedelta2num(delta):
    """
    Converts datetime.timedelta to float day number as used in Matplotlib.

    @type delta: datetime.timedelta
    @param delta: The time-delta to be converted in days.
    
    @rtype: float
    @return: The number of days in 'delta'.
    """
    if delta < datetime.timedelta(0):
        num = -(date2num(datetime.datetime(1,1,1) - delta) \
              - date2num(datetime.datetime(1,1,1)))
    else:
        num = date2num(datetime.datetime(1,1,1) + delta) \
              - date2num(datetime.datetime(1,1,1))
    return num
           

def get_simulation_dates(t_min, date_ref, delta_t, Nt):
    """ Get a list of dates corresponding to the simulation data.
    t_min can be a number of hours since date_ref, or a datetime
    object. In this case, date_ref is ignored.
    Returns list of datetime."""
    sim_dates = []
    if type(t_min) == datetime.datetime:
        sim_date_start = t_min
    else:
        sim_date_start = date_ref + datetime.timedelta(hours = t_min)
    for i in range(Nt):
        sim_dates.append(sim_date_start + \
                         datetime.timedelta(hours = i * delta_t))
    return sim_dates


def remove_missing(dates, data, rm_value = -999):
    """
    Removes given values from a data array and removes the corresponding
    dates.

    @type dates: list of datetime
    @param dates: The dates at which data is provided.
    @type data: 1D numarray.array
    @param data: The data array to be filtered.
    @type rm_values: float or list of floats
    @param rm_values: The value(s) to be removed from 'data'.

    @rtype: (list of datetime, 2D numarray.array)
    @return: The data array and its dates without the specified values.
    """
    if isinstance(rm_value, (list, tuple)):
        for x in rm_value:
            dates, data = remove_missing(dates, data, x)
        return dates, data
    condition = data != rm_value
    data = data[condition]
    dates = [d for d, c in zip(dates, condition) if c]
    return dates, data
