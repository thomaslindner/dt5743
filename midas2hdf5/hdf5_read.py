# hdf5 file reader for mpmt test stand digitizer data
# Ashley Ferreira
# March 2020

import sys
import numpy as np
import h5py
from datetime import date, datetime
import matplotlib.pyplot as plt


class hdf5_read:
    '''
    reads hdf5 file created by a_midas2hdf5.py and interprets digitizer data
    '''
    def __init__(self, hdf5_file_name):
        self.file_name=hdf5_file_name
        #self.bank_array=#you need to open groups, you need to decide on structure
        #self.monitor_pmt=data_array[0]
        #self.individual_pmt=data_array[1]
        #loop to get vals before close, bring reading part up here

    def min_vals_histo(self,bins,title):
        '''
        makes historgram of pulses
        '''
        hdf5_file=h5py.File(''.join([self.file_name, '.hdf5']), 'r') # you may specify file driver
        min_pulses=[]

        #for group_name in self.hdf5_file:
        #    for data_set in group_name:
        #        min_pulses.append(min(data_set[0])) #are the numbers pure y vals?

        keys=hdf5_file.keys()
        groups=[]
        for key in keys:
            groups.append(hdf5_file[key])

        dataset_keys=[]
        for group in groups:
            for data_set_name in group.keys():
                if data_set_name=="ch0":
                    data_set=group[data_set_name].value
                    min_pulses.append(np.min(data_set))

        #print(min_pulses)#lots more noise and round numbers than usual?


        hdf5_file.close()
        plt.hist(min_pulses, bins)
        plt.yscale('log')
        plt.xlabel('Waveform Minimum Value (ADC)')
        plt.ylabel('Frequency')
        plt.title(title)
        plt.savefig(title)

    def temp_vs_min(self):
        '''
        plots temperature versus pmt data
        '''
        hdf5_file=h5py.File(''.join([self.file_name, '.hdf5']), 'r')
        min_pulses=[] #clarify exactly what is the x axis

        #for group_name in self.hdf5_file:
        #    for data_set in group_name:
        #        min_pulses.append(min(data_set[0])) #are the numbers pure y vals?

        keys=hdf5_file.keys()
        groups=[]
        for key in keys:
            groups.append(hdf5_file[key])

        dataset_keys=[]
        for group in groups:
            for data_set_name in group.keys():
                if data_set_name=="ch0":
                    data_set=group[data_set_name].value
                    min_pulses.append(np.min(data_set))



writename=sys.argv[1]
plot_title=sys.argv[2]
bins=sys.argv[3]

test=hdf5_read("".join([writename,"ScanEvents"]))
# program to have it take this from sys once this is working
# test this with just basics working for now
test.min_vals_histo(bins,plot_title)
