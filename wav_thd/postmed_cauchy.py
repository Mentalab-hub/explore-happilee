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
import numpy as np
from wav_thd.cauchy_medzero import cauchy_medzero
from wav_thd.vecbinsolv import vecbinsolv

def postmed_cauchy(x, w):
    """
    Finds the posterior median of the Cauchy prior with
    mixing weight w, pointwise for each of the data point x.
    
    Args:
        x       : data array
        w       : weight value
    """
    if isinstance(x, int) or isinstance(x, float):
        x = np.float64(x)
        x = np.array([x])
    nx = len(x)
    z_est = np.resize(np.nan, nx)
    w = np.resize(w, nx)
    ax = abs(x)
    j = (ax < 20)
    
    z_est[~j] = ax[~j] - 2/ax[~j]
    if(sum(j) > 0):
        z_est[j] = vecbinsolv(zf=np.resize(0, sum(j)), func=cauchy_medzero,
                                t_lo=0, t_hi=max(ax[j]), z=ax[j], w=w[j])
    z_est[z_est<1e-7] = 0
    z_est = np.sign(x) * z_est
    return(z_est)