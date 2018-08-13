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
	if vessel_pos[1] < -0.3 and vessel_pos[1] > -15:
		if vessel_pos[0] > -2.4 and vessel_pos[0] < 2.4:
			if vessel_pos[2] > -2.4 and vessel_pos[2] < 2.4:
				return 1
			else:
				return -1
		else:
			return -1
	else:
		return -1

def draw_interface(conn, gen, ind):
	canvas = conn.ui.stock_canvas

	# Get the size of the game window in pixels
	screen_size = canvas.rect_transform.size

	# Add a panel to contain the UI elements
	panel = canvas.add_panel()

	# Position the panel on the left of the screen
	rect = panel.rect_transform
	rect.size = (200, 100)
	rect.position = (110-(screen_size[0]/2), 0)

	text = panel.add_text("Generation "+str(gen))
	text.rect_transform.position = (0, 20)
	text.color = (1, 1, 1)
	text.size = 18

	text2 = panel.add_text("Individual "+str(ind))
	text2.rect_transform.position = (0, -20)
	text2.color = (1, 1, 1)
	text2.size = 18


def start_scenario(knowlege_base,ksp_ip,gen_number,individual_name):

	conn = krpc.connect(name='Murph Trainer',address=ksp_ip, rpc_port=60000, stream_port=60001)
	vessel = conn.space_center.active_vessel

	time.sleep(1)
	print("Starting Scenario...")
	conn.space_center.load("002")
	#conn.space_center.load("Training02")

	draw_interface(conn, gen_number, individual_name)

	#Parametros iniciais da Nave
	time.sleep(1)
	vessel = conn.space_center.active_vessel
	resources = vessel.resources
	current = conn.space_center.active_vessel.parts.controlling.docking_port
	target = conn.space_center.target_vessel
	success = 0
	min_dist = 800
	final_score = 0
	curr_dist = 1

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

		#Confirmação de Docking
		if current.state == conn.space_center.DockingPortState.docked:
			success = 1
			final_score = 100 
			break

		#Tratamento para pré-Docking
		if current.state == conn.space_center.DockingPortState.docking:

			#Correção para mudança do alvo da nave para docking port
			new_target = conn.space_center.target_docking_port
			if new_target != None:
				target = new_target

			curr_dist = distance_calc(current, target)
			curr_rcs = resources.amount("MonoPropellant")

			#limite uso de RCS
			if start_rcs - 200 > curr_rcs:
				break

			#Score Menor Distancia
			if curr_dist < min_dist:
				min_dist = curr_dist
			elif curr_dist > min_dist+min_dist*0.5:
				#Condição para tratar Docking
				if curr_dist > 1:
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
		final_score = final_score + (200 - int(used_RCS))/8
	else:
		print("Docking Failed")
		used_RCS = start_rcs - final_rcs
		print("RCS used: "+str(used_RCS))
	
	final_score = final_score + 50 - min_dist
	print("Closest distance: "+str(final_dist))
	print("Final Score: "+str(final_score))
	conn.close()

	if final_score < 0:
		return 20
	else:
		return final_score
