from data_input import ExG_data
import numpy as np
import mne

def clean_ln(ExG_in: ExG_data):
    """
    Removes the line noise in the ExG data using CleanLineNoise method (from the PREP pipeline [Bigdely-Shamlo, et.al, 2015])
    Args:
        ExG_in      : the ExG data to be processed
    Returns:
        ExG_ln_rm   : procesed ExG data, line noise removed
    """
    # the frequencies to filter: line frequency and harmonics, up to s_rate / 2 (half the sampling rate)
    ln_freqs = np.arange(ExG_in.ln_freq, ExG_in.s_rate/2, ExG_in.ln_freq)

    # Removing line noise
    ExGdata_ln_rm = mne.filter.notch_filter( ExG_in.ExGdata[1:, :],
                                    Fs = ExG_in.s_rate,
                                    freqs = ln_freqs,
                                    method = "spectrum_fit",
                                    mt_bandwidth = 2,
                                    p_value = 0.01,
                                    filter_length = "4s")
    tmp = ExG_in.ExGdata[0, :]
    # include the timestamps
    ExGdata_ln_rm = np.transpose( np.c_[tmp, np.transpose(ExGdata_ln_rm)] )

    ExG_ln_rm = ExG_data(ExG_in.file_format, 
                        ExGdata_ln_rm, 
                        ExG_in.n_chan, 
                        ExG_in.ch_names, 
                        ExG_in.s_rate, 
                        ExG_in.ln_freq)
    return(ExG_ln_rm)
