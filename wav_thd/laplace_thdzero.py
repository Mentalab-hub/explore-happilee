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

def laplace_thdzero(x, s=1, w=0.5, a=0.5):
    """
    The function that has to be zeroed to find the threshold with the
    Laplace prior. Only allows a < 20 for input value.

   Args:
      x       : data array
      s       : standard deviation
      w       : weight value
      a       : scalar value
    """
    a = min(a, 20)
    xma = x/s - s*a
    z = norm.cdf(xma, loc=0, scale=1) - 1/a * (1/s*norm.pdf(xma)) * (1/w + beta_laplace(x,s,a))
    return(z)