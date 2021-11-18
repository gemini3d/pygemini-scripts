# imports
import os
import datetime
from gemini3d.utils import datetime2ymd_hourdec

# source and destination directories
direc_orig="~/simulations/raid/input/mooreOK_neutrals/"
direc_new="~/simulations/raid/input/mooreOK_neutrals_alttime2/"

# hardcoded timing info
t0old=71100
t0new=18900
tdur=18000
dt=6

# main loop
t=0
dateold=datetime.datetime(2013,5,20,19,45,00)
datenew=datetime.datetime(2016,3,3,5,15,00)
dtdate=datetime.timedelta(0,6)
while t<tdur:
    strold=datetime2ymd_hourdec(dateold)
    strold=strold.replace(" ","0")
    strnew=datetime2ymd_hourdec(datenew)
    strnew=strnew.replace(" ","0")
    command="cp -rv "+direc_orig+strold+".dat"+" "+direc_new+strnew+".dat"
    print(command)
    os.system(command)
    dateold=dateold+dtdate
    datenew=datenew+dtdate
    t+=dt
