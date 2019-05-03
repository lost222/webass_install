import os
import numpy as np
import matplotlib.pyplot as plt
import pandas


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


def performence_to_data(path):
    res = []
    with open(path) as file:
        line = file.readline()
        while line:
            if is_number(line):
                num = float(line)
                res.append(num)
            line = file.readline()
    return res


def get_bench_name(path):
    res = []
    with open(path) as file:
        line = file.readline()
        while line:
            if line[2] == 'c':
                l = line.split()
                benchname = l[2]
                res.append(benchname)
            line = file.readline()
    return res


def get_bench_data(path, benchname):
    res = pandas.Series([0.0] * len(benchname), index=benchname)
    with open(path) as file:
        line = file.readline()
        while line:
            if line[2] == 'c':
                l = line.split()
                name = l[2]
                line = file.readline()
                if is_number(line):
                    res[name] = float(line)
            line = file.readline()
    return res


if __name__ == '__main__':
    pwd = os.getcwd()
    files = os.listdir(pwd)
    G = []
    G_name = []
    W = []
    W_name = []
    for i in files:
        if i[0] == 'g':
            res = performence_to_data(i)
            name = get_bench_name(i)
            G.append(res)
            G_name.append(name)
        elif i[0] == 'W':
            res = performence_to_data(i)
            name = get_bench_name(i)
            W.append(res)
            W_name.append(name)
    data_g = []
    data_w = []
    for i in range(30):
        sum = 0
        for f in range(len(G)):
            sum += G[f][i]
        sum /= len(G)
        data_g.append(sum)
    for i in range(30):
        sum = 0
        for f in range(len(W)):
            sum += W[f][i]
        sum /= len(W)
        data_w.append(sum)

    si = get_bench_data('gcc_p1.txt', G_name[0])
    print(si)
    print(G[0])
    i = 0


    # create plot
    # fig, ax = plt.subplots()
    # index = np.arange(30)
    # bar_width = 0.35
    # opacity = 0.8
    #
    # rects1 = plt.bar(index, relative, bar_width,
    #                  alpha=opacity,
    #                  color='b',
    #                  label='WAM')
    #
    # # rects2 = plt.bar(index + bar_width, data_w, bar_width,
    # #                  alpha=opacity,
    # #                  color='g',
    # #                  label='WAM')
    #
    # plt.xlabel('benchMark')
    # plt.ylabel('relative time (gcc is 1.0)')
    # plt.title('Relative Benchmark performance')
    # plt.xticks(index, tuple(G_name[0]), rotation=90)
    # plt.legend()
    #
    # plt.tight_layout()
    # plt.savefig("relative.png")
