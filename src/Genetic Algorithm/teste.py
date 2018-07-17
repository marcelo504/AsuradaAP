#Generator teste

import population_generator
import rules_loader




population_generator.gen_population("Generations/",'0')
population_generator.gen_population("Generations/",'1')
rules_loader.member_plot('Generations/membership0.csv')
rules_loader.member_plot('Generations/membership1.csv')