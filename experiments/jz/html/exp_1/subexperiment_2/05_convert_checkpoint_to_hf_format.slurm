#!/bin/bash
#SBATCH --job-name=modelling-metadata-html-metadata-exp1-subexp2-transform-checkpoints     # (change me!) job name
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1                                            # crucial - only 1 task per dist per node!
#SBATCH --cpus-per-task=20                                             # (change me! between 0 and 40) number of cores per tasks
#SBATCH --hint=nomultithread                                           # we get physical cores not logical
#SBATCH --time 02:00:00                                                # (change me! between 0 and 20h) maximum execution time (HH:MM:SS)
#SBATCH --output=/gpfsdswork/projects/rech/six/uue59kq/logs/%x-%j.out  # output file name
#SBATCH --error=/gpfsdswork/projects/rech/six/uue59kq/logs/%x-%j.err   # error file name
#SBATCH --account=six@cpu # account

set -x -e

# Next line will:
# - load a conda environment with the dependencies on the master branch of github.com/bigscience-workshop/metadata/
# - setup env vars ($HOME, $WORK, etc)
# - load several modules (git)
# Note: We can afford to have two conda environments: one stable for running experiments and one for development.
# If there are new dependencies to install, you have to tell me about them and not do it in this script
source $HOME/start-user

module load git-lfs github-cli mc git

GIT_PATH=`which git`

PATH=$PATH:$GIT_PATH
export PATH

GIT_PYTHON_GIT_EXECUTABLE=$GIT_PATH
export GIT_PYTHON_GIT_EXECUTABLE

git config --global user.email "lucilesaul.com@gmail.com"
git config --global user.name "SaulLu"



echo "PATH: $PATH"
echo "GIT_PYTHON_GIT_EXECUTABLE: $GIT_PYTHON_GIT_EXECUTABLE"

# We are on an offline partition
export HF_DATASETS_OFFLINE=1
export TRANSFORMERS_OFFLINE=1

# Folder for the clone of github.com/bigscience-workshop/metadata/
cd $WORK/repos/sync/metadata/

# Now we launch the script that will perform the preprocessing of the dataset
# Feel free to add any arguments you like (change me!)
python experiments/jz/utils/convert_checkpoint_to_hf_format.py \
  out_dir="${SCRATCH}/metadata_outputs" \
  jobid="${SLURM_JOB_ID}" \
  local_repo_path="${SCRATCH}/tmp/html-metadata-exp1-subexp2-1929863" \
  training_jobid="1929863" \