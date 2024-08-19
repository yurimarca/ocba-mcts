#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 09:58:23 2021

@author: yuri
"""

import numpy as np
import random
import math

from abc import ABC, abstractmethod

from ocba import OCBA
# from scipy.stats import entropy

# from copy import deepcopy

# import matplotlib.pyplot as plt
# import scipy.stats as sk

# import statistics as stats

# ############################################################################################
#   TREE POLICY METHOD TEMPLATE
# ############################################################################################
class TreePolicy(ABC):

    def __init__(self):
        self.pcs = []
        self.n_samples_allocation = []
        self.name = "none"

    @abstractmethod
    def select(self, current_state):
        pass
        
    def set_pcs(self, pcs):
        self.pcs = pcs

    def set_n_samples_allocation(self, n_samples_allocation):
        self.n_samples_allocation = n_samples_allocation
        
        
# ############################################################################################
#   RANDOM SAMPLING
# ############################################################################################
class TreePolicy_Random(TreePolicy):

    def __init__(self):
        super().__init__()
        self.name = "random"
        self.color = 'yellow'

    def select_sample(self, bayesbelief):
        sample_index = random.randrange(0, bayesbelief.n_designs, 1)

        return sample_index
  

# ############################################################################################
#   OCBA
# ############################################################################################
class TreePolicy_OCBA(TreePolicy):

    def __init__(self):
        super().__init__()
        self.name = "ocba"
        
        self.ocba = OCBA()
        self.color = 'red'

    def select(self, current_state): 
        q_value_means = np.array([ actions.q_value_mean  for actions in current_state.actions ])
        q_value_stddevs = np.array([ math.sqrt(actions.q_value_stddev**2 + 10/actions.n)  for actions in current_state.actions ])
        ns = np.array([ actions.n  for actions in current_state.actions ])

        n_actions = len(ns)
        
        # Identify most starving item
        starving_index = self.ocba.OCBA_Starving(n_actions, ns, q_value_means, q_value_stddevs)
                
        return current_state.actions[starving_index]

# ############################################################################################
#   UCB
# ############################################################################################
class TreePolicy_UCB(TreePolicy):

    def __init__(self, exp_weight=1):
        super().__init__()
        self.name = "ucb"
        self.color = 'blue'
        self.exp_weight = exp_weight

    def select(self, current_state):
        choices_weights = [
            possible_action.q_value_mean  + self.exp_weight * np.sqrt((2 * np.log(current_state.n) / possible_action.n))
            for possible_action in current_state.actions
        ]
        return current_state.actions[np.argmax(choices_weights)]
