def padstr(simtime,simtimestr):
    simtimestrout=simtimestr
    if simtime<10000:
        simtimestrout="0"+simtimestrout     
    if simtime<1000:
        simtimestrout="0"+simtimestrout    
    if simtime<100:
        simtimestrout="0"+simtimestrout
    if simtime<10:
        simtimestrout="0"+simtimestrout
    return simtimestrout
