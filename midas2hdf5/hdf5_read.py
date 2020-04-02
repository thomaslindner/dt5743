# hdf5 file reader for mpmt test stand digitizer data
# Ashley Ferreira
# March 2020

import sys
import numpy as np
import h5py
from datetime import date, datetime

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt


class hdf5_read:
    '''
    after you call a_midas2hdf5.py to save MIDAS data
    reads hdf5 file created by a_midas2hdf5.py and interprets digitizer data
    '''
    def __init__(self, hdf5_file_name):
        self.file_name=hdf5_file_name
        #self.bank_array=#you need to open groups, you need to decide on structure
        #self.monitor_pmt=data_array[0]
        #self.individual_pmt=data_array[1]
        #loop to get vals before close, bring reading part up here

    def min_vals_histo(self):
        '''
        makes historgram of pulses
        '''
        hdf5_file=h5py.File(''.join([self.file_name, '.hdf5']), 'r') # you may specify file driver
        min_pulses=[]

        #for group_name in self.hdf5_file:
        #    for data_set in group_name:
        #        min_pulses.append(min(data_set[0])) #are the numbers pure y vals?

        keys=hdf5_file.keys()
        groups=[]
        for key in keys:
            groups.append(hdf5_file[key])

        dataset_keys=[]
        for group in groups:
            for data_set_name in group.keys():
                if data_set_name=="ch0":
                    data_set=group[data_set_name].value
                    min_pulses.append(np.min(data_set))

        #print(min_pulses)#lots more noise and round numbers than usual?
        #change to pick bin numbers automatically

        hdf5_file.close()
        plt.hist(min_pulses, bin_num)#directly input bin num to get rid of the error
        plt.yscale('log')
        plt.xlabel('Waveform Minimum Value (ADC)')
        plt.ylabel('Frequency')
        plt.title(''.join([self.file_name,'_histogram']))
        plt.savefig(self.file_name)

    def temp_vs_min(self,title):
        '''
        plots temperature of 5 sensors versus pmt data

        hdf5_file=h5py.File(''.join([self.file_name, '.hdf5']), 'r')
        min_pulses=[]

        temp1=[]
        temp2=[]
        temp3=[]
        temp4=[]
        temp5=[]

        keys=hdf5_file.keys()
        groups=[]
        for key in keys:
            groups.append(hdf5_file[key])

        dataset_keys=[]
        for group in groups:
            for data_set_name in group.keys():
                if data_set_name=="ch0":
                    data_set=group[data_set_name].value
                    min_pulses.append(np.min(data_set))
                    #read in temperature vals
                    all_temp=data_set["temp"]
                    temp1.append(all_temp[0])
                    temp2.append(all_temp[1])
                    temp3.append(all_temp[2])
                    temp4.append(all_temp[3])
                    temp5.append(all_temp[4])

        hdf5_file.close()
        plt.plot(min_pulses, temp1, label="Sensor 1")
        plt.plot(min_pulses, temp2, label="Sensor 2")
        plt.plot(min_pulses, temp3, label="Sensor 3")
        plt.plot(min_pulses, temp4, label="Sensor 4")
        plt.plot(min_pulses, temp5, label="Sensor 5")
        plt.legend(loc='best')
        plt.xlabel('Temperature Sensor Reading (Deg)')
        plt.ylabel('Waveform Minimum Value (ADC)')
        plt.title('Min PMT Pulse Val vs. Temp for ',title)
        plt.savefig(title)#this won't change but try it to see bugs
        '''
        return None


    def full_scan(self):
        '''
        creates a heat map of detection efficiency for every
        point in MIDAS test stand scan
        '''
        hdf5_file=h5py.File(''.join([self.file_name, '.hdf5']), 'r')
        min_pulses=[] # check if min pulse is bigger than histo val

        keys=hdf5_file.keys()
        groups=[]
        for key in keys:
            groups.append(hdf5_file[key])

        dataset_keys=[]
        scan_vals=[]
        x_pos=[]
        y_pos=[]
        old_position=-1
        colletive=[]
        temp_lst=[]
        for group in groups:
            for data_set_name in group.keys():
                if data_set_name=="ch0":
                    data_set=group[data_set_name].value
                    min_pulses.append(np.min(data_set))

                    #read in SCAN vals
                    position=data_set["position"]
                    scan_vals.append(position)
                    index=position[1]
                    x_pos.append(index//10)
                    y_pos.append(index%10)

                    if positon == old_position:
                        temp_lst.append(np.min(data_set))

                    else:
                        collective.append([old_position,temp_lst])
                        temp_lst=[]
                        temp_lst.append(np.min(data_set))

                    position=old_position

# non repeating list for pos, [0] makes xlist, [1] makes y list
# do you need to make non repeating? yeah to figure out how many at each positon
# just figure out how many also
        #pos_list=list(dict.fromkeys(scan_vals))

        # calculate detection efficiency for each scan point
#make deff a list?
        #filter out repeat positons?
        #for pos in pos_list:
            #pulses=

#easiest way to do the bottom part is have an dictonary with pos and then vals?
#make a list of min pulses for each scan spot
        d_eff_list=[]
        for i in range(len(collective)):
            loc=collective[i][0]#or is it the other way around?
            pulse_list=collective[i][1]
            hits=0
            numof_pulses=len(pulse_list)
            for pulse in pulse_list:
                if min_pulses[i]>2345: #make this dynamic later on
                    hits+=1
            d_eff=hits/numof_pulses #per event!
            d_eff_list.append(d_eff)


        #for pos in pos_list:
        #    while scan_vals[i]==scan_vals[i-1]:
        #        i+=1
        #these numbers need to be per event
            #    numof_pulses=len(min_pulses)
            #    hits=0
            #    for i in range(numof_pulses-1):#not working rn
            #        if min_pulses[i]>2345: #make this dynamic later on
            #            hits+=1

            #    d_eff=hits/numof_pulses #per event!
            #d_eff_list.append(d_eff)


        # then give one point and devide by number of events at that point in the scan
        # you need to add a part of the decode which has the scan values?

        #print(min_pulses)#lots more noise and round numbers than usual?
        #change to pick bin numbers automatically

        hdf5_file.close()

        a=np.array(x_pos,y_pos,d_eff_list) #maybe do store scan point only once?
        plt.imshow(a, cmap='hot', interpolation='nearest')
        plt.colorbar()
        #plt.imshow()#directly input bin num to get rid of the error

        plt.xlabel('X positon [m]')
        plt.ylabel('Y positon [m]')
        plt.title(''.join([self.file_name,'detection efficency']))
        plt.savefig(self.file_name)




writename=sys.argv[1]
#plot_title=sys.argv[2]
#bins=sys.argv[3]

test=hdf5_read("".join([writename,"ScanEvents"]))
# program to have it take this from sys once this is working
# test this with just basics working for now
test.min_vals_histo()
#test.temp_vs_min(plot_title)
