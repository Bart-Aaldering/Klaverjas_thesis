#!/bin/bash
#SBATCH --job-name=test
#SBATCH --output=%x_%j.out
#SBATCH --error=%x_%j.err
#SBATCH --partition="cpu-short"
#SBATCH --time=00:01:00
#SBATCH --ntasks=1
#SBATCH -c 1



echo "#### Starting Test"
echo "This is $SLURM_JOB_USER and my first job has the ID $SLURM_JOB_ID"
# get the current working directory
CWD=$(pwd)
echo "This job was submitted from $SLURM_SUBMIT_DIR and I am currently in $CWD"
# get the current time and date
DATE=$(date)

source thesis_env/bin/activate
python ~



echo "#### Finished Test. Have a nice day"





