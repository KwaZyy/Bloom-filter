#!/bin/bash -l
#SBATCH --account=lp_h_ds_students
#SBATCH --cluster=wice
#SBATCH --time=05:00:00
module load Miniforge3/25.3.0-3
source $(conda info --base)/etc/profile.d/conda.sh
conda activate bloom_filter_python
cd $SLURM_SUBMIT_DIR/..
export PYTHONPATH=$PYTHONPATH:$(pwd)/..
python TimeAddingSearching.py