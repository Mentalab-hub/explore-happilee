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
from wav_thd.ebayesthd import ebayesthd
import pywt

def ebayesthd_wav_dwt(x, s_rate=250, a=0.5, bayesfac=False):
    """
    Given an array x containing signal values, 
    Subjects the array to a multilevel wavelet transform, 
    then subjects the resulting wavelet coefficients to a level dependent hard thresholding.
    Returns the reconstructed signal after thresholding.

    Args:
        x       : array containing signal values
        s_rate  : sampling rate
        bayesfac: specifies whether to use the bayes factor threshold or the posterior median threshold.
    """
    # 1. Setting wavelet level based on the sampling rate (s_rate)
    if (s_rate > 500):
        wavLvl = 10
    elif (s_rate > 250 and s_rate <= 500):
        wavLvl = 9
    elif (s_rate <= 250):
        wavLvl = 8

    # 2. Wavelet transform
    x_dwt = pywt.wavedecn(x, wavelet='coif4', level=wavLvl, axes=0)
    
    # 3. Applying hard thresholding rule at each 
    x_thd_dwt = []
    x_thd_dwt.append(x_dwt[0])
    for level in range(1, wavLvl+1, 1):
        # Apply hard thresholding to the current level's wavelet coefficients
        lvl_coefs = x_dwt[level].get("d")
        lvl_coefs = ebayesthd(lvl_coefs, a, bayesfac)
        x_thd_dwt.append({"d": lvl_coefs})

    # 4. Reconstructing signal after being subjected to thresholding
    x_thd = pywt.waverecn(x_thd_dwt, 'coif4')
    x_thd = x_thd[: len(x)]

    return(x_thd)