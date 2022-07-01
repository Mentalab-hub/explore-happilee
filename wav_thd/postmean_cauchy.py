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

def postmean_cauchy(x, w):
    """
    Finds the posterior mean for the quasi-Cauchy prior with
    mixing weight w given data x.
    
    Args:
        x       : data array, may be a scalar
        w       : weight value
    """
    muhat = x
    ind = (x==0)
    x = x[~ind]
    ex = np.exp(-x**2 / 2)
    z = w * (x - (2 * (1 - ex)) / x)
    z = z / (w*(1-ex) + (1-w)*ex*x**2)
    muhat[~ind] = z
    return(muhat)