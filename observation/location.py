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


class Station:
    """
    Stores information about an observation station
    """
    
    def __init__(self, str = "", type = ""):
        """
        Initializes the instance in case 'str' and 'type' are not empty.

        @type str: string
        @param str: The string to initialize the station with.
        @type type: string
        @param type: The type of the initialization string 'str'. It could be
        Pioneer or Emep.
        """
        if str != "" and type != "":
            getattr(self, "From" + type.capitalize() + "String")(str)
        
    def __str__(self):
        return self.name + " [" + self.real_name + "] (" \
               + str(self.latitude) + ", " + str(self.longitude) + ") " \
               + self.type + " " \
               + self.country + " " \
               + self.network

    def FromPioneerString(self, str):
        """
        Sets station attributes from a string.

        @type str: string
        @param str: The string in Pioneer format that defines the station. The
        string contains the following fields (separated by blank spaces):
           0. the longitude (float);
           1. the latitude (float);
           2. discarded field;
           3. discarded field;
           4. country;
           5. station type;
           6. discarded field;
           7. station name;
           8. AASQA (network);
           9. other fields (discarded).
        """
        values = str.strip().split()
        try:
            self.longitude = float(values[0])
        except ValueError:
            self.longitude = 999.
        try:
            self.latitude = float(values[1])
        except ValueError:
            self.latitude = 999.
        self.country = values[4]
        self.type = values[5]
        self.name = values[7]
        self.network = values[8]
        
    def FromFile(self, filename, station_name, type):
        """
        Loads station attributes from a text file.

        @type filename: string
        @param filename: The text file in which station attributes are to be
        found.
        @type station_name: string
        @param station_name: The name of the station.
        @type type: string
        @param type: The type of station file: Pioneer or Emep.
        """
        lines = open(filename).readlines()
        for line in lines:
            if Station(line, type).name == station_name:
                self.FromString(line, type)
                break
    
    def IsInsideBox(self, lat_min, lat_max, lon_min, lon_max):
        """ Check wether the station is inside a given area.
        Returns Boolean.
        """
        return self.latitude >= lat_min \
               and self.latitude <= lat_max \
               and self.longitude >= lon_min \
               and self.longitude <= lon_max

    def IsInsideGridBox(self, origins, deltas, lengths):
        """ Check wether the station is located inside a given
        area defined by (lat, lon) origins, deltas on and lengths of
        cells.
        Returns Boolean.
        """
        return self.IsInsideBox(origins[0], origins[0] \
                                + deltas[0] * float(lengths[0]), \
                                origins[1], origins[1] \
                                + deltas[1] * float(lengths[1]))


def is_urban(station):
    """ Returns true if the station is of urban type, false otherwise.
    Returns Boolean."""
    return station.type1 == "URB"


def is_rural(station):
    """ Returns true if the station is of rural type, false otherwise.
    Returns Boolean."""
    return station.type1 == "RUR"


def has_valid_latlon(station):
    """ Returns True if the station has not-null latitude and longitude,
    False otherwise.
    Returns Boolean."""
    return station.latitude != 0.0 and station.longitude != 0.0


def get_simulated_at_location(origin, delta, data, point):
    """ Gets a time sequence of data at specified location
    using bilinear interpolation.
    Returns 1D array."""
    # data: numarray, T Y X
    # point: (latitude, longitude)
    # origin: (t_min, y_min, x_min)
    # delta: (delta_t, delta_y, delta_x)
    
    # Gets index of bottom right data point of specified point
    index_y = int((point[0] - origin[1]) / delta[1])
    index_x = int((point[1] - origin[2]) / delta[2])

    # Interpolation impossible.
    if index_x >= data.getshape()[2] or index_y >= data.getshape()[1] \
           or index_x < 0 or index_y < 0:
        return numarray.array([])

    # Interpolation coefficients.
    coeff_y = (point[0] - origin[1] - delta[1] * index_y) / delta[1]
    coeff_x = (point[1] - origin[2] - delta[2] * index_x) / delta[2]
    
    return (1.0 - coeff_y) * (1.0 - coeff_x) * data[:, index_y, index_x] \
           + coeff_y * coeff_x * data[:, index_y + 1, index_x + 1] \
           + coeff_y * (1.0 - coeff_x) * data[:, index_y + 1, index_x]  \
           + (1.0 - coeff_y) * coeff_x * data[:, index_y, index_x + 1]


def get_simulated_at_locations(origins, deltas, data, point_list):
    """ Gets a list of time sequences of data at specified
    locations using bilinear interpolation.
    Returns list of 1D arrays.
    """
    ret = []
    for i in point_list:
        ret.append(get_simulated_at_location(origins, deltas, data, i))
    return ret


def get_simulated_at_location_closest(origins, deltas, data, point):
    """ Gets a time sequence of data at specified location.
    Returns 1D array."""
    # data : numarray, T Y X
    # point : ( latitude, longitude )
    # origins : ( Xmin, Ymin, Tmin )
    # deltas : ( DeltaX, DeltaY, DeltaT )

    # Closest point :
    index_y = int(round((point[0] - origin[1]) / delta[1]))
    index_x = int(round((point[1] - origin[2]) / delta[2]))

    # point is on right border
    if index_x == data.getshape()[2]:
        index_x = index_x - 1
    # point is on top border
    if index_y == data.getshape()[1]:
        index_y = index_y - 1
    return data[:,index_y, index_x]


def get_simulated_at_locations_closest(origins, deltas, data, point_list):
    """ Gets a a list of time sequences of data at specified
    locations using closest point.
    Returns list of 1D arrays.
    """
    ret = numarray.array([])
    for i in point_list:
        ret.append(get_simulated_at_location_closest(origins, deltas, \
                                                     data, i))
    return ret


def get_simulated_at_station(origins, deltas, data, station):
    """ Gets a time sequence of data at specified station
    using bilinear interpolation.
    Returns 1D array."""
    # data: numarray, T Y X
    # point: (latitude, longitude)
    # origins: (t_min, y_min, x_min)
    # deltas: (delta_t, delta_y, delta_x)
    return get_simulated_at_location(origins, deltas, \
                                     data, (station.latitude, \
                                            station.longitude))


def get_simulated_at_stations(origins, deltas, data, stations):
    """ Gets a a list of time sequences of data at specified
    stations locations using bilinear interpolation.
    Returns list of 1D arrays.
    """
    ret = []
    for i in stations:
        ret.append(get_simulated_at_station(origins, deltas, data, i))
    return ret


def get_station(station_list, station_name):
    """ Gets a Station object given its name and a list of stations.
    Returns Station."""
    for i in station_list:
        if i.name == station_name:
            ret = i
            break
    return ret


def filter_stations(filter_func, station_list):
    """ Filters a station list in place according to the given filter.
    To have a filter not acting in place, use the filter python
    builtin.
    Returns Station list.
    """
    for i in range(len(station_list) - 1, -1, -1):
        if not filter_func(station_list[i]):
            station_list.pop(i)
    return station_list


def map_stations(bool_func, station_list):
    """ Returns a boolean list containing the return values of the
    given function applied on every station of the list.
    This just calls the map builtin function.
    Returns boolean list.
    """
    return map(bool_func, station_list)


def filter_stations_observations(filter_func, station_list, observations_list):
    """ Filters a station list and corresponding observations list in
    place according to the given filter which takes a station and an
    observation array in argument.
    Returns Station list and observation list (Array)."""
    for i in range(len(station_list) - 1, -1, -1):
        if not filter_func(station_list[i], observations_list[i]):
            station_list.pop(i)
            observations_list.pop(i)
    return station_list, observations_list


def map_stations_observations(map_func, station_list, observations_list):
    """ Returns a list containing the return values of the
    given function applied on every station and observation of the
    lists.
    Returns list.
    """
    ret = numarray.array([])
    for i in range(len(station_list)):
        ret.append(map_func(station_list[i], observations_list[i]))
    return ret
