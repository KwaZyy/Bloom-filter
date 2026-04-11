#!/bin/bash
#SBATCH --job-name=bloom-benchmark
#SBATCH --output=bloom-benchmark.out
#SBATCH --time=00:05:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1

set -euo pipefail

python scripts/benchmark.py --size 20000 --repeats 10 --limit 1000
