#Single test Simulation

#Local files Import
import scenario_eval

ksp_ip = "192.168.0.104"
gen_path = "Generations/Train01/generation"
generation = 45
ind = 1

#scenario_eval.start_scenario(gen_path+str(generation)+"/membership"+str(ind)+".csv",ksp_ip,generation,ind)

scenario_eval.start_scenario("first_solution"+".csv",ksp_ip,generation,ind)