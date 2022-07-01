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

def beta_laplace(x, s = 1, a = 0.5):
    """
    Given a single value or an array of x and s,
    Finds the function beta:
        beta(x, s, a) = g(x, s, a)/fn(x, 0, s) - 1
    where fn(x, 0, s) is the normal density with mean 0 and standard deviation s,
    and g is the convolution of the Laplace density with: 
        scale parameter a, gamma(mu, a), 
        with the normal density fn(x, mu, s) with mean mu and standard deviation s.
    
    Args:
        x       : a value or array containing data
        s       : a value or array of standard deviations (len(s) = len(X) if s is an array)
        a       : the scale parameter of the Laplace distribution
    Returns:
        beta    : a value or vector with the same length as x, containing values of the function beta
    """
    x = abs(x)
    xpa = x/s + s*a
    xma = x/s - s*a
    rat1 = 1/xpa
    
    rat1[xpa<35] = norm.cdf(-xpa[xpa<35], loc=0, scale=1) / norm.pdf(xpa[xpa<35], loc=0, scale=1)
    rat2 = 1/abs(xma)

    xma[xma>35] = 35
    rat2[xma>-35] = norm.cdf(xma[xma>-35], loc=0, scale=1) / norm.pdf(xma[xma>-35], loc=0, scale=1)

    beta = (a * s) / 2 * (rat1 + rat2) - 1
    return(beta)