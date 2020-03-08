# hdf5 file reader for mpmt test stand digitizer data
# Ashley Ferreira
# March 2020


import numpy as np
import h5py

import matplotlib.pyplot as plt


class hdf5_read:
    '''
    reads hdf5 file created by a_midas2hdf5.py and interprets digitizer data
    '''
    def __init__(self, hdf5_file_name):
        self.file_name=hdf5_file_name
        #self.bank_array=#you need to open groups, you need to decide on structure
        #self.monitor_pmt=data_array[0]#you need to put this into other code
        #`self.individual_pmt=data_array[1]
        #loop to get vals before close

    def min_vals_histo(bins):
        '''
        makes historgram of dark pulses

        this is a rough thing
        def return_name(name):
            print(name)
            return name
            #this is one way of iterating, but it goes through all trees
        groups.visit(return_name)
        '''
        hdf5_file=h5py.File(''.join(self.file_name, '.hdf5'), 'r') # you may specify file driver
        min_pulses=[]
        #the file is already well oragnized iterate through to get mins in dset for indic pmt
        for group_name in self.hdf5_file:
            for data_Set in group_name:
                min_pulses.append(min(data_set[1])) #are the numbers pure y vals?

        self.hdf5_file.close()

        plt.hist(min_pulses, bins)
        plt.show()

        #return min_pulses

    def temp_vs_min():
        '''
        plots temperature versus pmt data
        '''
        # get sc info into varibale and then into attrs and now retrieve


test=hdf5_read("".join([str(date.today()),"ScanEvents"]))
#program to have it take this from sys (cmd) once this is working
# test this with just basics working for now
