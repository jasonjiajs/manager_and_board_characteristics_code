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

#---------------------------------------------------------------------------------
# Job specific name (helps organize and track progress of jobs, optional parameters)
# '%A': array-job ID (e.g. 7823505)
# '%a': task ID (e.g. 1, 2, 3)
# '%J': job ID (e.g. 7823507, 7823506, 7823505)

#SBATCH --job-name=filterdatabyrowsstarter
#SBATCH --output=out/filterdatabyrowsstarter-%J.out 

#---------------------------------------------------------------------------------
# Print some useful variables

echo "-------------------------------------------"
echo "Job ID: $SLURM_JOB_ID"
echo "Job User: $SLURM_JOB_USER"
echo "Num Cores: $SLURM_JOB_CPUS_PER_NODE"

#---------------------------------------------------------------------------------
# Load necessary modules for the job

module load python/booth/3.8
pip install openpyxl

# Go into env
# source /home/jasonjia/standard_env_jason/bin/activate

#---------------------------------------------------------------------------------
# cd to folder containing code: cd /project/kh_mercury_1/manager_and_board_characteristics/code/02_get_initial_datasets/01.1_filter_isins_from_boardex_files
# Big command to enter on terminal: sbatch filter_data_by_rows_starter.sh filter_data_by_rows.sh filter_data_by_rows.py /project/kh_mercury_1/manager_and_board_characteristics/output/02_get_initial_datasets/output_filtered_by_rows /project/kh_mercury_1/manager_and_board_characteristics/output/01_convert_isins_and_gvkeys_to_boardex_companyids/companyids_to_search_for/companyids_to_search_for.xlsx

# Commands to execute below...
shell_program_path="$1" 
python_program_path="$2"
output_dir="$3"
companyid_listpath="$4"
echo "Shell Program Path: $shell_program_path"
echo "Python Program Path: $python_program_path"
echo "Output Directory: $output_dir"
echo "Filepath to list of company IDs we want to filter by: $companyid_listpath"
echo "-------------------------------------------"

# Europe
sbatch $shell_program_path $python_program_path /project/kh_mercury_1/manager_and_board_characteristics/data/boardex/europe_compensation $output_dir $companyid_listpath
sbatch $shell_program_path $python_program_path /project/kh_mercury_1/manager_and_board_characteristics/data/boardex/europe_companynetwork $output_dir $companyid_listpath
sbatch $shell_program_path $python_program_path /project/kh_mercury_1/manager_and_board_characteristics/data/boardex/europe_smallfiles $output_dir $companyid_listpath
sbatch $shell_program_path $python_program_path /project/kh_mercury_1/manager_and_board_characteristics/data/boardex/europe_network/europe_network1 $output_dir $companyid_listpath
sbatch $shell_program_path $python_program_path /project/kh_mercury_1/manager_and_board_characteristics/data/boardex/europe_network/europe_network2 $output_dir $companyid_listpath
sbatch $shell_program_path $python_program_path /project/kh_mercury_1/manager_and_board_characteristics/data/boardex/europe_network/europe_network3 $output_dir $companyid_listpath
sbatch $shell_program_path $python_program_path /project/kh_mercury_1/manager_and_board_characteristics/data/boardex/europe_network/europe_network4 $output_dir $companyid_listpath
sbatch $shell_program_path $python_program_path /project/kh_mercury_1/manager_and_board_characteristics/data/boardex/europe_network/europe_network5 $output_dir $companyid_listpath

# North America
sbatch $shell_program_path $python_program_path /project/kh_mercury_1/manager_and_board_characteristics/data/boardex/na_compensation $output_dir $companyid_listpath
sbatch $shell_program_path $python_program_path /project/kh_mercury_1/manager_and_board_characteristics/data/boardex/na_companynetwork $output_dir $companyid_listpath
sbatch $shell_program_path $python_program_path /project/kh_mercury_1/manager_and_board_characteristics/data/boardex/na_smallfiles $output_dir $companyid_listpath
sbatch $shell_program_path $python_program_path /project/kh_mercury_1/manager_and_board_characteristics/data/boardex/na_network/na_network_1 $output_dir $companyid_listpath
sbatch $shell_program_path $python_program_path /project/kh_mercury_1/manager_and_board_characteristics/data/boardex/na_network/na_network_2 $output_dir $companyid_listpath
sbatch $shell_program_path $python_program_path /project/kh_mercury_1/manager_and_board_characteristics/data/boardex/na_network/na_network_3 $output_dir $companyid_listpath
sbatch $shell_program_path $python_program_path /project/kh_mercury_1/manager_and_board_characteristics/data/boardex/na_network/na_network_4 $output_dir $companyid_listpath
sbatch $shell_program_path $python_program_path /project/kh_mercury_1/manager_and_board_characteristics/data/boardex/na_network/na_network_5 $output_dir $companyid_listpath
sbatch $shell_program_path $python_program_path /project/kh_mercury_1/manager_and_board_characteristics/data/boardex/na_network/na_network_6 $output_dir $companyid_listpath
sbatch $shell_program_path $python_program_path /project/kh_mercury_1/manager_and_board_characteristics/data/boardex/na_network/na_network_7 $output_dir $companyid_listpath
sbatch $shell_program_path $python_program_path /project/kh_mercury_1/manager_and_board_characteristics/data/boardex/na_network/na_network_8 $output_dir $companyid_listpath
sbatch $shell_program_path $python_program_path /project/kh_mercury_1/manager_and_board_characteristics/data/boardex/na_network/na_network_9 $output_dir $companyid_listpath
sbatch $shell_program_path $python_program_path /project/kh_mercury_1/manager_and_board_characteristics/data/boardex/na_network/na_network_10 $output_dir $companyid_listpath
sbatch $shell_program_path $python_program_path /project/kh_mercury_1/manager_and_board_characteristics/data/boardex/na_network/na_network_11 $output_dir $companyid_listpath
sbatch $shell_program_path $python_program_path /project/kh_mercury_1/manager_and_board_characteristics/data/boardex/na_network/na_network_12 $output_dir $companyid_listpath
sbatch $shell_program_path $python_program_path /project/kh_mercury_1/manager_and_board_characteristics/data/boardex/na_network/na_network_13 $output_dir $companyid_listpath
sbatch $shell_program_path $python_program_path /project/kh_mercury_1/manager_and_board_characteristics/data/boardex/na_network/na_network_14 $output_dir $companyid_listpath
sbatch $shell_program_path $python_program_path /project/kh_mercury_1/manager_and_board_characteristics/data/boardex/na_network/na_network_15 $output_dir $companyid_listpath
sbatch $shell_program_path $python_program_path /project/kh_mercury_1/manager_and_board_characteristics/data/boardex/na_network/na_network_16 $output_dir $companyid_listpath
sbatch $shell_program_path $python_program_path /project/kh_mercury_1/manager_and_board_characteristics/data/boardex/na_network/na_network_17 $output_dir $companyid_listpath
sbatch $shell_program_path $python_program_path /project/kh_mercury_1/manager_and_board_characteristics/data/boardex/na_network/na_network_18 $output_dir $companyid_listpath
sbatch $shell_program_path $python_program_path /project/kh_mercury_1/manager_and_board_characteristics/data/boardex/na_network/na_network_19 $output_dir $companyid_listpath

# Rest of World
sbatch $shell_program_path $python_program_path /project/kh_mercury_1/manager_and_board_characteristics/data/boardex/row_compensation $output_dir $companyid_listpath
sbatch $shell_program_path $python_program_path /project/kh_mercury_1/manager_and_board_characteristics/data/boardex/row_companynetwork $output_dir $companyid_listpath
sbatch $shell_program_path $python_program_path /project/kh_mercury_1/manager_and_board_characteristics/data/boardex/row_smallfiles $output_dir $companyid_listpath
sbatch $shell_program_path $python_program_path /project/kh_mercury_1/manager_and_board_characteristics/data/boardex/row_network/row_network_1 $output_dir $companyid_listpath
sbatch $shell_program_path $python_program_path /project/kh_mercury_1/manager_and_board_characteristics/data/boardex/row_network/row_network_2 $output_dir $companyid_listpath
sbatch $shell_program_path $python_program_path /project/kh_mercury_1/manager_and_board_characteristics/data/boardex/row_network/row_network_3 $output_dir $companyid_listpath

# UK
sbatch $shell_program_path $python_program_path /project/kh_mercury_1/manager_and_board_characteristics/data/boardex/uk_compensation $output_dir $companyid_listpath
sbatch $shell_program_path $python_program_path /project/kh_mercury_1/manager_and_board_characteristics/data/boardex/uk_companynetwork $output_dir $companyid_listpath
sbatch $shell_program_path $python_program_path /project/kh_mercury_1/manager_and_board_characteristics/data/boardex/uk_smallfiles $output_dir $companyid_listpath
sbatch $shell_program_path $python_program_path /project/kh_mercury_1/manager_and_board_characteristics/data/boardex/uk_network/uk_network_1 $output_dir $companyid_listpath
sbatch $shell_program_path $python_program_path /project/kh_mercury_1/manager_and_board_characteristics/data/boardex/uk_network/uk_network_2 $output_dir $companyid_listpath
sbatch $shell_program_path $python_program_path /project/kh_mercury_1/manager_and_board_characteristics/data/boardex/uk_network/uk_network_3 $output_dir $companyid_listpath

echo "Done!"