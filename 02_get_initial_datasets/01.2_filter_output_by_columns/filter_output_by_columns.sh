#!/bin/bash

#---------------------------------------------------------------------------------
# Account information

#SBATCH --account=pi-kilianhuber # account you belong to 
#SBATCH --mail-user=jason.jia@chicagobooth.edu

#---------------------------------------------------------------------------------
# Resources requested (recommended parameters to specify)

#SBATCH --partition=highmem  # standard (default), long, gpu, mpi, highmem
#SBATCH --cpus-per-task=16     # number of CPUs requested (for parallel tasks)
#SBATCH --mem-per-cpu=4G     # requested memory
#SBATCH --time=1-00:00:00     # Time your job is allowed to run (d-hh:mm:ss)

#---------------------------------------------------------------------------------
# Array information

#SBATCH --array=1-16

#---------------------------------------------------------------------------------
# Job specific name (helps organize and track progress of jobs, optional parameters)
# '%A': array-job ID (e.g. 7823505)
# '%a': task ID (e.g. 1, 2, 3)
# '%J': job ID (e.g. 7823507, 7823506, 7823505)

#SBATCH --job-name=filteroutputbycolumns
#SBATCH --output=filteroutputbycolumns%A-%a-%J.out 

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

module load python/booth/3.6/3.6.12

# Go into env
source /home/jasonjia/standard_env_jason/bin/activate

#---------------------------------------------------------------------------------
# Commands to execute below...

# cd to /project/kh_mercury_1/boardex/code/filter_output_by_columns first, i.e. folder containing the .py and .sh files.
# Big command to enter on terminal (for Step 1): 
# sbatch filter_output_by_columns.sh filter_output_by_columns.py /project/kh_mercury_1/boardex/data/boardex_colstokeep/List_of_Variables_for_Boardex_and_Execucomp_310322.xlsx /project/kh_mercury_1/boardex/data/output /project/kh_mercury_1/boardex/data/output_filtered_by_columns 0

program_path="$1" # i.e. filter_output_by_columns.py
listofcols_path="$2"
input_folder="$3"
output_folder="$4"
get_only_characteristics_and_educationandachievements="$5"

echo "Program Path: $program_path"
echo "File path of .xslx containing list of columns in Boardex and ExecuComp: $listofcols_path"
echo "Input Folder: $input_folder"
echo "Output Folder: $output_folder"
echo "Get only 'Characteristics' and 'EducationandAchievements': $get_only_characteristics_and_educationandachievements"
echo "-----------------------------------------------------------"

srun python3 $program_path $SLURM_ARRAY_TASK_ID $SLURM_ARRAY_TASK_COUNT $listofcols_path $input_folder $output_folder $get_only_characteristics_and_educationandachievements

echo "Done!"
