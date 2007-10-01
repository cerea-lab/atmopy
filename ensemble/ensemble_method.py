# Copyright (C) 2006-2007, ENPC - INRIA - EDF R&D
#     Author(s): Vivien Mallet
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


from numpy import *
from atmopy import *
import datetime
import scipy


##################
# ENSEMBLEMETHOD #
##################


class EnsembleMethod:
    """
    This class is the base class to all methods whose aim is to combine or
    select members in an ensemble to improve forecast performances.

    It provides a method 'Process' that computes the weights associated with
    each model. This method first calls 'Init'. Then it calls the method
    'UpdateWeight' for each timestep. It finally combines the models based on
    the weights.

    Time-dependent (derived) classes should at least include a method
    'UpdateWeight' that extends the weights (attribute 'weight') for a given
    timestep.

    After 'Process', below are the main available attributes:
       0. all_dates: dates in the covered period;
       1. date: the list (per station) of dates;
       2. sim: the ensemble combination;
       3. obs: corresponding observation;
       4. weight (if relevant): model weights as function of time;
       5. stat (possibly): global statistics;
       6. stat_step (possibly): statistics per time step.

    Warning: in 'UpdateWeight', it is assume that 'self.step' is the step of
    weights to be forecasted. The forecasted weights are therefore at date
    'self.all_dates[self.step]'. It means that available observations are in
    steps STRICTLY BEFORE 'self.step'. One may thus use observations for dates
    up to 'self.all_dates[self.step - 1]'. Otherwise this is cheating!
    """


    def __init__(self, ens, configuration_file = None, process = True,
                 statistics = True, Nskip = 0, Nlearning = 0,
                 option = "global", extended = False, U = 1.):
        """
        Attributes are initialized, ensemble combination may be computed and
        associated statistics may be computed.

        @type ens: EnsembleData
        @param ens: Ensemble data ready for computations.
        @type configuration_file: string
        @param configuration_file: The path to the configuration file.
        @type process: Boolean
        @param process: Should the ensemble combination be computed?
        @type statistics: Boolean
        @param statistics: Should statistics be computed?
        @type Nskip: integer
        @param Nskip: Number of timesteps to discard (no combination and no
        statistics).
        @type Nlearning: integer
        @param Nlearning: Number of learning timesteps. It must be less (or
        equal) to 'Nskip'.
        @type option: string
        @param option: The way members are combined. Usually 'global' means
        that all stations and all timesteps are included. Option 'station'
        means that weights are computed per station (a single weight for all
        timesteps). Option 'step' means that weights are computed per step (a
        single weight for all stations).
        @type extended: Boolean
        @param extended: use of the extended trick.
        @type U: float
        @param U: coefficient in the 'extended' activation.
        """
        self.ens = ens
        self.Nsim = self.ens.Nsim
        self.option = option
        self.weight = []
        self.weight_ext = []
        self.all_dates = []
        self.extended = extended
        self.U = U

        self.Nlearning = Nlearning
        self.Nskip = Nskip
        if Nskip < Nlearning:
            raise Exception, "Nskip < Nlearning"

        if statistics and configuration_file == None:
            raise Exception, \
                  "Unable to compute statistics without configuration."
        if statistics and not process:
            raise Exception, \
                  "Unable to compute statistics without ensemble combination."

        if configuration_file != None:
            self.LoadConfiguration(configuration_file)
        if process:
            self.Process()
        if statistics:
            self.ComputeStatistics()


    def LoadConfiguration(self, configuration_file):
        """
        Loads the configuration.

        @type configuration_file: string
        @param configuration_file: the path to the configuration file.
        """
        add_content = [("discarded_cells", "[input]", "Int"),
                       ("discarded_days", "[input]", "Int"),
                       ("concentrations", "[output]", "String"),
                       ("measure", "[output]", "StringList"),
                       ("cutoff", "[output]", "Float"),
                       ("select_station", "[output]", "StringList"),
                       ("paired", "[output]", "Bool"),
                       ("ratio", "[output]", "Float")]

        self.config = talos.Config(configuration_file,
                                   additional_content = add_content)

        # Filters config.measure.
        try:
            if "all" in self.config.measure:
                self.config.measure = "all"
        except:
            pass

        self.CheckConfiguration()


    def CheckConfiguration(self):
        """
        Checks that the configuration is valid.
        """
        # Checks that the considered period is included in the simulated
        # period.
        if self.config.t_range[0] < self.config.origin[0] \
               or self.config.t_range[1] > self.config.origin[0] \
               + datetime.timedelta(0, 3600 * self.config.Delta_t
                                    * self.config.Nt):
            raise Exception, "The period considered for computations must " \
                  + "be included in the simulated period."

        # Checks that the required concentrations are supported.
        if self.config.concentrations == "peak":
            # Checks that peaks are not paired.
            if self.config.paired:
                raise Exception, "Unable to deal with paired peaks."
        elif self.config.concentrations != "hourly":
            raise Exception, "Field \"concentrations\" is set to \"" \
                  + self.config.concentrations \
                  + "\" but should be \"hourly\" or \"peak\"."


    def Init(self):
        """
        Initialization of the combination process.
        """
        self.weight = []
        self.weight_ext = []
        self.all_dates = []
            

    def UpdateWeight(self):
        """
        Adds weights for the current step in the list 'weight' (attribute).
        """
        self.weight.append(ones(shape = (self.Nsim,), dtype = 'd') \
                           / float(self.Nsim))


    def GetInitialWeightExt(self):
        """
        Define the initial_weight_ext attribute with initial_weight.
        """
        size = len(self.initial_weight)
        initial_weight_ext = zeros(2 * size)
        initial_weight_ext[:self.Nsim] = self.initial_weight / 2
        initial_weight_ext[self.Nsim:] = self.initial_weight / 2
        return initial_weight_ext


    def __keep_date(self, x):
        """
        Checks whether an observation at date 'x' is in the learning
        period.

        @type x: datetime
        @param x: Date to be tested.
        """
        hour = self.ens.all_dates[self.step].hour
        return x.hour == hour


    def GetLearningDates(self):
        """
        Returns the simulated dates that are in the learning period. It
        manages peak and hourly observations.
        """
        if self.ens.config.concentrations == "peak":
            return self.ens.all_dates[(self.step - self.Nlearning):self.step]
        elif self.ens.config.concentrations == "hourly":
            return (filter(self.__keep_date,
                           self.ens.all_dates[:self.step]))[-self.Nlearning:]


    def GetPreviousWeight(self):
        """
        Return the previous weight vector in the different cases: peak, hourly.
        """
        if self.ens.config.concentrations == "peak":
            if self.weight == [] and self.extended:
                return self.GetInitialWeightExt()
            elif self.weight == []:
                return self.initial_weight
            elif self.extended:
                return self.weight_ext[-1]
            else:
                return self.weight[-1]
        elif self.ens.config.concentrations == "hourly":
            if len(self.weight)<24 and self.extended:
                return self.GetInitialWeightExt()
            elif len(self.weight)<24:
                return self.initial_weight
            elif self.extended:
                return self.weight_ext[-24]
            else :
                return self.weight[-24]


    def CollectDatas(self, period):
        """
        Get the datas with the right format following the activation of
        'extended' option.
        @type period: list of datetime
        @param period: It defines the selected list of dates.
        """
        s1,o = ensemble.collect_dates(self.ens.sim, self.ens.obs,
                                dates = self.ens.date, period = period)
        if self.extended:
            s = zeros([self.Nsim * 2 , s1.shape[1]], 'd')
            s[:self.Nsim] = self.U * s1
            s[self.Nsim:] = -self.U * s1
        else:
            s = s1
        return s,o


    def AcquireWeight(self, weight):
        """
        Acquisition of weight in UpdateWeight following the activation of
        'extended' option.
        """
        if self.extended:
            self.weight_ext.append(weight)
            reduced_weight = self.U * (weight[:self.Nsim] - weight[self.Nsim:])
            self.weight.append(reduced_weight)
        else:
            self.weight.append(weight)


    def Process(self):
        """
        Computes the weights and the resulting combination.
        """
        self.Init()

        for self.step in range(self.Nskip, len(self.ens.all_dates)):
            self.all_dates.append(self.ens.all_dates[self.step])
            self.UpdateWeight()
        self.weight = array(self.weight)

        if self.option == "global" or self.option == "step":
            self.date, self.sim = \
                       ensemble.combine_step(self.ens.date, self.ens.sim,
                                             self.all_dates, self.weight,
                                             restricted = True)
        if "bias" in dir(self):
            self.sim = ensemble.remove_bias_step(self.date, self.sim,
                                                 self.all_dates, self.bias)[0]

        self.obs = []
        for i in range(self.ens.Nstation):
            self.obs.append(observation.restrict_to_period(self.ens.date[i],
                                                           self.ens.obs[i],
                                                           self.all_dates)[1])
        self.CheckCompatibility(self.sim, self.obs)
        self.CheckCompatibility(self.date, self.obs)


    def ComputeStatistics(self, period = None):
        """
        Computes global statistics.
        """
        self.stat = stat.compute_stat(self.sim, self.obs,
                                      self.config.measure,
                                      cutoff = self.config.cutoff,
                                      period = period, dates = self.date)


    def ComputeStepStatistics(self, period = None):
        """
        Computes statistics per step.
        """
        self.stat_step = stat.compute_stat_step(self.date, self.sim, self.obs,
                                                self.config.concentrations,
                                                self.config.measure,
                                                cutoff = self.config.cutoff,
                                                period = period)


    def ComputeAllStatistics(self):
        """
        Computes global statistics and statistics per step.
        """
        self.ComputeStatistics()
        self.ComputeStepStatistics()


    def CheckCompatibility(self, sim, obs):
        """
        Checks that simulated concentrations and observations have compatible
        shapes.
        """
        compatible = len(sim) == len(obs)
        for istation in range(len(sim)):
            compatible = compatible \
                         and len(sim[istation]) == len(obs[istation])
        if not compatible:
            raise Exception, "Incompatible data: shapes of simulated " \
                  + "concentrations and observations do not match."


    def CheckDate(self, date, odate):
        """
        Checks that two date lists match.

        @type date: list of lists of datetime
        @param date: List (per station) of lists (per step) of dates.
        @type odate: list of lists of datetime
        @param odate: List (per station) of lists (per step) of dates.
        """
        self.CheckConfiguration(date, odate)
        for istation in range(len(date)):
            for idate in range(len(date[istation])):
                if date[istation][idate] != odate[istation][idate]:
                    raise Exception, "Dates do not match."


    def GetAllDates(self):
        """
        Updates 'all_dates' so that it covers the considered period.
        """
        # Covered period.
        self.period = [min([x[0] for x in self.date]),
                       max([x[-1] for x in self.date])]
        if self.config.concentrations == "hourly":
            delta = datetime.timedelta(0, 3600)
        else:   # Peaks.
            delta = datetime.timedelta(1)
        self.all_dates = [self.period[0]]
        while self.all_dates[-1] < self.period[-1]:
            self.all_dates.append(self.all_dates[-1] + delta)
        

    def RestrictToPeriod(self, period):
        """
        Restricts ensemble combination to a given period. It does not affect
        the underlying ensemble.

        @type period: list of datetime
        @param period: It defines the selected period through its bounds.
        """
        obs_out = []
        sim_out = []
        date_out = []
        restrict = observation.restrict_to_period
        for i in range(self.ens.Nstation):
            tmp = restrict(self.date[i], self.obs[i], period)
            date_out.append(tmp[0])
            obs_out.append(tmp[1])
            sim_out.append(restrict(self.date[i], self.sim[i], period)[1])
        self.sim = sim_out
        self.obs = obs_out
        self.date = date_out
        self.GetAllDates()


#############
# BESTMODEL #
#############


class BestModel(EnsembleMethod):
    """
    Selects the best model (for a given measure) in the ensemble.
    """
    

    def __init__(self, ens, measure = "rmse", option = "global",
                 configuration_file = None, process = True,
                 statistics = True, Nskip = 0):
        """
        See documentation of 'EnsembleMethod.__init__' for explanations about
        arguments not described below.

        @type measure: string
        @param measure: The measure according to which the model is the best.
        """
        self.measure = measure
        if option not in ["global"]:
            raise Exception, "Unsupported option: \"" + option + "\"."
        EnsembleMethod.__init__(self, ens,
                                configuration_file = configuration_file,
                                process = process, statistics = statistics,
                                Nskip = Nskip, option = option)


    def Process(self, select = argmin):
        """
        @type select: callable object
        @param select: function that returns the index of the best measure in
        a list. For example, it should return the index of the lowest number
        if the measure is RMSE, but the index of the closest number to one if
        the measure is correlation.
        """
        if self.option == "global":
            compute_stat = stat.compute_stat
            sim_stat = compute_stat(self.ens.sim, self.ens.obs,
                                    (self.measure,), dates = self.ens.date,
                                    period = self.ens.all_dates[self.Nskip:],
                                    cutoff = self.config.cutoff)
            i = select(sim_stat[self.measure])
            self.sim = self.ens.sim[i]

        self.date = self.ens.date
        self.obs = self.ens.obs

        self.all_dates = self.ens.all_dates[self.Nskip:]
        self.RestrictToPeriod(self.all_dates)


################
# ENSEMBLEMEAN #
################
        

class EnsembleMean(EnsembleMethod):
    """
    Computes the ensemble mean.
    """


    def __init__(self, ens, configuration_file = None, process = True,
                 statistics = True, Nskip = 0):
        """
        See documentation of 'EnsembleMethod.__init__' for explanations about
        arguments.
        """
        EnsembleMethod.__init__(self, ens,
                                configuration_file = configuration_file,
                                process = process, statistics = statistics,
                                Nskip = Nskip)


##################
# ENSEMBLEMEDIAN #
##################


class EnsembleMedian(EnsembleMethod):
    """
    Computes the ensemble median. If there is an even number of models, the
    mean of the two middle models is used.
    """
    

    def __init__(self, ens, configuration_file = None, process = True,
                 statistics = True, Nskip = 0):
        """
        See documentation of 'EnsembleMethod.__init__' for explanations about
        arguments.
        """
        EnsembleMethod.__init__(self, ens,
                                configuration_file = configuration_file,
                                process = process, statistics = statistics,
                                Nskip = Nskip)


    def Process(self):
        self.sim = []
        self.all_dates = self.ens.all_dates[Nskip:]

        restrict = observation.restrict_to_period
        
        for istation in range(self.ens.Nstation):
            for i in range(self.Nsim):
                date_rest, sim_rest = \
                           restrict(self.ens.date[istation],
                                    self.ens.sim[i][istation],
                                    self.ens.all_dates[Nskip:])
                sim_station.append(sim_rest)
            self.date.append(date_rest)
            self.sim.append(ensemble.m_median(array(sim_station)))

        self.obs = []
        for i in range(self.ens.Nstation):
            self.obs.append(restrict(self.ens.date[i], self.ens.obs[i],
                                     self.all_dates)[1])


#######
# ELS #
#######


class ELS(EnsembleMethod):
    """
    ELS method, where LS stands for least-squares, computes the a posteriori
    best constant linear combination.
    """
    

    def __init__(self, ens, configuration_file = None, process = True,
                 statistics = True, Nskip = 0, constraint = None):
        """
        See documentation of 'EnsembleMethod.__init__' for explanations about
        arguments not described below.

        @type constraint: string
        
        @param constraint: The constraint put on weights: "simplex" if the
        weights should lie in the simplex of probability distributions, None
        otherwise.
        """
        self.constraint = constraint
        EnsembleMethod.__init__(self, ens,
                                configuration_file = configuration_file,
                                process = process, statistics = statistics,
                                Nskip = Nskip, Nlearning = 0,
                                option = "global")


    def Init(self):
        """
        Initialization of the combination process.
        """
        self.all_dates = []


    def Process(self):
        """
        Computes the weights and the resulting combination.
        """
        self.Init()

        self.all_dates = self.ens.all_dates[self.Nskip:]

        s, o = ensemble.collect(self.ens.sim, self.ens.obs,
                                dates = self.ens.date,
                                period = self.all_dates)
        if self.constraint is None:
            self.weight = ensemble.w_least_squares(s, o)
        else:
            self.weight = ensemble.w_least_squares_simplex(s, o)
        # Reshapes to ease computations.
        weight = self.weight.copy()
        weight.shape = (weight.size, 1)

        self.sim = []
        for station in range(self.ens.Nstation):
            data = array([x[station] for x in self.ens.sim])
            self.sim.append(sum(data * weight, 0))

        obs_out = []
        date_out = []
        restrict = observation.restrict_to_period
        for i in range(self.ens.Nstation):
            tmp = restrict(self.ens.date[i], self.ens.obs[i], self.all_dates)
            date_out.append(tmp[0])
            obs_out.append(tmp[1])
        self.obs = obs_out
        self.date = date_out

        self.CheckCompatibility(self.sim, self.obs)
        self.CheckCompatibility(self.date, self.obs)


########
# ELSD #
########


class ELSd(EnsembleMethod):
    """
    This class does not give prediction, it computes a posteriori the optimal
    coefficients in the least-square sense at each step. The same coefficients
    are applied at all stations.
    """
    

    def __init__(self, ens, configuration_file = None, process = True,
                 statistics = True, Nskip = 1, Nlearning = 1):
        """
        See documentation of 'EnsembleMethod.__init__' for explanations about
        arguments.
        """
        EnsembleMethod.__init__(self, ens,
                                configuration_file = configuration_file,
                                process = process, statistics = statistics,
                                Nskip = Nskip, Nlearning = Nlearning,
                                option = "step")

        
    def UpdateWeight(self):
        period = self.ens.all_dates[self.step]
        s, o = ensemble.collect(self.ens.sim, self.ens.obs,
                                dates = self.ens.date, period = period)
        self.weight.append(ensemble.w_least_squares(s, o))



#########
# ELSDN #
#########


class ELSdN(EnsembleMethod):
    """
    ELS^{d, N} method where LS stands for least-squares, 'd' for date, and 'N'
    refers to the length of the learning period.
    """
    

    def __init__(self, ens, configuration_file = None, process = True,
                 statistics = True, Nskip = 1, Nlearning = 1,
                 Nlearning_min = None):
        """
        See documentation of 'EnsembleMethod.__init__' for explanations about
        arguments not described below.

        @type Nlearning_min: integer
        @param Nlearning_min: The minimum number of steps for the algorithm to
        compute weights. If None, it is set to 'Nlearning'.
        """
        if Nlearning_min is None:
            Nlearning_min = Nlearning
        self.Nlearning_max = Nlearning
        self.Nlearning = Nlearning
        EnsembleMethod.__init__(self, ens,
                                configuration_file = configuration_file,
                                process = process, statistics = statistics,
                                Nskip = Nskip, Nlearning = Nlearning_min,
                                option = "step")


    def UpdateWeight(self):
        self.Nlearning = self.step - max(0, self.step - self.Nlearning_max)
        period = self.GetLearningDates()
        s, o = ensemble.collect_dates(self.ens.sim, self.ens.obs,
                                dates = self.ens.date, period = period)
        self.weight.append(ensemble.w_least_squares(s, o))


#################
# BESTMODELSTEP #
#################


class BestModelStep(EnsembleMethod):
    """
    This method selects the best models in the learning period and use the
    mean of them for the next step.
    """
    

    def __init__(self, ens, configuration_file = None, process = True,
                 statistics = True, Nskip = 1, Nlearning = 1,
                 measure = "rmse", select = argmin, Nmodel = 1,
                 bias_removal = True):
        """
        See documentation of 'EnsembleMethod.__init__' for explanations about
        arguments not described below.

        @type measure: string
        @param measure: The measure according to which the model is the best.
        @type select: callable object
        @param select: function that returns the index of the best measure in
        a list. For example, it should return the index of the lowest number
        if the measure is RMSE, but the index of the closest number to one if
        the measure is correlation.
        @type Nmodel: integer
        @param Nmodel: The number of models to take into account.
        @type bias_removal: Boolean
        @param bias_removal: Should bias be removed?
        """
        self.measure = measure
        self.select = select
        self.Nmodel = Nmodel
        self.bias_removal = bias_removal

        EnsembleMethod.__init__(self, ens,
                                configuration_file = configuration_file,
                                process = process, statistics = statistics,
                                Nskip = Nskip, Nlearning = Nlearning,
                                option = "step")


    def Init(self):
        self.weight = []
        if self.bias_removal:
            self.bias = []
        self.all_dates = []
            

    def UpdateWeight(self):
        period = self.GetLearningDates()
        s, o = ensemble.collect_dates(self.ens.sim, self.ens.obs,
                                dates = self.ens.date, period = period)
        weight = zeros(shape = (self.Nsim, ), dtype = 'd')
        if self.bias_removal:
            s_mean = 0.
        measures = [getattr(stat, self.measure)(x, o) for x in s]
        indices = range(self.Nsim)
        for i in range(self.Nmodel):
            index = self.select(measures)
            weight[indices[index]] = 1. / float(self.Nmodel)
            if self.bias_removal:
                s_mean += s.mean() / float(self.Nmodel)
            measures.pop(index)
            indices.pop(index)
        self.weight.append(weight)

        if self.bias_removal:
            self.bias.append(s_mean - o.mean())


########################
# BESTMODELSTEPSTATION #
########################


class BestModelStepStation(EnsembleMethod):
    """
    This method selects the best models at each step and station.
    """
    

    def __init__(self, ens, configuration_file = None, process = True,
                 statistics = True):
        """
        See documentation of 'EnsembleMethod.__init__' for explanations about
        arguments.
        """
        EnsembleMethod.__init__(self, ens,
                                configuration_file = configuration_file,
                                process = process, statistics = statistics,
                                Nskip = 0, Nlearning = 0, option = "step")


    def Init(self):
        self.all_dates = []
        self.date = [[] for i in range(self.ens.Nstation)]
        self.sim = [[] for i in range(self.ens.Nstation)]
        self.isim = [[] for i in range(self.ens.Nstation)]
        self.obs = [[] for i in range(self.ens.Nstation)]
            

    def Process(self):
        self.Init()
        
        # Dates.
        for self.step in range(len(self.ens.all_dates)):
            self.all_dates.append(self.ens.all_dates[self.step])
        # Simulated data and observations.
        for istation in range(self.ens.Nstation):
            for step in range(len(self.ens.obs[istation])):
                self.date[istation].append(self.ens.date[istation][step])
                obs = self.ens.obs[istation][step]
                self.obs[istation].append(obs)
                i = array([abs(x[istation][step] - obs)
                           for x in self.ens.sim]).argmin()
                self.isim[istation].append(i)
                self.sim[istation].append(self.ens.sim[i][istation][step])
            self.sim[istation] = array(self.sim[istation])
            self.obs[istation] = array(self.obs[istation])
