"""
Script is designed to take in some supplied information about the layout of a room and a source of radiation and plot a map detailing the scatter radiation. 

Has functitonality for positioning of shielding in the path of the beam. 

The outputs are for presentation / instructional purposes only. Results are not guaranteed to be accurate. 
Transmission factors taken from BIR2012. 

Please check the documentation for instruction on plot layout.

Created by Ronan Coleman
v1.0.0 - 12/08/2021
"""


import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import math
import sys

room_width = int(input('Please input the width of the room (in cm): '))
room_length = int(input('Please input the length of the room (in cm): '))

source_location_x = int(input('Please input the distance of the source from the "left" wall (in cm): '))
source_location_y = int(input('Please input the distance of the source from the "bottom" wall (in cm): '))
source_location = np.array([source_location_y, source_location_x]) #inverted due to matrix notation

if source_location[0] > room_length:
    print(f'Source location out of bounds. Source Y position needs to be less than {room_length}.')
    sys.exit()
    
if source_location[1] > room_width:
    print(f'Source location out of bounds. Source X position needs to be less than {room_width}.')
    sys.exit()

source_size = int(input('Please input the source diameter (in cm): '))

scatter_reading = float(input('Please input the scatter reading (in µSv/hr): '))
scatter_distance = int(input('Please input the distance from the source the scatter reading was taken (in cm): '))

shield_yesno = input('Is a shield present in path of beam? (Input 0 for no shield and 1 for shield present.): ')
   
if shield_yesno == '0':
    print('Plotting basic scatter map now.')
    z = np.zeros([room_length, room_width])
    # Create index arrays to z
    I, J = np.meshgrid(np.arange(z.shape[0]), np.arange(z.shape[1]))
    # Calculate distance of all points to centre (transposed to keep frame the same)
    dist = np.sqrt((I - source_location[0])**2 + (J-source_location[1])**2).transpose()
    dose = ((scatter_distance + source_size/2)**2 / dist**2) * scatter_reading
    dose[np.where(dist<source_size/2)] = dose[np.where(dist==source_size/2)][0] #ensuring the source doesn't go to infinity dose.
    
    y_ratio = z.shape[1]/z.shape[0]
    x_size = 10
    plt.figure(figsize=(x_size, y_ratio * x_size))
    plt.imshow(dose, origin='lower', cmap='RdYlGn_r', norm=mpl.colors.LogNorm(), interpolation = 'gaussian')
    plt.axis('off')
    if z.shape[1] >= z.shape[0]:
        plt.colorbar(orientation='horizontal', label='Dose (µSv/hr)', pad = 0.0085)
    else:
        plt.colorbar(orientation='vertical', label='Dose (µSv/hr)', pad = 0.0085)
    filename = f"scatter_map_no_shield_{scatter_reading}µSvhr.png"
    plt.savefig(filename, bbox_inches='tight')
    
elif shield_yesno == '1':
    shield_pos_x = int(input('Please input the distance from the "left" wall to the start of the shield (in cm): '))
    shield_pos_y = int(input('Please input the distance from the "bottom" wall to the start of the shield (in cm): '))
    shield_length = int(input('Please input the length (in cm) of the shield: '))
    shield_angle = int(input('Please input the angle (in degrees) of the shield normal to the "bottom" wall: '))
    shield_code = input('Please input the code of shielding in place. (Eg. type 3 for Code 3 shielding): ')
    kvp_est = int(input('Please input the estimated energy of radiation (kVp) from the following: 30, 50, 70, 85, 90, 100, 125, 140: '))
    
    z = np.zeros([room_length, room_width])
    # Create index arrays to z
    I, J = np.meshgrid(np.arange(z.shape[0]), np.arange(z.shape[1]))
    # Calculate distance of all points to centre (transposed to keep frame the same)
    dist = np.sqrt((I - source_location[0])**2 + (J-source_location[1])**2).transpose()
    shield_angle_rad = math.radians(shield_angle)
    shield_pos_start = np.array([shield_pos_x, shield_pos_y])
    
    if shield_angle == 90:
        shield_pos_end_x = shield_pos_start[0]
        shield_pos_end_y = shield_pos_start[1] + shield_length
    if shield_angle == 180 or shield_angle ==0:
        shield_pos_end_x = shield_pos_start[0] + shield_length
        shield_pos_end_y = shield_pos_start[1]
    else:
        shield_pos_end_x = int(round(shield_length * np.cos(shield_angle_rad) + shield_pos_start[0]))
        shield_pos_end_y = int(round(shield_length * np.sin(shield_angle_rad) + shield_pos_start[1]))
        shield_pos_end = np.array([shield_pos_end_x, shield_pos_end_y])

    shield_slope = (shield_pos_end[1] - shield_pos_start[1]) / (shield_pos_end[0] - shield_pos_start[0])
    shield_line_constant = shield_pos_start[1] - (shield_slope * shield_pos_start[0])

    def shield_line(x):
        if np.isnan(shield_slope):
            return(shield_pos_end[1])
        else:
            return int(round(shield_slope*x + shield_line_constant))

    shield_x_boundary = np.array([shield_pos_start[0], shield_pos_end[0]])
    shield_y_boundary = np.array([shield_pos_start[1], shield_pos_end[1]])
    #i is y and j is x!
    for i in range(z.shape[0]):
        for j in range(z.shape[1]):
            if np.isinf(shield_slope):
                if j == shield_pos_start[0] and i > np.min(shield_y_boundary) and i < np.max(shield_y_boundary):
                    z[i,j] = 2
            else:
                if i == shield_line(j) and j > np.min(shield_x_boundary) and j < np.max(shield_x_boundary):
                    z[i,j] = 2
                    
    source_slope = shield_slope
    source_constant = source_location[0] - (source_slope * source_location[1])

    def source_line(x):
        if np.isnan(source_slope):
            return(source_location[1])
        else:
            return int(round(source_slope * x + source_constant))

    source_edge = []
    for i in range(z.shape[0]):
        for j in range(z.shape[1]):
            if np.isinf(source_slope):
                if abs(i-source_location[0]) == source_size/2 and j == source_location[1]:
                    source_edge.append([j, i])
            else:
                if round(np.sqrt((j-source_location[1])**2+(i-source_location[0])**2)) == source_size/2 and abs(i - source_line(j)) <=1:
                    source_edge.append([j, i])
                    print(j, i)
                    if len(source_edge) > 2:
                        print("Warning: Only two sets of points should be found for source edge. Dumping extras")
                        source_edge = [source_edge[0], source_edge[-1]]

    for i in range(z.shape[0]):
        for j in range(z.shape[1]):
            if np.isinf(source_slope):
                if (j == source_location[1]) and (i < source_location[0] + source_size/2) and (i > source_location[0] - source_size/2):
                    z[i, j] = 3
            else:
                if abs(i - source_line(j)) <=1 and j > np.min([source_edge[0][0], source_edge[1][0]]) and j < np.max([source_edge[0][0], source_edge[1][0]]):
                    z[i, j] = 3

    #if vertical, start will always be the first result, which should be the number closest to 0 
    if source_edge[0][0] > source_edge[1][0]:
        source_pos_end = source_edge[0]
        source_pos_start = source_edge[1]
    else:
        source_pos_end = source_edge[1]
        source_pos_start = source_edge[0]      

    if np.isinf(source_slope):
        if shield_pos_start[0] > source_pos_start[0]:
            layout = 1
        else: 
            layout = 2

    elif shield_pos_start[1] > source_line(shield_pos_start[0]):
        layout = 3
    else:
        layout = 4        

        
        
    ray_1a_slope = ((shield_pos_start[1] - source_pos_start[1]) / (shield_pos_start[0] - source_pos_start[0]))
    ray_1b_slope = ((shield_pos_end[1] - source_pos_start[1]) / (shield_pos_end[0] - source_pos_start[0]))
    ray_2a_slope = ((shield_pos_start[1] - source_pos_end[1]) / (shield_pos_start[0] - source_pos_end[0]))
    ray_2b_slope = ((shield_pos_end[1] - source_pos_end[1]) / (shield_pos_end[0] - source_pos_end[0]))

    ray_1a_constant = source_pos_start[1] - (ray_1a_slope * source_pos_start[0])
    ray_1b_constant = source_pos_start[1] - (ray_1b_slope * source_pos_start[0])
    ray_2a_constant = source_pos_end[1] - (ray_2a_slope * source_pos_end[0])
    ray_2b_constant = source_pos_end[1] - (ray_2b_slope * source_pos_end[0])

    def ray_1a_line(x):
        return int(round(ray_1a_slope * x + ray_1a_constant))
    def ray_1b_line(x):
        return int(round(ray_1b_slope * x + ray_1b_constant))
    def ray_2a_line(x):
        return int(round(ray_2a_slope * x + ray_2a_constant))
    def ray_2b_line(x):
        return int(round(ray_2b_slope * x + ray_2b_constant))

    if layout == 1:
        for i in range(z.shape[0]):
            for j in range(z.shape[1]):
                if i == ray_1a_line(j) or i == ray_1b_line(j) or i == ray_2a_line(j) or i == ray_2b_line(j):                    
                    if j < source_pos_start[0]:
                        continue
                    else:    
                        z[i,j] = 3

    elif layout == 2:
        for i in range(z.shape[0]):
            for j in range(z.shape[1]):
                if i == ray_1a_line(j) or i == ray_1b_line(j) or i == ray_2a_line(j) or i == ray_2b_line(j):                    
                    if j > source_pos_start[0]:
                        continue
                    else:    
                        z[i,j] = 3 

    elif layout == 3:
        for i in range(z.shape[0]):
            for j in range(z.shape[1]):
                if i == ray_1a_line(j) or i == ray_1b_line(j) or i == ray_2a_line(j) or i == ray_2b_line(j):                    
                    if i < source_line(j):
                        continue
                    else:
                        z[i,j] = 3
    else:
        for i in range(z.shape[0]):
            for j in range(z.shape[1]):
                if i == ray_1a_line(j) or i == ray_1b_line(j) or i == ray_2a_line(j) or i == ray_2b_line(j):                    
                    if i > source_line(j):
                        continue
                    else:
                        z[i,j] = 3
                        

    # if shield is vertical and to the right of source
    if np.isinf(shield_slope) and layout == 1:
        for i in range(z.shape[0]):
            for j in range(z.shape[1]):
                if j > shield_pos_start[0] and i > ray_1a_line(j) and i < ray_2b_line(j):
                    z[i,j] = 4

    #if shield is vertical and to the left of the source                
    if np.isinf(shield_slope) and layout == 2:
        for i in range(z.shape[0]):
            for j in range(z.shape[1]):
                if j < shield_pos_start[0] and i > ray_1a_line(j) and i < ray_2b_line(j):
                    z[i,j] = 4

    #if shield is horizontal and above the source
    if np.isnan(shield_slope) and layout == 3:
        for i in range(z.shape[0]):
            for j in range(z.shape[1]):
                if i > shield_line(j) and i > ray_1a_line(j) and i < ray_2b_line(j):
                    z[i,j] = 4

    #if shield is horizontal and below the source
    if np.isnan(shield_slope) and layout == 4:
        for i in range(z.shape[0]):
            for j in range(z.shape[1]):
                if i < shield_line(j) and i > ray_1a_line(j) and i < ray_2b_line(j):
                    z[i,j] = 4

    #if shield is angled and above source                
    if layout == 3:
        for i in range(z.shape[0]):
            for j in range(z.shape[1]):
                if i > shield_line(j) and i > ray_1a_line(j) and i < ray_2b_line(j):
                    z[i,j] = 4

    #if shield is angled and below source                
    if layout == 4:
        for i in range(z.shape[0]):
            for j in range(z.shape[1]):
                if i < shield_line(j) and i > ray_1a_line(j) and i < ray_2b_line(j):
                    z[i,j] = 4    
    
    lead_code = {'3':1.32,
            '4':1.8,
            '5':2.24,
            '6':2.65,
            '7':3.15,
            '8':3.55}
    
    lead_coeff = {30: {'alpha':38.79,
                  'beta':180,
                  'gamma':0.356},
             50: {'alpha':8.801,
                 'beta':27.28,
                 'gamma':0.296},
             70: {'alpha':5.369,
                 'beta':23.49,
                 'gamma':0.588},
             85: {'alpha':3.5504,
                 'beta':20.37,
                 'gamma':0.7555},
             90: {'alpha':3.067,
                 'beta':18.83,
                 'gamma':0.773},
             100: {'alpha':2.507,
                 'beta':15.33,
                 'gamma':0.912},
             125: {'alpha':2.233,
                 'beta':7.89,
                 'gamma':0.73},
             140: {'alpha':2.009,
                 'beta':3.99,
                 'gamma':0.342}}
    
    def transmission(pb_code, kvp):
        import math
        lead_thickness = lead_code[pb_code]
        alpha = lead_coeff[kvp]['alpha']
        beta = lead_coeff[kvp]['beta']
        gamma = lead_coeff[kvp]['gamma']

        step_1 = (math.exp(lead_thickness * alpha * gamma)) * (1 + (beta/alpha))
        step_2 = step_1 - (beta/alpha)
        step_3 = step_2**(-1/gamma)
        return step_3
    
    
    dose = ((scatter_distance + source_size/2)**2 / dist**2) * scatter_reading
    dose[np.where(dist<source_size/2)] = dose[np.where(dist==source_size/2)][0]
    dose[np.where(z==4)] = dose[np.where(z==4)] * transmission(shield_code, kvp_est)
    
    y_ratio = z.shape[1]/z.shape[0]
    x_size = 10
    plt.figure(figsize=(x_size, y_ratio * x_size))
    plt.imshow(dose, origin='lower', cmap='RdYlGn_r', norm=mpl.colors.LogNorm(), interpolation = 'gaussian')
    plt.axis('off')
    if z.shape[1] >= z.shape[0]:
        plt.colorbar(orientation='horizontal', label='Dose (µSv/hr)', pad = 0.0085)
    else:
        plt.colorbar(orientation='vertical', label='Dose (µSv/hr)', pad = 0.0085)
    filename = f"scatter_map_leadshield_{scatter_reading}µSvhr.png"
    plt.savefig(filename, bbox_inches='tight')
else:
    print(f'Error: Expected 0 or 1 for variable shield_yesno. Recieved {shield_yesno}. Try running the program again.')
    
    