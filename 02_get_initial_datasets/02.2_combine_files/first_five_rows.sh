#!/bin/bash

#---------------------------------------------------------------------------------
# Account information

#SBATCH --account=pi-kilianhuber # account you belong to 
#SBATCH --mail-user=jason.jia@chicagobooth.edu

#---------------------------------------------------------------------------------
# Resources requested (recommended parameters to specify)

#SBATCH --partition=standard  # standard (default), long, gpu, mpi, highmem
#SBATCH --cpus-per-task=1     # number of CPUs requested (for parallel tasks)
#SBATCH --mem-per-cpu=4G     # requested memory
#SBATCH --time=1-00:00:00     # Time your job is allowed to run (d-hh:mm:ss)

#---------------------------------------------------------------------------------
# Array information

# #SBATCH --array=1-64

#---------------------------------------------------------------------------------
# Job specific name (helps organize and track progress of jobs, optional parameters)
# '%A': array-job ID (e.g. 7823505)
# '%a': task ID (e.g. 1, 2, 3)
# '%J': job ID (e.g. 7823507, 7823506, 7823505)

#SBATCH --job-name=first_five_rows
#SBATCH --output=out/first_five_rows-%J.out 

#---------------------------------------------------------------------------------
# Print some useful variables

echo "-----------------------------------------------------------"
echo "Output from Shell Script:"
echo "Job ID: $SLURM_JOB_ID"
echo "Job User: $SLURM_JOB_USER"
echo "Num Cores: $SLURM_JOB_CPUS_PER_NODE"
echo "Array(Task ID): $SLURM_ARRAY_TASK_ID of $SLURM_ARRAY_TASK_COUNT"

#---------------------------------------------------------------------------------
# Load necessary modules for the job

module load python/booth/3.8
pip install openpyxl

# Go into env
# source /home/jasonjia/standard_env_jason/bin/activate

#---------------------------------------------------------------------------------
# Commands to execute below...

# cd to /project/kh_mercury_1/manager_and_board_characteristics/code/02_get_initial_datasets/02.2_combine_files first, i.e. folder containing the .py and .sh files.
# Big command to enter on terminal: 
# sbatch first_five_rows.sh first_five_rows.py /project/kh_mercury_1/manager_and_board_characteristics/output/02_get_initial_datasets/02.1_boardex_filtered_by_columns_and_rows /project/kh_mercury_1/manager_and_board_characteristics/output/02_get_initial_datasets/02.1_boardex_filtered_by_columns_and_rows/first_five_rows

program_path="$1" # i.e. first_five_rows.py
input_folder="$2"
output_folder="$3"

echo "Program Path: $program_path"
echo "Input Folder: $input_folder"
echo "Output Folder: $output_folder"
echo "-----------------------------------------------------------"

srun python3 $program_path $input_folder $output_folder

echo "Done!"
