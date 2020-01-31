import h5py
f = h5py.File('mytestfile.hdf5', 'r')
print f
print f.keys()
list(f.keys())



