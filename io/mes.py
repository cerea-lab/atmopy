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
import os, sys
sys.path.insert(0, os.path.split(os.path.dirname(os.path.abspath(__file__)))[0])
import observation
sys.path.pop(0)


def load_stations(filename, origins = (0, 0), \
                  deltas = (0, 0), lengths = (0, 0)):
    """ Loads stations description from text file. Removes stations
    outside the domain described by origins, deltas and
    lengths (if specified).
    filename: name of the file that describes the stations.
    origins: coordinates of the first cell in the mesh.
    deltas: mesh sizes.
    lengths: lengths of the mesh.
    Returns sequence of Station."""
    stations = []
    try:
        f = open(filename)
        for i in f.readlines():
            station = observation.Station(i)
            if deltas == (0,0) or \
                   station.IsInsideGridBox(origins, deltas, lengths):
                stations.append(observation.Station(i))
        f.close()
    except IOError:
        pass
    return stations


def load_station(filename, station_name):
    """ Loads a station description from text file.
    Returns Station."""
    station = observation.Station()
    try:
        f = open(filename)
        i = f.readline()
        station = observation.Station(i)
        while i != "" and station.name != station_name:
            i = f.readline()
            station = observation.Station(i)
        f.close()
    except IOError:
        pass
    return station


def load_file_observations(name, directory="", \
                           year="", obs_type=""):
    """ Loads observations data from a file, puts it in a sequence.
    Returns sequence of dates and array of values."""
    slash = ""
    if directory != "" and year != "" and obs_type != "":
        if directory[-1] != '/':
            slash = "/"
        filename = directory + slash + obs_type + "_" \
                   + name + "." + year
    else:
        filename = name
    dates = []
    observations = []
    try:
        f = open(filename)
        for i in f.readlines():
            date = i.strip().split()[0]
            (year, month, day) = (int(date[0:4]),
                                  int(date[4:6]),
                                  int(date[6:8]))
            if len(date) == 10:
                # obs hours are in 01->24 format, we need 00->23
                hour = int(date[8:10]) - 1
                dates.append(datetime.datetime(year, month, \
                                               day, hour))
            else:
                dates.append(datetime.datetime(year, month, day))
            observations.append(float(i.strip().split()[1]))
        f.close()
    except IOError:
        pass
    return numarray.array(observations, 'Float32'), dates


def load_observations(stations, directory, year, obs_type):
    """ Loads observations data from files for given stations
    Returns list of date list and list of observations arrays."""
    obs_dates_list = []
    obs_list = []
    for i in stations:
        dates, obs = load_file_observations(i.name, directory, \
                                            year, obs_type)
        obs_dates_list.append(dates)
        obs_list.append(obs)
    return obs_list, obs_dates_list
