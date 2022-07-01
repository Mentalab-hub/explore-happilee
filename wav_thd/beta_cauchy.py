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
import copy
from scipy.stats import norm

def beta_cauchy(x):
    """
    Function beta for the quasi-Cauchy prior
    Finds the function beta for the mixed normal prior with Cauchy tails.
        beta(x) = g(x)/phi(x) - 1
    It is assumed that the noise variance = 1.
    
    Args:
        x       : a value or array containing data
    Returns:
        beta    : value or array of values of the function beta
    """
    phi_x = norm.pdf(x, loc=0, scale=1)
    j = (x != 0)
    beta = copy.deepcopy(x)
    beta[~j] = -1/2
    beta[j] = (norm.pdf(0, loc=0, scale=1) / phi_x[j] - 1) / (x[j]**2) - 1

    return(beta)