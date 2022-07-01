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
from wav_thd.wfromt import wfromt
from wav_thd.beta_laplace import beta_laplace
from wav_thd.beta_cauchy import beta_cauchy

def wfromx(x, s=1, prior="cauchy", a=0.5, universalthd = True):
    """
    Given the data array x and standard deviation s, 
    Finds the value of w that zeroes S(w) in the range by 
    successive bisection, carrying out n_iter harmonic bisections of the
    original interval between wlo and 1.
    """
    n_iter = 30
    
    if (prior[0] == "c"):
        s = 1
    if (universalthd):
        t_univ = np.sqrt(2 * np.log(len(x))) * s
        w_lo = wfromt(t_univ, s, prior, a)
        w_lo = max(w_lo)
    else:
        w_lo = 0
    
    if(prior[0] == "l"):
        beta = beta_laplace(x, s, a)
    elif(prior[0] == "c"):
        beta = beta_cauchy(x)
    
    w_hi = 1
    beta = np.minimum(beta, 1e20)
    s_hi = sum(beta / (1+beta))
    if (s_hi >= 0):
        return(1)
    
    s_lo = sum(beta / (1 + w_lo*beta))
    if (s_lo <= 0):
        return(w_lo)
    
    for j in range(0, n_iter):
        w_mid = np.sqrt(w_lo * w_hi)
        s_mid = sum(beta / (1 + w_mid*beta))
        if (s_mid == 0):
            return(w_mid)
        elif(s_mid > 0):
            w_lo = w_mid
        else:
            w_hi = w_mid
    return(np.sqrt(w_lo * w_hi))