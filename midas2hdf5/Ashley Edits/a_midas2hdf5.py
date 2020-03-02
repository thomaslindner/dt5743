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

import sys
import numpy as np
import h5py
import midas.file_reader
import a_TDT743_decoder
import datetime

#sys.path.append("/Users/lindner/packages/midas/python")
sys.path.append("/home/mpmttest/packages/midas/python")

filename = sys.argv[1]

# Open our file
mfile = midas.file_reader.MidasFile(filename)

event = mfile.read_next_event()

# Create an .hdf5 file, and open it for writting
f_hdf5=h5py.File("".join(date.today(),"ScanEvents.hdf5"),"w")

# We can simply iterate over all events in the file
while event:
    # Create groups to store information of each event
    grp=f_hdf5.create_group("Event #",event.header.serial_number)
    grp.attrs["id"]=event.header.event_id
    grp.attrs["bank names"]=bank_names
    grp.attrs["number of banks"]=len(bank_names)
    grp.attrs["event time tag"]=0 #take from header

    bank_names = ", ".join(b.name for b in event.banks.values())
    print("Event # %s of type ID %s contains banks %s" % (event.header.serial_number,
                                                          event.header.event_id, bank_names))
    hit_first=False
    for bank_name, bank in event.banks.items():
        # print first entry in the bank info
        if hit_first==False:
            hit_first=True
            print("The first entry in bank %s is %x length: %i %s" % (bank_name, bank.data[0],len(bank.data),
                                                                          type(bank.data[0]).__name__))

        # a_TDT743_decoder decodes data and returns a np array, along with other useful info
        # bank_array[0] = pmt analogue data, bank_array[1] = monitor pmt
        important_bank, bank_array, number_groups, num_sample_per_group, group_mask =a_TDT743_decoder.a_TDT743_Decoder(bank.data, bank_name)

        # Create a data set (numpy array) for all important banks
        # we will then fill this array using the decoder function variables
        if important_bank==True:
            dset=grp.create_dataset(bank_name, bank_array.shape, data=bank_array)
            # add relevant metadata (attributes)
            dset.attrs["temp"]=getTemp()
            dest.attrs["time stamp"]=datetime.datetime.now() # change to midas
            dset.attrs["laser settings"]=getLaser()
            dset.attrs["name"]=bank_name
            dset.attrs["number of groups"]=number_groups # will help with slicing the array
            dset.attrs["samples per group"]=num_sample_per_group # will help with slicing the array
            dset.attrs["group mask"]=group_mask


    event = mfile.read_next_event()

f_hdf5.close()