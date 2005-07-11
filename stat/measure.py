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


import math
import numarray


### Sources for formulas :
# [1] http://nwairquest.wsu.edu/projects/presentations/WRAP_CMAQ_Eval.pdf
# [2] http://www.raqc.org/ozone/EAC/MRP/MM5_Report/Appen_A.pdf
# [3] http://www.cleanairinfo.com/PMModelPerformanceWorkshop2004/presentations/Tonnesen_Nested_Grids_WRAP.ppt


## Mean Bias Error
## (MB) in [1], (MBE) in [2]
##
## \begin{displaymath}
##   \textrm{MBE} = \frac{1}{n} \sum_{i=1}^{n} x_i - y_i 
## \end{displaymath}
def mbe(data1, data2):
    """ Computes Mean Bias Error between data1 and data2.
    Returns real."""
    if len(data1) != len(data2):
        raise ValueError, "Data samples do not have the same length."
    return (data1 - data2).mean()


## Mean Absolute Gross Error (MAGE)
## MAGE in [1] and [2]
##
## \begin{displaymath}
##   \textrm{MAGE} = \frac{1}{n} \sum_{i=1}^{n} |x_i - y_i|
## \end{displaymath}
def mage(data1, data2):
    """ Computes Mean Absolute Gross Error (MAGE) between data1 and
    data2.
    Returns real."""
    if len(data1) != len(data2):
        raise ValueError, "Data samples do not have the same length."
    return (abs(data1 - data2)).mean()


## Mean Absolute Normalized Gross Error (MANGE)
## MNGE, MNE in [1], MANGE in [2]
##
## \begin{displaymath}
##   \textrm{MANGE} = \frac{1}{n}
##   \sum_{i=1}^{n} \frac{|x_i - y_i|}{y_i}
## \end{displaymath}
def mange(data1, data2):
    """ Computes Mean Absolute Normalized Gross Error (MANGE) between
    data1 and data2 1D arrays.
    MNGE = 1 / n * NME
    Returns real."""
    if len(data1) != len(data2):
        raise ValueError, "Data samples do not have the same length."
    return (abs(data1 - data2) / data2).mean()


## Root Mean Square Error (RMSE)
## RMSE in [1] and [2]
##
## \begin{displaymath}
##   \textrm{RMSE} = \sqrt{\frac{1}{n} \sum_{i=1}^{n} (x_i - y_i)^{2}}
## \end{displaymath}
def rmse(data1, data2):
    """ Computes Root Mean Square Error (RMSE) between data1 and data2.
    Returns real."""
    if len(data1) != len(data2):
        raise ValueError, "Data samples do not have the same length."
    temp = data1 - data2
    temp = temp*temp
    return math.sqrt(temp.mean())


## Correlation coefficient
##
## \begin{displaymath}
##   \textrm{correlation} = \frac{ \frac{1}{n} \sum_{i=1}^{n}(x_i -
##     \overline{x})(y_i - \overline{y})}
##   {\sqrt{\frac{1}{n}\sum_{i=1}^{n} (x_i - \overline{x})^{2} *
##       \frac{1}{n}\sum_{i=1}^{n} (y_i - \overline{y})^{2}}}
## \end{displaymath}
def correlation(data1, data2):
    """ Computes the correlation between data1 and data2.
    Returns real."""
    if len(data1) != len(data2):
        raise ValueError, "Data samples do not have the same length."
    diff1 = data1 - data1.mean()
    diff2 = data2 - data2.mean()
    return (diff1 * diff2).mean() / math.sqrt((diff1*diff1).mean() \
                                              * (diff2*diff2).mean())


## Coefficient of determination
## in [1]
##
## \begin{displaymath}
##   \textrm{coefficient of determination} = \frac{\bigl[\sum_{i=1}^n
## (x_i- \overline{x})(y_i - \overline{y})\bigr]^2} {\sum_{i=1}^n
## {(x_i - \overline{x})}^2 \sum_{i=1}^n {(y_i - \overline{y})}^2 }
## \end{displaymath}
def determination(data1, data2):
    """ Computes the coefficient of determination between data1 and
    data2. This is the correlation coefficient squared.
    Returns real."""
    correl = correlation(data1, data2)
    return  correl * correl


## Mean Normalized Bias Error (MNBE)
## MNB in [1], MNBE in [2]
##
## \begin{displaymath}
##   \textrm{MNBE} = \frac{1}{n} \sum_{i=1}^{n} \frac{x_i - y_i}{y_i}
## \end{displaymath}
def mnbe(data1, data2):
    """ Computes Mean Normalized Bias Error (MNBE) between
    data1 and data2 1D arrays.
    Returns real."""
    if len(data1) != len(data2):
        raise ValueError, "Data samples do not have the same length."
    return ((data1 - data2) / data2).mean()


## Mean Fractionalized Bias Error (MFBE)
## MFB in [1], MFBE in [2]
##
## \begin{displaymath}
##   \textrm{MFBE} = \frac{2}{n} \sum_{i=1}^{n} \frac{x_i - y_i}{x_i +
##     y_i}
## \end{displaymath}
def mfbe(data1, data2):
    """ Computes Mean Fractionalized Bias Error (MFBE) between
    data1 and data2 1D arrays.
    Returns real."""
    if len(data1) != len(data2):
        raise ValueError, "Data samples do not have the same length."
    return 2 * ((data1 - data2) / (data1 + data2)).mean()


## Fractional Gross Error (FGE)
## in [1]
##
## \begin{displaymath}
##   \textrm{FE} = \frac{2}{n} \sum_{i=1}^{n} \arrowvert
##   \frac{x_i - y_i}{x_i + y_i} \arrowvert
## \end{displaymath}
def fge(data1, data2):
    """ Computes Fractional Gross Error (FE) between
    data1 and data2 1D arrays.
    Returns real."""
    if len(data1) != len(data2):
        raise ValueError, "Data samples do not have the same length."
    return 2 * (abs((data1 - data2) / (data1 + data2))).mean()


## Bias Factor (BF)
## in [3]
##
## \begin{displaymath}
##   \textrm{BF} =
##   \frac{1}{n} \sum_{i=1}^{n} \frac{x_i}{y_i}
## \end{displaymath}
def bf(data1, data2):
    """ Computes Bias Factor (BF) of data1 and data2.
    Returns Real.
    """
    if len(data1) != len(data2):
        raise ValueError, "Data samples do not have the same length."
    return (data1/data2).mean()


## Peak Estimation Accuracy
## 
## \begin{displaymath}
##   \textrm{UPA} =
##   \frac{x_{max} - y_{max}}{y_{max}}
## \end{displaymath}
def pea(data1, data2):
    """ Computes Peak Estimation Accuracy between data1 and data2.
    This can be paired or unpaired peak prediction accuracy
    depending on simulated data used (interpolated or not..)
    Returns real."""
    max2 = data2.max()
    return (data1.max() - max2) / max2


## Normalized Mean Bias (NMB)
## in [1], [3]
##
## \begin{displaymath}
##   \textrm{NMB} = \frac{\sum_{i=1}^{n} x_i - y_i}{\sum_{i=1}^{n}
##   y_i} 
## \end{displaymath}
def nmb(data1, data2):
    """ Computes Normalized Mean Bias (NMB) between data1 and data2.
    Returns real."""
    if len(data1) != len(data2):
        raise ValueError, "Data samples do not have the same length."
    return (data1 - data2).sum() / data2.sum()


## Normalized Mean Error (NME)
## in [1], [3]
##
## \begin{displaymath}
##   \textrm{NME} = \frac{\sum_{i=1}^{n} |x_i - y_i|}{\sum_{i=1}^{n}
##    y_i}
## \end{displaymath}
def nme(data1, data2):
    """ Computes Normalized Mean Error (NME) between data1 and data2.
    Returns real."""
    if len(data1) != len(data2):
        raise ValueError, "Data samples do not have the same length."
    return (abs(data1 - data2)).sum() / data2.sum()
