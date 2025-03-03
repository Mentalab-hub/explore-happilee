"""
The wavelet thresholding step used here is a Python implementation of the wdenoise
function from the Matlab Wavelet Toolbox as used in the HAPPILEE pipeline.
(Level dependent hard thresholding with Bayes thresholding method)

The empirical Bayes method used is a Python implementation of the R package:
   Silverman, B. (2012) EbayesThresh: Empirical Bayes Thresholding and
   Related Methods, http://CRAN.R-project.org/package=EbayesThresh.

   References:
   Johnstone, I. & Silverman, B. (2005). EbayesThresh: R Programs for
   Empirical Bayes Thresholding, Journal of Statistical Software, 12,1,
   pp. 1-38.
"""
import sys
import numpy as np


def vecbinsolv(zf, func, t_lo, t_hi, n_iter=30, **kwargs):
    """
    Solves a nonlinear equation or an array of nonlinear equations based on 
    an increasing function in a specified interval.
    
    Given a monotone function func, and a vector of values zf, 
    Finds a vector of numbers t such that f(t) = zf.
    The solution is constrained to lie on the interval (t_lo, t_hi)

    Additional arguments to func can be passed through

    By successive bisection, carries out n_iter harmonic bisections of the
    interval between t_lo and t_hi
        
    Args:
        zf      : array of values
        func    : monotone function
        t_lo    : lower constraint of the interval
        t_hi    : upper constraint of the interval
        n_iter  : number of iterations
    """
    if isinstance(zf, int) or isinstance(zf, float):
        z_f = np.float64(zf)
        z_f = np.array([zf])
        nz = len(z_f)
    else:
        nz = len(zf)
    
    if isinstance(t_lo, int) or isinstance(t_lo, float) or (len(t_lo)==1):
        t_lo = np.float64(t_lo)
        t_lo = np.resize(t_lo, nz)
    elif (len(t_lo)!=nz):
        sys.exit("Lower constraint has to be homogeneous or has the same length as function")
    
    if isinstance(t_hi, int) or isinstance(t_hi, float) or (len(t_hi)==1):
        t_hi = np.float64(t_hi)
        t_hi = np.resize(t_hi, nz)
    elif (len(t_hi)!=nz):
        sys.exit("Upper constraint has to be homogeneous or has the same length as function")

    # n_iter bisections
    for j in range(0, n_iter):
        t_mid = (t_lo + t_hi)/2
        f_mid = func(t_mid, **kwargs)
        indt = (f_mid <= zf)
        t_lo[indt] = t_mid[indt]
        t_hi[~indt] = t_mid[~indt]
    
    t_sol = (t_lo + t_hi) / 2
    return(t_sol)