# -*- coding: utf-8 -*-
"""
Created on Sat Feb 19 22:14:16 2022

@author: tobycrisford
"""

import numpy as np

N = 6
max_bet = 3
rate = 0.01

def optimize_b(a, b_init):
    b = np.copy(b_init)
    for i in range(N):
        for j in range(max_bet):
            if np.sum(a[:,j]) != 0:
                p_b_win = np.sum(a[0:(i+1),j]) / np.sum(a[:,j])
                b_winnings = p_b_win * (2+j) - (1-p_b_win)*j
                b[i,j] += b_winnings * rate
                
    b[b > 1.0] = 1.0
    b[b < 0.0] = 0.0
    
    return b


def optimize_a(b, a_init):
    
    c = np.zeros((N, max_bet, N))
    
    for i in range(N):
        for j in range(max_bet):
            for k in range(N):
                if i > k:
                    bet_reward = j+2
                else:
                    bet_reward = -j
                c[i,j,k] = 2*(1-b[k,j]) + b[k,j] * bet_reward
    
    coeffs = np.sum(c, axis=2)
    
    
    
    a = np.copy(a_init)
    for i in range(N):
        bad_pos = np.where(coeffs[i,:] != np.max(coeffs[i,:]))[0]
        opt = np.copy(a[i,:])
        opt[bad_pos] = 0.0
        opt = opt / np.sum(opt)
        a[i,:] = a[i,:] + (opt - a[i,:]) * rate
        a[i,:] = a[i,:] / np.sum(a[i,:])
    a[a<0] = 0.0
    
        
    return a

def value_of_game(a,b):
    
        
    c = np.zeros((N, max_bet, N))
    
    for i in range(N):
        for j in range(max_bet):
            for k in range(N):
                if i > k:
                    bet_reward = j+2
                else:
                    bet_reward = -j
                c[i,j,k] = 2*(1-b[k,j]) + b[k,j] * bet_reward
    
    coeffs = np.sum(c, axis=2)
    
    return np.sum(a * coeffs * (1/N**2)), coeffs


a = np.random.rand(N,max_bet)
b = np.random.rand(N,max_bet)

for c in range(10000):
    b_new = optimize_b(a,b)
    a_new = optimize_a(b_new, a)
    print(np.sum((a-a_new)**2))
    a = a_new
    b = b_new
    