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
from wav_thd.wpost_laplace import wpost_laplace

def postmean_laplace(x, s=1, w=0.5, a=0.5):
    """
    Finds the posterior mean for the double exponential prior for
    a given x, s, w, and a. Only allows a < 20 for input value.
    
    Args:
        x       : data array
        s       : standard deviation
        w       : weight value
        a       : scalar value
    """
    a = min(a, 20)

    # Finding the probability of being non-zero
    wpost = wpost_laplace(w, x, s, a)

    # Finding the posterior mean conditional on being non-zero
    sx = np.sign(x)
    x = abs(x)
    xpa = x/s + s*a
    xma = x/s - s*a
    xpa[xpa>35] = 35
    xpa[xpa<-35] = -35

    cp1 = norm.cdf(xma, loc=0, scale=1)
    cp2 = norm.cdf(-xpa, loc=0, scale=1)
    ef = np.exp(np.minimum(2*a*x, 100))
    postmeancond = x - a * s**2 * (2*cp1 / (cp1 + ef*cp2) - 1)
    postmean = sx * wpost * postmeancond

    # Return posterior mean
    return(postmean)