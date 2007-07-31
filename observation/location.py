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
#     http://www.enpc.fr/cerea/polyphemus/atmopy.html


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

    def GetRealName(self):
        """
        Returns the real name of the station.

        @rtype: string
        @return: The real name of the station.
        """
        try:
            return self.real_name
        except:
            return self.name

    def GetName(self):
        """
        Returns the name of the station.

        @rtype: string
        @return: The name of the station.
        """
        return self.name

    def GetLatitude(self):
        """
        Returns the latitude of the station.

        @rtype: float
        @return: The latitude of the station.
        """
        return self.latitude

    def GetLongitude(self):
        """
        Returns the longitude of the station.

        @rtype: float
        @return: The longitude of the station.
        """
        return self.longitude

    def GetAltitude(self):
        """
        Returns the altitude of the station.

        @rtype: float
        @return: The altitude of the station.
        """
        try:
            return self.altitude
        except:
            return 0.

    def GetCountry(self):
        """
        Returns the country of the station.

        @rtype: string
        @return: The country of the station.
        """
        return self.country

    def GetType(self):
        """
        Returns the type of the station.

        @rtype: string
        @return: The type of the station.
        """
        return self.type

    def GetNetwork(self):
        """
        Returns the network name of the station.

        @rtype: string
        @return: The network name of the station.
        """
        return self.network

    def FromAirparifString(self, str):
        """
        Sets station attributes from a string.

        @type str: string
        @param str: The string in Airparif format that defines the station.
        The string contains the following fields (separated by comas):
           0. the station name;
           1. the longitude (format: DD MM SS);
           2. the latitude (format: DD MM SS);
           3. the type.
        where coordinates are provided with degrees (DD), minutes (MM)
        and seconds (SS).
        """
        l = str.strip().split(",")
        self.name = l[0]
        longitude = (l[1]).split(" ")
        latitude = (l[2]).split(" ")
        self.type = l[3]
        self.latitude = float(latitude[0]) + float(latitude[1]) / 60. \
                        + float(latitude[2]) / 3600.
        self.longitude = float(longitude[0]) + float(longitude[1]) / 60. \
                         + float(longitude[2]) / 3600.
        self.network = "Airparif"
        self.country = "FR"

    def FromBdqaString(self, str):
        """
        Sets station attributes from a string.

        @type str: string
        @param str: The string in BDQA format that defines the station. The
        string contains the following fields (separated by blank spaces):
           0. the station name (BDQA code);
           1. the station real-name;
           2. the latitude (float);
           3. the longitude (float);
           4. the type.
        """
        def convert(str):
            latlon = str.strip()
            pos = True
            if latlon[0] == '-':
                latlon = latlon[1:]
                pos = False
            latlon = latlon.split('.')[0]
            if len(latlon) > 6:
                return 999.
            latlon = latlon.zfill(6)
            res = float(latlon[0:2]) \
                  + float(latlon[2:4]) / 60. + float(latlon[4:6]) / 3600.
            if pos:
                return res
            else:
                return -res
        l = str.strip().split(',')
        self.name = l[0]
        self.real_name = l[1]
        self.latitude = convert(l[2])
        self.longitude = convert(l[3])
        self.altitude = float(l[4])
        self.network = "BDQA"
        self.type = l[5]
        self.country = "FR"

    def FromEmepString(self, str):
        """
        Sets station attributes from a string.

        @type str: string
        @param str: The string in Emep format that defines the station. The
        string contains the following fields (separated by blank spaces):
           0. the station name (Emep code);
           1. the station real-name;
           2. the latitude (DD MM SS [NS]);
           3. the longitude (DD MM SS [EO]);
           4. altitude (float).
        """
        l = str.strip().split()
        self.name = l[0]
        self.country = self.name[:2]
        self.real_name = " ".join(l[1:-9])
        self.altitude = float(l[-1])
        self.longitude = float(l[-5]) \
                         + float(l[-4]) / 60. + float(l[-3]) / 3600.
        if l[-2].lower() != 'e':
            self.longitude *= -1.
        self.latitude = float(l[-9]) \
                        + float(l[-8]) / 60. + float(l[-7]) / 3600.
        if l[-6].lower() != 'n':
            self.latitude *= -1.
        self.network = "EMEP"
        self.type = "EMEP"
        
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
        self.real_name = self.name
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
        lines = [x for x in open(filename).readlines() if x.strip() != '']
        for line in lines:
            if Station(line, type).name == station_name:
                self.FromString(line, type)
                break
    
    def IsInsideBox(self, lat_min, lat_max, lon_min, lon_max):
        """
        Checks wether the station is inside a given area.

        @type lat_min: float
        @param lat_min: Minimum latitude for area.
        @type lat_max: float
        @param lat_max: Maximum latitude for area.
        @type lon_min: float
        @param lon_min: Minimum longitude for area.
        @type lon_max: float
        @param lon_max: Maximum longitude for area.

        @rtype: Boolean
        @return: True if Station is in given area, False otherwise.
        """
        return self.latitude >= lat_min \
               and self.latitude <= lat_max \
               and self.longitude >= lon_min \
               and self.longitude <= lon_max

    def IsInsideGridBox(self, origins, deltas, lengths):
        """
        Checks wether the station is located inside a given
        area defined by (lat, lon) origins, deltas and lengths of
        cells.

        @type origins: (float, float) tuple
        @param origins: (latitude, longitude) coordinates of the SW
        origin for the area.
        @type deltas: (float, float) tuple
        @param deltas: (deltax, deltay) distance between two cells on latitude
        and longitude.
        @type lengths: (int, int) tupe
        @param lengths: (sizex, sizey) number of cells on latitude and longitude.
        @rtype: Boolean
        @return: True if station is in given area, False otherwise.
        """
        return self.IsInsideBox(origins[0], origins[0] \
                                + deltas[0] * float(lengths[0] - 1), \
                                origins[1], origins[1] \
                                + deltas[1] * float(lengths[1] - 1))


def is_urban(station):
    """
    Tests if the station is of urban type.

    @type station: Station
    @param station: The station to test as urban or not.
    @rtype: Boolean
    @return: True if station is marked as urban, False otherwise.
    """
    return station.type1 == "URB"


def is_rural(station):
    """
    Tests if the station is of rural type.

    @type station: Station
    @param station: The station to test as rural or not.
    @rtype: Boolean
    @return: True if station is marked as rural, False otherwise.
    """
    return station.type1 == "RUR"


def has_valid_latlon(station):
    """
    Tests if the given station has valid latitude and longitude (ie not null).
    @type station: Station
    @param station: The station to test.
    @rtype: Boolean
    @return: True if station has not null lagitude or longitude ,
    False otherwise (both null).
    """
    return station.latitude != 0.0 and station.longitude != 0.0


def get_simulated_at_location(origin, delta, data, point):
    """
    Gets a time sequence of data at specified location
    using bilinear interpolation.

    @type origin: (*, float, float) tuple
    @param origin: Grid origin, ie (t_min, y_min, x_min).
    Only y_min and x_min are used in this function.
    @type delta: (*, float, float) tuple
    @param delta: Grid deltas, ie (delta_t, delta_y, delta_x). Only
    delta_x and delta_y are used in this function.
    @type data: 3D numpy.array
    @param data: 3D array of data to interpolate with T, Y, X dimensions.
    @type point: (float, float) tuple
    @param point: (latitude, longitude) of the point where the time sequence
    must be computed.
    @rtype: 1D numpy.array
    @return: Time sequence of data at given point.
    """
    # Gets index of bottom right data point of specified point
    index_y = int((point[0] - origin[1]) / delta[1])
    index_x = int((point[1] - origin[2]) / delta[2])

    # Interpolation impossible.
    if index_x >= data.shape[2] or index_y >= data.shape[1] \
           or index_x < 0 or index_y < 0:
        return numpy.array([])

    # Interpolation coefficients.
    coeff_y = (point[0] - origin[1] - delta[1] * index_y) / delta[1]
    coeff_x = (point[1] - origin[2] - delta[2] * index_x) / delta[2]

    return (1.0 - coeff_y) * (1.0 - coeff_x) * data[:, index_y, index_x] \
           + coeff_y * coeff_x * data[:, index_y + 1, index_x + 1] \
           + coeff_y * (1.0 - coeff_x) * data[:, index_y + 1, index_x]  \
           + (1.0 - coeff_y) * coeff_x * data[:, index_y, index_x + 1]


def get_simulated_at_locations(origins, deltas, data, point_list):
    """
    Gets a list of time sequences of data at specified
    locations using bilinear interpolation.

    @type origins: (*, float, float) tuple
    @param origins: Grid origin, ie (t_min, y_min, x_min).
    Only y_min and x_min are used in this function.
    @type deltas: (*, float, float) tuple
    @param deltas: Grid deltas, ie (delta_t, delta_y, delta_x). Only
    delta_x and delta_y are used in this function.
    @type data: 3D numpy.array
    @param data: 3D array of data to interpolate with T, Y, X dimensions.
    @type point_list: sequence of (float, float) tuples
    @param point_list: Sequence of (latitude, longitude) of the points where the time
    sequences must be computed.
    @rtype: sequence of 1D numpy.array
    @return: Sequence of time sequences of data at given points.
    """
    ret = []
    for i in point_list:
        ret.append(get_simulated_at_location(origins, deltas, data, i))
    return ret


def get_simulated_at_location_closest(origins, deltas, data, point):
    """
    Gets a time sequence of data at specified location using closest
    neighbour values.

    @type origins: (*, float, float) tuple
    @param origins: Grid origin, ie (t_min, y_min, x_min).
    Only y_min and x_min are used in this function.
    @type deltas: (*, float, float) tuple
    @param deltas: Grid deltas, ie (delta_t, delta_y, delta_x). Only
    delta_x and delta_y are used in this function.
    @type data: 3D numpy.array
    @param data: 3D array of data to interpolate with T, Y, X dimensions.
    @type point: (float, float) tuple
    @param point: (latitude, longitude) of the point where the time sequence
    must be computed.
    @rtype: 1D numpy.array
    @return: Time sequence of data at given point.
    """
    # data : numpy, T Y X
    # point : ( latitude, longitude )
    # origins : ( Xmin, Ymin, Tmin )
    # deltas : ( DeltaX, DeltaY, DeltaT )

    # Closest point :
    index_y = int(round((point[0] - origins[1]) / deltas[1]))
    index_x = int(round((point[1] - origins[2]) / deltas[2]))

    # point is on right border
    if index_x == data.shape[2]:
        index_x = index_x - 1
    # point is on top border
    if index_y == data.shape[1]:
        index_y = index_y - 1
    return data[:,index_y, index_x]


def get_simulated_at_locations_closest(origins, deltas, data, point_list):
    """
    Gets a list of time sequences of data at specified
    locations using closest neighbours.

    @type origins: (*, float, float) tuple
    @param origins: Grid origin, ie (t_min, y_min, x_min).
    Only y_min and x_min are used in this function.
    @type deltas: (*, float, float) tuple
    @param deltas: Grid deltas, ie (delta_t, delta_y, delta_x). Only
    delta_x and delta_y are used in this function.
    @type data: 3D numpy.array
    @param data: 3D array of data to interpolate with T, Y, X dimensions.
    @type point_list: sequence of (float, float) tuples
    @param point_list: Sequence of (latitude, longitude) of the points where the time
    sequences must be computed.
    @rtype: sequence of 1D numpy.array
    @return: Sequence of time sequences of data at given points.
    """
    ret = numpy.array([])
    for i in point_list:
        ret.append(get_simulated_at_location_closest(origins, deltas, \
                                                     data, i))
    return ret


def get_simulated_at_station(origins, deltas, data, station):
    """
    Gets a time sequence of data at specified station
    using bilinear interpolation.

    @type origins: (*, float, float) tuple
    @param origins: Grid origin, ie (t_min, y_min, x_min).
    Only y_min and x_min are used in this function.
    @type deltas: (*, float, float) tuple
    @param deltas: Grid deltas, ie (delta_t, delta_y, delta_x). Only
    delta_x and delta_y are used in this function.
    @type data: 3D numpy.array
    @param data: 3D array of data to interpolate with T, Y, X dimensions.
    @type station: Station
    @param station: station where the time sequence must be computed.
    @rtype: 1D numpy.array
    @return: Time sequence of data at given point.
    """
    # data: numpy, T Y X
    # point: (latitude, longitude)
    # origins: (t_min, y_min, x_min)
    # deltas: (delta_t, delta_y, delta_x)
    return get_simulated_at_location(origins, deltas, \
                                     data, (station.latitude, \
                                            station.longitude))


def get_simulated_at_station_closest(origins, deltas, data, station):
    """
    Gets a time sequence of data at specified station using the closest data,
    that is, without interpolation.

    @type origins: (*, float, float) tuple
    @param origins: Grid origin, ie (t_min, y_min, x_min).
    Only y_min and x_min are used in this function.
    @type deltas: (*, float, float) tuple
    @param deltas: Grid deltas, ie (delta_t, delta_y, delta_x). Only
    delta_x and delta_y are used in this function.
    @type data: 3D numpy.array
    @param data: 3D array of data to interpolate with T, Y, X dimensions.
    @type station: Station
    @param station: station where the time sequence must be computed.
    @rtype: 1D numpy.array
    @return: Time sequence of data at given point.
    """
    return get_simulated_at_location_closest(origins, deltas, \
                                             data, (station.latitude, \
                                                    station.longitude))


def get_simulated_at_stations(origins, deltas, data, stations):
    """
    Gets a list of time sequences of data at specified
    stations using bilinear interpolation.

    @type origins: (*, float, float) tuple
    @param origins: Grid origin, ie (t_min, y_min, x_min).
    Only y_min and x_min are used in this function.
    @type deltas: (*, float, float) tuple
    @param deltas: Grid deltas, ie (delta_t, delta_y, delta_x). Only
    delta_x and delta_y are used in this function.
    @type data: 3D numpy.array
    @param data: 3D array of data to interpolate with T, Y, X dimensions.
    @type stations: sequence of (float, float) tuples
    @param stations: Sequence of Station giving the stations where the time
    sequences must be computed.
    @rtype: sequence of 1D numpy.array
    @return: Sequence of time sequences of data at given points.
    """
    ret = []
    for i in stations:
        ret.append(get_simulated_at_station(origins, deltas, data, i))
    return ret


def get_station(station_list, station_name):
    """
    Gets a Station object given its name and a list of stations.

    @type station_list: sequence of Station
    @param station_list: Sequence of stations in which to search
    the given station name.
    @type station_name: string
    @param station_name: Name of the station to search for in the list.
    @rtype: Station
    @return: The Station object corresponding to the station name in the given list
    of stations.
    """
    for i in station_list:
        if i.name == station_name:
            ret = i
            break
    return ret


def filter_stations(filter_func, station_list):
    """
    Filters a station list in place according to the given filter.
    To have a filter not acting in place, use the filter python
    builtin.

    @type filter_func: Python function
    @param filter_func: The function used to filter the station list. This function must
    take a Station object as argument, and must return a boolean.
    @type station_list: sequence of Station
    @param station_list: sequence of stations to filter.
    @rtype: sequence of Station
    @return: Sequence of stations filtered in place.
    """
    for i in range(len(station_list) - 1, -1, -1):
        if not filter_func(station_list[i]):
            station_list.pop(i)
    return station_list


def map_stations(bool_func, station_list):
    """
    Returns a boolean list containing the return values of the
    given function applied on every station of the list.
    This just calls the map builtin function.

    @type bool_func: Python function
    @param bool_func: The function mapped to every station of the station_list.
    @type station_list: sequence of Station
    @param station_list: sequence of stations to apply bool_func to.
    @rtype: Boolean sequence
    @return: A boolean sequence, results of bool_func applied to every
    stations of the list.
    """
    return map(bool_func, station_list)


def filter_stations_observations(filter_func, station_list, observations_list):
    """
    Filters a station list and corresponding observations list in
    place according to the given filter which takes a station and an
    observation array in argument.

    @type filter_func: Python function
    @param filter_func: The function used to filter the station sequence
    and observation sequence . This function must
    take a Station object and the corresponding observations sequence as argument,
    and must return a boolean.
    @type station_list: sequence of Station
    @param station_list: sequence of stations to filter.
    @type observations_list: sequence of 1D numpy.array
    @param observations_list: sequence of observations to filter.
    @rtype: Station sequence, 1D numpy.array sequence
    @return: Stations sequence and observations sequence, filtered in place.
    """
    for i in range(len(station_list) - 1, -1, -1):
        if not filter_func(station_list[i], observations_list[i]):
            station_list.pop(i)
            observations_list.pop(i)
    return station_list, observations_list


def map_stations_observations(map_func, station_list, observations_list):
    """
    Returns a sequence containing the return values of the
    given function applied on every station and observation of the
    sequences.

    @type map_func: Python function
    @param map_func: The function used to map the station sequence
    and observation sequence. This function must
    take a Station object and the corresponding observations array as argument,
    and must return a boolean.
    @type station_list: sequence of Station
    @param station_list: sequence of stations to map.
    @type observations_list: sequence of 1D numpy.array
    @param observations_list: sequence of observations to filter.
    @rtype: Boolean sequence
    @return: A boolean sequence, results of map_func applied to every
    stations and observations of the sequences.
    """
    ret = numpy.array([])
    for i in range(len(station_list)):
        ret.append(map_func(station_list[i], observations_list[i]))
    return ret
