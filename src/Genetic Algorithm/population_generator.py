#SA initial Population Generator

import csv
from random import *

max_dist = 800
max_speed = 50
max_fire = 2000

def gen_population(file_path,gen_number):
	with open(file_path+'/membership'+str(gen_number)+'.csv','w',newline='') as member_file:
		write_file = csv.writer(member_file, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
		write_file.writerow(['pos_name', 'tri1', 'tri2', 'tri3'])

		high = 0
		med = 0
		low = 0

		#Relative Position
	
		#Positive_Big
		high = max_dist
		med = max_dist
		low = randint(int(max_dist/4),max_dist-1)
		#Load Values to file
		write_file.writerow(['pb',low, med, high])
		write_file.writerow(['nb',high*-1, med*-1, low*-1])

		#Positive_Small
		high = randint(low+1, int((high+low)/2)+1)
		low = randint(0, low-1)
		med = int((high+low)/2)
		#Load Values
		write_file.writerow(['ps',low, med, high])
		write_file.writerow(['ns',high*-1, med*-1, low*-1])

		#Positive_Close
		high = randint(low+1,int((high+low)/2)+1)
		low = -1
		med = int(high/2)
		#Load Values
		write_file.writerow(['pc',low, med, high])
		write_file.writerow(['nc',high*-1, med*-1, low*-1])

		#Relative Velocity
		#Positive_Big
		high = max_speed
		med = max_speed
		low = randint(int(max_speed/4),max_speed-1)
		#Load Values to file
		write_file.writerow(['pb',low, med, high])
		write_file.writerow(['nb',high*-1, med*-1, low*-1])

		#Positive_Small
		high = randint(low+1, int((high+low)/2)+1)
		low = randint(0, low-1)
		med = int((high+low)/2)
		#Load Values
		write_file.writerow(['ps',low, med, high])
		write_file.writerow(['ns',high*-1, med*-1, low*-1])

		#Positive_Close
		high = randint(low+1,int((high+low)/2)+1)
		low = -1
		med = int(high/2)
		#Load Values
		write_file.writerow(['pc',low, med, high])
		write_file.writerow(['nc',high*-1, med*-1, low*-1])

		#RCS Control

		write_file.writerow(['nc',0, 0, 0])

		high = max_fire
		med = max_fire
		low = randint(int(max_fire/4),max_fire-1)

		write_file.writerow(['pb',low, med, high])
		write_file.writerow(['nb',high*-1, med*-1, low*-1])

		high = randint(low+1,int((high+low)/2)+1)
		low = -1
		med = int(high/2)
		write_file.writerow(['ps',low, med, high])
		write_file.writerow(['ns',high*-1, med*-1, low*-1])
