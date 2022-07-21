import numpy as np
import matplotlib.pyplot as plt


def subplot(n_rows, n_cols, title, x_axes, y_axes, x_labels, y_labels, plot_labels, plot_colors):
    """
    Args:
        n_rows      : number of rows in the figure
        n_cols      : number of columns in the figure
        title       : figure title
        x_axes      : list of x axes' values
        y_axes      : list of x axes' values
        x_labels    : list of labels for x axis of each subplot
        y_labels    : list of labels for y axis of each subplot
        plot_labels : list of labels for each plot
        plot_colors : list of colors for each plot
    """
    fig, ax = plt.subplots(n_rows, n_cols)
    
    SMALL_SIZE = 20
    MEDIUM_SIZE = 22
    BIGGER_SIZE = 24
    plt.rc('font', size = SMALL_SIZE)          # controls default text sizes
    plt.rc('axes', titlesize = MEDIUM_SIZE)    # fontsize of the axes title
    plt.rc('xtick', labelsize = SMALL_SIZE)    # fontsize of the tick labels
    plt.rc('figure', titlesize = BIGGER_SIZE)  # fontsize of the figure title
    plt.rc('axes', labelsize = MEDIUM_SIZE)    # fontsize of the x and y labels 

    for i in range(0, n_rows*n_cols):
        ax[i].plot(x_axes[i], y_axes[i], color=plot_colors[i], lw=0.5, label=plot_labels[i])
        ax[i].set_ylim([y_axes[i].min(), y_axes[i].max()])
        ax[i].set_xlabel(x_labels[i])
        ax[i].set_ylabel(y_labels[i])
        ax[i].legend()
    plt.suptitle(title)
    plt.show()


def plot_psd (t: np.array, signal: np.array, s_rate, ch_name):
    """
    Plots the signal along with the power spectrum density of the signal stored in array.
    """
    [freq, idxs_half, psd] = compute_fft(t, signal)

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


def compute_fft(t: np.array, signal: np.array):
    n = len(t)
    dt = t[1] - t[0]
    freq = (1/(dt*n)) * np.arange(n)                            # frequency array
    idxs_half = np.arange(1, np.floor(n/2), dtype=np.int32)     # first half index
    fhat = np.fft.fft(signal)                                   # computes the fft
    psd = fhat * np.conj(fhat)/n
    return([freq, idxs_half, psd])