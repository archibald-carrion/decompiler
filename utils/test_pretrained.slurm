#!/bin/bash
#SBATCH --job-name=test_pretrained
#SBATCH --partition=gpu
#SBATCH --account=2025-i-ci0148
#SBATCH --time=1:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --gpus-per-node=1
#SBATCH --cpus-per-task=8
#SBATCH --gres=gpu:1
#SBATCH --output=test_pretrained_%j.out
#SBATCH --error=test_pretrained_%j.err
#SBATCH --mail-user=javier.solanosaltachin@ucr.ac.cr
#SBATCH --mail-type=END,FAIL

# Cargar CUDA
module load cuda/12.5

# Configurar CUDA y NVIDIA HPC SDK
export NVHPC_ROOT=/opt/nvidia/hpc_sdk/Linux_x86_64/24.5
export CUDA_HOME=$NVHPC_ROOT/cuda/12.4
export PATH=$CUDA_HOME/bin:$PATH
export LD_LIBRARY_PATH=$CUDA_HOME/targets/x86_64-linux/lib:$LD_LIBRARY_PATH

# Imprimir variables de entorno para diagnóstico
echo "=== Variables de entorno ==="
echo "NVHPC_ROOT: $NVHPC_ROOT"
echo "CUDA_HOME: $CUDA_HOME"
echo "LD_LIBRARY_PATH: $LD_LIBRARY_PATH"
echo ""

# Activar el entorno Python
source /home/javier.solanosaltachin/decompiler/bin/activate

# Verificar que CUDA está funcionando
echo "=== Verificando CUDA con Python ==="
python -c "
import sys
import os
print('Python version:', sys.version)
print('CUDA_HOME:', os.environ.get('CUDA_HOME'))
print('LD_LIBRARY_PATH:', os.environ.get('LD_LIBRARY_PATH'))

import torch
print('\nPyTorch info:')
print('PyTorch version:', torch.__version__)
print('CUDA available:', torch.cuda.is_available())
print('CUDA version:', torch.version.cuda)
if torch.cuda.is_available():
    print('GPU count:', torch.cuda.device_count())
    print('GPU name:', torch.cuda.get_device_name(0))

try:
    import cupy as cp
    print('\nCuPy info:')
    print('CuPy version:', cp.__version__)
    print('CuPy CUDA version:', cp.cuda.runtime.runtimeGetVersion(), '\n')
except Exception as e:
    print('\nError importing CuPy:', str(e), '\n')
"

set -x
# Ejecutar el script
srun python ~/decompiler/fine_tuning/basemodel_setup.py ~/pretrained_model/
