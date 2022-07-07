from data_input import ExG_data
import numpy as np
import mne

def lp_filt(ExG_in: ExG_data, cutoff_freq=100):
    """
    Applies low-pass filtering with a cutoff frequency of 100 Hz,
    Applied to all channels in ExG_in.ExGdata

    Args:
        ExG_in      : the ExG data to be processed
        cutoff_freq : cutoff frequency
    Returns:
        ExG_lpf   : procesed ExG data, filtered
    """
    ExGdata_lpf = mne.filter.filter_data(ExG_in.ExGdata[1:, :],
                                            sfreq = ExG_in.s_rate,
                                            h_freq = cutoff_freq,
                                            l_freq = None)
    tmp = ExG_in.ExGdata[0, :]
    # include the timestamps
    ExGdata_lpf = np.transpose( np.c_[tmp, np.transpose(ExGdata_lpf)] )

    ExG_lpf = ExG_data(ExG_in.file_format, 
                        ExGdata_lpf, 
                        ExG_in.n_chan, 
                        ExG_in.ch_names, 
                        ExG_in.s_rate, 
                        ExG_in.ln_freq)
    return(ExG_lpf)

def lp_filt_ch(ExG_in_ch: np.array, s_rate, cutoff_freq=100):
    """
    Applies low-pass filtering with a cutoff frequency of 100 Hz,
    Applied to 1 channel in an array

    Args:
        ExG_in_ch       : numpy array containing ExG data (1 channel)
        cutoff_Freq     : cutoff frequency
        s_rate          : sampling rate
    Returns:
        ExG_lpf_ch      : procesed ExG data, low-pass filtered
    """
    ExGdata_lpf_ch = mne.filter.filter_data( ExG_in_ch,
                                    sfreq = s_rate,
                                    h_freq = cutoff_freq,
                                    l_freq = None)
    return(ExGdata_lpf_ch)