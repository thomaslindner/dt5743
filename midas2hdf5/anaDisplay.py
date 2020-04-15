import sys
import numpy as np
import h5py

import matplotlib
#matplotlib.use('Agg')

import matplotlib.pyplot as plt


def waveform_display(run,event):
    '''
    displays waveform of specified event # and run #/filename
    '''
    hdf5_file=h5py.File(''.join([run,'ScanEvents', '.hdf5']), 'r')

    keys=hdf5_file.keys()
    for key in keys:
        if "".join(["Event #",str(event)])==key:
            group=hdf5_file[key]
    for data_set_name in group.keys():
        if data_set_name=="ch0":
            data_set=group[data_set_name].value

    hdf5_file.close()

    length=len(data_set)
    avg=sum(data_set)/length
    event_num=event
    standard_dev=np.std(data_set)

    fig, ax = plt.subplots()

    textstr = '\n'.join(["Entries ", str(length), "\nMean ",str(avg),"\nStd Dev",str(standard_dev)])
    props = dict(boxstyle='round', facecolor='white', alpha=0.5)
    ax.text(0.05, 0.5, textstr, transform=ax.transAxes, fontsize=10,
    verticalalignment='top', bbox=props)

    #assuming its 0-300ns
    x=np.linspace(0,300,length)
    ax.plot(x, data_set, color='black')
    plt.ylabel('Waveform Minimum Value (ADC)')
    plt.xlabel('Time (ns)') #you will need to specify the trigger value?
    plt.title(''.join([run,' event #', str(event_num),' DT743 Waveform for channel=0']))
    plt.show()
    #plt.savefig('Waveform Example')



def online_waveform_display():
    '''

    '''
    return None


fname=sys.argv[1]
event_num=int(sys.argv[2])

waveform_display(fname,event_num)
