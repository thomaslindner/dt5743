# hdf5 file reader for mpmt test stand digitizer data
# includes varius functions for plotting the data
# Ashley Ferreira
# April 2020

import sys
import numpy as np
import h5py

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt

from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap


class hdf5_read:
    '''
    after you call a_midas2hdf5.py to save MIDAS data
    reads hdf5 file created by a_midas2hdf5.py and interprets digitizer data
    '''
    def __init__(self, hdf5_file_name):
        self.file_name=hdf5_file_name


    def min_vals_histo(self, save_plot):
        '''
        makes historgram of pulses
        with bin number generated automatically
        '''
        hdf5_file=h5py.File(''.join([self.file_name, 'ScanEvents', '.hdf5']), 'r')
        min_pulses=[]


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

        hdf5_file.close()

        plt.figure()
        x_hist, y_hist, patches = plt.hist(min_pulses, bins=100)#bins='auto')

        if save_plot:
            plt.yscale('log')
            plt.xlabel('Waveform Minimum Value (ADC)')
            plt.ylabel('Frequency')
            plt.title(''.join([self.file_name,' histogram']))
            plt.savefig(''.join([self.file_name,'_histogram']))

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
        plt.savefig(title)
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


        newcmp = ListedColormap(reversed_magma)
        newcmp.set_bad(color='w')


        def calc_cutoff(lst):
            pedastal=max(lst)
            ind=lst.index(pedastal)
            lst.pop(ind)
            pe_peak=max(lst)

            while pe_peak>pedastal*0.98:
                ind=lst.index(pe_peak)
                lst.pop(ind) #loop this?
                pe_peak=max(lst)

            cutoff=(pedastal+pe_peak)/2
            return cutoff


        def position_vals():
            keys=hdf5_file.keys()
            groups=[]
            scan_vals=[]
            for key in keys:
                groups.append(hdf5_file[key])
            for group in groups:
                for data_set_name in group.keys():#order these
                    if data_set_name=="ch0":
                        data_set=group[data_set_name].value
                        dset=group[data_set_name]

                        #moto_exists=dset.attrs["motors running"]
                        moto_exists=False#temporary for debugging

                        if moto_exists:
                            pos=dset.attrs["moto position"]
                        else:
                            pos=dset.attrs["scan position"]

                        scan_vals.append(pos)

            return moto_exists, scan_vals


        def detection_eff(scan_vals):
            i=0
            x_pos=[]
            y_pos=[]
            collective=[]
            temp_lst=[]

            if moto_exists:
                old_pos=[0,0]
                for pos in scan_vals:
                    if pos[0] == old_pos[0] and pos[1]==old_pos[1]:
                        temp_lst.append(min_pulses[i])

                    else:
                        x_pos.append(old_pos[0])
                        y_pos.append(old_pos[1])

                        collective.append([old_pos,temp_lst])
                        temp_lst=[]
                        temp_lst.append(min_pulses[i])

                    i+=1
                    old_pos=pos


            else:
                old_pos=0
                for pos in scan_vals:
                    if pos == old_pos:
                        temp_lst.append(min_pulses[i])
                    else:
                        x_pos.append(old_pos)
                        y_pos.append(old_pos)
                        #print(old_pos)
                        collective.append([old_pos,temp_lst])
                        temp_lst=[]
                        temp_lst.append(min_pulses[i])

                    i+=1
                    old_pos=pos

                x_pos=list(map(lambda x: x//10, x_pos))
                y_pos=list(map(lambda y: y%10, y_pos))

            d_eff_list=[]

            for i in range(len(collective)):
                loc=collective[i][0]
                pulse_list=collective[i][1]
                hits=0
                numof_pulses=len(pulse_list)
                for pulse in pulse_list:
                    if pulse<cutoff:
                        hits+=1

                hits1=float(hits)
                pulses=float(numof_pulses)
                if pulses>0:
                    d_eff=hits1/pulses
                else:
                    d_eff=0.0
                d_eff_list.append(d_eff)

            return d_eff_list, x_pos, y_pos


        def plotting():
            xl,yl=np.meshgrid(x,y)

            side=int(np.sqrt(len(d_eff_l)))
            Z=np.resize(d_eff_l,(side,side))

            plt.figure(figsize=(5, 5))
            plt.imshow(Z, cmap=newcmp, interpolation='nearest', extent=[min(x),max(x),min(y),max(y)])#make extent dynamic
            plt.colorbar()
            plt.xlabel('X positon [m]')
            plt.ylabel('Y positon [m]')
            plt.title(''.join([self.file_name,' detection efficency']))
            plt.savefig(''.join([self.file_name,'_detectionEfficency']))


        hdf5_file=h5py.File(''.join([self.file_name,'ScanEvents', '.hdf5']), 'r')
        print("progress:")

        y_hist, min_pulses = self.min_vals_histo(False)
        cutoff = calc_cutoff(list(y_hist))

        print("1/4")

        moto_exists, scan_lst=position_vals()
        moto_exists=False #this is done temporarily to debug SCAN

        print("2/4")

        d_eff_l, x, y = detection_eff(scan_lst)

        hdf5_file.close()
        print("3/4")

        # setting values of exactly zero equal to nan
        # so they show up as white on the plot
        for i in range(len(d_eff_l)):
            if d_eff_l[i] == 0.0:
                d_eff_l[i] = np.nan

        plotting()

        print("4/4 \nplot saved in midas2hdf5 folder")



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

        y_hist, min_pulses = self.min_vals_histo(False)
        noise_cutoff=max(y_hist)-3

        noise_only=list(filter(lambda x: x>=noise_cutoff, min_pulses))
        numof_noise_only=len(noise_only)
        numof_total_pulses=len(min_pulses)

        pourcentage_of_noise=100*numof_noise_only/numof_total_pulses

        str_toprint=str(''.join(["percentage of triggers with no P.E. pulses in them: ", str(pourcentage_of_noise), "%"]))
        print(str_toprint)

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

        elif (five_pe_pourcentage-0.2)>=pourcentage_of_noise>=0:#make sure all of these make sense
            print("Six or more PE")

        else:
            print("Does not clearly fit a PE level")



fname=sys.argv[1]
function=sys.argv[2]

obj=hdf5_read(fname)

if function=='histogram':
    obj.min_vals_histo(True)
elif function=='scan':
    obj.full_scan()
elif function=='pelevel':
    obj.pe_levels()
else:
    print("Not a valid function")
