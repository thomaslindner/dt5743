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

#sys.path.append("/Users/lindner/packages/midas/python")
sys.path.append("/home/mpmttest/packages/midas/python")

filename = sys.argv[1]

# Open our file
mfile = midas.file_reader.MidasFile(filename)

event = mfile.read_next_event()

# Create an .hdf5 file, and open it for writting
f_hdf5=h5py.File("testfile1.hdf5","w")

# We can simply iterate over all events in the file
while event:
    # Create a groups to store information of each event
    grp=f_hdf5.create_group("Event #",event.header.serial_number)

    bank_names = ", ".join(b.name for b in event.banks.values())
    print("Event # %s of type ID %s contains banks %s" % (event.header.serial_number,
                                                          event.header.event_id, bank_names))
    i=0
    for bank_name, bank in event.banks.items():
        # Create a data set (numpy array)
        # we will then fill this array using the decoder functiojn
        dset=grp.create_dataset(bank_name, (100,), dtype='i')

        if i==0:
            i=1
            print("The first entry in bank %s is %x length: %i %s" % (bank_name, bank.data[0],len(bank.data),
                                                                          type(bank.data[0]).__name__))

        bank_array=a_TDT743_decoder(bank.data) # a_TDT743_decoder decodes data and returns a np array
        dset=grp.create_dataset(bank_name, (100,), data=bank_array)


    event = mfile.read_next_event()
