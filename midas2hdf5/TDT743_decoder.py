# decoder for TDT743 digitizer
# Thomas Lindner
# Dec 2019
#
# Edits made by Ashley Ferreira, Feb 2020

import numpy as np


class TDT743_decoder:
    '''
    used in a_midas2hdf5.py to convert from MIDAS format to
    key information needed to write to hdf5 file
    '''
    def __init__(self, all_data, bank_name):
        self.data=all_data
        self.name=bank_name


    def decoder(self):
        '''
        decodes MIDAS data
        '''
        important_bank=False
        decoded_arr=[]

        #if self.data[0] != 0xa0000000:
        #    print("First word has wrong identifier; first word = 0x", self.data[0])
        #    return important_bank, None, None, None, None, None

        # Decode DT5743 bank
        if self.name == "43FS":
            important_bank=True

            # which one is the correct way? cpp just uses GetChMask()
            # grp_mask = (self.data[3] & 0xff)
            # group_mask = (self.data[3] & 0xff) + ((self.data[4] & 0xff000000) >> 16)

            group_mask=3#int(str(self.data[3]),2)

            number_groups = 0
            msk_str=str(self.data[3])
            for i in range(len(msk_str)):
                if msk_str[i]=="1":
                    number_groups+=1

            num_sample_per_group = (len(self.data) - 6)/ number_groups

            #print("grp mask: %x sample_per_group %i " % (group_mask,num_sample_per_group))

            #print("%x %x %x %x %x %x" % (self.data[2],self.data[3],self.data[4],self.data[5],
                                         #self.data[6],self.data[7]))


            #if group_mask == 3: # expand/generalize this later, once you start using more inputs
                #print("group_mask = 0x3, this means group 0 and 1 are participating (channel 0 and 1 are taking input)")

            # get samples for first and second channel
            samples_chan0 = []
            samples_chan1 = []
            for i in range(0, num_sample_per_group-1):
                if i % 17 != 0:  # skip bogus data in every 17th sample.
                    samples_chan0.append((self.data[6+i] & 0xfff))
                    samples_chan1.append(((self.data[6+i] & 0xfff000) >> 12))
            #print("Channel 0 samples:", samples_chan0)
            #print("Channel 1 samples:", samples_chan1)

            #decoded_arr.append(samples_chan0)#samples_chan1])
            #decoded_arr=np.array(decoded_arr).astype(np.float)

            ch0_arr=np.array(samples_chan0)#.astype(np.float)
            ch1_arr=np.array(samples_chan1)#.astype(np.float)

            return important_bank, ch0_arr, ch1_arr, number_groups, num_sample_per_group, group_mask

        # will return this if bank_name=/="43FS"
        return important_bank, None, None, None, None, None
