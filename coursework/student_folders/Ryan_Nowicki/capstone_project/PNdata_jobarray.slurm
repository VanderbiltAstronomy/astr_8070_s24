#!/bin/bash
#
#SBATCH  -J arraytest # A single job name for the array
#SBATCH -n 1 # Number of cores
#SBATCH -p production # Run on the debug/production queue
#SBATCH -t 12:00:00 # Run time (hh:mm:ss)
#SBATCH -o arraytest.%j.%a.out # Standard output
#SBATCH -e arraytest.%j.%a.err # Standard error

#SBATCH --mail-user=ryan.nowicki@vanderbilt.edu
#SBATCH --constraint=zen
## mailtype begin, end, fail, all, time_limit_50, time_limit_80, time_limit_90
#SBATCH --mail-type=fail    # email me when the job fails
 
#module load Python3.7.12 #load python if not yet loaded

python mpar_gen.py #running python script to make files

##run the executable:
/home/nowickr/nbody/nowickr/PNevo/PNevo *idx"${SLURM_ARRAY_TASK_ID}".mpar 
##yourexecutable /data/username/yourdirectory inputfilename"${SLURM_ARRAY_TASK_ID}".param



##to run 30 jobs with inputfilename1.param through inputfilename30.param as your input files
## type the following into your command line: sbatch --array=1-30 arraytest.slurm

