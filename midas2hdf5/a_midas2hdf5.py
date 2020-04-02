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


# print statements commented out for now so code goes faster in cmd

import sys
import numpy as np
import h5py

sys.path.append("/home/mpmttest/online/dt5743/midas2hdf5")
import a_TDT743_decoder
from datetime import date, datetime


sys.path.append("/home/mpmttest/packages/midas/python")
import midas.file_reader

# call this python file in cmd as follows:
# python a_midas2hdf5 ~/online/data/run_____sub000.mid.gz "run___"
# fill in the blanks with run number from MIDAS
filename = sys.argv[1]
writename = sys.argv[2]

# Open MIDAS file
mfile = midas.file_reader.MidasFile(filename)

event = mfile.read_next_event()

# Create an .hdf5 file, and open it for writting
f_hdf5=h5py.File("".join([writename,"ScanEvents.hdf5"]),"w")
#f_hdf5=h5py.File("".join([str(datetime.now()),"ScanEvents.hdf5"]),"w")

latest_temp=0 #or a list?
#latest_pos=0 or set it to a list?
counter=0

# Iterate over all events in MIDAS file
# as we read each event, we write it to our .hfd5 file
while event:
    # Create hdf5 groups to store information of each event
    #grp=f_hdf5.create_group("".join(["Event #",str(event.header.serial_number)]))
    counter+=1
    grp=f_hdf5.create_group("".join(["Event #",str(counter)]))

    bank_names = ", ".join(b.name for b in event.banks.values())
    #print("Event # %s of type ID %s contains banks %s" % (event.header.serial_number,event.header.event_id, bank_names))

    # add relevant metadata to hdf5 group (attributes)
    grp.attrs["id"]=event.header.event_id
    grp.attrs["bank names"]=bank_names
    grp.attrs["number of banks"]=len(bank_names)
    grp.attrs["event time tag"]=0 #take from header -> look at midas documentation now

    hit_first=False
    latest_pos=0
    latest_temp=0
    for bank_name, bank in event.banks.items():
        # print first entry in the bank
        if hit_first==False:
            hit_first=True
            print("The first entry in bank %s is %x length: %i %s"
                % (bank_name, bank.data[0],len(bank.data),type(bank.data[0]).__name__))

        if bank_name=="TEMP":
            lastest_temp=bank.data

        if bank_name=="SCAN":
            latest_pos=bank.data
            print(latest_pos)

        #if bank_name=="43SL":


        if bank_name=="43FS":
            file_todecode=a_TDT743_decoder.a_TDT743_decoder(bank.data, bank_name)

            important_bank, ch0_arr, ch1_arr, number_groups, num_sample_per_group, group_mask=file_todecode.decoder()

            dset=grp.create_dataset("ch0", ch0_arr.shape, data=ch0_arr)
            #dset=grp.create_dataset("ch1", ch1_arr.shape, data=ch1_arr)

            # add relevant metadata to data set (attributes)
            dset.attrs["name"]=bank_name
            dset.attrs["number of groups"]=number_groups # will help with slicing
            dset.attrs["samples per group"]=num_sample_per_group # will help with slicing
            dset.attrs["group mask"]=group_mask
            dset.attrs["temp"]=latest_temp
            dest.attrs["position"]=latest_pos #will be a pixilated scan
            #dest.attrs["time stamp"]=datetime.datetime.now() # change to midas
            #dset.attrs["laser settings"]=getLaser()


    event = mfile.read_next_event()

f_hdf5.close()
