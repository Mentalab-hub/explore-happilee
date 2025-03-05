import numpy as np
import matplotlib.pyplot as plt
import data_input
import ch_selection
import ln_removal
import filtering
from wav_thresholding import wav_thresholding

def main():

    # Loading ExG data
    file_format = data_input.in_file_format()
    ExGdata = data_input.in_ExGdata(file_format)
    n_chan = data_input.get_n_chan(ExGdata)
    ch_names = data_input.in_ch_names(n_chan)
    s_rate = data_input.get_s_rate(ExGdata)
    ln_freq = data_input.in_ln_freq()
    A = data_input.ExG_data(file_format, ExGdata, n_chan, ch_names, s_rate, ln_freq)

    # Display the values
    print("File format (1: .csv, 2: .edf):", A.file_format)
    print("Number of channels:", A.n_chan)
    print("Timestamps (s):", A.ExGdata[0, :])
    print("Channel names: ", A.ch_names)
    print("Sampling rate: ", A.s_rate)
    print("Line frequency: ", A.ln_freq)
    print("ExGdata shape:", A.ExGdata.shape)

    # Apply the HAPPILEE pipeline
    # Select channels
    ExG_sel = ch_selection.select(A)
    ExG_wav_thd.save_to_csv('out_ExG_raw.csv')

    # Remove line noise
    ExG_ln_rm = ln_removal.clean_ln(ExG_sel)

    # Apply low-pass filter 30 Hz
    ExG_lpf = filtering.lp_filt(ExG_ln_rm, 30)

    # Apply high-pass filter 1 Hz
    ExG_lpf = filtering.hp_filt(ExG_ln_rm, 1)

    # Apply wavelet thresholding
    ExG_wav_thd = wav_thresholding(ExG_lpf)

    # Save the processed data to a CSV file
    ExG_wav_thd.save_to_csv('out_ExG_wav_thd.csv')
    

if __name__ == "__main__":
    main()