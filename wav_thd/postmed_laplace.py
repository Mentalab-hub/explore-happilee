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

def postmed_laplace(x, s=1, w=0.5, a=0.5):
    """
    Finds the posterior median for the Laplace prior for
    a given x, s, w, and a. Only allows a < 20 for input value.
    
    Args:
        x       : data array
        s       : standard deviation
        w       : weight value
        a       : scalar
    """
    a = min(a, 20)

    # Work with the absolute value of x, and for x > 25, uses the
    # approximation to norm.pdf(x-a) * beta_laplace(x,s,a)
    sx = np.sign(x)
    x = abs(x)
    xma = x/s - s*a
    zz = 1/a * (1/s*norm.pdf(xma, loc=0, scale=1)) * (1/w + beta_laplace(x,s,a))
    zz[xma>25] = 1/2
    
    mucor = norm.ppf(np.minimum(zz, 1), loc=0, scale=1)
    muhat = sx * np.maximum(0, xma - mucor) * s
    return(muhat)