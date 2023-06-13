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

#SBATCH --array=1-64

#---------------------------------------------------------------------------------
# Job specific name (helps organize and track progress of jobs, optional parameters)
# '%A': array-job ID (e.g. 7823505)
# '%a': task ID (e.g. 1, 2, 3)
# '%J': job ID (e.g. 7823507, 7823506, 7823505)

#SBATCH --job-name=filterboardexbycolumnsandrows
#SBATCH --output=out/filterboardexbycolumnsandrows%A-%a-%J.out 

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

# cd to /project/kh_mercury_1/manager_and_board_characteristics/code/02_get_initial_datasets/01.2_filter_output_by_columns first, i.e. folder containing the .py and .sh files.
# Big command to enter on terminal: 
# sbatch filter_boardex_by_columns_and_rows.sh filter_boardex_by_columns_and_rows.py /project/kh_mercury_1/manager_and_board_characteristics/output/02_get_initial_datasets/02.1_boardex_colstokeep/List_of_Variables_for_Boardex_and_Execucomp_010523.xlsx /project/kh_mercury_1/manager_and_board_characteristics/output/01_convert_isins_and_gvkeys_to_boardex_companyids/companyids_to_search_for/companyids_to_search_for.xlsx /project/kh_mercury_1/manager_and_board_characteristics/data/boardex /project/kh_mercury_1/manager_and_board_characteristics/output/02_get_initial_datasets/02.1_boardex_filtered_by_columns_and_rows

program_path="$1" # i.e. filter_boardex_by_columns_and_rows.py
listofcols_path="$2"
companyid_listpath="$3"
input_folder="$4"
output_folder="$5"

echo "Program Path: $program_path"
echo "Filepath of .xslx containing list of columns in Boardex and ExecuComp: $listofcols_path"
echo "Filepath to list of company IDs we want to filter by: $companyid_listpath"
echo "Input Folder: $input_folder"
echo "Output Folder: $output_folder"
echo "-----------------------------------------------------------"

srun python3 $program_path $SLURM_ARRAY_TASK_ID $SLURM_ARRAY_TASK_COUNT $listofcols_path $companyid_listpath $input_folder $output_folder

echo "Done!"
