from data_input import ExG_data
import numpy as np
import mne

def lp_filt(ExG_in: ExG_data, cutoff_freq=100):
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
