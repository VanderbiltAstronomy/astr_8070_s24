#GENERATING MPARS FROM INPUT ARRAY

#import tools
import numpy as np

#-----------------------
#parameter arrays: adjust this as you see fit
q       = [4,5,6,7,8,9,10,11]
S1mag   = [0.1,0.3,0.5,0.7,0.9,0.99]
beta    = [120, 150, 160, 170, 175]#, 180]
     ###alpha = [-90,-45,0,45,90]

#TESTS
#q = [4,5]
#S1mag = [0.7]
#beta = [120]

#output:
#R(L=S)
n_points = len(q)*len(S1mag)*len(beta)#*len(alpha)
print(n_points)

#creating all points to test over
qgrid, S1grid, betagrid = np.meshgrid(q,S1mag,beta)
fullgrid = np.vstack((qgrid.flatten(),S1grid.flatten(),betagrid.flatten())).T
print(fullgrid.shape)
#print(fullgrid[:2])

#convert mag, angle, angle to xyz components of spin
def angle_to_components(mag,Z,X=0): #feed angles in degrees; Z is angle from z axis, X is angle from x axis
    Zrad = Z*np.pi/180
    Xrad = X*np.pi/180
    Sz = mag*np.cos(Zrad) #z component of spin

    mag_xy = mag*np.sin(Zrad)
    Sx = mag_xy*np.cos(Xrad) #x component of spin
    Sy = mag_xy*np.sin(Xrad) #y component of spin

    return Sx, Sy, Sz
    
#converting test points to form needed for input in mpar files
param_in = []
for i in range(len(fullgrid)):
    qn = fullgrid[i,0]
    Sx, Sy, Sz= angle_to_components(fullgrid[i,1],fullgrid[i,2])
    param_in.append([qn,Sx,Sy,Sz])
#print(S_input)
param_in = np.array(param_in)
#print(param.shape)

#-----------------------

# Define the values of M and Q
#M_values = [10, 20]
#Q_values = [1, 2, 3, 4]
#Q_values = param[:,0]
#Sx_values = param[:,1]
#Sy_values = param[:,2]
#Sz_values = param[:,3]

# Define the folder where you want to save the text files
folder_path = "/home/nowickr/nbody/nowickr/PNevo/mpars_for_astr8070/"

# Create the folder if it does not exist
import os
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# Iterate through each combination of M and Q
for i in range(len(param_in)):
    #define parameters
    Q = param_in[i,0]
    Sx = param_in[i,1]
    Sy = param_in[i,2]
    Sz = param_in[i,3]

    # Create the file name based on values
    file_name = f"q{Q:.1f}_s{Sx:.4f}_{Sy:.4f}_{Sz:.4f}_idx{i+1}.mpar"

    # Define the file path for the current combination of M and Q
    file_path = os.path.join(folder_path, file_name)

    # Open the file in write mode
    with open(file_path, "w") as file:
                    # Write the header
                    file.write(f"par.initial_sep = 150.0\n")
                    file.write(f"par.final_sep = 11.0\n")
                    file.write(f"par.MM = 1.0\n")
                    file.write(f"par.mass_ratio = {Q}\n")
                    file.write(f"par.a1x = {Sx}\n")
                    file.write(f"par.a1y = {Sy}\n")
                    file.write(f"par.a1z = {Sz}\n")
                    file.write(f"par.a2x = 0.0\n")
                    file.write(f"par.a2y = 0.0\n")
                    file.write(f"par.a2z = 0.0\n")
                    file.write(f"par.manual_p0 = 0\n")
                    file.write(f"par.px0 = 0.0\n")
                    file.write(f"par.py0 = 0.0\n")
                    file.write(f"par.pz0 = 0.0\n")
                    file.write(f"par.fixed_dt = 0\n")
                    file.write(f"par.dtfac = 25.0\n")
                    file.write(f"par.spinspin = 1\n")
                    file.write(f"par.radrxn = 1\n")
                    file.write(f"par.out_time = 10\n")
                    file.write(f"par.out_baum_file = 1\n")
                    file.write(f"par.out_rpar_head = 1\n")
                    file.write("\n")

    #You can add additional content or leave it blank as needed
    print(f"Data has been saved to {file_path}")

#-----------------------
#Inline comments do not always work, so be careful. Stick to separate lines if you can.
#New IO functions let you be flexible with whitespace, ordering of declarations, and new and improved error messages.
#
############################
#Documentation
############################
#par.initial_sep   : Separation of black holes at the start of the simulation (number of orbits)
#par.final_sep     : Separation of black holes when simulation is haulted
#par.MM            : normalized mass, M0
#par.mass_ratio    : M1/M2, always make mass_ratio >= 1
#par.a1x           : a1 and a2 are dimensionless spin vectors for each black hole. Make sure the vector has |a|<1
#par.a1y           : ^
#par.a1z           : ^
#par.a2x           : ^
#par.a2y           : ^
#par.a2z           : ^
#par.manual_p0     : 
#par.px0           : momentum of center of mass. Set to zero for almost all cases
#par.py0           : ^
#par.pz0           : ^
#par.fixed_dt      : 
#par.dtfac         : looking at [dtfac]M in time and changing fixed_dt each time
#par.spinspin      : spin correlation term (spin spin PN): keep it at 1 
#par.radrxn        : radiation reaction (causes orbit shrinkage): keep at 1
#par.out_time      : which iteration is kept as ascii output
#par.out_baum_file : 
#par.out_rpar_head : 
#-----------------------

