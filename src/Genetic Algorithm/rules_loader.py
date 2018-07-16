#Rules Loader
import csv
import skfuzzy as fuzz
import skfuzzy.control as ctrl

#Plotter Import
import time
import numpy as np
import matplotlib.pyplot as plt

print("end")

def load_membership(rel_position, rel_velocity, rcs_output, file_path):

    #Fuzzy membership Functions
    
    #Loading Membership drom file
    
    with open(file_path) as member_file:
        member_csv = csv.reader(member_file, delimiter=',')
        number = 0
        for row in member_csv:
            
            if(number > 0 and number < 7):
                #print("Rel_position:")
                rel_position[row[0]] = fuzz.trimf(rel_position.universe, [int(row[1]),int(row[2]),int(row[3])])
                
            elif(number > 6 and number < 13):
                #print("Rel_velocity:")
                rel_velocity[row[0]] = fuzz.trimf(rel_velocity.universe, [int(row[1]),int(row[2]),int(row[3])])
            
            elif(number > 12 and number < 18):
                #print("RCS_output:")
                rcs_output[row[0]] = fuzz.trimf(rcs_output.universe, [int(row[1]),int(row[2]),int(row[3])])
            number = number + 1

def member_plot(file_path):

    #Input
    rel_position = []
    rel_velocity = []
    rcs_output = []

    position_range = np.arange(-800, 800, 1)
    velocity_range = np.arange(-50, 50, 1)
    rcs_out = np.arange(-2000, 2000, 1)


    with open(file_path) as member_file:
        member_csv = csv.reader(member_file, delimiter=',')
        number = 0
        for row in member_csv:
            
            if(number > 0 and number < 7):
                #print("Rel_position:")
                rel_position.append(fuzz.trimf(position_range, [int(row[1]),int(row[2]),int(row[3])]))
                
            elif(number > 6 and number < 13):
                #print("Rel_velocity:")
                rel_velocity.append(fuzz.trimf(velocity_range, [int(row[1]),int(row[2]),int(row[3])]))
            
            elif(number > 12 and number < 18):
                #print("RCS_output:")
                rcs_output.append(fuzz.trimf(rcs_out, [int(row[1]),int(row[2]),int(row[3])]))
            number = number + 1




        #Plotagem das Funções de Membership DATA BASE
        fig,(rel_pos, rel_vel, rcs_plot) = plt.subplots(nrows=3, figsize=(8,9))

        rel_pos.plot(position_range, rel_position[0], 'b', linewidth=1.5, label='POSITIVE_BIG')
        rel_pos.plot(position_range, rel_position[1], 'g', linewidth=1.5, label='POSITIVE_SMALL')
        rel_pos.plot(position_range, rel_position[2], 'r', linewidth=1.5, label='POSITIVE_CLOSE')
        rel_pos.plot(position_range, rel_position[3], 'c', linewidth=1.5, label='NEGATIVE_BIG')
        rel_pos.plot(position_range, rel_position[4], 'y', linewidth=1.5, label='NEGATIVE_SMALL')
        rel_pos.plot(position_range, rel_position[5], 'm', linewidth=1.5, label='NEGATIVE_CLOSE')
        rel_pos.set_title('Relative Position')
        rel_pos.legend()

        rel_vel.plot(velocity_range, rel_velocity[0], 'b', linewidth=1.5, label='POSITIVE_BIG')
        rel_vel.plot(velocity_range, rel_velocity[1], 'g', linewidth=1.5, label='POSITIVE_SMALL')
        rel_vel.plot(velocity_range, rel_velocity[2], 'r', linewidth=1.5, label='POSITIVE_CLOSE')
        rel_vel.plot(velocity_range, rel_velocity[3], 'c', linewidth=1.5, label='NEGATIVE_BIG')
        rel_vel.plot(velocity_range, rel_velocity[4], 'y', linewidth=1.5, label='NEGATIVE_SMALL')
        rel_vel.plot(velocity_range, rel_velocity[5], 'm', linewidth=1.5, label='NEGATIVE_CLOSE')
        rel_vel.set_title('Relative Velocity')
        rel_vel.legend()

        rcs_plot.plot(rcs_out, rcs_output[0], 'b', linewidth=1.5, label='POSITIVE_BIG')
        rcs_plot.plot(rcs_out, rcs_output[1], 'g', linewidth=1.5, label='POSITIVE_SMALL')
        rcs_plot.plot(rcs_out, rcs_output[2], 'r', linewidth=1.5, label='NO CHANGE')
        rcs_plot.plot(rcs_out, rcs_output[3], 'c', linewidth=1.5, label='NEGATIVE_SMALL')
        rcs_plot.plot(rcs_out, rcs_output[4], 'm', linewidth=1.5, label='NEGATIVE_BIG')
        rcs_plot.set_title('RCS Control(ms)')
        rcs_plot.legend()

        plt.tight_layout()
        plt.show()

#member_plot('Generations/membership0.csv')