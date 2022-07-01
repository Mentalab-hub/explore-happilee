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

def cauchy_medzero(x, z, w):
    """
    The objective function that has to be zeroed, component by component, 
    to find the posterior median when the quasi-Cauchy prior is used.
    
    Args:
        x       : parameter array, may be scalar
        z       : data array, may be scalar
        w       : weighat value or array of weight values
    """
    hh = z - x
    dnhh = norm.pdf(hh, loc=0, scale=1)
    yleft = ( norm.cdf(hh, loc=0, scale=1) - z*dnhh + ((z*x - 1) * dnhh * norm.cdf(-x, loc=0, scale=1) / 
                norm.pdf(x, loc=0, scale=1)) )
    yright2 = 1 + np.exp(-z**2 / 2) * (z**2 * (1/w - 1) - 1)
    
    return(yright2/2 - yleft)