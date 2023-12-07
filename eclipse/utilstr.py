#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 16:13:47 2023

@author: zettergm
"""

def padstr(simtime,simtimestr):
    simtimestrout=simtimestr
    if simtime<10:
        simtimestrout="0000"+simtimestrout
    elif simtime<100:
        simtimestrout="000"+simtimestrout
    elif simtime<1000:
        simtimestrout="00"+simtimestrout
    elif simtime<10000:
        simtimestrout="0"+simtimestrout
    return simtimestrout

