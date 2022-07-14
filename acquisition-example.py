"""An example code for data acquisition from Explore device"""

import time
import explorepy
from explorepy.stream_processor import TOPICS
from explorepy import filters
import argparse
import numpy as np
from ln_removal import clean_ln_ch
from filtering import lp_filt_ch
from wav_thresholding import wav_thresholding_ch

ln_freq = 50
s_rate = 250
exg_data_in = np.array([])
filt_bpf = filters.ExGFilter(cutoff_freq=[.5, 60], filter_type='bandpass', s_rate=s_rate, n_chan=4)
filt_nf = filters.ExGFilter(cutoff_freq=50, filter_type='notch', s_rate=s_rate, n_chan=4)

def noise_removal(packet):
    #############
    # YOUR CODE #
    #############    
    exg_packet = filt_nf.apply(filt_bpf.apply(packet))
    # A function that receives ExG packets and does some operations on the data
    t_vector, exg_data = exg_packet.get_data()

    global exg_data_in
    exg_data_in = np.append(exg_data_in, exg_data[0])
    
    if (len(exg_data_in) > 500):
        # 1. Line noise removal
        exg_lnrm = clean_ln_ch(exg_data_in, ln_freq, s_rate)
        # 2. Filtering
        exg_lpf = lp_filt_ch(exg_lnrm, s_rate)
        # 3. Wavelet thresholding
        exg_wav_thd = wav_thresholding_ch(exg_lpf, s_rate)
        
        print(exg_data_in, "---", exg_wav_thd)
        
        exg_data_in = np.array([])


def my_orn_function(packet):
    """A function that receives orientation packets and does some operations on the data"""
    timestamp, orn_data = packet.get_data()
    # print("Received an orientation packet: ", orn_data)
    #############
    # YOUR CODE #
    #############


def main():
    parser = argparse.ArgumentParser(description="Example code for data acquisition")
    parser.add_argument("-n", "--name", dest="name", type=str, help="Name of the device.")
    args = parser.parse_args()

    # Create an Explore object
    exp_device = explorepy.Explore()

    # Connect to the Explore device using device bluetooth name or mac address
    exp_device.connect(device_name=args.name)

    # Subscribe your function to the stream publisher
    exp_device.stream_processor.subscribe(callback=noise_removal, topic=TOPICS.raw_ExG)
    exp_device.stream_processor.subscribe(callback=my_orn_function, topic=TOPICS.raw_orn)
    
    try:     
        while True:
            time.sleep(.5)
    except KeyboardInterrupt:
        return


if __name__ == "__main__":
    main()