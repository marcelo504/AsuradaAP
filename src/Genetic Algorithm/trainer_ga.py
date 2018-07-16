

#Local files Import
import scenario_eval

#Treinamento com Alogritmos Genéticos



def run_initialization():
	pass


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
