#SA Population Selecter and Breeder

import csv
from random import *

max_dist = 800
max_speed = 50
max_fire = 2000

def selecter(pop_score):
	#score sum
	score_total = 0
	for x in range(len(pop_score)):
		score_total += pop_score[x]

	sel_value = uniform(0,score_total)

	current = 0
	for pos in range(len(pop_score)):
		current += pop_score[pos]
		if current > sel_value:
			return pos

def mutate(type, write_file):
	high = 0
	med = 0
	low = 0

	if type == "rp":
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

	elif type == "rv":

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

	else:

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


def put_csv(csv_file, object):
	csv_file.writerow([object[0], object[1], object[2], object[3]])


def breeder(file_path,generation ,father ,mother ,child_number):
	
	with open(file_path+str(generation-1)+"/membership"+str(father)+".csv") as father_file:
		with open(file_path+str(generation-1)+"/membership"+str(mother)+".csv") as mother_file:
			with open(file_path+str(generation)+'/membership'+str(child_number)+'.csv','w',newline='') as member_file:
				write_file = csv.writer(member_file, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)

				father_csv = csv.reader(father_file, delimiter=',')
				mother_csv = csv.reader(mother_file, delimiter=',')

				#Grava Cabeçalho
				put_csv(write_file,mother_csv.__next__())
				father_csv.__next__()

				#Relative Position

				selection = randint(1,2)
				
				if randint(1,10) == 5: #Probabilidade de ecorrer mutação

					mutate("rp",write_file)
					for n in range(6):
						father_csv.__next__()
						mother_csv.__next__()

				else:
					for n in range(3):
						if selection == 1:
							put_csv(write_file,father_csv.__next__())
							put_csv(write_file,father_csv.__next__())
							mother_csv.__next__()
							mother_csv.__next__()
						else:
							put_csv(write_file,mother_csv.__next__())
							put_csv(write_file,mother_csv.__next__())
							father_csv.__next__()
							father_csv.__next__()


				#Relative Velocity

				selection = randint(1,2)
				
				if randint(1,10) == 5: #Probabilidade de ecorrer mutação

					mutate("rv",write_file)
					for n in range(6):
						father_csv.__next__()
						mother_csv.__next__()

				else:
					for n in range(3):
						if selection == 1:
							put_csv(write_file,father_csv.__next__())
							put_csv(write_file,father_csv.__next__())
							mother_csv.__next__()
							mother_csv.__next__()
						else:
							put_csv(write_file,mother_csv.__next__())
							put_csv(write_file,mother_csv.__next__())
							father_csv.__next__()
							father_csv.__next__()


				#RCS Control

				selection = randint(1,2)
				if randint(1,10) == 5: #Probabilidade de ecorrer mutação

					mutate("rcs",write_file)

				else:
					for n in range(2):
						if selection == 1:
							put_csv(write_file,father_csv.__next__())
							put_csv(write_file,father_csv.__next__())
							mother_csv.__next__()
							mother_csv.__next__()
						else:
							put_csv(write_file,mother_csv.__next__())
							put_csv(write_file,mother_csv.__next__())
							father_csv.__next__()
							father_csv.__next__()

					if selection == 1:
						put_csv(write_file,father_csv.__next__())
						mother_csv.__next__()
					else:
						put_csv(write_file,mother_csv.__next__())
						father_csv.__next__()

#Main
#score = [12,23,1,12,45]
#print(selecter(score))
#breeder("Generations/",0,1,2,0)