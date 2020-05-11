#!/usr/bin/env python
# midas to hdf5 converter program
# Thomas Lindner
# Dec 2019
#
# Edits made by Ashley Ferreira, Feb 2020
#
# Writes to .hdf5 in the following way:
# group=event / dataset=bank


import sys
import numpy as np
import h5py

sys.path.append("/home/mpmttest/online/dt5743/midas2hdf5")
import TDT743_decoder
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

# Create an hdf5 file, and open it for writting
f_hdf5=h5py.File("".join([writename,"ScanEvents.hdf5"]),"w")

# initialize list of temperature sensors data
latest_temp=[]

# initilize list of motor positons
moto_pos=[]

# initialize variables used to test if motors are running
moto_exists=False
moto_hit=False

# initialize scan value
scan_pos=0

counter=0

# Iterate over all events in MIDAS file
# as we read each event, we write it to our hfd5 file
while event:
    # Create hdf5 groups to store information of each event
    counter+=1

    # create group with event number as its name
    grp=f_hdf5.create_group(str(counter))
    #grp=f_hdf5.create_group("".join(["Event #",str(counter)]))

    bank_names = ", ".join(b.name for b in event.banks.values())
    #print("Event # %s of type ID %s contains banks %s" % (event.header.serial_number,event.header.event_id, bank_names))

    # add relevant metadata to hdf5 group (attributes)
    grp.attrs["id"]=event.header.event_id
    grp.attrs["bank names"]=bank_names
    grp.attrs["number of banks"]=len(bank_names)
    grp.attrs["serial number"]=event.header.serial_number
    grp.attrs["event time tag"]=event.header.timestamp # time in seconds since 1.1.1970 00:00:00 UTC

    # tells us if we have already read in the first entry
    hit_first=False

    # interate though the banks
    for bank_name, bank in event.banks.items():
        # print first entry in the bank
        if hit_first==False:
            hit_first=True
            print("The first entry in bank %s is %x length: %i %s"
                % (bank_name, bank.data[0],len(bank.data),type(bank.data[0]).__name__))

        # update temperature list as new sensor data comes in
        if bank_name=="TEMP":
            latest_temp=bank.data

        # update motor position xy values as new motor data comes in
        elif bank_name=="MOTO":
            # if a MOTO bank value hasn't been read in before,
            # initialize the xy motor position to the bank values
            if moto_hit==False:
                moto_pos=[bank.data[0],bank.data[1]]

            # if MOTO bank has been hit before but the motor values
            # are not changing, assume motors are not running
            # (right now, motors aren't running but the MOTO bank returns
            # [1, 0] over and over)
            #
            # if the motor bank values aren't changing, assume the motors
            # are running and store the latest xy positon in moto_pos
            if moto_hit==True:
                if moto_pos!=[bank.data[0],bank.data[1]]:
                    moto_exists=True
                    moto_pos=[bank.data[0],bank.data[1]]

        # update scan value as new scan data comes in
        elif bank_name=="SCAN":
            scan_pos=float(bank.data[1])

        # if the current bank is the digitizer bank then initialize
        # a new data set under this group for the event where you store
        # the digitizer data as an array and the information from previous
        # banks described as metadata attached to the digitizer dataset
        elif bank_name=="43FS":
            # use digitizer decoder program to return important formatted data
            file_todecode=TDT743_decoder.TDT743_decoder(bank.data, bank_name)
            important_bank, ch0_arr, ch1_arr, number_groups, num_sample_per_group, group_mask=file_todecode.decoder()

            # create hdf5 dataset for single PMT
            dset=grp.create_dataset("ch0", ch0_arr.shape, data=ch0_arr)
            #dset=grp.create_dataset("ch1", ch1_arr.shape, data=ch1_arr)

            # attach relevant metadata to data set (attributes)
            dset.attrs["name"]=bank_name
            dset.attrs["number of groups"]=number_groups
            dset.attrs["samples per group"]=num_sample_per_group
            dset.attrs["group mask"]=group_mask
            dset.attrs["temp"]=latest_temp
            dset.attrs["scan position"]=scan_pos

            if moto_exists:
                dset.attrs["motors running"]=True
                dset.attrs["moto position"]=moto_pos
            else:
                dset.attrs["motors running"]=False


    event = mfile.read_next_event()

# close hdf5 file for writting
f_hdf5.close()
