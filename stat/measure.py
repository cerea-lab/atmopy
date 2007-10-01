# Copyright (C) 2005-2007, ENPC - INRIA - EDF R&D
#     Author(s): Vincent Picavet
#
# This file is part of AtmoPy library, a tool for data processing and
# visualization in atmospheric sciences.
#
# AtmoPy is developed in the INRIA - ENPC joint project-team CLIME and in
# the ENPC - EDF R&D joint laboratory CEREA.
#
# AtmoPy is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# AtmoPy is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# For more information, visit the AtmoPy home page:
#     http://cerea.enpc.fr/polyphemus/atmopy.html


import math


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
    """
    Computes Mean Bias Error between data1 and data2.

    @type data1: numpy.array
    @param data1: 1D array to compute bias from.

    @type data2: numpy.array
    @param data2: 1D array to compute bias from.

    @rtype: float
    @return: Mean Bias Error between data1 and data2.
    """
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
    """
    Computes Mean Absolute Gross Error (MAGE) between data1 and
    data2.
    
    @type data1: numpy.array
    @param data1: 1D array to compute error.

    @type data2: numpy.array
    @param data2: 1D array to compute error.

    @rtype: float
    @return: Mean Absolute Gross Error between data1 and data2.
    """
    if len(data1) != len(data2):
        raise ValueError, "Data samples do not have the same length."
    return (abs(data1 - data2)).mean()


## Mean Normalized Gross Error (MNGE)
## MNGE, MNE in [1], MANGE in [2]
##
## \begin{displaymath}
##   \textrm{MNGE} = \frac{1}{n}
##   \sum_{i=1}^{n} \frac{|x_i - y_i|}{y_i}
## \end{displaymath}
def mnge(data1, data2, cutoff = 0.):
    """
    Computes Mean Normalized Gross Error (MNGE) between data1 and data2 1D
    arrays.
    ( MNGE = 1 / n * NME )
    
    @type data1: numpy.array
    @param data1: 1D array to compute error.

    @type data2: numpy.array
    @param data2: 1D array to compute error.

    @type cutoff: float
    @param cutoff: The value below (or equal) which data is discarded. This
    filters 'data2' and corresponding 'data1' values.

    @rtype: float
    @return: Mean Normalized Gross Error (MNGE) between data1 and data2.
    """
    if len(data1) != len(data2):
        raise ValueError, "Data samples do not have the same length."
    data1 = data1[data2 > cutoff]
    data2 = data2[data2 > cutoff]
    return (abs(data1 - data2) / data2).mean()


## Root Mean Square Error (RMSE)
## RMSE in [1] and [2]
##
## \begin{displaymath}
##   \textrm{RMSE} = \sqrt{\frac{1}{n} \sum_{i=1}^{n} (x_i - y_i)^{2}}
## \end{displaymath}
def rmse(data1, data2):
    """ Computes Root Mean Square Error (RMSE) between data1 and data2.

    @type data1: numpy.array
    @param data1: 1D array to compute error.

    @type data2: numpy.array
    @param data2: 1D array to compute error.

    @rtype: float
    @return: Root Mean Square Error (RMSE) between data1
    and data2.
    """
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
    @type data1: numpy.array
    @param data1: 1D array to compute correlation.

    @type data2: numpy.array
    @param data2: 1D array to compute correlation.

    @rtype: float
    @return: Correlation coefficient between data1 and data2.
    """
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

    @type data1: numpy.array
    @param data1: 1D array to compute coefficient of determination.

    @type data2: numpy.array
    @param data2: 1D array to compute coefficient of determination.

    @rtype: float
    @return: Coefficient of determination between data1 and data2.
    """
    correl = correlation(data1, data2)
    return  correl * correl


## Mean Normalized Bias Error (MNBE)
## MNB in [1], MNBE in [2]
##
## \begin{displaymath}
##   \textrm{MNBE} = \frac{1}{n} \sum_{i=1}^{n} \frac{x_i - y_i}{y_i}
## \end{displaymath}
def mnbe(data1, data2, cutoff = 0.):
    """ Computes Mean Normalized Bias Error (MNBE) between
    data1 and data2 1D arrays.

    @type data1: numpy.array
    @param data1: 1D array to compute MNBE.

    @type data2: numpy.array
    @param data2: 1D array to compute MNBE.

    @type cutoff: float
    @param cutoff: The value below (or equal) which data is discarded. This
    filters 'data2' and corresponding 'data1' values.

    @rtype: float
    @return: Mean Normalized Bias Error between data1 and data2.
    """
    if len(data1) != len(data2):
        raise ValueError, "Data samples do not have the same length."
    data1 = data1[data2 > cutoff]
    data2 = data2[data2 > cutoff]
    return ((data1 - data2) / data2).mean()


## Mean Fractionalized Bias Error (MFBE)
## MFB in [1], MFBE in [2]
##
## \begin{displaymath}
##   \textrm{MFBE} = \frac{2}{n} \sum_{i=1}^{n} \frac{x_i - y_i}{x_i +
##     y_i}
## \end{displaymath}
def mfbe(data1, data2, cutoff = 0.):
    """ Computes Mean Fractionalized Bias Error (MFBE) between
    data1 and data2 1D arrays.

    @type data1: numpy.array
    @param data1: 1D array to compute MFBE.

    @type data2: numpy.array
    @param data2: 1D array to compute MFBE.

    @type cutoff: float
    @param cutoff: The value below (or equal) which data is discarded. This
    filters 'data2' and corresponding 'data1' values.

    @rtype: float
    @return: Mean Fractionalized Bias Error between data1 and data2.
    """
    if len(data1) != len(data2):
        raise ValueError, "Data samples do not have the same length."
    data1 = data1[data2 > cutoff]
    data2 = data2[data2 > cutoff]
    return 2 * ((data1 - data2) / (data1 + data2)).mean()


## Fractional Gross Error (FGE)
## in [1]
##
## \begin{displaymath}
##   \textrm{FE} = \frac{2}{n} \sum_{i=1}^{n} \arrowvert
##   \frac{x_i - y_i}{x_i + y_i} \arrowvert
## \end{displaymath}
def fge(data1, data2, cutoff = 0.):
    """ Computes Fractional Gross Error (FE) between
    data1 and data2 1D arrays.

    @type data1: numpy.array
    @param data1: 1D array to compute FE.

    @type data2: numpy.array
    @param data2: 1D array to compute FE.

    @type cutoff: float
    @param cutoff: The value below (or equal) which data is discarded. This
    filters 'data2' and corresponding 'data1' values.

    @rtype: float
    @return: Fractional Gross Error between data1 and data2.
    """
    if len(data1) != len(data2):
        raise ValueError, "Data samples do not have the same length."
    data1 = data1[data2 > cutoff]
    data2 = data2[data2 > cutoff]
    return 2 * (abs((data1 - data2) / (data1 + data2))).mean()


## Bias Factor (BF)
## in [3]
##
## \begin{displaymath}
##   \textrm{BF} =
##   \frac{1}{n} \sum_{i=1}^{n} \frac{x_i}{y_i}
## \end{displaymath}
def bf(data1, data2, cutoff = 0.):
    """ Computes Bias Factor (BF) of data1 and data2.

    @type data1: numpy.array
    @param data1: 1D array to compute BF.

    @type data2: numpy.array
    @param data2: 1D array to compute BF.

    @type cutoff: float
    @param cutoff: The value below (or equal) which data is discarded. This
    filters 'data2' and corresponding 'data1' values.

    @rtype: float
    @return: Bias Factor of data1 and data2.
    """
    if len(data1) != len(data2):
        raise ValueError, "Data samples do not have the same length."
    data1 = data1[data2 > cutoff]
    data2 = data2[data2 > cutoff]
    return (data1/data2).mean()


## Unpaired Peak Accuracy (or Peak Estimation Accuracy)
## 
## \begin{displaymath}
##   \textrm{UPA} =
##   \frac{x_{max} - y_{max}}{y_{max}}
## \end{displaymath}
def upa(data1, data2):
    """ Computes Unpaired Peak Accuracy between data1 and data2.
    This can be paired or unpaired peak prediction accuracy
    depending on simulated data used (interpolated or not..)

    @type data1: numpy.array
    @param data1: 1D array to compute Peak Estimation Accuracy.

    @type data2: numpy.array
    @param data2: 1D array to compute Peak Estimation Accuracy.

    @rtype: float
    @return: Unpaired Peak Accuracy of data1 and data2.
    """
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

    @type data1: numpy.array
    @param data1: 1D array to compute NMB.

    @type data2: numpy.array
    @param data2: 1D array to compute NMB.

    @rtype: float
    @return: Normalized Mean Bias between data1 and data2.
    """
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

    @type data1: numpy.array
    @param data1: 1D array to compute NME.

    @type data2: numpy.array
    @param data2: 1D array to compute NME.

    @rtype: float
    @return: Normalized Mean Error between data1 and data2.
    """
    if len(data1) != len(data2):
        raise ValueError, "Data samples do not have the same length."
    return (abs(data1 - data2)).sum() / data2.sum()
