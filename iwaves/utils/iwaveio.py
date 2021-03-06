##################
# IO routines
##################
import xarray as xray
from iwaves.kdv.kdv import KdV
from iwaves.kdv.vkdv import vKdV
import numpy as np

import pdb


def from_netcdf(kdvfile):
    """
    Load a KdV object from a pre-computed netcdf file
    """
    
    # Load the data file (hope it's in the right format)
    kdvx = xray.open_dataset(kdvfile)
    
    # These are the attributes that KdV requires
    #attrs = ['L_d','Nx','Lw','a0','Cmax','nu_H','x0']
    attrs = [  
                #'Nx',\
                #'L_d',\
                'a0',\
                'Lw',\
                'x0',\
                'mode',\
                'Cmax',\
                'nu_H',\
                'dx_s',\
                'dz_s',\
                'dt_s',\
                'c1',\
                'mu',\
                'epsilon',\
                'r01',\
                'r10',\
                'spongedist',\
                't',\
                #'ekdv',
        ]



    kwargs = {}
    for aa in attrs:
        kwargs.update({aa:getattr(kdvx,aa)})

    z = kdvx.z.values
    rhoz = kdvx.rhoz.values
    x= kdvx.x.values

    # Let the class compute everything else...
    kdv = KdV(rhoz, z, x=x, **kwargs)

    # Set the amplitude function
    kdv.B[:] = kdvx.B.values
    
    # Return the time-variable amplitude array as well
    if 'B_t' in list(kdvx.variables.keys()):
        B_t  = kdvx['B_t']
    else:
        B_t = None
    
    return kdv, B_t

    

def vkdv_from_netcdf(ncfile, a0=None, wavefunc=None, mode=None):
    """
    Wrapper to load an object directly from a pre-saved file
    """

    ds = xray.open_dataset(ncfile)

    if a0 is None:
        a0 = ds.a0

    if wavefunc is None:
        args = {}
    else:
        args = {'wavefunc':wavefunc}
    
    if mode is None:
        args.update({'mode':0})

    # Need this for backward compatability...
    if hasattr(ds,'r20'):
        r20 = ds.r20.values
        D20 = ds.D20.values
        phi20 = ds.phi20.values
        ekdv = ds.ekdv
    else:
        r20 = np.zeros_like(ds.x.values)
        ekdv = False
        D20 = np.zeros_like(ds.D10)
        phi20 = np.zeros_like(ds.D10)


    mykdv = vKdV(
        ds.rhoZ.values[:,0],
        ds.Z.values[:,0],
        ds.h.values,
        x=ds.x.values,\
        #mode=ds.mode,\
        a0=a0,\
        #Lw=ds.Lw,\
        x0=0,\
        ekdv=ekdv,
        #nu_H=ds.nu_H,\
        #spongedist=ds.spongedist,\
        #Cmax=ds.Cmax,\
        #dt=ds.dt_s,
        Cn=ds.Cn.values,
        Phi=ds.Phi.values,
        Alpha=ds.Alpha.values,
        Beta=ds.Beta.values,
        Qterm=ds.Qterm.values,
        phi01=ds.phi01.values,
        phi10=ds.phi10.values,
        D01=ds.D01.values,
        D10=ds.D10.values,
        phi20=phi20,
        D20=D20,
        r20=r20,
        **args
    )

    # Return the time-variable amplitude array as well
    if 'B_t' in list(ds.variables.keys()):
        B_t  = ds['B_t']
    else:
        B_t = None

    return mykdv, B_t
 







