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
from scipy.stats import norm
from wav_thd.beta_laplace import beta_laplace

def wfromt(tt, s=1, prior="cauchy", a=0.5):
    """
    Finds the weight that has posterior median threshold tt,
    given s and a.
    """
    if isinstance(s, int) or isinstance(s, float):
        s = np.array([s])

    if (prior[0] == "l"):
        tma = tt/s - s*a
        wi = 1/abs(tma)
        wi[tma>-35] = norm.cdf(tma[tma>-35], loc=0, scale=1) / norm.pdf(tma[tma>-35], loc=0, scale=1)
        wi = a*s*wi - beta_laplace(tt, s, a)
    
    elif(prior[0] == "c"):
        dnz = norm.pdf(tt, loc=0, scale=1)
        wi = (1 + (norm.cdf(tt, loc=0, scale=1) - tt*dnz - 1/2) /
                (np.sqrt(np.pi/2) * dnz * (tt**2)) )
        if isinstance(wi, int) or isinstance(wi, float):
            wi = np.array([wi])
        wi[~np.isfinite(wi)] = 1
    return(1/wi)