#! /bin/python3

import re
import matplotlib.pyplot as plt
import os
import random
import string
import sys
import glob

def show(path, name, time, data):

    fig, ((ax0, ax2), (ax1, ax3)) = plt.subplots(ncols=2, nrows=2)
    fig.tight_layout(pad=3.0)

    axes = (ax0, ax1, ax2, ax3)
    cols = ('Greys_r', 'Reds', 'Greens', 'hot_r')
    titles = ('Permiability', 'Lethality', 'Population', 'Deaths')

    for ax, co, da, ti in zip(axes, cols, data, titles):
        po = ax.imshow(da, cmap=co, interpolation='none', vmin=0)
        ax.set_title(ti)
        fig.colorbar(po, ax=ax)

    fig.suptitle(f"{name} at time={time:04}")
    plt.savefig(os.path.join(path, f"frame_{time:06}.png"))
    plt.close()
    print('#', end='', flush=True)
    #plt.show()

def copy_data(data):
    return list(list(list(c for c in b) for b in a) for a in data)
    output = []
    for i, a in enumerate(data):
        output.append([])
        for j, b in enumerate(a):
            output[i].append([])
            for k, c in enumerate(b):
                output[i][j].append(c)
    return output


def parse(file):
    time = -1
    #perm, leth, pop, dead
    data = [[],[],[],[]]

    for line in file:
        if re.match(r'^\d+$', line):
            if(time > 0):
                #print(f"show time = {time}")
                yield(time, data)
            time = int(line)
        else:
            # [cadmium::celldevs::cell_ports_def<std::vector<int, std::allocator<int> >, samc>::cell_out: {(1,2) ; [1, 0, 8.94109, 0]}] generated by model samc_map_(1,2)
            x,y = [int(n) for n in line[line.rfind('(')+1:line.rfind(')')].split(',')]
            for i, n in enumerate([float(n) for n in line[line.rfind('[')+1:line.rfind('}')-1].split(',')]):
                #print(i, n)
                while len(data[i]) <= y:
                    data[i].append([])
                while len(data[i][y]) <= x:
                    data[i][y].append(0)
                data[i][y][x] = n;

    yield(time, data)

def run(filename_path):
    print(f"'./bin/samc' '{filename_path}'")
    os.system(f"'./bin/samc' '{filename_path}'")

    filename = os.path.split(filename_path)[-1]

    name = filename[:filename.rfind('.')]

    #path = os.path.join(".", "fig", (name+'_'+''.join(random.choice(string.ascii_lowercase) for _ in range(6))))
    output_path = os.path.join(".", "fig", name)
    #print(path)
    print(f"rm -rf '{output_path}'")
    os.system(f"rm -rf '{output_path}'")
    print(f"rm -rf '{output_path}.gif'")
    os.system(f"rm -rf '{output_path}.gif'")
    print(f"mkdir -p '{output_path}'")
    os.system(f"mkdir -p '{output_path}'")

    with open("./results/output_messages.txt") as file:
        for frame in parse(file):
            show(output_path, name, *frame)
    print('')
    #This is 'imagemagick convert'
    print(f"convert '{os.path.join(output_path, '*')}' '{os.path.join('.', 'fig', (name+'.gif'))}'")
    os.system(f"convert '{os.path.join(output_path, '*')}' '{os.path.join('.', 'fig', (name+'.gif'))}'")


if len(sys.argv) > 1:
    for filename_glob in sys.argv[1:]:
        for filename in glob.glob(filename_glob, recursive=True):
            #print(filename)
            run(filename)
else:
    for filename in os.listdir(os.path.join(".", "config")):
        run(os.path.join(".", "config", filename))



