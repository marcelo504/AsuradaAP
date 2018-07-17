import krpc
import time
import numpy as np
import numpy.linalg as la
import _thread

#local import 
import train_fuzzy

#Config
#ksp_ip = "192.168.0.101"

def distance_calc(current, target):
	current_position = current.position(target.reference_frame)
	displacement = np.array(current_position)
	return la.norm(displacement)


def collision_detection(vessel_pos):
	if vessel_pos[1] < -0.1 and vessel_pos[1] > -14:
		if vessel_pos[0] > -2.3 and vessel_pos[0] < 2.3:
			if vessel_pos[2] > -2.3 and vessel_pos[2] < 2.3:
				return 1
			else:
				return -1
		else:
			return -1
	else:
		return -1


def start_scenario(knowlege_base,ksp_ip):

	conn = krpc.connect(name='Trainer v1',address=ksp_ip, rpc_port=60000, stream_port=60001)
	vessel = conn.space_center.active_vessel

	time.sleep(1)
	print("Starting Scenario...")
	conn.space_center.load("Training02")


	#Parametros iniciais da Nave
	time.sleep(1)
	vessel = conn.space_center.active_vessel
	resources = vessel.resources
	current = conn.space_center.active_vessel.parts.controlling.docking_port
	target = conn.space_center.target_vessel
	success = 0
	final_score = 0

	#Combustivel Inicial
	start_rcs = resources.amount("MonoPropellant")
	start_dist = distance_calc(current, target)
	print("Running...")
	#print("Controlling "+vessel.name)
	#print("Initial RCS quantity: "+str(start_rcs))
	#print("Distance:" +str(start_dist))

	#Distancia maxima de operação
	max_dist = start_dist + start_dist/10

	control = _thread.allocate_lock()
	_thread.start_new_thread( train_fuzzy.asuradaRun,(control,ksp_ip,knowlege_base))


	#Verifica acoplagem com sucesso, colisão e afastamento 
	while True:

		#Correção para mudança do alvo da nave para docking port
		new_target = conn.space_center.target_docking_port
		if new_target != None:
			target = new_target

		#Confirmação de Docking
		if current.state == conn.space_center.DockingPortState.docked:
			success = 1
			final_score = 10000
			break

		#Detecção de Afastamento
		if max_dist < distance_calc(current, target):
			break
		#Detecção de Colisão
		if collision_detection(current.position(target.reference_frame)) > 0:
			print("Colision Detected")
			break
		#Delay
		time.sleep(0.2)

	#Stop AsuradaAP
	control.acquire()

	final_dist = distance_calc(current, target)

	resources = conn.space_center.active_vessel.resources
	final_rcs = resources.amount("MonoPropellant")
	if success == 1:
		print("Docking Complete:")
		used_RCS = start_rcs - final_rcs
		print("RCS used: "+str(used_RCS))
	else:
		print("Docking Failed")
		used_RCS = start_rcs - final_rcs
		print("RCS used: "+str(used_RCS))

	final_score = final_score + 220 - int(used_RCS)
	if final_dist < 200:
		final_score = final_score + 200 - final_dist
	
	print("Final Score: "+str(final_score))
	return final_score
