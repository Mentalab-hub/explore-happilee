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
from wav_thd.beta_laplace import beta_laplace

def wpost_laplace(w, x, s=1, a=0.5):
    """
    Calculates the posterior weight for non-zero effect
    
    Args:
        w       : weight value
        x       : data array
        s       : standard deviation
        a       : scalar value
    """
    wpost = 1 - (1-w) / (1 + w*beta_laplace(x,s,a))
    return(wpost)