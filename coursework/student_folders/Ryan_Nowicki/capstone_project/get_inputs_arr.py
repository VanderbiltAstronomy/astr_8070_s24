#GENERATING .NPY INPUT ARRAY

#import tools
import numpy as np

#-----------------------
#parameter arrays: adjust this as you see fit
q       = [4,5,6,7,8,9,10,11]
S1mag   = [0.1,0.3,0.5,0.7,0.9,0.99]
beta    = [120, 150, 160, 170, 175]

#creating all points to test over
qgrid, S1grid, betagrid = np.meshgrid(q,S1mag,beta)
inputs_arr = np.vstack((qgrid.flatten(),S1grid.flatten(),betagrid.flatten())).T

#-----------------------
# Define the folder where you want to save the text files
folder_path = "/home/nowickr/nbody/nowickr/PNevo/mpars_for_astr8070/"

# Create the folder if it does not exist
import os
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

#Save array as .npy file
np.save('inputs_arr.npy',inputs_arr)
print(f"Inputs have been saved as .npy to {folder_path}/inputs_arr.npy")

#-----------------------
