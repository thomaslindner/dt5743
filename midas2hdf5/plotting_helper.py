import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt

def heat_plot(arr):
    plt.imshow(arr)
    plt.show()
