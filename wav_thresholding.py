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
from data_input import ExG_data
from wav_thd.ebayesthd_wav_dwt import ebayesthd_wav_dwt

def wav_thresholding(ExG_in: ExG_data):
    """
    Subjects the signal to wavelet thresholding.
    The wavelet thresholding step used here is a Python implementation of the wdenoise
    function from the Matlab Wavelet Toolbox as used in the HAPPILEE pipeline.
    (Level dependent hard thresholding with Bayes thresholding method)

    The empirical Bayes method used is a Python implementation of the R package:
        Silverman, B. (2012) EbayesThresh: Empirical Bayes Thresholding and
        Related Methods, http://CRAN.R-project.org/package=EbayesThresh.

    Args:
        ExG_in      : the ExG data to be processed
    Returns:
        ExG_wav_thd : procesed ExG data, artifacts removed
    """
    # Applying wavelet thresholding to signal from each channel 
    ExGdata_wav_thd = ExG_in.ExGdata[0, :] # include the timestamps
    for channel in range(1, ExG_in.n_chan+1):
        artifacts = ebayesthd_wav_dwt(ExG_in.ExGdata[channel], ExG_in.s_rate)
        signal = ExG_in.ExGdata[channel] - artifacts
        ExGdata_wav_thd = np.c_[ExGdata_wav_thd, signal]
    ExGdata_wav_thd = np.transpose(ExGdata_wav_thd)

    # Denoised data
    ExG_wav_thd = ExG_data(ExG_in.file_format, 
                        ExGdata_wav_thd, 
                        ExG_in.n_chan, 
                        ExG_in.ch_names, 
                        ExG_in.s_rate, 
                        ExG_in.ln_freq)
    
    return(ExG_wav_thd)