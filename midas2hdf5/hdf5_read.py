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
        plt.hist(min_pulses, 100)#directly input bin num to get rid of the error
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
        min_pulses=[]

        keys=hdf5_file.keys()
        groups=[]
        for key in keys:
            groups.append(hdf5_file[key])

        dataset_keys=[]
        scan_vals=[]
        x_pos=[]
        y_pos=[]
        old_pos=0
        p=0
        #pos=0
        collective=[]
        temp_lst=[]
        for group in groups:
            for data_set_name in group.keys():
                if data_set_name=="ch0":
                    data_set=group[data_set_name].value
                    dset=group[data_set_name]
                    min_pulses.append(np.min(data_set)) #up until here works for sure

                    #read in SCAN vals
                    k=list(dset.attrs.keys())
                    v=list(dset.attrs.values())
                    #print(k)
                    #print(v)
                    ind=k.index("position")
                    p=v[ind]
                    #pos+=0.5
                    #pos=dset.attrs["position"] #ISSUE retriving pos
                    #print("pos:",pos)
                    scan_vals.append(p)

        scan_vals=list(map(float, scan_vals))
        scan_vals.sort()

        for pos in scan_vals:
            if pos == old_pos: #its saying they arent equal but all -1?
                temp_lst.append(np.min(data_set))

            else:
                x_pos.append(old_pos) #maybe adjust x and y later?
                y_pos.append(old_pos)
                #p+=1
                #x_pos.append(p)
                #y_pos.append(p)

                collective.append([old_pos,temp_lst])
                temp_lst=[]
                temp_lst.append(np.min(data_set))

            old_pos=pos

        x_pos=list(map(lambda x: x//10, x_pos))
        y_pos=list(map(lambda y: y%10, y_pos))

        d_eff_list=[]
        #print(collective,"was collective")
        for i in range(len(collective)-1):
            #print("collective item:",collective[i])
            loc=collective[i+1][0]#or is it the other way around? you just want the 1 and zero but you need a list of the collectives?
            pulse_list=collective[i+1][1]
            hits=0
            numof_pulses=len(pulse_list) #this is giving zero?
            #print(numof_pulses,"shouldnt be zero, but code thinks it is")
            for pulse in pulse_list: #you arent iterating through the pulses here
                #print("pulse",pulse)
                if pulse<2345: #make this dynamic later on
                    hits+=1
            d_eff=hits/numof_pulses #per event!
            d_eff_list.append(d_eff)

        d_eff_list.append(0)
#collective item prints wrong but the individual parts are right
        hdf5_file.close()

        arr = []

        print(x_pos)
        print("------------------------------------------------------------------------------")
        print(y_pos)

        for i in range(len(x_pos)):
            arr.append([x_pos[i],y_pos[i],d_eff_list[i]])

        X = np.array(arr, dtype=np.float64)
        #a=np.array(x_pos,y_pos,d_eff_list) #maybe do store scan point only once?
        #X = [x_pos,y_pos,d_eff_list]
        plt.imshow(np.real(X), cmap='hot', interpolation='nearest')
        plt.colorbar()
        #plt.imshow()#directly input bin num to get rid of the error
        plt.xlabel('X positon [m]')
        plt.ylabel('Y positon [m]')
        plt.title(''.join([self.file_name,'detection efficency']))
        plt.savefig(self.file_name)

        plt.plot(x_pos, y_pos)
        plt.savefig("test plot")

        #print(scan_vals)

#sort scan vals


writename=sys.argv[1]
#plot_title=sys.argv[2]
#bins=sys.argv[3]

test=hdf5_read("".join([writename,"ScanEvents"]))
#test.min_vals_histo()
test.full_scan()
#test.temp_vs_min(plot_title)
