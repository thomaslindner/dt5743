# decoder for TDT743 digitizer
# Thomas Lindner
# Dec 2019
#
# Edits made by Ashley Ferreira, Feb 2020

class TDT743_decoder(data):
    '''
    decodes data from digitizer
    '''
    def __init__(self, data):
        self.data=data

    def TDT743_decoder(self):
        if self.data[2] != 0xa0000000:
            return "".join("First word has wrong identifier; first word = 0x", data[2])

        # Decode DT5743 bank
        if bank_name == "43FS":

            grp_mask = (self.data[3] & 0xff)

            number_groups = 0
            for i in range(16):
                if ((a<<ch)&GetChMask()): # findout how to do this bitwise operator stuff in python
                    number_groups+=1

            #number_groups = 2  # do this calculation correctly, what is number groups?
            num_sample_per_group = (len(self.data) - 6)/ number_groups # 4 instead of 6 in cpp code


            print("grp mask: %x sample_per_group %i " % (grp_mask,num_sample_per_group))

            print("%x %x %x %x %x %x" % (self.data[2],self.data[3],self.data[4],self.data[5],
                                         self.data[6],self.data[7]))

            for i in range(number_groups):
                if ((self.data[i] & 0xfff000) != 0xaa000000):
                    print("Bad first word for group: 0x",self.data[i])
                if((1<<i)&GetChMask()):
                    # try to get samples for first and second channel
                    samples_chan0 = [];
                    samples_chan1 = [];
                    for i in range(0, num_sample_per_group-1):
                        if i % 17 != 0:  # skip bogus data in every 17th sample.
                            samples_chan0.append((self.data[6+i] & 0xfff))
                            samples_chan1.append(((self.data[6+i] & 0xfff000) >> 12))
                    print("Channel 0 samples:")
                    print(samples_chan0)
                    print("Channel 1 samples:")
                    print(samples_chan1)

                #get extra info sphere

'''
still need to intergrate the following
'''

                RawChannelMeasurement meas0 = RawChannelMeasurement(gr*2);
                  meas0.AddSamples(Samples0);
                  meas0.SetFrequency(freq);
                  meas0.SetHitCounter(hit0);
                  meas0.SetTimeCounter(time0);
                  fMeasurements.push_back(meas0);

                  RawChannelMeasurement meas1 = RawChannelMeasurement(gr*2+1);
                  meas1.AddSamples(Samples1);
                  fMeasurements.push_back(meas1);

                  if(0)std::cout << freq << " " << hit0 << " " << hit1
            		     << " " << time0 << " " << time1 << std::endl;


                    # Do some simple decoding...
                    group_mask = (self.data[3] & 0xff) + ((self.data[4] & 0xff000000) >> 16);



        return decoded #still have yet to define this part
