import curses
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

# Set up curses
stdscr = curses.initscr()
curses.nocbreak()
stdscr.keypad(1)
curses.noecho()


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
    
    
    #rel_position
    #rel_position['pb'] = fuzz.trimf(rel_position.universe, [500,800,800])    #POSITIVE_BIG
    #rel_position['ps'] = fuzz.trimf(rel_position.universe, [200,400,600])    #POSITIVE_SMALL
    #rel_position['pc'] = fuzz.trimf(rel_position.universe, [-1,150,300])      #POSITIVE_CLOSE
    #rel_position['nb'] = fuzz.trimf(rel_position.universe, [-800,-800,-500]) #NEGATIVE_BIG
    #rel_position['ns'] = fuzz.trimf(rel_position.universe, [-600,-400,-200]) #NEGATIVE_SMALL
    #rel_position['nc'] = fuzz.trimf(rel_position.universe, [-300,-150,1])    #NEGATIVE_CLOSE
    #rel_velocity
    #rel_velocity['pb'] = fuzz.trimf(rel_velocity.universe, [20,50,50])       #POSITIVE_BIG
    #rel_velocity['ps'] = fuzz.trimf(rel_velocity.universe, [5,15,30])        #POSITIVE_SMALL
    #rel_velocity['pc'] = fuzz.trimf(rel_velocity.universe, [-1,5,10])         #POSITIVE_CLOSE
    #rel_velocity['nb'] = fuzz.trimf(rel_velocity.universe, [-50,-50,-20])    #NEGATIVE_BIG
    #rel_velocity['ns'] = fuzz.trimf(rel_velocity.universe, [-30,-15,-5])     #NEGATIVE_SMALL
    #rel_velocity['nc'] = fuzz.trimf(rel_velocity.universe, [-10,-5,1])       #NEGATIVE_CLOSE

    #rcs_output['pb'] = fuzz.trimf(rcs_output.universe, [1000,2000,2000])      #POSITIVE_BIG
    #rcs_output['ps'] = fuzz.trimf(rcs_output.universe, [0,500,1000])          #POSITIVE_SMALL
    #rcs_output['nc'] = fuzz.trimf(rcs_output.universe, [0,0,0])               #NO CHANGE
    #rcs_output['ns'] = fuzz.trimf(rcs_output.universe, [-1000,-500,0])        #NEGATIVE_SMALL
    #rcs_output['nb'] = fuzz.trimf(rcs_output.universe, [-2000,-2000,-1000])   #NEGATIVE_BIG


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

    print('Fuzzy Setup complete...')

    return fuzzy


def runFuzzy(fuzzy, position, velocity):
    
    #Inserindo Dados de teste deve se usar a label definida
    fuzzy.input['position'] = position
    fuzzy.input['velocity'] = velocity

    fuzzy.compute()
    
    return fuzzy.output['output']
    
    
def threadAxisControl(axis):
    
    #Determina qual Eixo a Thread ira cuidar
    if axis == 'right':
        axisN = 0
    elif axis == 'up':
        axisN = 2
    else:
        axisN = 1
    
    name = 'Automated Docking: '+axis
    
    conn = krpc.connect(name,address='192.168.0.101', rpc_port=60000, stream_port=60001)
    vessel = conn.space_center.active_vessel
    current = None
    target = None
    manu = None
    
    #Iniciando Controlador Fuzzy
    fuzzy = startFuzzy()
    
    while True:

        current = conn.space_center.active_vessel.parts.controlling.docking_port
        target = conn.space_center.target_docking_port

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
            
    
try:
    # Connect to kRPC
    conn = krpc.connect(name='Asurada AP',address='192.168.0.101', rpc_port=60000, stream_port=60001)
    vessel = conn.space_center.active_vessel
    current = None
    target = None
    manu = None
    
    activeThread = 0
    
    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, '-- Docking Autopilot --')

        current = conn.space_center.active_vessel.parts.controlling.docking_port
        target = conn.space_center.target_docking_port

        if current is None:
            stdscr.addstr(2, 0, 'Awaiting control from docking port...')

        elif target is None:
            stdscr.addstr(2, 0, 'Awaiting target docking port...')

        else:
            
            
            #Travando Coordenadas do Alvo
            vessel.auto_pilot.reference_frame = vessel.orbital_reference_frame
            tgtdir = target.direction(vessel.orbital_reference_frame)
            vessel.auto_pilot.target_direction = [tgtdir[0]*-1, tgtdir[1]*-1, tgtdir[2]*-1]
            vessel.auto_pilot.target_roll = 180
            vessel.auto_pilot.engage()
            
            
            #Alvo Travado Iniciando Threads de Controle
            if activeThread == 0:
                _thread.start_new_thread( threadAxisControl,('up',))
                _thread.start_new_thread( threadAxisControl,('forward',))
                _thread.start_new_thread( threadAxisControl,('right',))
                activeThread = 1
            
            # Get positions, distances, velocities and
            # speeds relative to the target docking port
            current_position = current.position(target.reference_frame)
            velocity = current.part.velocity(target.reference_frame)

            # Get the docking port state
            if current.state == conn.space_center.DockingPortState.ready:
                state = 'Ready to dock'
            elif current.state == conn.space_center.DockingPortState.docked:
                state = 'Docked'
            elif current.state == conn.space_center.DockingPortState.docking:
                state = 'Docking...'
            else:
                state = 'Unknown'

            # Output information
            stdscr.addstr(2, 0, 'Current ship: {:30}'.format(current.part.vessel.name[:30]))
            stdscr.addstr(3, 0, 'Current port: {:30}'.format(current.part.title[:30]))
            stdscr.addstr(5, 0, 'Target ship:  {:30}'.format(target.part.vessel.name[:30]))
            stdscr.addstr(6, 0, 'Target port:  {:30}'.format(target.part.title[:30]))
            stdscr.addstr(8, 0, 'Raw Telemetry: {:10}'.format(state))
            stdscr.addstr(10, 0, '          +---------------------------+')
            stdscr.addstr(11, 0, '          |  Distance  |  Speed       |')
            stdscr.addstr(12, 0, '+---------+------------+--------------+')
            stdscr.addstr(13, 0, '|    X    |  {:>+6.2f} m  |  {:>+6.2f} m/s  |' #Left/Right +R
                          .format(current_position[0], velocity[0]))
            stdscr.addstr(14, 0, '|    Z    |  {:>+6.2f} m  |  {:>+6.2f} m/s  |' #Forward/Back +N
                          .format(current_position[1], velocity[1]))
            stdscr.addstr(15, 0, '|    Y    |  {:>+6.2f} m  |  {:>+6.2f} m/s  |' #Up/Down +I
                          .format(current_position[2], velocity[2]))
            stdscr.addstr(16, 0, '+---------+------------+--------------+')
            

        stdscr.refresh()

finally:
    # Shutdown curses
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()

 