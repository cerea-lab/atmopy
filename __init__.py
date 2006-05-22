# Copyright (C) 2005 CEREA
#     Authors: Vincent Picavet, Vivien Mallet
#
# This file is part of AtmoPy package.


"""
Copyright (C) 2005 CEREA

CEREA (http://www.enpc.fr/cerea/) is a joint laboratory of
ENPC (http://www.enpc.fr/) and EDF R&D (http://www.edf.fr/).

AtmoPy is a tool for data processing and visualization in atmospheric
sciences.

AtmoPy is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

AtmoPy is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License (file ``license'') for more details.

For more information, please see the AtmoPy home page:
http://www.enpc.fr/cerea/atmopy/
"""


import display
try:
    import ensemble
except:
    pass
import io
import observation
import stat
import talos
