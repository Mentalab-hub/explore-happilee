from data_input import ExG_data
import numpy as np

def select(ExG_in: ExG_data):
    """
    The user selects which channels from the ExGdata that will be processed
    'all'   = all channels in the data will be processed
    'coi'   = select channels will be processed
              The user then inputs the channel names that are selected
    Args:
        ExG_in  = ExG_data containing information: file_format, ExGdata, n_chan, ch_names, s_rate
    Returns:
        ExG_sel = ExG_data containing the selected channels and their recorded data from ExG_in
    """
    n_chan_sel = 0
    ch_selected = []
    ExGdata_ch_sel = []

    # Save timestamps into selected data:
    ExGdata_ch_sel.append(ExG_in.ExGdata[0, :])
    ch_name_sel = 'not_done'
    

    selection = input("Type:\n'all': to process all channels in the ExG data\n'coi': to process selected channels")

    if selection == 'coi':
        while (n_chan_sel < ExG_in.n_chan) and (ch_name_sel != 'done'):
            ch_name_sel = input("Enter the name of the selected channel.\nEnter 'done' if all channels have been selected.\n")
            if (ch_name_sel in ExG_in.ch_names) and (ch_name_sel not in ch_selected):
                ch_selected.append(ch_name_sel)
                n_chan_sel += 1

        for ch_name in ch_selected:
            tmp = ExG_in.ExGdata[ExG_in.ch_names.index(ch_name), :]
            ExGdata_ch_sel.append(tmp)
        ExGdata_ch_sel = np.array(ExGdata_ch_sel)
    
    else: # selection == 'all'
        ExGdata_ch_sel = ExG_in.ExGdata
        n_chan_sel = ExG_in.n_chan
        ch_selected = ExG_in.ch_names
    
    ExG_sel = ExG_data(ExG_in.file_format, ExGdata_ch_sel, n_chan_sel, ch_selected, ExG_in.s_rate, ExG_in.ln_freq)

    return ExG_sel
