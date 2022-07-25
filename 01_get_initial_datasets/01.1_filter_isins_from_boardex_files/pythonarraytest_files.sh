#!/bin/bash

#---------------------------------------------------------------------------------
# Account information

#SBATCH --account=pi-kilianhuber # account you belong to 
#SBATCH --mail-user=jason.jia@chicagobooth.edu

#---------------------------------------------------------------------------------
# Resources requested (recommended parameters to specify)

#SBATCH --partition=standard  # standard (default), long, gpu, mpi, highmem
#SBATCH --cpus-per-task=8     # number of CPUs requested (for parallel tasks)
#SBATCH --mem-per-cpu=2G     # requested memory
#SBATCH --time=1-00:00:00     # Time your job is allowed to run (d-hh:mm:ss)

#---------------------------------------------------------------------------------
# Array information

#SBATCH --array=1-8

#---------------------------------------------------------------------------------
# Job specific name (helps organize and track progress of jobs, optional parameters)
# '%A': array-job ID (e.g. 7823505)
# '%a': task ID (e.g. 1, 2, 3)
# '%J': job ID (e.g. 7823507, 7823506, 7823505)

#SBATCH --job-name=pythonarraytest
#SBATCH --output=pythonarraytest%A-%a-%J.out 

#---------------------------------------------------------------------------------
# Print some useful variables

echo "-------------------------------------------"
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
program_path="$1"
input_dir="$2"
output_dir="$3"
echo "Program Path: $program_path"
echo "Input Directory: $input_dir"
echo "Output Directory: $output_dir"
echo "-------------------------------------------"

srun python3 $program_path $SLURM_ARRAY_TASK_ID $SLURM_ARRAY_TASK_COUNT $input_dir $output_dir

echo "Done!"
