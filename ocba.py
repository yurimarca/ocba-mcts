#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 12:39:54 2020

@author: yuri
"""

import numpy as np
import math

class OCBA():
    def __init__(self):
        self.prev_prop = None

    def choose_best_np(self, J_est):
        best = np.unravel_index(np.argmax(J_est, axis=None), J_est.shape)
        
        return int(best[0])
    
    def choose_second_best_np(self, J_est):
        best = np.unravel_index(np.argmax(J_est, axis=None), J_est.shape)
        
        new_J_est = np.copy(J_est)
        new_J_est[best] = 0
        sec_best = np.unravel_index(np.argmax(new_J_est, axis=None), new_J_est.shape)
        
        return int(sec_best[0])
    
    def delta(self, k, best, mean):
        delta = np.zeros(k)
        for i in range(k):  
            if i != best :
                delta[i] = mean[best] - mean[i]
        return delta
    
    def calculate_ratio(self, k, mean, std_dev):
    
        # Find best and second best
        best = self.choose_best_np(mean)
        # if best == 0:
        #     second_best = 1
        # else:
        #     second_best = 0
        second_best = self.choose_second_best_np(mean)
        
        ratio = np.zeros(k)
        
        ratio[second_best] = 1.0
        
        for j in range(k): 
            if ((j != best) and (j != second_best)):
                if mean[best] == mean[j]:
                    ratio[j] = 1.0
                else:
                    temp = std_dev[j]*(mean[best] - mean[second_best])/(std_dev[second_best]*(mean[best] - mean[j]))
                    ratio[j] = temp*temp
                
        # Now we calculate the ratio of design b
        #given that we know the ratios of the other designs
        temp = 0
        for j in range(k):
            if j != best:
                temp += (ratio[j]/std_dev[j])**2
        
        ratio[best] = math.sqrt(temp)*std_dev[best]
        
        # Now implement a simple calculation that gives the fraction required 
        #for each design i (incl b)
        new_ratio = np.zeros(k)
        
        
        for i in range(k):
            if ratio.sum() > 0:
                new_ratio[i] =  ratio[i] / ratio.sum()
            else:
                new_ratio[i] =  ratio[i]
    
        # Returns an array of fractions, whose sum of course equals 1
        return new_ratio
    
    
    
    def OCBA_Starving(self, k, no_sims, mean, std_dev):
        """
        This function provides the solution to deciding where to allocate a single 
        replication. It judges which is the most 'starving' design ie which has
        the largest increase in proportion from the previous iteration
    
        Parameters
        ----------
        k       : int
                number of designs to compare
        no_sims : np.array()
                array with number of simulations for each design k
        mean    : np.array()
                array with mean values from k designs
        std_dev : np.array()
                array with standard deviation of mean values from k designs
        
        Returns
        -------
        starving : int
                 index number of the most starving design
        """
        # if self.prev_prop == None:
        #     self.prev_prop = np.full(k, 0)
            
        # Calculate current_n_ratio
        total_n = 0
        for i in range(k):
            total_n += no_sims[i]
        previous_n_ratio = no_sims/total_n
    
        new_n_ratio = self.calculate_ratio(k, mean, std_dev)
        
        difference_n_ratio = np.zeros(k)
        for i in range(k):
            # difference_n_ratio[i] = new_n_ratio[i] - self.prev_prop[i]
            difference_n_ratio[i] = new_n_ratio[i] - previous_n_ratio[i]
            
        # self.prev_prop = new_n_ratio
        
        # Finds the index of the design with the biggest difference
        starving = np.where(difference_n_ratio == difference_n_ratio.max())[0][0]
         
        return starving


    def OCBA_Starving_List(self, k, no_sims, mean, std_dev):
        """
        This function provides the solution to deciding where to allocate a single 
        replication. It judges which is the most 'starving' design ie which has
        the largest increase in proportion from the previous iteration
    
        Parameters
        ----------
        k       : int
                number of designs to compare
        no_sims : np.array()
                array with number of simulations for each design k
        mean    : np.array()
                array with mean values from k designs
        std_dev : np.array()
                array with standard deviation of mean values from k designs
        
        Returns
        -------
        starving : int
                 index number of the most starving design
        """
        # if self.prev_prop == None:
        #     self.prev_prop = np.full(k, 0)
            
        # Calculate current_n_ratio
        total_n = 0
        for i in range(k):
            total_n += no_sims[i]
        previous_n_ratio = no_sims/total_n
    
        new_n_ratio = self.calculate_ratio(k, mean, std_dev)
        
        difference_n_ratio = np.zeros(k)
        for i in range(k):
            difference_n_ratio[i] = new_n_ratio[i] - previous_n_ratio[i]
                   
        starving_list = np.argsort(-difference_n_ratio)
         
        return starving_list


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    