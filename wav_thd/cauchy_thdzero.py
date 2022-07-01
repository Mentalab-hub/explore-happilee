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

def cauchy_thdzero(z, w):
    """
    The objective function that has to be zeroed to find the Cauchy threshold
    
    Args:
        z       : putative threshold array
        w       : weighat value or array of weight values
    """
    y = norm.cdf(z, loc=0, scale=1) - z * norm.pdf(z, loc=0, scale=1) - 1/2 - (z**2 * np.exp(-z**2 / 2) * (1/w - 1)) / 2
    return(y)