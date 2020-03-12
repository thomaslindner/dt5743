#!/usr/bin/env python
# midas to hdf5 converter program
# Thomas Lindner
# Dec 2019
#
# Edits made by Ashley Ferreira, Feb 2020
# changes made: decoder in new class, now program
# writes to hdf5 file as it reads from midas
#
# Writes to .hdf5 in the following way:
# group=event / dataset=bank
# event #/bin of data


# still left to do:
# set SL data to global variables to store in metadata
# add temperature, motor settings, [etc...] as metadata
# update time using MIDAS and event time tag
# store channels in different dataset/array format?

# print statements commented out for now so code goes faster in cmd

import sys
import numpy as np
import h5py

sys.path.append("/home/mpmttest/online/dt5743/midas2hdf5")
import a_TDT743_decoder
from datetime import date, datetime

#sys.path.append("/Users/lindner/packages/midas/python")
sys.path.append("/home/mpmttest/packages/midas/python")
import midas.file_reader

filename = sys.argv[1]
writename = sys.argv[2]

# Open our file
mfile = midas.file_reader.MidasFile(filename)

event = mfile.read_next_event()

# Create an .hdf5 file, and open it for writting
#f_hdf5=h5py.File("".join([str(datetime.now()),"ScanEvents.hdf5"]),"w")
f_hdf5=h5py.File("".join([writename,"ScanEvents.hdf5"]),"w")

latest_temp=0
counter=0
# We can simply iterate over all events in the file
while event:
    # Create groups to store information of each event
    #grp=f_hdf5.create_group("".join(["Event #",str(event.header.serial_number)]))
    counter+=1
    grp=f_hdf5.create_group("".join(["Event #",str(counter)])) #temporary way

    bank_names = ", ".join(b.name for b in event.banks.values())
    #print("Event # %s of type ID %s contains banks %s" % (event.header.serial_number,event.header.event_id, bank_names))

    # add relevant metadata to group (attributes)
    grp.attrs["id"]=event.header.event_id
    grp.attrs["bank names"]=bank_names
    grp.attrs["number of banks"]=len(bank_names)
    grp.attrs["event time tag"]=0 #take from header

    hit_first=False
    for bank_name, bank in event.banks.items():
        # print first entry in the bank info
        if hit_first==False:
            hit_first=True
            #print("The first entry in bank %s is %x length: %i %s" % (bank_name, bank.data[0],len(bank.data),type(bank.data[0]).__name__))

        # case statements for the different bank names?

        if bank_name=="TEMP":#you will have had to create the dataset fist, but temp would come fitst?
            lastest_temp=bank.data #ask what is in this bank format wise?

        # Create a data set (numpy array) for all important banks
        # we will then fill this array using the decoder function variables
        if bank_name=="43FS":
        #if important_bank==True:
            # a_TDT743_decoder decodes data and returns a np array, along with other useful info
            # bank_array[1] = pmt analogue data, bank_array[0] = monitor pmt (CURRENTLY JUST PMT at ch0 and seperate arrays)
            file_todecode=a_TDT743_decoder.a_TDT743_decoder(bank.data, bank_name)
            important_bank, ch0_arr, ch1_arr, number_groups, num_sample_per_group, group_mask=file_todecode.decoder()
            dset=grp.create_dataset("ch0", ch0_arr.shape, data=ch0_arr)#specificy names based on decoders response
            dset=grp.create_dataset("ch1", ch1_arr.shape, data=ch1_arr)
            #dset=grp.create_dataset(bank_name, bank_array.shape, data=bank_array)

            # add relevant metadata to data set (attributes)
            dset.attrs["name"]=bank_name
            dset.attrs["number of groups"]=number_groups # will help with slicing
            dset.attrs["samples per group"]=num_sample_per_group # will help with slicing
            dset.attrs["group mask"]=group_mask
            dset.attrs["temp"]=latest_temp #split into the 5
            #dest.attrs["time stamp"]=datetime.datetime.now() # change to midas
            #dset.attrs["laser settings"]=getLaser()


    event = mfile.read_next_event()

f_hdf5.close()
