import os,sys

#Local files Import
import scenario_eval
import population_generator
#Treinamento com Alogritmos Genéticos

def run_initialization():
	os.mkdir("Generations/generation"+generation)

	for ind in range(pop_number):
		population_generator.gen_population("Generations/generation"+generation,ind)

def run_evaluation():
	pass

def run_selection():
	pass

def run_recombination():
	pass


#--------------------------MAIN PROC---------------------------

generation = 0
pop_number = 10

#Popular geração 0
population = []
run_initialization()

while true:
	print("Starting generation: "+generation)

	run_evaluation()

	if run_check_end() > 0:
		break

	#Preparando nova população
	generation = generation + 1

	run_selection()
	run_recombination()



print("Solution found...")
