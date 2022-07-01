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
import pywt
import numpy as np
import copy
from statsmodels.robust.scale import mad
from wav_thd.wfromx import wfromx
from wav_thd.tfromw import tfromw


def ebayesthd(coefs, a=0.5, bayesfac=False, universalthd=True):
    """
    Given an array coefs containing wavelet coefficients, 
    Finds the marginal maximum likelihood estimator of the mixing weight w,
    and applies a thresholding rule with this weight.
    
    The applied thresholding rule is hard thresholding rule.
    Since level dependent thresholding is applied, the standard deviation is first calculated.

    bayesfac specifies whether to use the bayes factor threshold or the posterior median threshold.
    If universalthd=True,
        the thresholds will be upper-bounded by universal threshold adjusted by standard deviation;
        otherwise, weight w will be searched in [0, 1].
    """
    x = copy.deepcopy(coefs)

    # Calculating the standard deviation 
    sdev = mad(x, center=0)
    m_sdev = np.mean(sdev)
    s = sdev/m_sdev
    x = x/m_sdev

    # Calculating threshold values
    w = wfromx(x, s, prior="cauchy", a=a, universalthd=universalthd)
    tt = tfromw(w, s, prior="cauchy", bayesfac=bayesfac, a=a)

    # Applying hard thresholding rule
    muhat = pywt.threshold(x, tt,  mode='hard')
    muhat = muhat * m_sdev

    return(muhat)