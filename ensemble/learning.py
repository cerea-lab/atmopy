# Copyright (C) 2006-2007 CEREA
#     Author: Gilles Stoltz, Boris Mauricette, Vivien Mallet
#
# CEREA (http://www.enpc.fr/cerea/) is a joint laboratory of
# ENPC (http://www.enpc.fr/) and EDF R&D (http://www.edf.fr/).
#
# This file is part of Polyphemus, a modeling system for air quality. It
# provides facilities to deal with ensemble forecast.
#
# Polyphemus is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Polyphemus is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License (file "license") for more details.
#
# For more information, please see the AtmoPy home page:
#     http://www.enpc.fr/cerea/polyphemus/atmopy.html


import sys, os
sys.path.insert(0,
                os.path.split(os.path.dirname(os.path.abspath(__file__)))[0])
from ensemble_method import *
sys.path.pop(0)


################################
# EXPONENTIALLYWEIGHTEDAVERAGE #
################################


class ExponentiallyWeightedAverage(EnsembleMethod):
    """
    This class implements the exponentially weighted average algorithm
    (Cesa-Bianchi, Lugosi 2006).
    """
    

    def __init__(self, ens, configuration_file = None, process = True,
                 statistics = True, extended = False, U = 1., Nskip = 1,
                 Nlearning = 1, learning_rate = 3.e-6):
        """
        See documentation of 'EnsembleMethod.__init__' for explanations about
        arguments.

        @type learning_rate: float
        @param learning_rate: Learning rate.
        """
        self.learning_rate = learning_rate
        EnsembleMethod.__init__(self, ens,
                                configuration_file = configuration_file,
                                process = process, statistics = statistics,
                                Nskip = Nskip, Nlearning = Nlearning,
                                option = "step", extended = extended, U = U)

        
    def Init(self):
        self.initial_weight = ones((self.Nsim), 'd') / float(self.Nsim)


    def UpdateWeight(self):
        period = self.GetLearningDates()
        s, o = self.CollectDatas(period)
        previous_weight = self.GetPreviousWeight()

        loss = sum((s - o) ** 2 , 1)
        weight = previous_weight * exp(-self.learning_rate * loss)
        weight /= weight.sum()

        self.AcquireWeight(weight)


#########################
# EXPONENTIATEDGRADIENT #
#########################


class ExponentiatedGradient(EnsembleMethod):
    """
    This class implements the exponentiated gradient algorithm (Kivinen and
    Warmuth, 1997).
    """
  

    def __init__(self, ens, configuration_file = None, process = True,
                 statistics = True, extended = False, U = 1., Nskip = 1,
                 Nlearning = 1, learning_rate = 2.e-5):
        """
        See documentation of 'EnsembleMethod.__init__' for explanations about
        arguments.

        @type learning_rate: float
        @param learning_rate: Learning rate.
        """
        self.learning_rate = learning_rate
        EnsembleMethod.__init__(self, ens,
                                configuration_file = configuration_file,
                                process = process, statistics = statistics,
                                Nskip = Nskip, Nlearning = Nlearning,
                                option = "step", extended = extended, U = U)


    def Init(self):
        self.initial_weight = ones((self.Nsim), 'd') / float(self.Nsim)
        

    def UpdateWeight(self):
        period = self.GetLearningDates()
        s, o = self.CollectDatas(period)
        previous_weight = self.GetPreviousWeight()

        loss = 2. * sum((dot(previous_weight, s) - o) * s, 1)
        weight = previous_weight * exp(-self.learning_rate * loss)
        weight /= weight.sum()

        self.AcquireWeight(weight)


########
# PROD #
########


class Prod(EnsembleMethod):
    """
    This class implements the prod-type algorithms (Cesa-Bianchi, Mansour, and
    Stoltz, 2006).
    """

    def __init__(self, ens, configuration_file = None, process = True,
                 statistics = True, extended = False, U = 1., Nskip = 1,
                 Nlearning = 1, learning_rate = 5.5e-7):

        """
        See documentation of 'EnsembleMethod.__init__' for explanations about
        arguments.

        @type learning_rate: float
        @param learning_rate: Learning rate.
        """
        self.learning_rate = learning_rate
        EnsembleMethod.__init__(self, ens,
                                configuration_file = configuration_file,
                                process = process, statistics = statistics,
                                Nskip = Nskip, Nlearning = Nlearning,
                                option = "step", extended = extended, U = U)

        
    def Init(self):
        self.initial_weight = ones((self.Nsim), 'd') / float(self.Nsim)
        if self.extended:
            self.confidence = ones((2 * self.Nsim), 'd') / float(2 * self.Nsim)
        else:
            self.confidence = ones((self.Nsim), 'd') / float(self.Nsim)


    def UpdateWeight(self):
        period = self.GetLearningDates()
        s, o = self.CollectDatas(period)
        previous_weight = self.GetPreviousWeight()

        loss = 2. * sum( (dot(previous_weight, s) - o) * s, 1)
        self.confidence *= (1 - self.learning_rate * loss)
        if (self.confidence < 0.).any():
            raise Exception, "Too large parameter eta"
        weight = self.confidence / self.confidence.sum()

        self.AcquireWeight(weight)


####################
# GRADIENT DESCENT #
####################


class GradientDescent(EnsembleMethod):
    """
    This class implements algorithm GD (Cesa-Bianchi, 1999).
    """
    

    def __init__(self, ens, configuration_file = None, process = True,
                 statistics = True, extended = False, U= 1.,Nskip = 1,
                 Nlearning = 1, learning_rate = 4.5e-9, lamb = 1):
        """
        See documentation of 'EnsembleMethod.__init__' for explanations about
        arguments.

        @type learning_rate: float
        @param learning_rate: Learning rate.
        @type lamb: float
        @param lamb: Lambda coefficient of initial vector
        """
        self.lamb = lamb
        self.learning_rate = learning_rate
        EnsembleMethod.__init__(self, ens,
                                configuration_file = configuration_file,
                                process = process, statistics = statistics,
                                Nskip = Nskip, Nlearning = Nlearning,
                                option = "step", extended = extended, U = U)


    def Init(self):
        self.initial_weight = self.lamb * ones((self.Nsim), 'd') \
                              / float(self.Nsim)


    def UpdateWeight(self):
        period = self.GetLearningDates()
        s, o = self.CollectDatas(period)        
        previous_weight = self.GetPreviousWeight()

        loss = 2. * sum((dot(previous_weight, s) - o) * s, 1)
        weight = previous_weight - self.learning_rate * loss
        
        self.AcquireWeight(weight)


#####################
# GREEDY PROJECTION #
#####################


def projection_simplex(v):
    """
    Projection of the vector onto the simplex of probability distributions.

    @type v: array
    @param v: array.
    """
    v = -v
    li = argsort(v)
    v.sort()
    v = -v
    vc = 0.
    m = 1
    while vc <= 1. and m < len(v):
        vc += m * (v[m-1] - v[m])
        m += 1
    m -= 1
    z = v[:m]
    la = 1. / m * (1 - sum(z))
    z = z + la
    z = concatenate([z, zeros(len(v) - m)], 0)
    Inv = [list(li).index(j) for j in range(len(v))]
    return z[Inv]


def projection_cubic(v, r):
    """
    Projection of the vector onto the cube of radius r.

    @type v: array
    @param v: array.
    @type r: float
    @param r: radius of the cube.
    """
    return minimum(maximum(-r, v), r)


def projection_L2(v, r):
    """
    Projection of the vector onto the ball of radius r

    @type v: array
    @param v: array.
    @type r: float
    @param r: radius of the ball.
    """
    return r * v / sqrt((v * v).sum())


class Zink(EnsembleMethod):
    """
    This class implements the greedy projection gradient algorithm (Zinkevich,
    2003).
    """
    

    def __init__(self, ens, configuration_file = None, process = True,
                 statistics = True, extended = False, U = 1., Nskip = 1,
                 Nlearning = 1, learning_rate = 1.e-6, radius = 1.,
                 projection_function = projection_simplex):
        """
        See documentation of 'EnsembleMethod.__init__' for explanations about
        arguments.

        @type learning_rate: float
        @param learning_rate: Learning rate.
        @type projection_function: function
        @param projection_function: Projection on simplex or ball
        """
        self.learning_rate = learning_rate
        self.radius = radius
        self.projection_function = projection_function
        EnsembleMethod.__init__(self, ens,
                                configuration_file = configuration_file,
                                process = process, statistics = statistics,
                                Nskip = Nskip, Nlearning = Nlearning,
                                option = "step", extended = extended, U = U)


    def Init(self):
        self.initial_weight = ones((self.Nsim), 'd') / float(self.Nsim)
        

    def UpdateWeight(self):
        import inspect
        period = self.GetLearningDates()
        s, o = self.CollectDatas(period)
        previous_weight = self.GetPreviousWeight()
        loss = 2. * sum((dot(previous_weight, s) - o) * s, 1)

        if len(inspect.getargspec(self.projection_function)[0]) == 1:
            weight = self.projection_function(previous_weight
                                              - self.learning_rate * loss)
        else:
            weight = self.projection_function(previous_weight
                                              - self.learning_rate * loss,
                                              self.radius)
            
        self.AcquireWeight(weight)


####################
# RIDGE REGRESSION #
####################


class RidgeRegression(EnsembleMethod):
    """
    This class implements a modified ridge-regression algorithm
    (Cesa-Bianchi, Lugosi, 2006).
    """


    def __init__(self, ens, configuration_file = None, process = True,
                 statistics = True, extended = False, U = 1., Nskip = 1,
                 Nlearning = 1, penalization = 1.):
        """
        See documentation of 'EnsembleMethod.__init__' for explanations about
        arguments.

        @type penalization: float
        @param penalization: penalization of the norm of the weights.
        """
        self.penalization = penalization
        EnsembleMethod.__init__(self, ens,
                                configuration_file = configuration_file,
                                process = process, statistics = statistics,
                                Nskip = Nskip, Nlearning = Nlearning,
                                option = "step", extended = extended, U = U)
            

    def Init(self):
        self.initial_weight = zeros(self.Nsim)
        if self.extended:
            self.A = self.penalization * identity(2 * ens.Nsim)
        else:
            self.A = self.penalization * identity(ens.Nsim)
        

    def UpdateWeight(self):
        period = self.GetLearningDates()
        s, o = self.CollectDatas(period)
        previous_weight = self.GetPreviousWeight()

        # Nobs: number of stations.
        Nobs = len(o)
        if self.extended:
            Bt = zeros(2 * self.Nsim)
        else:
            Bt = zeros(self.Nsim)
        for i in range(Nobs):
            # s[:, i] is the vector of the self.Nsim models on station i+1.
            x_it = s[:, i]
            self.A += outer(x_it, x_it)
            Bt += (inner(x_it, previous_weight) - o[i]) * x_it
            # Warning: A grows quickly (but linearly).
        weight = previous_weight - dot(inv(self.A), Bt)

        self.AcquireWeight(weight)


###########
# MIXTURE #
###########


def uniformSimplex(a, b, N):
    """
    simulation of a uniform probaility on the simplex.
    """
    P = []
    list = []
    for i in range(N):
        list.append(random.uniform(a,b))
    list = sort(list)    
    for i in range(N - 1):
        P.append(list[i+1] - list[i])
    return P


class Mixture(EnsembleMethod):
    """
    This class implements the exponentially weighted average mixture algorithm
    (Cesa-Bianchi, Lugosi 2006).
    """
    

    def __init__(self, ens, configuration_file = None, process = True,
                 statistics = True, extended = False, U = 1.,Nskip = 1,
                 Nlearning = 1, learning_rate = 1.e-4, Napprox = 5000):
        """
        See documentation of 'EnsembleMethod.__init__' for explanations about
        arguments.

        @type learning_rate: float
        @param learning_rate: Learning rate.
        @type Napprox: float
        @param Napprox: number of points to approximate the integral
        over the simplex with a trivial quadrature formula.
        """
        self.Napprox = Napprox
        self.learning_rate = learning_rate
        EnsembleMethod.__init__(self, ens,
                                configuration_file = configuration_file,
                                process = process, statistics = statistics,
                                Nskip = Nskip, Nlearning = Nlearning,
                                option = "step", extended = extended, U = U)

        
    def Init(self):
        self.initial_weight = ones(self.Nsim, 'd') / self.Nsim
        self.confidence = ones(self.Napprox) / self.Napprox
        self.interpolweights = zeros([self.Nsim, self.Napprox])
        # keep the points of quadrature in the simplex
        for i in range(self.Napprox):
            self.interpolweights[:, i] = uniformSimplex(0,1,self.Nsim+1)


    def UpdateWeight(self):
        period = self.GetLearningDates()
        s, o = self.CollectDatas(period)

        for i in range(self.Napprox):
            loss = exp(-self.learning_rate *
            sum((dot(self.interpolweights[:, i], s) - o) *
            (dot(self.interpolweights[:, i], s) - o)))
            self.confidence[i] *= loss
        # this line stabilize the algo but we lose the exact loss of expert j
        self.confidence /= self.confidence.sum()
        weight = sum(self.confidence * self.interpolweights , 1)

        self.AcquireWeight(weight)


#####################################
# EXPONENTIATEDGRADIENT WITH WINDOW #
#####################################


def Upkeep( method , loss , previous_weight):
    """
    Upkeep of method.kept_weight in 'hourly' and 'peak' modes.
    Return the weight.
    """
    if len(method.kept_weight) < method.Nkeep and\
    method.ens.config.concentrations == "peak":
        method.kept_weight.append( exp(-method.learning_rate * loss) ) 
        weight = previous_weight * exp(-method.learning_rate * loss)
    elif len(method.kept_weight) < 24 * method.Nkeep and\
    method.ens.config.concentrations == "hourly":
        method.kept_weight.append(exp(-method.learning_rate * loss) )
        weight = previous_weight * exp(-method.learning_rate * loss)
    elif len(method.kept_weight) == method.Nkeep and\
    method.ens.config.concentrations == "peak":
        method.kept_weight.append( exp(-method.learning_rate * loss) )
        old_confidence = method.kept_weight.pop(0)
        weight = previous_weight * exp(-method.learning_rate * loss) / old_confidence
    elif len(method.kept_weight) == 24 * method.Nkeep and\
    method.ens.config.concentrations == "hourly":
        method.kept_weight.append( exp(-method.learning_rate * loss) )
        old_confidence = method.kept_weight.pop(0)
        weight = previous_weight * exp(-method.learning_rate * loss) / old_confidence
    weight /= weight.sum()
    return weight
    

class ExponentiatedGradientWindow(EnsembleMethod):
    """
    This class implements a modified exponentiated gradient algorithm (Kivinen and
    Warmuth, 1997).
    """
    

    def __init__(self, ens, configuration_file = None, process = True,
                 statistics = True, extended = False, U = 1., Nskip = 1,
                 Nlearning = 1, learning_rate = 2.e-5, Nkeep = 20):
        """
        See documentation of 'EnsembleMethod.__init__' for explanations about
        arguments.

        @type learning_rate: float
        @param learning_rate: Learning rate.
        @type Nkeep: integer
        @param Nkeep: number of training steps.
        """
        self.learning_rate = learning_rate
        self.Nkeep = Nkeep
        EnsembleMethod.__init__(self, ens,
                                configuration_file = configuration_file,
                                process = process, statistics = statistics,
                                Nskip = Nskip, Nlearning = Nlearning,
                                option = "step", extended = extended, U = U)


    def Init(self):
        self.initial_weight = ones((self.Nsim), 'd') / float(self.Nsim)
        self.kept_weight = []


    def UpdateWeight(self):
        period = self.GetLearningDates()
        s, o = self.CollectDatas(period)
        previous_weight = self.GetPreviousWeight()

        loss = 2. * sum((dot(previous_weight, s) - o) * s, 1)
        weight = Upkeep(self , loss, previous_weight)

        self.AcquireWeight(weight)
