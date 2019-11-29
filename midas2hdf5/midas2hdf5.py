#!/usr/bin/env python
# midas to hdf5 converter program
# Thomas Lindner
# Dec 2019
#
import sys
sys.path.append("/home/lindner/packages/midas/python")
#import midas
import midas.file_reader

# Open our file
mfile = midas.file_reader.MidasFile("/daq/daqstore/mpmttest/data/run00027sub000.mid")

event = mfile.read_next_event()

# We can simply iterate over all events in the file
#for event in mfile.read:

while event:
    bank_names = ", ".join(b.name for b in event.banks.values())
    print("Event # %s of type ID %s contains banks %s" % (event.header.serial_number, event.header.event_id, bank_names))
    
    for bank_name, bank in event.banks.items():
        if len(bank.data):
            print("    The first entry in bank %s is %x length: %i %s" % (bank_name, bank.data[0],len(bank.data),
                                                                          type(bank.data[0]).__name__))
        if len(bank.data) > 10:
            print("%x %x %x %x %x %x" % (bank.data[2],bank.data[3],bank.data[4],bank.data[5],bank.data[6],bank.data[7]))
    
    event = mfile.read_next_event()
