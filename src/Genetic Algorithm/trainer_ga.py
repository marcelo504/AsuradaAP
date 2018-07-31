import os,sys
import time
import random

#Local files Import
import scenario_eval
import population_generator
import selecter_breeder

ksp_ip = "192.168.0.103"

#Treinamento com Alogritmos Genéticos

gen_path = "Generations/generation"

def run_initialization(pop_score):
	os.mkdir("Generations/generation"+str(generation))

	for ind in range(pop_number):
		population_generator.gen_population(gen_path+str(generation),ind)

def run_evaluation(pop_score):
	for ind in range(pop_number):
		print("Individual "+str(ind))
		pop_score.append(scenario_eval.start_scenario(gen_path+str(generation)+"/membership"+str(ind)+".csv",ksp_ip))
		#pop_score.append(random.randint(1,60))
		time.sleep(2)
	return 0

def run_breed(pop_score):
	#Seleciona 4 Novos Pais para a proxima geração
	new_pop = []
	child_id = 0

	os.mkdir("Generations/generation"+str(generation))

	for child in range(parents_number):
		father = selecter_breeder.selecter(pop_score)
		
		#Membros da populacao foram escolhidos logo nao serao escolhidos de novo
		pop_score[father] = 0

		mother = selecter_breeder.selecter(pop_score)

		#Membros da populacao foram escolhidos logo nao serao escolhidos de novo
		pop_score[mother] = 0

		#Breed
		for n in range(childs_number):
			selecter_breeder.breeder(gen_path,generation,father,mother,child_id)
			child_id = child_id + 1

	#New generation
	#del pop_score
	#pop_score = new_pop
	pop_score.clear()

def run_check_end():
	return 0

#--------------------------MAIN PROC---------------------------

generation = 0
pop_number = 12
parents_number = 4
childs_number = 3

#Popular geração 0
pop_score = []
run_initialization(pop_score)

while True:
	print("Starting generation: "+str(generation))

	run_evaluation(pop_score)
	
	print("Results:")
	print(pop_score)
	print(max(pop_score))
	if max(pop_score) > 1000:
		break

	#Preparando nova população
	generation = generation + 1

	run_breed(pop_score)

print("Solution found...")
print("Membership"+str(max(pop_score)))