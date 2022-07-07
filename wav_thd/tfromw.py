"""
The wavelet thresholding step used here is a Python implementation of the wdenoise
function from the Matlab Wavelet Toolbox as used in the HAPPILEE pipeline.
(Level dependent hard thresholding with Bayes thresholding method)

The empirical Bayes method used a Python implementation of the R package:
   Silverman, B. (2012) EbayesThresh: Empirical Bayes Thresholding and
   Related Methods, http://CRAN.R-project.org/package=EbayesThresh.

   References:
   Johnstone, I. & Silverman, B. (2005). EbayesThresh: R Programs for
   Empirical Bayes Thresholding, Journal of Statistical Software, 12,1,
   pp. 1-38.
"""
import numpy as np
from wav_thd.cauchy_thdzero import cauchy_thdzero
from wav_thd.laplace_thdzero import laplace_thdzero
from wav_thd.vecbinsolv import vecbinsolv
from wav_thd.beta_laplace import beta_laplace
from wav_thd.beta_cauchy import beta_cauchy

def tfromw(w, s=1, prior="cauchy", bayesfac=False, a=0.5):
    """
    Given array of weights w and standard deviation s, 
    Finds the threshold or array of thresholds corresponding to these weights,
    under the specified prior.

    If bayesfac=True the Bayes factor thresholds are found, 
    otherwise the posterior median thresholds are found.

    If the Laplace prior is used, 
    a gives the value of the inverse scale (i.e. rate) parameter
    """
    
    if isinstance(w, int) or isinstance(w, float):
        w = np.float(w)
        w = np.array([w])
    if isinstance(s, int) or isinstance(s, float):
        s = np.float(s)
        s = np.array([s])
    
    if (bayesfac):
        z = 1/w - 2
        if (prior[0] == "l"):
            if (len(w) >= len(s)):
                zz = z
            else:
                zz = np.resize(z, len(s))
            tt = vecbinsolv(zf=zz, func=beta_laplace, t_lo=0, t_hi=10, s=s, a=a)
        elif (prior[0] == "c"):
            tt = vecbinsolv(zf=z, func=beta_cauchy, t_lo=0, t_hi=20)
    
    else:
        z = 0
        if (prior[0] == "l"):
            zz = np.resize(z, max(len(s), len(w)))

            # When (x/s - s*a > 25), laplace_thdzero has value close to 1/2.
            # The boundary value of x can be treated as the upper bound for search.
            tt = vecbinsolv(zf=zz, func=laplace_thdzero, t_lo=0, t_hi=s * (25 + s*a),
                            s=s, w=w, a=a)
        
        elif (prior[0] == "c"):
            zz = np.resize(z, len(w))
            tt = vecbinsolv(zf=zz, func=cauchy_thdzero, t_lo=0, t_hi=10, w=w)
    return(tt)

           