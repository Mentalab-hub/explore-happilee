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
import sys
from wav_thd.postmed_cauchy import postmed_cauchy
from wav_thd.postmed_laplace import postmed_laplace

def postmed(x, s=1, w=0.5, prior="laplace", a=0.5):
    """
    Given a single value or an array of data and sampling standard deviations
    (for Cauchy prior, sd=1), 
    Finds the corresponding posterior median estimate(s) for a given x, s, w, and a.
    
    Args:
        x       : data array
        s       : standard deviation
        w       : weight value
        a       : scalar value
    """
    if (prior[0] == "l"):
        muhat = postmed_laplace(x, s, w, a=a)
    elif(prior[0] == "c"):
        if isinstance(s, int) or isinstance(s, float):
            if (s != 1):
                sys.exit("Only standard deviation of 1 is allowed for Cauchy prior")
            else:
                muhat = postmed_cauchy(x, w)
        else:
            if (any(s!=1)):
                sys.exit("Only standard deviation of 1 is allowed for Cauchy prior")
            else:
                muhat = postmed_cauchy(x, w)

    return(muhat)