#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 16:41:38 2021

@author: yuri
"""
import numpy as np
import pandas as pd

class MonteCarloTreeSearch():
    def __init__(self, root_state, tree_policy):
        """
        Parameters
        ----------
        root_state : root state x0
        """
        self.root_state = root_state
        self.tree_policy = tree_policy
        
    def search(self, N):
        """
        Parameters
        ----------
        N : simulation budget (roll-out number)

        Output
        ----------
        best_action : optimal action that achieves the highest cumulative 
                      reward at the root node
        best_value : estimated value of the root node
        """
        for n in range(N):
            new_node = self.tree_walk()
            reward = new_node.rollout()# self.simulate(leaf)
            new_node.backpropagate(reward)

        q_values = [ actions.q_value_mean  for actions in self.root_state.actions ]
        ns = [ actions.n  for actions in self.root_state.actions ]
        indexes = [ actions.move_id  for actions in self.root_state.actions ]
        
        df = pd.DataFrame({'Q':q_values,'N':ns}, index=indexes)

        return df.sort_index()
    
    def tree_walk(self):
        """
        Sample a root-to-leaf path
        ----------
        Output:
        """
        current_node = self.root_state
        while not current_node.is_terminal_node():
            #if not current_node.is_fully_expanded():
            if current_node.is_expandable():
                new_state_action = current_node.expand()
                new_state = new_state_action.expand()
                return new_state
            else:
                current_node = self.tree_policy_selection(current_node)
        
        return current_node

    
    def tree_policy_selection(self, node):
        action_selected = self.tree_policy.select(node)
        next_state = action_selected.expand()
        return next_state
    

    def best_action(self):
        """
        Sample a root-to-leaf path
        ----------
        Output:
        """
        action_q_values = [ possible_action.q_value_mean for possible_action in self.root_state.actions ]
        return self.root_state.actions[np.argmax(action_q_values)]

