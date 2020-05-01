import matplotlib
import matplotlib.pyplot as plt

def heat_plot(arr):
    plt.imshow(arr)
    plt.savefig('test_detectionEfficency')

Z=np.random.random((10,10))
heat_plot(Z)
