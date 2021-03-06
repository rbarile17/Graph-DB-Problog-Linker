# -*- coding: utf-8 -*-
## @package StructureLearning
# Implements classes fro structure learning
# @author Pasquale De Marinis, Barile Roberto, Caputo Sergio
import random

from probfoil.data import DataFile
from probfoil.probfoil import ProbFOIL2, ProbFOIL
from probfoil.score import accuracy, precision, recall
import time

from problog.util import init_logger


##
# Represents the ProbFOIL module and permits to use it as an object
class StructureLearner:

    ## The constructor
    # @param: *data: list of data sources
    # @param: log_file: log file name (no log produced if None)
    # @param: seed: seed that initialize random generations
    def __init__(self, *data, log_file=None, seed=None):
        self.__data = DataFile(*data)
        self.__learner = None
        self.__hypothesis = None
        self.__rules = None
        if log_file is not None:
            self.__log_file = open(log_file, 'w')
        else:
            self.__log_file = None
        self.__log = None

        if seed:
            self.__seed = seed
        else:
            self.__seed = str(random.random())
        random.seed(self.__seed)

    ## Set the data input of structure learning (BG and examples)
    # @param: *data: list of data sources
    def set_data(self, *data):
        self.__data = DataFile(*data)

    ## Set the log file
    # @param: log_file: log file name
    def set_log_file(self, log_file):
        self.__log_file = open(log_file, 'w')

    ## Learns the structure and validate __rules member
    # @param: significance: minimum significance of learned rule
    # @param: beam_size: size of the population of Beam search algorithm
    # @param: max_rule_length: max length of body of the learned rules
    # @param: m_estimator
    # @param: deterministic: set if learn deterministic rules, so using ProbFOIL1 or ProbFOIL2
    # @returns time spent for learning
    def learn(self, significance=None, max_rule_length=None, beam_size=5, m_estimator=1, deterministic=False):
        log_name = 'structure_learner'
        if self.__log_file is not None:
            self.__log = init_logger(verbose=True, name=log_name, out=self.__log_file)
            self.__log.info('Random seed: %s' % self.__seed)

        if deterministic:
            learn_class = ProbFOIL
        else:
            learn_class = ProbFOIL2

        self.__learner = learn_class(self.__data, logger=log_name, p=significance, l=max_rule_length,
                                     beam_size=beam_size, m=m_estimator)

        time_start = time.time()
        self.__hypothesis = self.__learner.learn()
        self.__rules = self.__hypothesis.to_clauses(self.__hypothesis.target.functor)

        # First rule is failing rule: don't consider it if there are other rules.
        if len(self.__rules) > 1:
            del self.__rules[0]
        time_total = time.time() - time_start
        if self.__log is not None:
            self.__log.info('ACCURACY: %f' % self.accuracy())
            self.__log.info('PRECISION: %f' % self.precision())
            self.__log.info('RECALL: %f' % self.recall())
            self.__log.info('ACCURACY: %f' % self.accuracy())
            self.__log.info('Total time:\t%.4fs' % time_start)
        return time_total

    def get_learned_rules(self):
        return self.__rules

    def accuracy(self):
        return accuracy(self.__hypothesis)

    def precision(self):
        return precision(self.__hypothesis)

    def recall(self):
        return recall(self.__hypothesis)

    def get_statistics(self):
        return self.__learner.statistics()
