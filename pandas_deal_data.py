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
                name = l[2].rstrip(".js")
                line = file.readline()
                if is_number(line):
                    res[name] = float(line)
            line = file.readline()
    return res


if __name__ == '__main__':
    pwd = os.getcwd()
    files = os.listdir(pwd)
    name = ""
    for u in files:
        if u[0] == 'g':
            name = u
            break
    bench_names = get_bench_name(name)
    G = []
    W = []
    for f in files:
        if f[0] == "g":
            si = get_bench_data(f, bench_names)
            G.append(si)
        elif f[0] == 'W':
            sw = get_bench_data(f, bench_names)
            W.append(sw)

    g_sum = pandas.Series([0.0]*len(bench_names), index=bench_names)
    for g in G:
        g_sum += g
    g_mean = pandas.Series(g_sum.values / len(G), index=g_sum.index)

    w_sum = pandas.Series([0.0]*len(bench_names), index=bench_names)
    for w in W:
        w_sum += w
    w_mean = pandas.Series(w_sum.values / len(W), index=w_sum.index)

    relative = w_mean.divide(g_mean)
    print(relative)
    relative = relative.sort_index()
    print(relative)
    # create plot
    fig, ax = plt.subplots()
    index = np.arange(30)
    bar_width = 0.35
    opacity = 0.8

    rects1 = plt.bar(index, relative.values, bar_width,
                     alpha=opacity,
                     color='b',
                     label='WAM')

    # rects2 = plt.bar(index + bar_width, data_w, bar_width,
    #                  alpha=opacity,
    #                  color='g',
    #                  label='WAM')

    plt.xlabel('benchMark')
    plt.ylabel('relative time (gcc is 1.0)')
    plt.title('Relative Benchmark performance')
    plt.xticks(index, tuple(relative.index), rotation=90)
    plt.legend()

    plt.tight_layout()
    plt.savefig("relative.png")
