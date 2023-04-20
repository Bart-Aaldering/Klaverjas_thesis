#!/bin/bash
#SBATCH --job-name=run_main
#SBATCH --output=%x_%j.out
#SBATCH --error=%x_%j.err
#SBATCH --mem-per-cpu=500M
#SBATCH --time=02:00:00
#SBATCH --partition=cpu-short
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=15
#SBATCH --gpus=1


echo "[$SHELL] #### Starting Python test"
echo "[$SHELL] ## This is $SLURM_JOB_USER on $HOSTNAME and this job has the ID $SLURM_JOB_ID"
# get the current working directory
export CWD=$(pwd)
echo "[$SHELL] ## current working directory: "$CWD

# Run the file
echo "[$SHELL] ## Run script"
python3 main.py
echo "[$SHELL] ## Script finished"

echo "[$SHELL] #### Finished Python test. Have a nice day"