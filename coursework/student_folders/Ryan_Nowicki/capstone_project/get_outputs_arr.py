##WITH FILES, READ OUTPUT AND SAVE TO NEW DATA ARRAY
import os
import numpy as np
import sys

#######################################################
#DEFINING NEEDED FUNCTIONS
#put data into its corresponding columns
def PNEvoColumnGet(PN_data):
        #split data into columns
        #time data
        t = PN_data[:,1]
        #position data
        x = PN_data[:,2]
        y = PN_data[:,3]
        z = PN_data[:,4]
        #momentum data
        px = PN_data[:,5]
        py = PN_data[:,6]
        pz = PN_data[:,7]
        #spin data
        S1x = PN_data[:,8]
        S1y = PN_data[:,9]
        S1z = PN_data[:,10]
        S2x = PN_data[:,11]
        S2y = PN_data[:,12]
        S2z = PN_data[:,13]
        return t,x,y,z,px,py,pz,S1x,S1y,S1z,S2x,S2y,S2z

#orbital angular momentum calculator (Newtonian)
def L_calc(x,y,z,px,py,pz):
        Lx = y*pz - z*py
        Ly = z*px - x*pz
        Lz = x*py - y*px
        Lmag = (Lx**2 + Ly**2 + Lz**2)**(1/2)
        return Lmag, Lx,Ly,Lz
    
#function that will take read-in data and return output
def read_and_output(idx):
    # Parent directory containing subdirectories
    parent_directory = f"/home/nowickr/nbody/nowickr/PNevo/mpars_for_astr8070/"
    #parent_directory = f"/home/nowickr/pnevo/PNevo/astr8070/MPARs_for_Project/"
    sub_directory = "" #f"*idx{idx}/" ############################################################################ idk if this will work
    # Directory to collect outputs
    np_directory = f"{parent_directory}npy_outputs/"
    # Specific filename ending
    file_extension = f"{idx}.asc"  # Change this to your desired file extension

    #Generate empty array that can take desired output values
    output_list = []
    print('Ready to Iterate')

    # Iterate over each subdirectory in the parent directory
    for root, dirs, files in os.walk(os.path.join(parent_directory, sub_directory)):
        # Iterate over each file in the current subdirectory
        for filename in files:
            # Check if the file has the desired file extension
            if filename.endswith(file_extension):
                # Construct the full path to the file
                file_path = os.path.join(root, filename)

                #read data
                sim_data = np.loadtxt(file_path)
                #read in variables
                t,x,y,z,px,py,pz,S1x,S1y,S1z,S2x,S2y,S2z = PNEvoColumnGet(sim_data)

                #compute L and S over time
                Lmag, Lx,Ly,Lz = L_calc(x,y,z,px,py,pz)
                Sx = S1x + S2x
                Sy = S1y + S2y
                Sz = S1z + S2z
                Smag = (Sx**2 + Sy**2 + Sz**2)**(1/2)

                #separation
                r = np.sqrt(x**2 + y**2 + z**2)

                #USING WHERE Lmag GOES FROM GREATER THAN TO LESS THAN Smag           
                R_tsp = np.nan
                for i in range(len(Lmag)-1):
                    if Lmag[i]>Smag[i] and Lmag[i+1]<Smag[i+1]:
                        R_tsp = r[i+1]         #separation at which spin flipping occurs
                        #print('Yay!', R_tsp, filename)
                        pass
                    else:
                        pass
                print(R_tsp, filename)

                #append list with R_tsp value (real or None)
                output_list.append([Smag[0], R_tsp])

                #with list of R_tsp values, output_array, make an array
                outputs_arr = np.array([output_list]).T

                #Save array as .npy file                                                                                                                                                                                    
                np.save(f'{np_directory}outputs_arr_{idx}.npy',outputs_arr)
                print(f"Outputs have been saved as .npy to {np_directory}outputs_arr_{idx}.npy")

##sim_data = np.loadtxt("%s"%folder_path+"%s"%file_name.removesuffix('.mpar')+"/%s"%file_name.removesuffix('.mpar')+".asc")

###############################################################
###############################################################
#MAIN
#reading in argument
if len(sys.argv)==2:
     idx=sys.argv[1]
     #run function to get output
     read_and_output(idx=idx)
else:
     raise ValueError("Expected 1 Additional Argument, %i Additional Arguments Received Instead" %(len(sys.argv)-1))
###############################################################
###############################################################
