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


def button_action(button,control,ksp_ip):
	if button.text.content == "Engage":
		print("Engaging")
		button.text.content = "Abort"
		if control.locked == True:
			control.release()

		_thread.start_new_thread( train_fuzzy.asuradaRun,(control,ksp_ip,"first_solution.csv"))

	elif button.text.content == "Abort":
		print("Aborting")
		button.text.content = "Engage"
		#Stop AsuradaAP
		control.acquire()
		time.sleep(5)

	button.clicked = False


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

	# Position the panel on the left of the screen
	rect = panel.rect_transform
	rect.size = (200, 100)
	rect.position = (110-(screen_size[0]/2), 0)

	#Interface
	message = panel.add_text("Starting...")
	message.rect_transform.position = (0, 20)
	message.color = (1, 1, 1)
	message.size = 18

	action_button = panel.add_button("Engage")
	action_button.rect_transform.position = (0, -20)
	action_button.text.content = "Disabled"

	running = False;

	while True:
		vessel = conn.space_center.active_vessel
		target = conn.space_center.target_vessel
		current = conn.space_center.active_vessel.parts.controlling.docking_port

		#Check Button
		if action_button.clicked:
			running = True;
			vessel.control.rcs = True;
			button_action(action_button,control,ksp_ip)

		#Update Interface
		if running == True:
			if action_button.clicked:
				button_action(action_button,control,ksp_ip)
				running = False;

			if current.state != conn.space_center.DockingPortState.docking:
				running = False;

		elif current == None:
			message.content = "Invalid Control"
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


main_run("192.168.0.101")
#main_run("192.168.43.55")
