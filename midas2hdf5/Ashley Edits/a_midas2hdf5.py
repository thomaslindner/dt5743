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
# group/dataset
# event #/bin of data

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

    bank_names = ", ".join(b.name for b in event.banks.values())
    print("Event # %s of type ID %s contains banks %s" % (event.header.serial_number,
                                                          event.header.event_id, bank_names))
    i=0
    for bank_name, bank in event.banks.items():
        # Create a data set (numpy array)
        # we will then fill this array using the decoder functiojn
        bank_array=a_TDT743_decoder.a_TDT743_Decoder(bank.data, bank_name) # a_TDT743_decoder decodes data and returns a np array
        dset=grp.create_dataset(bank_name, bank_array.shape, data=bank_array)

        # add relevant metadata (attributes)
        dset.attrs["temp"]=getTemp() #develop functions
        dest.attrs["time stamp"]=datetime.datetime.now() 
        dset.attrs["laser settings"]=getLaser()
        dset.attrs["name"]=bank_name
        
        if i==0:
            i=1
            print("The first entry in bank %s is %x length: %i %s" % (bank_name, bank.data[0],len(bank.data),
                                                                          type(bank.data[0]).__name__))


    event = mfile.read_next_event()

f_hdf5.close()
