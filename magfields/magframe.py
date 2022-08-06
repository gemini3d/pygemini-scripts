import numpy as np
import os
import gemini3d.find
import gemini3d.read
import h5py

def magframe(filename: str,**opts):
    """
    # example use
    # dat = gemini3d.read.magframe(filename)
    # dat = gemini3d.read.magframe(folder, "time", datetime)
    # dat = gemini3d.read.magframe(filename, "config", cfg)

    Translated from magframe.m 
    2022/07/05
    Spencer M Hatch
    
    Tweaks to deal with pygemini API idiodsyncracies.  Also force
      return with no value if binary files used (should be deprecated
      soon) -MZ.
    2022/7/7
    """

    # arguments
    # filename (1,1) string {mustBeNonzeroLengthText}
    # opts.time datetime {mustBeScalarOrEmpty} = datetime.empty
    # opts.cfg struct {mustBeScalarOrEmpty} = struct.empty
    # opts.gridsize (1,3) {mustBeInteger} = [-1,-1,-1]    # [lr,ltheta,lphi] grid sizes
    # end

    time = None
    gridsize = [-1,-1,-1]
    if 'time' in opts:
        time = opts['time']

    if 'gridsize' in opts:
        gridsize = opts['gridsize']

    # make sure to add the default directory where the magnetic fields are to
    # be found
    if os.path.isfile(filename):
        direc = os.path.dirname(os.path.dirname(filename));
    else:
        direc = os.path.dirname(filename);
    basemagdir = os.path.join(direc,"magfields")

    # find the actual filename if only the directory was given
    if not os.path.isfile(filename):
        if time is not None:
            filename = gemini3d.find.frame(basemagdir, opts['time'])

    # read the config file if one was not provided as input
    if 'config' in opts:
        cfg = opts['cfg']
    else:
        cfg = gemini3d.read.config(direc)

    # some times might not have magnetic field computed
    if len(str(filename)) == 0:
        print("SKIP: read.magframe %s", str(time))
        return

    # load and construct the magnetic field point grid
    assert cfg['file_format'] in ['.dat','.h5'], 'Unrecognized input field point file format {:s}'.format(cfg['file_format'])
    if cfg['file_format'] == '.dat':
        print("Have not implemented magframe in python for file_format=='dat'!")
        return;
        # fn = os.path.join(direc,'inputs/magfieldpoints.dat');
        # assert os.path.isfile(fn), fn + " not found"

        # fid = fopen(fn, 'r');
        # lpoints = fread(fid,1,'integer*4');
        # r = fread(fid,lpoints,'real*8');
        # theta = fread(fid,lpoints,'real*8');    #by default these are read in as a row vector, AGHHHH!!!!!!!!!
        # phi = fread(fid,lpoints,'real*8');
        # fclose(fid);
    elif cfg['file_format'] == '.h5':
        fn = os.path.join(direc,'inputs/magfieldpoints.h5');
        assert os.path.isfile(fn), fn + " not found"

        # matl = dict()
        # matl['lpoints'] = f3['lpoints'][()]
        # matl['gridsize'] = f3['gridsize'][:]
        # matl['r'] = f3['r'][:]
        # matl['theta'] = f3['theta'][:]
        # matl['phi'] = f3['phi'][:]

        with h5py.File(fn, "r") as h5f:
            lpoints   = h5f['lpoints'][()]
            gridsize  = h5f['gridsize'][:]
            r         = h5f['r'][:]
            theta     = h5f['theta'][:]
            phi       = h5f['phi'][:]

    # Reorganize the field points if the user has specified a grid size
    if any(elem < 0 for elem in gridsize):
        gridsize=[lpoints,1,1]    # just return a flat list if the user has not specified any gridding
        flatlist = True
    else:
        flatlist = False

    lr,ltheta,lphi = gridsize
    r = r.reshape(gridsize)
    theta = theta.reshape(gridsize)
    phi = phi.reshape(gridsize)

    # Sanity check the grid size and total number of grid points
    assert lpoints == np.prod(gridsize), 'Incompatible data size and grid specification...'

    # Create grid alt, magnetic latitude, and longitude (assume input points
    # have been permuted in this order)...
    mlat = 90-theta*180/np.pi
    mlon = phi*180/np.pi
    # breakpoint()
    dat = dict()
    if ~flatlist:   # we have a grid of points
        ilatsort = np.argsort(mlat[0,0,:])
        # [~,ilatsort]=sort(mlat(1,:,1))    #mlat runs against theta...
        dat['mlat'] = np.squeeze(mlat[0,0,ilatsort])
        # [~,ilonsort]=sort(mlon(1,1,:))
        ilonsort = np.argsort(mlon[0,:,0])
        dat['mlon'] = np.squeeze(mlon[0,ilonsort,0])
        dat['r'] = r[:,0,0]    # assume already sorted properly
    else:    # we have a flat list of points
        ilatsort = slice(0,lpoints)
        ilonsort = slice(0,lpoints)
        dat['mlat'] = mlat
        dat['mlon'] = mlon
        dat['r'] = r

    # allocate output arrays
    dat['Br'] = np.zeros((lr,ltheta,lphi))
    dat['Btheta'] = np.zeros((lr,ltheta,lphi))
    dat['Bphi'] = np.zeros((lr,ltheta,lphi))

    # Br
    if cfg['file_format'] == '.dat':
        return;
        #        fid = fopen(os.path.join(basemagdir,strcat(filename,".dat")),'r');
        # fid = fopen(filename,'r');
        # data = fread(fid,lpoints,'real*8');
    elif cfg['file_format'] == '.h5':
        data = np.array(h5py.File(filename, 'r')['/magfields/Br'])

    dat['Br'] = data.reshape([lr,ltheta,lphi]);
    if ~flatlist:
        dat['Br'] = dat['Br'][:,ilatsort,:]
        dat['Br'] = dat['Br'][:,:,ilonsort]

    # Btheta
    if cfg['file_format'] == '.dat':
        return;
        #data = fread(fid,lpoints,'real*8');
    elif cfg['file_format'] == '.h5':
        data = np.array(h5py.File(filename, 'r')['/magfields/Btheta'])

    dat['Btheta'] = data.reshape([lr,ltheta,lphi])
    if ~flatlist:
        dat['Btheta'] = dat['Btheta'][:,ilatsort,:]
        dat['Btheta'] = dat['Btheta'][:,:,ilonsort]

    # Bphi
    if cfg['file_format'] == '.dat':
        #data = fread(fid, lpoints,'real*8')
        return;
    if cfg['file_format'] == '.h5':
        data = np.array(h5py.File(filename, 'r')['/magfields/Bphi'])

    dat['Bphi'] =data.reshape([lr,ltheta,lphi])
    if ~flatlist:
        dat['Bphi'] = dat['Bphi'][:,ilatsort,:]
        dat['Bphi'] = dat['Bphi'][:,:,ilonsort]

    return dat
