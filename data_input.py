import numpy as np
import os.path
import matplotlib.pyplot as plt
from plotting import plot_psd
import mne

class ExG_data():
    """
    ExG_data contains information:
        file_format : type of file containing the EEG data (1 - .csv, 2 - .edf)
        ExGdata     : numpy array containing recorded ExG data
        n_chan      : number of channels
        ch_names    : channel names
        s_rate      : sampling rate
    """
    def __init__(self, file_format, ExGdata, n_chan, ch_names, s_rate, ln_freq):
        self.file_format = file_format
        self.ExGdata = ExGdata
        self.n_chan = n_chan
        self.ch_names = ch_names
        self.s_rate = s_rate
        self.ln_freq = ln_freq


    def plot_ExGdata(self):
        """
        Plots the ExG data stored in the self.ExGdata numpy array
        """
        fig, ax = plt.subplots(self.n_chan, sharex=True, sharey=False)

        SMALL_SIZE = 18
        MEDIUM_SIZE = 20
        BIGGER_SIZE = 22
        plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
        plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
        plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
        plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title
        plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels

        plt.rcParams['figure.figsize'] = [28, 5*self.n_chan]
        plt.rcParams['figure.dpi'] = 100

        fig.suptitle('ExG data')
        if self.n_chan == 1:
            ax.set_ylabel(f"{self.ch_names[0]} (mV)")
            ax.plot(self.ExGdata[0, :], self.ExGdata[1, :])
            ax.set_xlabel("Time (s)")
        else:
            for i in range(self.n_chan):
                ax[i].set_ylabel(f"{self.ch_names[i]} (mV)")
                ax[i].plot(self.ExGdata[0, :], self.ExGdata[i+1, :])
            ax[-1].set_xlabel("Time (s)")

    
    def plot_ExGdata_psd(self):
        """
        Plots the power spectrum density of the ExG data stored in the self.ExGdata numpy array
        """
        for channel in range(1, np.shape(self.ExGdata)[0]):
            plot_psd(self.ExGdata[channel], self.ExGdata[0], self.s_rate, ch_name=self.ch_names[channel-1])

        
    def save_to_csv(self, file_path):
        """
        Saves the ExGdata array to a CSV file.
        The timestamp column is shown with four decimals,
        while channel values columns are limited to two decimals.

        Args:
            file_path : path to save the CSV file
        """
        temp_data = self.ExGdata.copy()
        temp_data[0, :] = np.round(temp_data[0, :], 4)
        
        header = "TimeStamp," + ",".join(self.ch_names)
        
        # Format: first column (timestamp) with 4 decimals, others with 2 decimals
        formats = ['%.4f'] + ['%.2f'] * (temp_data.shape[0] - 1)
        
        np.savetxt(
            file_path,
            temp_data.T,
            delimiter=',',
            header=header,
            comments='',
            fmt=formats
        )


def in_file_format():
    """
    Asks the user for the file format:  
        1 - .csv
        2 - .edf
    """
    while True:
        file_format = input("Select File Format:\n\t1 - .csv\n\t2 - .edf\n")
        if not file_format.isnumeric() or int(file_format) not in range(1, 3):
            print("Invalid input: please enter 1 or 2.\n")
        else:
            break
    return(int(file_format))


def in_ExGdata(file_format):
    """
    Asks the user for the path to the recorded ExG data and
    Loads the ExG data as a numpy array  

    Returns:
        ExGdata : numpy array containing the recorded ExG data 
                    (   ExGdata[0, :]: Timestamps
                        ExGdata[1, :]: Recorded data from channel 1
                        ExGdata[2, :]: Recorded data from channel 2
                        ...)
    """
    while True:
        file_path = input("Input the path to the recorded data, including the file name:\n")
        if not os.path.exists(file_path):
            print("File does not exist. Please input the correct path and file name.\n")
        else:
            break
    
    if file_format == 1: # file format: 1 - .csv
        ExGdata = np.transpose( np.genfromtxt(file_path, delimiter = ',') )
        ExGdata = ExGdata[:, 1:]
        ExGdata[0] = ExGdata[0] - ExGdata[0][0] # timestamp starts at 0s
            # ExGdata[0, :]: Timestamps
            # ExGdata[1, :]: Recorded data from channel 1
            # ExGdata[2, :]: Recorded data from channel 2
            # ...
    
    elif file_format == 2: # file format: 2 - .edf
        raw = mne.io.read_raw_edf(file_path, preload=True)
        # Get data up to 10 seconds
        data, times = raw[:, :int(10 * raw.info['sfreq'])]  # Limit to first 10 seconds
        ExGdata = np.vstack((times, data))
        ExGdata[0] = ExGdata[0] - ExGdata[0][0]  # timestamp starts at 0s
    
    return(ExGdata)


def get_n_chan(ExGdata: np.array):
    """
    Detects the number of recorded channels from the loaded file (ExGdata)  

    Args:
        ExGdata : numpy array containing the recorded ExG data
    """
    n_chan = ExGdata.shape[0] - 1

    return(n_chan) 


def in_ch_names(n_chan):
    """
    Asks the user for each channel name.  

    Args:
        n_chan  : number of channels recorded
    """
    ch_names = []
    for i in range(n_chan):
        ch_name = input("Input the name for channel " + str(i+1) + ":\n")
        ch_names.append(ch_name)
    return(ch_names)


def get_s_rate(ExGdata: np.array):
    """
    Detects the sampling rate from the loaded file (ExGdata)  

    Args:
        ExGdata : numpy array containing the recorded ExG data
    Returns:
        s_rate  : sampling rate from the recorded ExGdata
    """
    s_rate = ExGdata.shape[1] / (ExGdata[0][-1] - ExGdata[0][0])

    if s_rate < 300:
        s_rate = 250
    elif s_rate < 600:
        s_rate = 500
    else: 
        s_rate = 1000

    return(s_rate)


def in_ln_freq():
    """
    Asks the user for the line frequency.
    """
    ln_freq = int(input("Input the frequency of the line noise:\n"))
    return(ln_freq)
