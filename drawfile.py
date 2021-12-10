import matplotlib.pyplot as plt
import numpy as np

def plot_file():
    f = open('out.log','r')
    result = []
    tmp_result = []
    for i in f.readlines():
        if i.strip() == 'pen down' or i.strip() == 'pen up':
            result.append(tmp_result)
            tmp_result=[]
            continue
        a= i.strip().split(',')
        a[0] = int(a[0])
        a[1] = int(a[1])
        tmp_result.append(a)

    result.append(tmp_result)
    arr = np.array(result)

    for r in result:
        if r == []:
            continue
        arr = np.array(r)
        plt.scatter(arr[:,0], arr[:,1])
    plt.show()