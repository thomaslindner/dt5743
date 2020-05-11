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
    after you call midas2hdf5.py to save MIDAS data to an HDF5 file this
    class includes functions which read the HDF5 file created and analyze
    the data in different ways
    '''
    def __init__(self, hdf5_file_name):
        self.file_name=hdf5_file_name


    def min_vals_histo(self, save_plot):
        '''
        makes historgram of minimum pulse values
        with bin number set automatically
        '''
        # open the hdf5 file for reading
        hdf5_file=h5py.File(''.join([self.file_name, 'ScanEvents', '.hdf5']), 'r')

        # save the name of all the groups (events)
        # stored in the hdf5 file
        keys=hdf5_file.keys()

        # since the groups are python dictorinary
        # keys they are not sorted in the order that they
        # were stored so they need to be formatted
        # and then properly stored
        keys=list(map(int, list(keys)))
        keys.sort()

        # make a list containing all the groups in the file
        groups=[]
        for key in keys:
            groups.append(hdf5_file[str(key)])

        # initialize the list to store all the
        # minimum pulse values
        min_pulses=[]

        # loop through each group and store the
        # PMT data from digitizer ch0 into
        # data_set and then find the minimum value
        # of data_set to find the minimum pulse value
        for group in groups:
            for data_set_name in group.keys():
                if data_set_name=="ch0":
                    data_set=group[data_set_name].value
                    min_pulses.append(np.min(data_set))

        # close the hdf5 file for reading
        hdf5_file.close()

        # create histogram of the minimum pulse values
        plt.figure()
        x_hist, y_hist, patches = plt.hist(min_pulses, bins=100)#bins='auto')

        # if the plot needs to be visually seen (sometimes just the values
        # plt.hist returns are needed) then this section will plot the histogram
        # and save it as a picture under the midas2hdf5 folder
        if save_plot:
            plt.yscale('log')
            plt.xlabel('Waveform Minimum Value (ADC)')
            plt.ylabel('Frequency')
            plt.title(''.join([self.file_name,' histogram']))
            plt.savefig(''.join([self.file_name,'_histogram']))

        return y_hist, min_pulses


    def temp_vs_min(self,title):
        '''
        plots temperature of 5 sensors versus PMT data
        THIS CODE WAS NOT FINISHED // THE SENSORS HAVE NOT BEEN INSTALLED
        AND SO MIDAS JUST READS IN CONSTANT PRESET TEMPERATURES

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
        # magma_r.colors gives us the colormap values below
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

        # using the magma_r.color values we are able to create the
        # whole color map using ListedColormap()
        newcmp = ListedColormap(reversed_magma)

        # we then set nan values to show up as 'white'
        # which we will use to help us see errors
        newcmp.set_bad(color='w')


        def calc_cutoff(lst):
            '''
            calculates the single PE ADC cutoff value from the minimum pulse
            histogram bar values. specifically, it picks the ADC value
            directly between the pedastal and single PE peak.
            '''
            # assumes pedestal is tallest point on minimum
            # pulse histogram
            pedastal=max(lst)

            # assumes single PE peak is second tallest
            # point on minimum pulse historgam
            ind=lst.index(pedastal)
            lst.pop(ind)
            pe_peak=max(lst)

            # if the single PE peak is too close to the
            # pedestal it recalculates the single PE peak
            while pe_peak>pedastal*0.98:
                ind=lst.index(pe_peak)
                lst.pop(ind) #loop this?
                pe_peak=max(lst)

            # calculates the cutoff to be the point between
            # the single PE peak and the pedastal
            cutoff=(pedastal+pe_peak)/2
            return cutoff


        def position_vals():
            '''
            creates a list of the xy position values
            at each event # using MOTO bank if motors
            are running, and the SCAN bank if not

            '''
            # open the hdf5 file for reading
            hdf5_file=h5py.File(''.join([self.file_name, 'ScanEvents', '.hdf5']), 'r')

            # save the name of all the groups (events)
            # stored in the hdf5 file
            keys=hdf5_file.keys()

            # since the groups are python dictorinary
            # keys they are not sorted in the order that they
            # were stored so they need to be formatted
            # and then properly stored
            keys=list(map(int, list(keys)))
            keys.sort()

            # make a list containing all the groups in the file
            groups=[]
            for key in keys:
                groups.append(hdf5_file[str(key)])

            # initialize the list to store all the
            # position values from the scan
            scan_vals=[]

            # loop through each group and store the
            # position data in scan_vals
            #
            # when the motors are not running this code
            # uses the SCAN bank to simulate xy data that
            # would normally come from the MOTO bank
            for group in groups:
                for data_set_name in group.keys():
                    if data_set_name=="ch0":
                        data_set=group[data_set_name].value
                        dset=group[data_set_name]

                        moto_exists=dset.attrs["motors running"]

                        if moto_exists:
                            pos=dset.attrs["moto position"]
                        else:
                            pos=dset.attrs["scan position"]

                        scan_vals.append(pos)

            return moto_exists, scan_vals


        def detection_eff(scan_vals):
            '''
            calculates the detection efficiency at each xy position
            and creates a list of all the xy positions without duplicates
            '''

            # initialize counter
            i=0

            # initialize list to store xy positions
            x_pos=[]
            y_pos=[]

            # initialize list to save xy position and
            # minimum pulse values associated with that position
            collective=[]

            # initialize list to use as temporary storage in loop
            temp_lst=[]

            # if the motors are running use real xy position values
            #
            # for each position, associate a list of all the
            # minimum pulse values at that position
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

            # if motos aren't running, use simulated xy data from SCAN bank
            #
            # for each position, associate a list of all the
            # minimum pulse values at that position
            else:
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

            # initilize list of detection efficiency at each point
            d_eff_list=[]

            # for each xy position, calculate the pourcentage of
            # associated minimum pulse values which lie below
            # the cutoff ADC val (which mean a PE was seen by the PMT)
            # then save these pourcentages in d_eff_list
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
            '''
            using the list of detection efficincies and the xy positions
            this function plots a heat map of the detection efficiencies
            on the xy positions of the scan
            '''
            side=int(np.sqrt(len(d_eff_l)))
            Z=np.resize(d_eff_l,(side,side))

            # plots heat map for detection efficiency and saves photo of it
            # under the midas2hdf5 folder
            plt.figure(figsize=(5, 5))
            plt.imshow(Z, cmap=newcmp, interpolation='nearest', extent=[min(x),max(x),min(y),max(y)])
            plt.colorbar()
            plt.xlabel('X positon [m]')
            plt.ylabel('Y positon [m]')
            plt.title(''.join([self.file_name,' detection efficency']))
            plt.savefig(''.join([self.file_name,'_detectionEfficency']))


        # opens the hdf5 file for reading
        hdf5_file=h5py.File(''.join([self.file_name,'ScanEvents', '.hdf5']), 'r')

        # print the progress of the program
        print("progress:")

        y_hist, min_pulses = self.min_vals_histo(False)
        cutoff = calc_cutoff(list(y_hist))
        print("1/4")

        moto_exists, scan_lst=position_vals()
        print("2/4")

        d_eff_l, x, y = detection_eff(scan_lst)
        # closes the hdf5 file for reading
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

        elif (five_pe_pourcentage-0.2)>=pourcentage_of_noise>=0:
            print("Six or more PE")

        else:
            print("Does not clearly fit a PE level")


# takes in hdf5 file name to read from as second
# command line argument
fname=sys.argv[1]

# takes in function user wishes to execute as third
# commend line argument
function=sys.argv[2]

# initialize hdf5_read class with the hdf5 file name
obj=hdf5_read(fname)

# executes function user was interested in
if function=='histogram':
    obj.min_vals_histo(True)
elif function=='scan':
    obj.full_scan()
elif function=='pelevel':
    obj.pe_levels()
else:
    print("Not a valid function")
