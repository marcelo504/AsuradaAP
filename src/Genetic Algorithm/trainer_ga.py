import os,sys
import time
import random

#Local files Import
import scenario_eval
import population_generator
import selecter_breeder

ksp_ip = "192.168.0.104"

#Treinamento com Alogritmos Genéticos

gen_path = "Generations2/generation"

def run_initialization(pop_score):
	os.mkdir(gen_path+str(generation))

	for ind in range(pop_number):
		population_generator.gen_population(gen_path+str(generation),ind)

def run_evaluation(pop_score, generation_number):
	for ind in range(pop_number):
		print("Individual "+str(ind))
		pop_score.append(scenario_eval.start_scenario(gen_path+str(generation)+"/membership"+str(ind)+".csv",ksp_ip,generation_number,ind))
		#pop_score.append(random.randint(1,60))
		time.sleep(2)
	return 0

def run_breed(pop_score):
	#Seleciona 4 Novos Pais para a proxima geração
	new_pop = []
	child_id = 0

	os.mkdir(gen_path+str(generation))

	for child in range(parents_number):
		father = selecter_breeder.selecter(pop_score)
		
		#Membros da populacao foram escolhidos logo nao serao escolhidos de novo
		pop_score[father] = 0

		mother = selecter_breeder.selecter(pop_score)

		#Membros da populacao foram escolhidos logo nao serao escolhidos de novo
		pop_score[mother] = 0

		#Breed v1
		# for n in range(childs_number):
		# 	selecter_breeder.breeder(gen_path,generation,father,mother,child_id)
		# 	child_id = child_id + 1

		#Breed v2
		selecter_breeder.breeder(gen_path,generation,father,father,child_id) #Child identical to Father
		child_id = child_id + 1
		selecter_breeder.breeder(gen_path,generation,mother,mother,child_id) #Child identical to mother
		child_id = child_id + 1
		selecter_breeder.breeder(gen_path,generation,father,mother,child_id) #New Child
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

if len(sys.argv) > 1:
	gen_input = sys.argv[1]
	generation = int(gen_input)
else:
	run_initialization(pop_score)

while True:
	print("Starting generation: "+str(generation))

	run_evaluation(pop_score, generation)
	
	print("Results:")
	print(pop_score)
	print(max(pop_score))
	if max(pop_score) > 1400:
		break

	#Preparando nova população
	generation = generation + 1

	run_breed(pop_score)

print("Solution found...")
print("Membership"+str(max(pop_score)))