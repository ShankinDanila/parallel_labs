from pwn import *
from prettytable.colortable import ColorTable, Themes
import matplotlib.pyplot as plt

def inp():
	data = open('data.txt','rb')
	try:
		num_of_threads = u32(data.read(4))
		threads = [i+1 for i in range(num_of_threads)]
		iterations = u32(data.read(4))
		time = [[] for i in range(num_of_threads)]
		for i in range(iterations * num_of_threads):
			time[i % num_of_threads].append(float(struct.unpack('f',data.read(4))[0]))
	finally:
		data.close()
		return time, threads

def plots(times, threads):
	time_average = [sum(k)/len(k) for k in times]
	expected_time = [time_average[0]/(k + 1) for k in range(len(threads))]
	plt.title('Execution time', fontsize=20)
	plt.plot(threads, expected_time, 'r--')
	plt.plot(threads, time_average, 'b')
	plt.xlabel('Threads')
	plt.ylabel('Time')
	plt.grid(1)
	plt.legend(['Expected time', 'Experimental time'])
	plt.show()
	s = [(sum(times[0])/len(times[0]))/(sum(k)/len(k)) for k in times]
	expected_s = [time_average[0]/k for k in expected_time]
	plt.title('Acceleration', fontsize=20)
	plt.plot(threads, expected_s, 'r--')
	plt.plot(threads, s, 'b')
	plt.xlabel('Threads')
	plt.ylabel('Acceleration')
	plt.grid(1)
	plt.legend(['Expected acceleration', 'Experimental acceleration'])
	plt.show()
	e = [s[k]/(k + 1) for k in range(len(s))]
	expected_e = [expected_s[k]/(k + 1) for k in range(len(s))]
	plt.title('Efficiency', fontsize=20)
	plt.plot(threads, expected_e, 'r--')
	plt.plot(threads, e, 'b')
	plt.xlabel('Threads')
	plt.ylabel('Efficiency')
	plt.grid(1)
	plt.legend(['Expected efficiency', 'Experimental efficiency'])
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

if __name__ == '__main__':
	exp = inp()
	plots(exp[0], exp[1])
	table(exp[0], exp[1])
