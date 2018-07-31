#Single test Simulator


#Local files Import
import scenario_eval

ksp_ip = "192.168.0.101"
gen_path = "Generations/generation"
generation = 0
ind = 10

#scenario_eval.start_scenario(gen_path+str(generation)+"/membership"+str(ind)+".csv",ksp_ip)
scenario_eval.start_scenario("first_solution"+".csv",ksp_ip)