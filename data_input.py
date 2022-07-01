import numpy as np
import os.path
import matplotlib.pyplot as plt

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
        plt.rc('font', size = SMALL_SIZE)          # controls default text sizes
        plt.rc('axes', titlesize = SMALL_SIZE)     # fontsize of the axes title
        plt.rc('xtick', labelsize = SMALL_SIZE)    # fontsize of the tick labels
        plt.rc('figure', titlesize = BIGGER_SIZE)  # fontsize of the figure title
        plt.rc('axes', labelsize = MEDIUM_SIZE)    # fontsize of the x and y labels 

        """
        plt.rc('ytick', labelsize = SMALL_SIZE)    # fontsize of the tick labels
        plt.rc('legend', fontsize = SMALL_SIZE)    # legend fontsize
        """
        
        plt.rcParams['figure.figsize'] = [28, 5*self.n_chan]
        plt.rcParams['figure.dpi'] = 100
        
        fig.suptitle('ExG data')
        if (self.n_chan == 1):
            ax.set_ylabel(self.ch_names[0])
            ax.set_yticks([])
            ax.plot(self.ExGdata[0,:], self.ExGdata[1, :])
        else:
            for i in range(0, self.n_chan, 1):
                ax[i].set_ylabel(self.ch_names[i])
                ax[i].set_yticks([])
                ax[i].plot(self.ExGdata[0,:], self.ExGdata[i+1, :])
        

    
    def plot_ExGdata_psd(self):
        """
        Plots the power spectrum density of the ExG data stored in the self.ExGdata numpy array
        """
        for channel in range(1, np.shape(self.ExGdata)[0]):
            plot_psd(self.ExGdata[channel], self.ExGdata[0], self.s_rate, ch_name=self.ch_names[channel-1])

        


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
        pass
    
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


def plot_psd (signal: np.array, t: np.array, s_rate, ch_name):
    """
    Plots the signal along with the power spectrum density of the signal stored in array.
    """
    # Commputing Fourier Transform
    n = len(t)
    dt = 1/s_rate
    fhat = np.fft.fft(signal, n) # computes the fft
    psd = fhat * np.conj(fhat)/n
    freq = (1/(dt*n)) * np.arange(n) # frequency array
    idxs_half = np.arange(1, np.floor(n/2), dtype=np.int32) # first half index

    SMALL_SIZE = 18
    MEDIUM_SIZE = 20
    BIGGER_SIZE = 22
    plt.rc('font', size = SMALL_SIZE)          # controls default text sizes
    plt.rc('axes', titlesize = SMALL_SIZE)     # fontsize of the axes title
    plt.rc('xtick', labelsize = SMALL_SIZE)    # fontsize of the tick labels
    plt.rc('figure', titlesize = BIGGER_SIZE)  # fontsize of the figure title
    plt.rc('axes', labelsize = MEDIUM_SIZE)    # fontsize of the x and y labels 

    fig, ax = plt.subplots(2,1)
    plt.rcParams['figure.figsize'] = [28, 10]

    ax[0].plot(t, signal, color='b', lw=0.5, label='Signal '+ch_name)
    ax[0].set_ylim([signal.min(), signal.max()])
    ax[0].set_xlabel('Time')
    ax[0].legend()

    ax[1].plot(freq[idxs_half], np.abs(psd[idxs_half]), color='b', lw=1, label='PSD '+ch_name)
    ax[1].set_xlabel('Frequencies in Hz')
    ax[1].set_ylabel('Amplitude')
    ax[1].legend()


