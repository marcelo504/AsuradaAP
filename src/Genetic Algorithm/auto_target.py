import time
import numpy as np
import numpy.linalg as la
import krpc
import skfuzzy as fuzz
import skfuzzy.control as ctrl




conn = krpc.connect(name='Asurada AP',address='192.168.0.101', rpc_port=60000, stream_port=60001)
vessel = conn.space_center.active_vessel

target = conn.space_center.target_vessel

while True:
	docking_port = target.parts.with_title('Clamp-O-Tron Docking Port')[0]
	if docking_port != None:
		
		conn.space_center.target_docking_port = docking_port.docking_port
		print("Target acquired")
		break