"""An example code for data acquisition from Explore device"""

import time
import explorepy
from explorepy.settings_manager import SettingsManager
from explorepy.stream_processor import TOPICS
from explorepy import filters
import argparse
import numpy as np
from ln_removal import clean_ln_ch
from filtering import lp_filt_ch
from wav_thresholding import wav_thresholding_ch
import csv

# Constants
LN_FREQ = 50
S_RATE = 250
EXG_DATA_BUFFER_SIZE = 500

# Global variables
exg_data_in = np.array([])
filt_bpf = None
filt_nf = None

def noise_removal(packet):
    """Process ExG packets."""
    """For demonstration this method processes ExG packets to remove noise and apply filtering from all channels, then save to CSV."""
    global exg_data_in
    exg_packet = filt_nf.apply(filt_bpf.apply(packet))
    t_stamp, exg_data = exg_packet.get_data()

    if exg_data_in.size == 0:
        exg_data_in = exg_data
    else:
        exg_data_in = np.concatenate((exg_data_in, exg_data), axis=1)

    if exg_data_in.shape[1] > EXG_DATA_BUFFER_SIZE:
        exg_lnrm = clean_ln_ch(exg_data_in, LN_FREQ, S_RATE)
        exg_lpf = lp_filt_ch(exg_lnrm, S_RATE)
        exg_wav_thd = wav_thresholding_ch(exg_lpf, S_RATE)
        print(exg_data_in, "---", exg_wav_thd)

        # Write filtered data to CSV
        csv_filename = 'filtered_exg_data.csv'
        with open(csv_filename, 'a', newline='') as f:
            writer = csv.writer(f)
            if f.tell() == 0:
                headers = ["TimeStamp"] + [f"Ch{i+1}" for i in range(exg_wav_thd.shape[0])]
                writer.writerow(headers)

            t_samples = [t_stamp + (i / S_RATE) for i in range(exg_wav_thd.shape[1])]        
            for i in range(exg_wav_thd.shape[1]):
                row = [f"{t_samples[i]:.4f}"] + [f"{val:.2f}" for val in exg_wav_thd[:, i]]
                writer.writerow(row)

        # Re-initialize holding array for the next batch
        exg_data_in = np.empty((exg_data.shape[0], 0))

def my_orn_function(packet):
    """Process orientation packets."""
    timestamp, orn_data = packet.get_data()
    # Add your code here to process orientation data

def main():
    """Main function to set up device connection and data processing."""
    global filt_bpf, filt_nf
    parser = argparse.ArgumentParser(description="Example code for data acquisition")
    parser.add_argument("-n", "--name", dest="name", type=str, required=True, help="Name of the device.")
    args = parser.parse_args()

    # Initialize the Explore device - connect to the device
    exp_device = explorepy.Explore()
    exp_device.connect(device_name=args.name)

    # Get the number of channels from the device
    channel_count = SettingsManager(args.name).get_channel_count()

    # Initialize the filters
    filt_bpf = filters.ExGFilter(cutoff_freq=[.5, 60], filter_type='bandpass', s_rate=S_RATE, n_chan=channel_count)
    filt_nf = filters.ExGFilter(cutoff_freq=50, filter_type='notch', s_rate=S_RATE, n_chan=channel_count)

    # Subscribe "your function" to the raw ExG and orientation topics
    exp_device.stream_processor.subscribe(callback=noise_removal, topic=TOPICS.raw_ExG)
    exp_device.stream_processor.subscribe(callback=my_orn_function, topic=TOPICS.raw_orn)
    
    try:     
        while True:
            time.sleep(.5)
    except KeyboardInterrupt:
        return

if __name__ == "__main__":
    main()