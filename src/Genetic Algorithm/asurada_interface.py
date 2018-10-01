import krpc
import time
import numpy as np
import numpy.linalg as la
import _thread
import datetime

#local import 
import train_fuzzy

gen_path = "Generations2/generation"
generation = 18
ind = 9

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


def button_action(vessel,button,message,control,ksp_ip):
	if button.text.content == "Engage":
		print("Engaging")
		running = True
		vessel.control.rcs = True;
		message.content = "Docking in progress..."
		button.text.content = "Abort"



		_thread.start_new_thread( train_fuzzy.asuradaRun,(control,ksp_ip,gen_path+str(generation)+"/membership"+str(ind)+".csv"))

	elif button.text.content == "Abort":
		print("Aborting")
		message.content = "Aborting..."
		button.text.content = "Disabled"
		#Stop AsuradaAP
		control.acquire()
		time.sleep(5)
		control.release()
		running = False
	else:
		running = False

	button.clicked = False
	return running

def adv_action(button, state):
	print("Clicked")
	time.sleep(0.5)
	button.clicked = False;
	if state == True:
		return False
	else:
		return True


def main_run(ksp_ip):


	conn = krpc.connect(name='Asurada Interface',address=ksp_ip, rpc_port=60000, stream_port=60001)

	#Parametros iniciais da Nave
	vessel = conn.space_center.active_vessel
	resources = vessel.resources
	current = conn.space_center.active_vessel.parts.controlling.docking_port
	target = conn.space_center.target_vessel
	success = 0
	control = _thread.allocate_lock()

	#Time Parameters
	start_time = datetime.datetime.now()
	actual_time = start_time

	#RCS Parameters
	start_rcs = 0
	actual_rcs = 0

	#Start interface
	canvas = conn.ui.stock_canvas
	# Get the size of the game window in pixels
	screen_size = canvas.rect_transform.size

	# Add a panel to contain the UI elements
	panel = canvas.add_panel()

	# Posicionamento da Interface no Jogo 
	rect = panel.rect_transform
	rect.size = (200, 250)
	rect.position = (110-(screen_size[0]/2), 0)
	rect.color = (1,1,1)

	#Itens da Interface

	#Titulo
	start_offset = 105
	title = panel.add_text("Super")
	title.rect_transform.position = (0, start_offset)
	title.size = 26
	title.style = title.style.bold
	title.alignment = title.alignment.middle_center
	title.color = (0,1,0)
	title.font = "OCR-A BT"

	title2 = panel.add_text("Asurada")
	title2.rect_transform.position = (0, start_offset - 25)
	title2.size = 26
	title2.style = title.style.bold
	title2.alignment = title.alignment.middle_center
	title2.color = (0,1,0)
	title2.font = "OCR-A BT"
	#print(title.available_fonts)

	desc = panel.add_text("Docking Autopilot")
	desc.rect_transform.position = (0, start_offset - 55)
	desc.alignment = desc.alignment.middle_center
	desc.size =16
	desc.color = (0,.7,0)



	#Status & button_action
	status_pos = start_offset - 125
	status = panel.add_text("Status:")
	status.rect_transform.position = (0, status_pos)
	status.size=16
	status.color = (0,.7,0)

	message = panel.add_text("Initializing...")
	message.rect_transform.position = (0, status_pos - 15)
	message.alignment = message.alignment.middle_center
	message.color = (1, 1, 1)
	message.size = 16

	action_button = panel.add_button("Engage")
	action_button.rect_transform.position = (0, status_pos - 50)
	action_button.rect_transform.size = (180,40)
	action_button.text.content = "Disabled"

	#Button Advanced
	adv_button = panel.add_button("Advanced")
	adv_button.rect_transform.position = (0, status_pos - 85)
	adv_button.rect_transform.size = (180,15)
	adv_button.text.content = "Advanced Mode"
	adv_button.text.size = 12


	running = False;
	advanced_mode = False;
	mode = False

	while True:
		#try:

		
		vessel = conn.space_center.active_vessel
		target = conn.space_center.target_vessel
		current = conn.space_center.active_vessel.parts.controlling.docking_port

		#Check Button
		if action_button.clicked:
			running = button_action(vessel,action_button,message,control,ksp_ip)
			#Button activated docking
			if action_button.text.content == "Abort":
				#Get readings
				start_time = datetime.datetime.now()
				start_rcs = conn.space_center.active_vessel.resources.amount("MonoPropellant")


		#Check Advanced Mode Button
		if adv_button.clicked:
			advanced_mode = adv_action(adv_button, advanced_mode)

		
		#Check Interface Mode
		if advanced_mode == True and mode == False: #Advanced Mode
			mode = advanced_mode

			rect.size = (200, 300)
			print("Adv Mode")

			start_offset = 135
			title.rect_transform.position = (0, start_offset)
			title2.rect_transform.position = (0, start_offset - 25)
			desc.rect_transform.position = (0, start_offset - 55)

			#Docking information

			info_pos = start_offset - 95
			time_title = panel.add_text("Docking time:")
			time_title.rect_transform.position = (0, info_pos)
			time_title.size = 16
			time_title.color = (1, 1, 1)

			time_ela = panel.add_text(str(actual_time - start_time))
			time_ela.rect_transform.position = (0, info_pos - 15)
			time_ela.size = 16
			time_ela.alignment = title.alignment.middle_center
			time_ela.color = (1, 1, 1)

			rcs_title = panel.add_text("RCS used:")
			rcs_title.rect_transform.position = (0, info_pos - 45)
			rcs_title.size = 16
			rcs_title.color = (1, 1, 1)

			rcs_reads = panel.add_text("0.00")
			rcs_reads.rect_transform.position = (0, info_pos - 60)
			rcs_reads.size = 16
			rcs_reads.alignment = title.alignment.middle_center
			rcs_reads.color = (1, 1, 1)


			status_pos = start_offset - 185
			status.rect_transform.position = (0, status_pos)
			message.rect_transform.position = (0, status_pos - 15)
			action_button.rect_transform.position = (0, status_pos - 50)
			adv_button.rect_transform.position = (0, status_pos - 85)


		elif advanced_mode == False and mode == True: # Normal Mode
			mode = advanced_mode
			print(mode)
			print("Normal Mode")

			rect.size = (200, 250)

			time_title.remove()
			time_ela.remove()
			rcs_title.remove()
			rcs_reads.remove()

			start_offset = 105
			title.rect_transform.position = (0, start_offset)
			title2.rect_transform.position = (0, start_offset - 25)
			desc.rect_transform.position = (0, start_offset - 55)
			status_pos = start_offset - 125
			status.rect_transform.position = (0, status_pos)
			message.rect_transform.position = (0, status_pos - 15)
			action_button.rect_transform.position = (0, status_pos - 50)
			adv_button.rect_transform.position = (0, status_pos - 85)

		#Check if ships docked if running
		if running == True:
			if current.state == conn.space_center.DockingPortState.docking:
				running = False;

			#Docking is Running update values to advanced mode
			actual_time = datetime.datetime.now()
			actual_rcs = conn.space_center.active_vessel.resources.amount("MonoPropellant")
			if advanced_mode:
				time_ela.content = str(actual_time - start_time)
				rcs_reads.content = str(start_rcs - actual_rcs)


			pass

		#Update Interface
		elif current == None:
			message.content = "Select Docking Port"
			action_button.text.content = "Disabled"

		elif target == None: #Not Ready
			message.content = "No target selected"
			action_button.text.content = "Disabled"

		elif distance_calc(current,target) > 900:
			message.content = "Too far from target"
			action_button.text.content = "Disabled"

		else: #Ready
			message.content = "Ready to Dock"
			
			if action_button.text.content != "Abort":
				action_button.text.content = "Engage"

		target = conn.space_center.target_vessel
		time.sleep(0.1)

		# except Exception as e:
		# 	time.sleep(2)
		# 	print("An unexpected error happened but it recovered...")


main_run("192.168.0.101")
#main_run("192.168.43.55")
#Gen 10 ind 3
#Gen 18 ind 9 score: 172