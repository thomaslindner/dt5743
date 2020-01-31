#!/usr/bin/env python
# midas to hdf5 converter program
# Thomas Lindner
# Dec 2019
#
import sys
sys.path.append("/Users/lindner/packages/midas/python")
#import midas
import midas.file_reader

# Open our file
mfile = midas.file_reader.MidasFile("/Users/lindner/sample_data/mpmt/run00028sub000.mid.gz")

event = mfile.read_next_event()

# We can simply iterate over all events in the file
#for event in mfile.read:

while event:
    bank_names = ", ".join(b.name for b in event.banks.values())
    print("Event # %s of type ID %s contains banks %s" % (event.header.serial_number,
                                                          event.header.event_id, bank_names))
    
    for bank_name, bank in event.banks.items():
        if len(bank.data):
            print("    The first entry in bank %s is %x length: %i %s" % (bank_name, bank.data[0],len(bank.data),
                                                                          type(bank.data[0]).__name__))


            # Decode DT5743 bank (move this to separate python class eventually
        if bank_name == "43FS":

            grp_mask = (bank.data[3] & 0xff);
            number_groups = 2  # do this calculation correctly            
            num_sample_per_group = (len(bank.data) - 6)/ number_groups
            

            print("grp mask: %x sample_per_group %i " % (grp_mask,num_sample_per_group))
            
            print("%x %x %x %x %x %x" % (bank.data[2],bank.data[3],bank.data[4],bank.data[5],
                                         bank.data[6],bank.data[7]))


        
    event = mfile.read_next_event()
