import numpy as np
import os
import gemini3d.read as read
import gemini3d.write as write
RE = 6370e3

def makegrid(direc: str,
             dang=1.5,
             ltheta: int=16,
             lphi: int=16,
             return_grid=True,
             write_grid=False,
):
    #   dang (1,1) {mustBeNumeric} = 1.5 # ANGULAR RANGE TO COVER FOR THE CALCULATIONS (THIS IS FOR THE FIELD POINTS - SOURCE POINTS COVER ENTIRE GRID)

    assert (write_grid or return_grid),"Either 'return_grid' or 'write_grid' must be True"
    
    direc = os.path.expanduser(direc);
    assert os.path.isdir(direc), direc + " is not a directory"

    #SIMULATION METADATA
    cfg = read.config(direc)

    #WE ALSO NEED TO LOAD THE GRID FILE
    xg = read.grid(direc)
    print('Grid loaded')

    # lx1 = xg.lx(1);
    lx3 = xg['lx'][2]
    # lh=lx1;   %possibly obviated in this version - need to check
    if (lx3==1):
        flag2D=True
        print('2D meshgrid')
        #     x1=xg.x1(3:end-2);
        #     x2=xg.x2(3:end-2);
        #     x3=xg.x3(3:end-2);
        #     [X2,X1]=meshgrid(x2(:),x1(1:lh)');
    else:
        flag2D=False;
        print('3D meshgrid')
        #     x1=xg.x1(3:end-2);
        #     x2=xg.x2(3:end-2);
        #     x3=xg.x3(3:end-2);
        #     [X2,X1,X3]=meshgrid(x2(:),x1(1:lh)',x3(:));

    #TABULATE THE SOURCE OR GRID CENTER LOCATION
    if 'sourcemlon' not in cfg.keys():
        thdist = np.mean(xg['theta'])
        phidist = np.mean(xg['phi'])
    else:
        thdist= np.pi/2 - np.deg2rad(cfg['sourcemlat']);    #zenith angle of source location
        phidist= np.deg2rad(cfg['sourcemlon']);

    #FIELD POINTS OF INTEREST (CAN/SHOULD BE DEFINED INDEPENDENT OF SIMULATION GRID)
    # ltheta = 40
    if flag2D:
        lphi = 1
    else:
        # lphi = 40
        lphi = ltheta
    lr = 1

    thmin = thdist - np.deg2rad(dang);
    thmax = thdist + np.deg2rad(dang);
    phimin = phidist - np.deg2rad(dang);
    phimax = phidist + np.deg2rad(dang);

    theta = np.linspace(thmin,thmax,ltheta);
    if flag2D:
        phi = phidist;
    else:
        phi = np.linspace(phimin,phimax,lphi);

    r = RE*np.ones((ltheta,lphi));                          #use ground level for altitude for all field points

    phi,theta = np.meshgrid(phi,theta,indexing='ij');

    ## CREATE AN INPUT FILE OF FIELD POINTS
    gridsize = np.int32([lr,ltheta,lphi])
    mag = dict()
    mag['r'] = np.float32(r).ravel()
    mag['phi'] = np.float32(phi).ravel()
    mag['theta'] = np.float32(theta).ravel()
    mag['gridsize'] = gridsize

    mag['lpoints'] = np.prod(gridsize)

    if write_grid:
        filename = os.path.join(direc, "inputs/TESTmagfieldpoints.h5")
        print(f"Writing grid to {filename}")
        write.maggrid(filename, mag)
        print("Done!")

    if return_grid:
        return mag
