#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 15:15:34 2021

@author: yuri
"""

import numpy as np
import statistics as stats

from abc import ABC, abstractmethod

from graphviz import Digraph


class Node(ABC):

    def __init__(self):
        self.digraph_filecount = 0

    @property
    @abstractmethod
    def n(self):
        pass

    @abstractmethod
    def expand(self):
        pass

    @abstractmethod
    def backpropagate(self, reward):
        pass
    
    @abstractmethod
    def plot_node(self):
        pass
    
    def plot_tree(self, first_layer=False):
        file_name = "tree" + str(self.digraph_filecount) + ".gv"
        self.digraph_filecount += 1
        self.digraph = Digraph('g', filename=file_name,
            node_attr={'shape': 'record', 'height': '.1', 'fontname': 'Lucida Console'})
        self.plot_node(digraph=self.digraph, first_layer=first_layer)
        self.digraph.view()


# +
class Node(ABC):

    def __init__(self):
        self.digraph_filecount = 0

    @property
    @abstractmethod
    def n(self):
        pass

    @abstractmethod
    def expand(self):
        pass

    @abstractmethod
    def backpropagate(self, reward):
        pass
    
    @abstractmethod
    def plot_node(self):
        pass
    
    def plot_tree(self, first_layer=False):
        file_name = "tree" + str(self.digraph_filecount) + ".gv"
        self.digraph_filecount += 1
        self.digraph = Digraph('g', filename=file_name,
            node_attr={'shape': 'record', 'height': '.1', 'fontname': 'Lucida Console'})
        self.plot_node(digraph=self.digraph, first_layer=first_layer)
        self.digraph.view()
        
        
class StateNode(Node):

    def __init__(self, env_state, prev_node=None):
        super().__init__()
        self.env_state = env_state
        self.prev_node = prev_node

        self._untried_actions = None
        
        self.number_of_visits = 0
        self.value_function = 0
        
        self.actions = []
        
    @property
    def untried_actions(self):
        if self._untried_actions is None:
            self._untried_actions = self.env_state.get_legal_actions()
        return self._untried_actions
        
    @property
    def n(self):
        return self.number_of_visits

    def expand(self):
        n_untried_actions = len(self.untried_actions)
        if n_untried_actions > 0:
            random_action = np.random.randint(n_untried_actions)
            action = self.untried_actions[random_action]
            self.untried_actions.remove(action)
            
            next_env_state = self.env_state.move(action)
            move_id = action.x_coordinate*3 + action.y_coordinate
            state_action = StateActionNode(next_env_state, self, move_id)
            self.actions.append(state_action)
        else:
            ns = [ actions.n  for actions in self.actions ]
            ns_min_arg = np.argmin(ns)
            
            if ns[ns_min_arg] > 1:
                print("-- Error -- : should not be able to expand")
            
            state_action = self.actions[ns_min_arg]
            
        return state_action

        # legal_actions = self.env_state.get_legal_actions()
        # random_action = np.random.randint(len(legal_actions))
        # action = legal_actions[random_action]
        
        # if action in self.actions_explored:
        #     # return stateaction from df linked with action
        #     index = np.where(action == self.actions_explored)
        #     return self.next_state_nodes[index]
        # else: 
        #     self.actions_explored.append(action)
        
        #     next_env_state = self.env_state.move(action)
        #     next_state_node = StateNode(next_env_state, self)
            
        #     self.next_state_nodes.append(next_state_node)
        
        #     return next_state_node


    def rollout(self):
        current_env_state = self.env_state
        # current_env_state.print_board()
        #reward = current_env_state.get_reward()
        while not current_env_state.is_game_over():
            # find a ransom child state-action node
            possible_moves = current_env_state.get_legal_actions()
            action = self.rollout_policy(possible_moves)
            current_env_state = current_env_state.move(action)
        
        if(current_env_state.game_result == self.env_state.player):
            return 1
        elif current_env_state.game_result == 0:
            return 0.5
        else:
            return 0


    def backpropagate(self, reward):
        self.number_of_visits += 1
        # print("n=" + str(self.number_of_visits))
        
        # print("vf=" + str(self.value_function) + ", r=" + str(reward))
        self.value_function = self.value_function*(self.n - 1)/self.n + (1/self.n)*reward 
        # print("new_vf=" + str(self.value_function))           
        
        if self.prev_node:
            self.prev_node.backpropagate(self.value_function)


    def is_fully_expanded(self):
        return len(self.untried_actions) == 0

    def is_expandable(self):
        if not self.is_fully_expanded():
            return True
        
        ns = [ actions.n  for actions in self.actions ]
        ns_min_arg = np.argmin(ns)
        
        if ns[ns_min_arg] > 1:
            return False
        else:
            return True


    def is_terminal_node(self):
        return self.env_state.is_game_over()


    def rollout_policy(self, possible_moves):        
        return possible_moves[np.random.randint(len(possible_moves))]


    def plot_node(self, digraph, draw_node_name="node", first_layer=False):
        node_info = self.get_info()
        if self.is_terminal_node():
            digraph.node(draw_node_name, label=node_info, shape='box')
        else:
            digraph.node(draw_node_name, label=node_info, shape='oval')
            
        if self.actions:
            it = 0
            for a in self.actions:
                action_name = draw_node_name + str(it)
                it += 1
                a.plot_node(digraph, action_name, first_layer)
                digraph.edge(draw_node_name, action_name)
    
    def get_info(self):
        # node_info = "vf = " + str(self.value_function) + "\l n = " + str(self.n) 
        node_info = "vf = " + ("%.5f" % self.value_function) + "\l n = " + str(self.n) 
        node_info += self.env_state.draw_board()
        return node_info


# -

class StateActionNode(Node):
    
    def __init__(self,env_state, state_node, move_id):
        super().__init__()
        self.number_of_visits = 0
        
        self.env_state = env_state
        self.state_node = state_node
        
        self.move_id = move_id
        
        self.q_value_samples = []
        self.q_value_mean = 0
        self.q_value_stddev = 0
        
        self.actions_explored = []
        self.next_state_nodes = []

    @property
    def n(self):
        return self.number_of_visits

    def expand(self):
        legal_actions = self.env_state.get_legal_actions()
        random_action = np.random.randint(len(legal_actions))
        action = legal_actions[random_action]
        
        if action in self.actions_explored:
            # return stateaction from df linked with action
            index = np.where(action == self.actions_explored)
            return self.next_state_nodes[index]
        else: 
            self.actions_explored.append(action)
        
            next_env_state = self.env_state.move(action)
            next_state_node = StateNode(next_env_state, self)
            
            self.next_state_nodes.append(next_state_node)
        
            return next_state_node

    def backpropagate(self, value_function):
        self.number_of_visits += 1

        q_hat = value_function #+ R(x,a)
        self.q_value_samples.append(q_hat)
        
        if self.number_of_visits > 1:
            self.q_value_mean = stats.mean(self.q_value_samples)
            self.q_value_stddev = stats.stdev(self.q_value_samples)
        else:
            self.q_value_mean = q_hat
            self.q_value_stddev = 0

        self.state_node.backpropagate(self.q_value_mean)

    def plot_node(self, digraph, draw_node_name="node", first_layer=False):
        node_info = self.get_info()
        digraph.node(draw_node_name, label=node_info, shape='box')
        
        if not first_layer:
            it = 0
            for s in self.next_state_nodes:
                state_name = draw_node_name + str(it)
                it += 1
                s.plot_node(digraph, state_name)
                digraph.edge(draw_node_name, state_name)

    def get_info(self):
        # node_info = "q = " + str(self.q_value) + "\l n = " + str(self.n) 
        node_info = "q = " + ("%.5f" % self.q_value_mean) + "\l n = " + str(self.n) 
        node_info += self.env_state.draw_board()

        return node_info
