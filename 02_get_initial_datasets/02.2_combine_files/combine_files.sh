#!/bin/bash

#---------------------------------------------------------------------------------
# Account information

#SBATCH --account=pi-kilianhuber # account you belong to 
#SBATCH --mail-user=jason.jia@chicagobooth.edu

#---------------------------------------------------------------------------------
# Resources requested (recommended parameters to specify)

#SBATCH --partition=highmem  # standard (default), long, gpu, mpi, highmem
#SBATCH --cpus-per-task=1     # number of CPUs requested (for parallel tasks)
#SBATCH --mem-per-cpu=128G     # requested memory
#SBATCH --time=2-00:00:00     # Time your job is allowed to run (d-hh:mm:ss)

#---------------------------------------------------------------------------------
# Array information

# #SBATCH --array=1-64

#---------------------------------------------------------------------------------
# Job specific name (helps organize and track progress of jobs, optional parameters)
# '%A': array-job ID (e.g. 7823505)
# '%a': task ID (e.g. 1, 2, 3)
# '%J': job ID (e.g. 7823507, 7823506, 7823505)

#SBATCH --job-name=combine_files
#SBATCH --output=out/combine_files-%J.out 

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
# sbatch combine_files.sh combine_files.py /project/kh_mercury_1/manager_and_board_characteristics/output/02_get_initial_datasets/02.1_boardex_filtered_by_columns_and_rows /project/kh_mercury_1/manager_and_board_characteristics/output/02_get_initial_datasets/02.2_boardex_combined /project/kh_mercury_1/manager_and_board_characteristics/output/02_get_initial_datasets/02.2_boardex_director_smde_map/director_smde_map_010523.xlsx

# Command used for testing (using a test folder than contains most files + only the first 5 rows of each file):
# sbatch combine_files.sh combine_files.py /project/kh_mercury_1/manager_and_board_characteristics/output/02_get_initial_datasets/02.1_boardex_filtered_by_columns_and_rows/first_five_rows /project/kh_mercury_1/manager_and_board_characteristics/output/02_get_initial_datasets/02.2_boardex_combined/test /project/kh_mercury_1/manager_and_board_characteristics/output/02_get_initial_datasets/02.2_boardex_director_smde_map/director_smde_map_010523.xlsx

program_path="$1" # i.e. combine_files.py
input_folder="$2"
output_folder="$3"
director_smde_map="$4"

echo "Program Path: $program_path"
echo "Input Folder: $input_folder"
echo "Output Folder: $output_folder"
echo "Filepath to director-smde-rootname map: $director_smde_map"
echo "-----------------------------------------------------------"

srun python3 $program_path $input_folder $output_folder $director_smde_map

echo "Done!"
