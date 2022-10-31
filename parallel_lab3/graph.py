from pwn import *
from prettytable import PrettyTable
import matplotlib.pyplot as plt
import numpy as np


def inp(file_name):
    data = open(file_name, 'rb')
    try:
        num_of_threads = u32(data.read(4))
        threads = [i + 1 for i in range(num_of_threads)]
        iterations = u32(data.read(4))
        time = [[] for i in range(num_of_threads)]
        for i in range(iterations * num_of_threads):
            time[i % num_of_threads].append(float(struct.unpack('f', data.read(4))[0]))
    finally:
        data.close()
        return time, threads, num_of_threads


def plots(times, threads):

    list_t1 = []
    list_s = []
    list_e = []
    rgby = ['r','g','b','y']

    for i in range(len(times)):
        # 1
        t1 = [sum(k) / len(k) for k in times[i]]
        list_t1.append(t1)
        plt.plot(threads[i], t1, rgby[i])

    plt.title('Execution time', fontsize=20)


    plt.xlabel('Threads')
    plt.ylabel('Time')
    plt.grid(1)
    plt.legend(['rand','corr','wrong','strange'])
    plt.show()


    for i in range(len(times)):
        # 2
        s = [(sum(times[i][0]) / len(times[i][0])) / (sum(k) / len(k)) for k in times[i]]
        list_s.append(s)
        plt.plot(threads[i], s, rgby[i])


    plt.title('Acceleration', fontsize=20)

    plt.xlabel('Threads')
    plt.ylabel('Acceleration')
    plt.grid(1)
    plt.legend(['rand','corr','wrong','strange'])
    plt.show()


    for i in range(len(times)):
        # 3
        e = [list_s[i][k] / (k + 1) for k in range(len(list_s[i]))]
        list_e.append(e)
        plt.plot(threads[i], e, rgby[i])


    plt.title('Efficiency', fontsize=20)

    plt.xlabel('Threads')
    plt.ylabel('Efficiency')
    plt.grid(1)
    plt.legend(['rand','corr','wrong','strange'])
    plt.show()


# Table
def show_table(times, threads):
    title_text = 'Time table'

    fig_background_color = 'skyblue'
    fig_border = 'steelblue'

    column_headers = [i + 1 for i in range(len(times[0]))]
    row_headers = [i + 1 for i in range(threads)]

    cell_text = []
    for row in times:
        cell_text.append([f'{round(x, 5)}' for x in row])

    rcolors = plt.cm.BuPu(np.full(len(row_headers), 0.1))
    ccolors = plt.cm.BuPu(np.full(len(column_headers), 0.1))
    plt.figure(linewidth=10,
               edgecolor=fig_border,
               facecolor=fig_background_color,
               tight_layout={'pad': 2},
               )
    the_table = plt.table(cellText=cell_text,
                          rowLabels=row_headers,
                          rowColours=rcolors,
                          rowLoc='right',
                          colColours=ccolors,
                          colLabels=column_headers,
                          loc='center')

    the_table.scale(1, 1.75)
    ax = plt.gca()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    plt.box(on=None)
    plt.suptitle(title_text)
    plt.draw()
    plt.show()


def main():
    files = tuple(['d_rand.txt', 'd_corr.txt', 'd_wrong.txt', 'd_strange.txt'])
    times = []
    threads = []
    num_threads = []

    for file in files:
        exp = inp(file)
        times.append(exp[0])
        threads.append(exp[1])
        num_threads.append(exp[2])

    plots(times, threads)

    for i in range(len(num_threads)):
        show_table(times[i], num_threads[i])


if __name__ == '__main__':
    main()
