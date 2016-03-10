f1 = open('res', 'r')
f2 = open('res2', 'r')


for line in f1:
	score = f2.readline()
	arr = line.strip().split(' ')

	print arr[-1], score