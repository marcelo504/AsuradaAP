import os,sys

#Local files Import
import scenario_eval
import population_generator
import selecter_breeder

#Treinamento com Alogritmos Genéticos

def run_initialization(pop_score):
	os.mkdir("Generations/generation"+generation)

	for ind in range(pop_number):
		population_generator.gen_population("Generations/generation"+generation,ind)

def run_evaluation(pop_score):
	for ind in range(pop_number):
		pop_score.append(scenario_eval.start_scenario("Generations/generation"+generation+"/membership"+ind+".py"))
	return 0

def run_recombination(mother, father):

	pass

def run_breed(pop_score):
	#Seleciona 4 Novos Pais para a proxima geração
	new_pop = []

	os.mkdir("Generations/generation"+generation)

	for parents in range(parents_number):
		father = selecter_breeder.selecter(pop_score)
		
		#Membros da populacao foram escolhidos logo nao serao escolhidos de novo
		pop_score[father] = 0

		mother = selecter_breeder.selecter(pop_score)

		#Membros da populacao foram escolhidos logo nao serao escolhidos de novo
		pop_score[mother] = 0

		#Breed

	#New generation
	del pop_score
	pop_score = new_pop




#--------------------------MAIN PROC---------------------------

generation = 0
pop_number = 12
parents_number = 4
childs_number = 3

#Popular geração 0
pop_score = []
run_initialization(pop_score)

while true:
	print("Starting generation: "+generation)

	run_evaluation(pop_score)

	if run_check_end() > 0:
		break

	#Preparando nova população
	generation = generation + 1

	run_breed(pop_score)



print("Solution found...")
