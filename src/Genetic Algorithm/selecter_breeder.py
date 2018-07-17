#SA Population Selecter and Breeder

import csv
from random import *

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

def mutate(type, csv_object):
	pass

def breeder(file_path,father ,mother ,gen_number , child_number):
	
	with open("Generations/membership"+str(father)+".csv") as father_file:
		with open("Generations/membership"+str(mother)+".csv") as mother_file:
			with open(file_path+'membership'+gen_number+'.csv','w',newline='') as member_file:
				write_file = csv.writer(member_file, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)

				father_csv = csv.reader(father_file, delimiter=',')
				mother_csv = csv.reader(mother_file, delimiter=',')

				#Grava Cabeçalho
				print(mother_csv.__next__())
				father_csv.__next__()

				#Relative Position

				selection = randint(1,2)
				
				if randint(1,80) == 50: #Probabilidade de ecorrer mutação

					mutate("rp","placeholder")

				else:
					for n in range(3):
						if selection == 1:
							print(father_csv.__next__())
							print(father_csv.__next__())
							mother_csv.__next__()
							mother_csv.__next__()
						else:
							print(mother_csv.__next__())
							print(mother_csv.__next__())
							father_csv.__next__()
							father_csv.__next__()


				#Relative Velocity

				selection = randint(1,2)
				
				if randint(1,80) == 50: #Probabilidade de ecorrer mutação

					mutate("rv","placeholder")

				else:
					for n in range(3):
						if selection == 1:
							print(father_csv.__next__())
							print(father_csv.__next__())
							mother_csv.__next__()
							mother_csv.__next__()
						else:
							print(mother_csv.__next__())
							print(mother_csv.__next__())
							father_csv.__next__()
							father_csv.__next__()


				#RCS Control

				selection = randint(1,2)
				
				if randint(1,80) == 50: #Probabilidade de ecorrer mutação

					mutate("rcs","placeholder")

				else:
					for n in range(2):
						if selection == 1:
							print(father_csv.__next__())
							print(father_csv.__next__())
							mother_csv.__next__()
							mother_csv.__next__()
						else:
							print(mother_csv.__next__())
							print(mother_csv.__next__())
							father_csv.__next__()
							father_csv.__next__()

						if selection == 1:
							print(father_csv.__next__())
							mother_csv.__next__()
						else:
							print(mother_csv.__next__())
							father_csv.__next__()

#Main
#score = [12,23,1,12,45]
#print(selecter(score))
breeder(0,1,0,0)