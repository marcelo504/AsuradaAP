import time
import numpy as np
import numpy.linalg as la
import krpc
import skfuzzy as fuzz
import skfuzzy.control as ctrl

import _thread

#Local files Import
import rules_loader
import csv

def distance_calc(current, target):
    current_position = current.position(target.reference_frame)
    displacement = np.array(current_position)
    return la.norm(displacement)


def reaction(vessel,axis,manu):
    
    #print('RCS Firing Time: {:>6.2f} ms'.format(manu))
    
    if axis == 'up':
        if manu > 0:
            vessel.control.up = -1
            time.sleep(abs(manu)/1000)
            vessel.control.up = 0
        elif manu != 0:
            vessel.control.up = 1
            time.sleep(abs(manu)/1000)
            vessel.control.up = 0
    
    elif axis == 'forward':
        if manu > 0:
            vessel.control.forward = -1
            time.sleep(abs(manu)/1000)
            vessel.control.forward = 0
        elif manu != 0:
            vessel.control.forward = 1
            time.sleep(abs(manu)/1000)
            vessel.control.forward = 0
    
    elif axis == 'right':
        if manu > 0:
            vessel.control.right = -1
            time.sleep(abs(manu)/1000)
            vessel.control.right = 0
        elif manu != 0:
            vessel.control.right = 1
            time.sleep(abs(manu)/1000)
            vessel.control.right = 0
    

def startFuzzy():
    #Variaveis
    #Input
    rel_position = ctrl.Antecedent(np.arange(-800, 800, 1),'position')
    rel_velocity = ctrl.Antecedent(np.arange(-50, 50, 1),'velocity')
    #Output
    rcs_output = ctrl.Consequent(np.arange(-2000, 2000, 1),'output') #ms

    #Loads Fuzzy membership Functions
    rules_loader.load_membership(rel_position,rel_velocity,rcs_output)

    #Fuzzy Rules
    rulePB = ctrl.Rule(antecedent=( (rel_position['pc'] & rel_velocity['nb'])|
                                    (rel_position['nb'] & rel_velocity['pc'])|
                                    (rel_position['nb'] & rel_velocity['nb'])|
                                    (rel_position['nb'] & rel_velocity['ns'])|
                                    (rel_position['nb'] & rel_velocity['nc'])|
                                    (rel_position['nc'] & rel_velocity['nb'])|
                                    (rel_position['ns'] & rel_velocity['nb'])|
                                    (rel_position['ns'] & rel_velocity['ns'])|
                                    (rel_position['ns'] & rel_velocity['nc'])),
                        consequent=rcs_output['pb'], label='Rule Positive Big')

    rulePS = ctrl.Rule(antecedent=( (rel_position['pc'] & rel_velocity['ns'])|
                                    (rel_position['nb'] & rel_velocity['ps'])|
                                    (rel_position['nc'] & rel_velocity['ns'])|
                                    (rel_position['nc'] & rel_velocity['nc'])|
                                    (rel_position['ps'] & rel_velocity['nb'])|
                                    (rel_position['ns'] & rel_velocity['pc'])),
                        consequent=rcs_output['ps'], label='Rule Positive Small')

    ruleNC = ctrl.Rule(antecedent=( (rel_position['pb'] & rel_velocity['nb'])|
                                    (rel_position['ps'] & rel_velocity['ns'])|
                                    (rel_position['pc'] & rel_velocity['nc'])|
                                    (rel_position['nb'] & rel_velocity['pb'])|
                                    (rel_position['ns'] & rel_velocity['ps'])|
                                    (rel_position['nc'] & rel_velocity['pc'])),
                        consequent=rcs_output['nc'], label='Rule No Change ')

    ruleNS = ctrl.Rule(antecedent=( (rel_position['ps'] & rel_velocity['nc'])|
                                    (rel_position['pc'] & rel_velocity['ps'])|
                                    (rel_position['pc'] & rel_velocity['pc'])|
                                    (rel_position['nc'] & rel_velocity['ps'])|
                                    (rel_position['pb'] & rel_velocity['ns'])|
                                    (rel_position['ns'] & rel_velocity['pb'])),
                        consequent=rcs_output['ns'], label='Rule Negative Small ')

    ruleNB = ctrl.Rule(antecedent=( (rel_position['pb'] & rel_velocity['pb'])|
                                    (rel_position['pb'] & rel_velocity['ps'])|
                                    (rel_position['pb'] & rel_velocity['pc'])|
                                    (rel_position['pb'] & rel_velocity['nc'])|
                                    (rel_position['ps'] & rel_velocity['pb'])|
                                    (rel_position['ps'] & rel_velocity['ps'])|
                                    (rel_position['ps'] & rel_velocity['pc'])|
                                    (rel_position['pc'] & rel_velocity['pb'])|
                                    (rel_position['nc'] & rel_velocity['pb'])),
                        consequent=rcs_output['nb'], label='Rule Negative Big ')


    system = ctrl.ControlSystem([rulePB, rulePS, ruleNC, ruleNS, ruleNB])

    fuzzy = ctrl.ControlSystemSimulation(system)

    return fuzzy


def runFuzzy(fuzzy, position, velocity):
    
    #Inserindo Dados de teste deve se usar a label definida
    fuzzy.input['position'] = position
    fuzzy.input['velocity'] = velocity

    fuzzy.compute()
    
    return fuzzy.output['output']
    
    
def threadAxisControl(control, ip, axis):
    
    #Determina qual Eixo a Thread ira cuidar
    if axis == 'right':
        axisN = 0
    elif axis == 'up':
        axisN = 2
    else:
        axisN = 1
    
    name = 'Automated Docking: '+axis
    
    conn = krpc.connect(name,address=ip, rpc_port=60000, stream_port=60001)
    vessel = conn.space_center.active_vessel
    current = None
    target = None
    manu = None
    docking_mode = 0

    current = conn.space_center.active_vessel.parts.controlling.docking_port
    target = conn.space_center.target_vessel
    
    #Iniciando Controlador Fuzzy
    fuzzy = startFuzzy()
    
    while True:

        if control.locked():
            conn.close()
            break

        #Correção para mudança do alvo da nave para docking port
        new_target = conn.space_center.target_docking_port
        if new_target != None and docking_mode == 0:
            target = new_target
            print("Switching to Docking mode...")
            docking_mode = 1

        if current is None:
            return 0

        elif target is None:
            return 0 

        else:
            # Get positions, distances, velocities and
            # speeds relative to the target docking port
            current_position = current.position(target.reference_frame)
            velocity = current.part.velocity(target.reference_frame)

            #Run Fuzzy
            manu = runFuzzy(fuzzy, current_position[axisN],velocity[axisN])
            #print("Position: {0}".format(current_position[axisN])+" Velocity: {0}".format(velocity[axisN]))
            
            #Engage RCS Engines
            reaction(vessel,axis,manu)
    _thread.exit()

def asuradaRun(stop_signal, ip):
    try:
        # Connect to kRPC
        conn = krpc.connect(name='Asurada AP',address=ip, rpc_port=60000, stream_port=60001)
        vessel = conn.space_center.active_vessel
        current = None
        target = None
        manu = None
        mode = 1 # Target mode, 1- far, 0-close
        
        activeThread = 0
        control_stop= None

        current = conn.space_center.active_vessel.parts.controlling.docking_port
        target = conn.space_center.target_vessel
        
        while True:

            if mode == 0:
                current = conn.space_center.active_vessel.parts.controlling.docking_port
                target = conn.space_center.target_docking_port
            else:
                current = conn.space_center.active_vessel.parts.controlling.docking_port
                target = conn.space_center.target_vessel


            if stop_signal.locked():
                #send signal to kill threads
                control_stop.acquire()
                #
                time.sleep(5)
                break

            if distance_calc(current, target) < 190:
                if mode == 1:
                    docking_port = target.parts.with_title('Clamp-O-Tron Docking Port')[0]
                    conn.space_center.target_docking_port = docking_port.docking_port
                    target = conn.space_center.target_docking_port
                    mode = 0
                
            #Travando controles de rotação com o Alvo
            vessel.auto_pilot.reference_frame = vessel.orbital_reference_frame
            tgtdir = target.direction(vessel.orbital_reference_frame)
            vessel.auto_pilot.target_direction = [tgtdir[0]*-1, tgtdir[1]*-1, tgtdir[2]*-1]
            if mode == 0:
                vessel.auto_pilot.target_roll = 180
            else:
                vessel.auto_pilot.target_roll = 180
            vessel.auto_pilot.engage()
            
            
            #Alvo Travado Iniciando Threads de Controle
            if activeThread == 0:
                control_stop = _thread.allocate_lock()

                _thread.start_new_thread( threadAxisControl,(control_stop,ip,'up',))
                _thread.start_new_thread( threadAxisControl,(control_stop,ip,'forward',))
                _thread.start_new_thread( threadAxisControl,(control_stop,ip,'right',))
                activeThread = 1

            else:
                time.sleep(0.5)
    finally:
        pass 

    print("Stopping asuradaAP...")
    conn.close()
    _thread.exit()
    return 0