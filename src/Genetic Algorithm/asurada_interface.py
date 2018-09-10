import krpc
import time
import numpy as np
import numpy.linalg as la
import _thread

#local import 
import train_fuzzy


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

		_thread.start_new_thread( train_fuzzy.asuradaRun,(control,ksp_ip,"first_solution.csv"))

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

def main_run(ksp_ip):
	conn = krpc.connect(name='Asurada Interface',address=ksp_ip, rpc_port=60000, stream_port=60001)

	#Parametros iniciais da Nave
	vessel = conn.space_center.active_vessel
	resources = vessel.resources
	current = conn.space_center.active_vessel.parts.controlling.docking_port
	target = conn.space_center.target_vessel
	success = 0
	control = _thread.allocate_lock()

	#Start interface
	canvas = conn.ui.stock_canvas
	# Get the size of the game window in pixels
	screen_size = canvas.rect_transform.size

	# Add a panel to contain the UI elements
	panel = canvas.add_panel()

	# Posicionamento da Interface no Jogo 
	rect = panel.rect_transform
	rect.size = (200, 200)
	rect.position = (110-(screen_size[0]/2), 0)
	rect.color = (1,1,1)

	#Itens da Interface
	title = panel.add_text("Asurada")
	title.rect_transform.position = (0, 80)
	title.size = 26
	title.style = title.style.bold
	title.alignment = title.alignment.middle_center
	title.color = (0,1,0)
	title.font = "OCR-A BT"
	#print(title.available_fonts)

	desc = panel.add_text("Docking Autopilot")
	desc.rect_transform.position = (0, 48)
	desc.alignment = desc.alignment.middle_center
	desc.size =18
	desc.color = (0,.7,0)

	status = panel.add_text("Status:")
	status.rect_transform.position = (0, -10)
	status.size=16
	status.color = (0,.7,0)

	message = panel.add_text("Initializing...")
	message.rect_transform.position = (0, -25)
	message.alignment = message.alignment.middle_center
	message.color = (1, 1, 1)
	message.size = 16

	action_button = panel.add_button("Engage")
	action_button.rect_transform.position = (0, -60)
	action_button.rect_transform.size = (180,40)
	action_button.text.content = "Disabled"


	running = False;

	while True:
		vessel = conn.space_center.active_vessel
		target = conn.space_center.target_vessel
		current = conn.space_center.active_vessel.parts.controlling.docking_port

		#Check Button
		if action_button.clicked:
			running = button_action(vessel,action_button,message,control,ksp_ip)

		#Check if ships docked if running
		if running == True:
			if current.state == conn.space_center.DockingPortState.docking:
				running = False;
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


main_run("192.168.0.103")
#main_run("192.168.43.55")
