#Generator teste

import population_generator
import rules_loader

gen = 44
ind = 2


#population_generator.gen_population("Generations/",'0')
#population_generator.gen_population("Generations/",'1')
#rules_loader.member_plot('first_solution.csv')
#rules_loader.member_plot('first_solution.csv')
rules_loader.member_plot('Generations/generation'+str(gen)+'/membership'+str(ind)+'.csv')