from data_input import ExG_data
import numpy as np
import mne

def clean_ln(ExG_in: ExG_data):
    """
    Removes the line noise in the ExG data using CleanLineNoise method from the PREP pipeline
        (Bigdely-Shamlo N, Mullen T, Kothe C, Su K-M and Robbins KA (2015)
         The PREP pipeline: standardized preprocessing for large-scale EEG analysis
         https://doi.org/10.3389/fninf.2015.00016)
    Applied to all channels in ExG_in.ExGdata

    Args:
        ExG_in      : the ExG data to be processed
    Returns:
        ExG_lnrm   : procesed ExG data, line noise removed
    """
    # the frequencies to filter: line frequency and harmonics, up to s_rate / 2 (half the sampling rate)
    ln_freqs = np.arange(ExG_in.ln_freq, ExG_in.s_rate/2, ExG_in.ln_freq)

    # Removing line noise
    ExGdata_lnrm = mne.filter.notch_filter( ExG_in.ExGdata[1:, :],
                                    Fs = ExG_in.s_rate,
                                    freqs = ln_freqs,
                                    method = "spectrum_fit",
                                    mt_bandwidth = 2,
                                    p_value = 0.01,
                                    filter_length = "4s")
    tmp = ExG_in.ExGdata[0, :]
    # include the timestamps
    ExGdata_lnrm = np.transpose( np.c_[tmp, np.transpose(ExGdata_lnrm)] )

    ExG_lnrm = ExG_data(ExG_in.file_format, 
                        ExGdata_lnrm, 
                        ExG_in.n_chan, 
                        ExG_in.ch_names, 
                        ExG_in.s_rate, 
                        ExG_in.ln_freq)
    return(ExG_lnrm)


def clean_ln_ch(ExG_in_ch: np.array, ln_freq, s_rate):
    """
    Removes the line noise in the ExG data using CleanLineNoise method from the PREP pipeline
        (Bigdely-Shamlo N, Mullen T, Kothe C, Su K-M and Robbins KA (2015)
         The PREP pipeline: standardized preprocessing for large-scale EEG analysis
         https://doi.org/10.3389/fninf.2015.00016)
    Applied to 1 channel in an array

    Args:
        ExG_in_ch       : numpy array containing ExG data (for 1 channel)
        ln_Freq         : frequency of the line noise
        s_rate          : sampling rate
    Returns:
        ExGdata_lnrm_ch : procesed ExG data, line noise removed
    """
    # the frequencies to filter: line frequency and harmonics, up to s_rate / 2 (half the sampling rate)
    ln_freqs = np.arange(ln_freq, s_rate/2, ln_freq)

    # Removing line noise
    ExGdata_lnrm_ch = mne.filter.notch_filter( ExG_in_ch,
                                    Fs = s_rate,
                                    freqs = ln_freqs,
                                    method = "spectrum_fit",
                                    mt_bandwidth = 2,
                                    p_value = 0.01,
                                    filter_length = "4s")
    return(ExGdata_lnrm_ch)