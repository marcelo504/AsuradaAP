#Rules Loader

import csv
import skfuzzy as fuzz
import skfuzzy.control as ctrl



print("end")

def load_membership(rel_position, rel_velocity, rcs_output):

    #Fuzzy membership Functions
    
    #Loading Membership drom file
    
    with open('membership.csv') as member_file:
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
