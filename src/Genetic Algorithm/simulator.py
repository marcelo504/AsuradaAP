#Single test Simulation

#Local files Import
import scenario_eval

ksp_ip = "192.168.0.104"
#ksp_ip = "192.168.43.55"
#gen_path = "Generations/Train01/generation"
gen_path = "Generations2/generation"
generation = 18
ind = 9

scenario_eval.start_scenario(gen_path+str(generation)+"/membership"+str(ind)+".csv",ksp_ip,generation,ind)

#scenario_eval.start_scenario("first_solution"+".csv",ksp_ip,generation,ind)