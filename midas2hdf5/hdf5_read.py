# hdf5 file reader for mpmt test stand digitizer data
# includes varius functions for plotting the data
# Ashley Ferreira
# March 2020

import sys
import numpy as np
import h5py

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
#print(plt.colormaps())
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
#use notebook to get list of colors for magma_r and then initialize
#magma_r here


#from matplotlib.colors import LinearSegmentedColormap

#import colormaps as cmaps
#plt.register_cmap(name='viridis', cmap=cmaps.viridis)
#plt.set_cmap(cmaps.viridis)

#plt.register_cmap(name='viridis', cmap=plt.cm.viridis)
#plt.set_cmap(plt.cm.viridis)

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
        with bin number generated automatically
        '''
        hdf5_file=h5py.File(''.join([self.file_name, 'ScanEvents', '.hdf5']), 'r') # you may specify file driver
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

        #print("min pulses",min_pulses)

        hdf5_file.close()
        # do you need the underscore?
        #y_hist, x_hist, patches = plt.hist(min_pulses, bins='auto')
        y_hist, x_hist, patches = plt.hist(min_pulses, bins=100)
        #dk = plt.hist(min_pulses, bins='auto')
        #print(dk)
        plt.yscale('log')
        plt.xlabel('Waveform Minimum Value (ADC)')
        plt.ylabel('Frequency')
        plt.title(''.join([self.file_name,' histogram']))
        plt.savefig(''.join([self.file_name,'_histogram']))

        #return x_hist, y_hist, min_pulses#perhaps make it just return 2 max vals and min pulses?
        #return the pedastal val="" and cutoff of single pe peak and then pulse vals
        #return x_hist, y_hist, min_pulses
        #return x.max(), y.max(), min_pulses
        return y_hist, min_pulses

    def temp_vs_min(self,title):
        '''
        plots temperature of 5 sensors versus pmt data

        hdf5_file=h5py.File(''.join([self.file_name, 'ScanEvents', '.hdf5']), 'r')
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

        def calc_cutoff():
            pedastal=max(y_hist)
            ind=y_hist.index(pedastal)
            pe_peak=y_hist.pop(ind)
            #define local functions for much of this stuff
            #is smaller actually correct here?
            if without_ped>pedastal*0.95: #make this less arbirtrary, curve fit?
                cutoff=(pedastal+without_ped)/2
            else:
                #find new cutoff
                ind=y_hist.index(without_ped)
                pe_peak=y_hist.pop(ind) #loop this?

            calc_cutoff=(pedastal+pe_peak)/2

            return calc_cutoff


        dataset_keys=[]
        #scan_vals=[]
        #old_pos=0
        p=0
        #pos=0


        def position_vals():
            keys=hdf5_file.keys()
            groups=[]
            scan_vals=[]
            for key in keys:
                groups.append(hdf5_file[key])
            for group in groups:
                for data_set_name in group.keys():
                    if data_set_name=="ch0":
                        data_set=group[data_set_name].value
                        dset=group[data_set_name]
                        #min_pulses.append(np.min(data_set))
                        #read in SCAN vals
                        k=list(dset.attrs.keys())
                        v=list(dset.attrs.values())
                        ind=k.index("position")
                        p=v[ind]
                        #pos=dset.attrs["position"]
                        scan_vals.append(p)

            #scan_vals=list(map(float, scan_vals))
            #scan_vals.sort()

            return scan_vals


        def detection_eff():
            i=0
            x_pos=[]
            y_pos=[]
            collective=[]
            temp_lst=[]
            old_pos=0
            for pos in scan_vals:
                if pos == old_pos:
                    temp_lst.append(min_pulses[i])

                else:
                    x_pos.append(old_pos)
                    y_pos.append(old_pos)

                    collective.append([old_pos,temp_lst])
                    temp_lst=[]
                    temp_lst.append(min_pulses[i])

                i+=1
                old_pos=pos

            x_pos=list(map(lambda x: x//10, x_pos))
            y_pos=list(map(lambda y: y%10, y_pos))

            d_eff_list=[]

            for i in range(len(collective)-1):
                loc=collective[i+1][0]
                pulse_list=collective[i+1][1]
                hits=0
                numof_pulses=len(pulse_list)
                for pulse in pulse_list:
                        #if pulse<cutoff:
                    if pulse>2080: #temporary because of 2048 issue
                        #if pulse>cutoff:
                        hits+=1

                    hits1=float(hits)
                    pulses=float(numof_pulses)
                    d_eff=hits1/pulses
                    d_eff_list.append(d_eff)

            d_eff_list.insert(0,0) #temporary

            return d_eff_list, x_pos, y_pos


        def plotting():
            xl=np.linspace(0,10,10)
            yl=np.linspace(0,10,10)
            xl,yl=np.meshgrid(x,y)

            Z=np.resize(d_eff_l,xl.shape)


            #color_map = plt.imshow(x)
            #color_map.set_cmap("Blues_r")
            #plt.colorbar()

            #plt.imshow(Z, cmap=plt.cm.get_cmap(name='magma'), interpolation='nearest', extent=[0,10,0,10]) #make extent dynamic later
            plt.imshow(Z, interpolation='nearest', extent=[0,10,0,10])
            plt.colorbar()
            plt.xlabel('X positon [m]')
            plt.ylabel('Y positon [m]')
            plt.title(''.join([self.file_name,' detection efficency']))
            plt.savefig(''.join([self.file_name,'_detectionEfficency']))


        hdf5_file=h5py.File(''.join([self.file_name,'ScanEvents', '.hdf5']), 'r')
        print("1/4")
        #min_pulses=[] #get this stuff returned from histo?
        y_hist, min_pulses = self.min_vals_histo()#might not need to enter global variable
        #cutoff = calc_cutoff() #stop using local and global names twice
        # move non-functions down
        #scan_vals = position_vals()
        print("2/4")
        scan_vals=position_vals()
        print("3/4")
        d_eff_l, x, y = detection_eff()

        hdf5_file.close()
        print("4/4")
        plotting()

        #arr = []
        #for i in range(len(x_pos)):
            #arr.append([x_pos[i],y_pos[i],d_eff_list[i]])
        #X = np.array(arr, dtype=np.float64)
        #a=np.array(x_pos,y_pos,d_eff_list)
        #X = [x_pos,y_pos,d_eff_list]

    def waveform_display(self,event):
        '''
        displays waveform of specified event #
        '''
        hdf5_file=h5py.File(''.join([self.file_name,'ScanEvents', '.hdf5']), 'r')

        #iterate to get the event and plot it!
        keys=hdf5_file.keys()
        #if "".join(["Event #",str(event)]) in keys:

        groups=[]
        #bank_vals=[]
        for key in keys:
            if "".join(["Event #",str(event)])==key:
                groups.append(hdf5_file[key])
        for group in groups:
            for data_set_name in group.keys():
                if data_set_name=="ch0":
                    data_set=group[data_set_name].value
                    #bank_vals.append(data_set)
            #        dset=group[data_set_name]
                    #min_pulses.append(np.min(data_set))
                    #read in SCAN vals
        hdf5_file.close()

        length=len(data_set)
        avg=sum(data_set)/length
        event_num=event
        standard_dev=np.std(data_set)

        fig, ax = plt.subplots()

        textstr = '\n'.join(["Entries ", str(length), "\nMean ",str(avg),"\nStd Dev",str(standard_dev)])

        props = dict(boxstyle='round', facecolor='white', alpha=0.5)

# place a text box in upper left in axes coords
        ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=14,
        verticalalignment='bottom', bbox=props)

        #what exactly are we plotting?
        #assuming its 0-300ns
        x=np.linspace(0,300,length)
        ax.plot(x, data_set, color='black')
        plt.ylabel('Waveform Minimum Value (ADC)')
        plt.xlabel('Time (ns)')
        plt.title(''.join([self.file_name,' event #', str(event_num),' DT743 Waveform for channel=0']))
        plt.savefig('Waveform Example')
        #show and dont save in the future
        #its not showing it so you might just have to save


fname=sys.argv[1]
#plot_title=sys.argv[2]
#bins=sys.argv[3]

#test=hdf5_read("".join([writename,"ScanEvents"]))
test=hdf5_read(fname)
#test.min_vals_histo() # get binning done automatically
#test.full_scan()
#test.temp_vs_min(plot_title)
test.waveform_display(20)
