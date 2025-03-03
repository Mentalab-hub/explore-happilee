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


def clean_ln_ch(ExG_in: np.ndarray, ln_freq: float, s_rate: float):
    """
    Removes line noise for single or multiple channels using the CleanLineNoise method
    from the PREP pipeline. Automatically handles 1D (single channel) or 2D (multi-channel) input.

    Args:
        ExG_in   : NumPy array of shape (n_samples,) for single channel,
                   or (n_channels, n_samples) for multi-channel.
        ln_freq  : Frequency of the line noise.
        s_rate   : Sampling rate in Hz.

    Returns:
        ExGdata_lnrm : Processed ExG data with line noise removed,
                       having the same shape as ExG_in.
    """
    ln_freqs = np.arange(ln_freq, s_rate / 2, ln_freq)

    # If single-channel data is passed in 1D shape, reshape to 2D
    single_channel = False
    if ExG_in.ndim == 1:
        ExG_in = ExG_in[np.newaxis, :]
        single_channel = True

    ExGdata_lnrm = mne.filter.notch_filter(
        ExG_in,
        Fs=s_rate,
        freqs=ln_freqs,
        method="spectrum_fit",
        mt_bandwidth=2,
        p_value=0.01,
        filter_length="4s"
    )

    # Reshape back to 1D if the original input was single-channel
    if single_channel:
        ExGdata_lnrm = ExGdata_lnrm.flatten()

    return ExGdata_lnrm