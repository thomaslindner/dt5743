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
        x_hist, y_hist, patches = plt.hist(min_pulses, bins=100)#changed x and y order
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
        #magma_r.colors gives us the values below
        reversed_magma=np.array([[0.987053, 0.991438, 0.749504, 1.00000],
                        [0.995131, 0.827052, 0.585701, 1.00000],
                        [0.996341, 0.660969, 0.451160, 1.00000],
                        [0.979645, 0.491014, 0.367783, 1.00000],
                        [0.913354, 0.330052, 0.382563, 1.00000],
                        [0.786212, 0.241514, 0.450184, 1.00000],
                        [0.639216, 0.189921, 0.494150, 1.00000],
                        [0.494258, 0.141462, 0.507988, 1.00000],
                        [0.347636, 0.0829460, 0.494121, 1.00000],
                        [0.198177, 0.0638620, 0.404009, 1.00000],
                        [0.0697640, 0.0497260, 0.193735, 1.00000],
                        [0.00146200, 0.000466000, 0.013866, 1.00000]])

        #white = np.array([0, 0, 0, 0])
        #reversed_magma[:1, :] = white
        newcmp = ListedColormap(reversed_magma)
        newcmp.set_bad(color='w')#but now you need to mask the values

        #double check this only makes exactly zero = white
        #use set bad?

        def calc_cutoff():
            pedastal=max(y_hist)#yhist might be wrong
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

                        #temp commented out
                        #k=list(dset.attrs.keys())
                        #v=list(dset.attrs.values())
                        #ind=k.index("position")
                        #p=v[ind]
                        moto_exists=dset.attrs["motors running"]

                        if moto_exists:
                            pos=dset.attrs["moto position"]
                        else:
                            pos=dset.attrs["scn position"]

                        scan_vals.append(pos)

            #scan_vals=list(map(float, scan_vals))
            #scan_vals.sort()

            return moto_exists, scan_vals


        def detection_eff():#change structure based on this variable, you could just use size of scan and make a mesh
            i=0
            x_pos=[]
            y_pos=[]
            collective=[]
            temp_lst=[]

            if moto_exists:
                old_pos=[]
            else:
                old_pos=0

            for pos in scan_vals:
                if pos == old_pos:
                    temp_lst.append(min_pulses[i])

                else:
                    x_pos.append(old_pos[0])
                    y_pos.append(old_pos[1])

                    collective.append([old_pos,temp_lst])
                    temp_lst=[]
                    temp_lst.append(min_pulses[i])

                i+=1
                old_pos=pos

            if not(moto_exists):
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
            yl=np.linspace(0,10,10)#generalize this part
            #xl,yl=np.meshgrid(x,y)
            xl,yl=np.meshgrid(xl,yl)

            Z=np.resize(d_eff_l,xl.shape)


            #color_map = plt.imshow(x)
            #color_map.set_cmap("Blues_r")
            #plt.colorbar()

            #i cant find where other cmap was specified so im doing it right in imshow

            #plt.imshow(Z, cmap=plt.cm.get_cmap(name='magma'), interpolation='nearest', extent=[0,10,0,10]) #make extent dynamic later
            plt.imshow(Z, cmap=newcmp, interpolation='nearest', extent=[0,10,0,10])
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
        moto_exists, scan_vals=position_vals()
        print("3/4")
        d_eff_l, x, y = detection_eff()

        hdf5_file.close()
        print("4/4")

        #mention that you set nan to 0?
        for val in d_eff_l:
            if val == 0:
                val = np.nan

        plotting()

        #arr = []
        #for i in range(len(x_pos)):
            #arr.append([x_pos[i],y_pos[i],d_eff_list[i]])
        #X = np.array(arr, dtype=np.float64)
        #a=np.array(x_pos,y_pos,d_eff_list)
        #X = [x_pos,y_pos,d_eff_list]


    def pe_levels(self):
        '''
        returns roughly how many PEs are being
        observed by the PMT
        '''
        # the following are taken directly from the poisson distribution
        # formula, where k=0 and lambda=pe level
        one_pe_pourcentage=36.8
        two_pe_pourcentage=13.5
        three_pe_pourcentage=4.98
        four_pe_pourcentage=1.83
        five_pe_pourcentage=0.674
        #calculate the rest
        y_hist, min_pulses = self.min_vals_histo()
        noise_cutoff=max(y_hist)-3#should be around 2350

        #str_toprint1=str(''.join(["bottom of noise",str(noise_cutoff)]))
        #print(str_toprint1)

        noise_only=list(filter(lambda x: x>=noise_cutoff, min_pulses)) #shouldnt it be <
        #pe_observed=list(filter(lambda x: x>2350, min_pulses))
        numof_noise_only=len(noise_only)
        numof_total_pulses=len(min_pulses)
        #print(numof_noise_only,numof_total_pulses)
        #numof_pe_observed=len(pe_observed)
        pourcentage_of_noise=100*numof_noise_only/numof_total_pulses

        str_toprint=str(''.join(["percentage of triggers with no P.E. pulses in them: ", str(pourcentage_of_noise), "%"]))
        print(str_toprint)

        #if 46.8<pourcentage_of_noise<100:#make this more dybnamic like single pourcentage +10
        #    print("Most likely no PE")

        #elif abs(pourcentage_of_noise-single_pe_pourcentage)<=10:
        #    print("Single PE levels")

        #elif 18.5<pourcentage_of_noise<26.8:
        #    print("1-2 PE")

        #elif abs(pourcentage_of_noise-double_pe_pourcentage)<=5:
        #    print("Double PE levels")

        #elif abs(pourcentage_of_noise-more_pe_pourcentage)<=5:
        #    print("Three or more PE")

        #else:
        #    print("Many PEs")

        #maybe standardize just like +-5% of the value

        if (one_pe_pourcentage+5)<=pourcentage_of_noise<=100:
            print("Zero PE")

        elif (one_pe_pourcentage-5)<=pourcentage_of_noise<(one_pe_pourcentage+5):
            print("Single PE")

        elif (two_pe_pourcentage-3)<=pourcentage_of_noise<(two_pe_pourcentage+3):
            print("Double PE")

        elif (three_pe_pourcentage-2)<=pourcentage_of_noise<(three_pe_pourcentage+2):
            print("Triple PE")

        elif (four_pe_pourcentage-1)<=pourcentage_of_noise<(four_pe_pourcentage+1):
            print("Four PE")

        elif (five_pe_pourcentage-0.2)<=pourcentage_of_noise<(five_pe_pourcentage+0.2):
            print("Five PE")

        elif (five_pe_pourcentage+0.2)<=pourcentage_of_noise<=0:
            print("Six or more PE")

        else:
            print("Does not clearly fit a PE level")


fname=sys.argv[1]
function=sys.argv[2]
#plot_title=sys.argv[2]
#bins=sys.argv[3]

#test=hdf5_read("".join([writename,"ScanEvents"]))
obj=hdf5_read(fname)

if function=='histogram':
    obj.min_vals_histo()
elif function=='scan':
    obj.full_scan()
elif function=='pelevel':
    obj.pe_levels()
else:
    print("Not a valid function")

#test.temp_vs_min(plot_title)
#test.waveform_display(20)
#test.pe_levels()
