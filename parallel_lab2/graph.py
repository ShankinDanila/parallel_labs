from pwn import *
from prettytable.colortable import ColorTable, Themes
import matplotlib.pyplot as plt
import numpy as np

def inp(name):
	data = open(name,'rb')
	try:
		num_of_threads = u32(data.read(4))
		threads = [i+1 for i in range(num_of_threads)]
		iterations = u32(data.read(4))
		time = [[] for i in range(num_of_threads)]
		for i in range(iterations * num_of_threads):
			time[i % num_of_threads].append(float(struct.unpack('f',data.read(4))[0]))
	finally:
		data.close()
		return time, threads, num_of_threads

def plots(times, threads):
    #1
	t1 = [sum(k)/len(k) for k in times] #
	expected_time = [t1[0]/(k + 1) for k in range(len(threads))]
	plt.title('Execution time', fontsize=20)
	plt.plot(threads, expected_time, 'b--')
	plt.plot(threads, t1, 'g')
	plt.xlabel('Threads')
	plt.ylabel('Time')
	plt.grid(1)
	plt.legend(['Expected time', 'Real time'])
	plt.show()
    #2
	s = [(sum(times[0])/len(times[0]))/(sum(k)/len(k)) for k in times]
	expected_s = [t1[0]/k for k in expected_time] #prefer
	plt.title('Acceleration', fontsize=20)
	plt.plot(threads, expected_s, 'b--')
	plt.plot(threads, s, 'g')
	plt.xlabel('Threads')
	plt.ylabel('Acceleration')
	plt.grid(1)
	plt.legend(['Expected acceleration', 'Real acceleration'])
	plt.show()
    #3
	e = [s[k]/(k + 1) for k in range(len(s))]
	expected_e = [expected_s[k]/(k + 1) for k in range(len(s))]
	plt.title('Efficiency', fontsize=20)
	plt.plot(threads, expected_e, 'b--')
	plt.plot(threads, e, 'g')
	plt.xlabel('Threads')
	plt.ylabel('Efficiency')
	plt.grid(1)
	plt.legend(['Expected efficiency', 'Real efficiency'])
	plt.show()

def table(times, threads):
	table = ColorTable(theme=Themes.DEFAULT)
	table.field_names = ['Thread'] + [i+1 for i in range(len(times[0]))]
	for i in range(len(threads)):
		times[i].insert(0, i+1)
	for i in range(len(times)):
		for j in range(len(times[i])):
			times[i][j] = round(times[i][j], 5)
	table.add_rows(times)
	print(table)

def compare():
	data = inp('data.txt')
	data_cancel = inp('data_cancel.txt')
	times = data[0]
	times_cancel = data_cancel[0]
	threads = data[1]
	t1 = [sum(k)/len(k) for k in times]
	t2 = [sum(k)/len(k) for k in times_cancel]
#	ratio = []
#	for i in range(0, len(t1)):
#		ratio.append(t2[i]/t1[i])
	plt.plot(threads, t2, 'g')
	plt.plot(threads, t1, 'b--')
	plt.xlabel('Threads')
	plt.ylabel('Time comparison')
	plt.grid(1)
	plt.show()

if __name__ == '__main__':
	exp = inp('data.txt')
	times = exp[0]
	threads = exp[1]
	num_threads = exp[2]
	#plots(times,threads)
	compare()
	table(exp[0], exp[1])
