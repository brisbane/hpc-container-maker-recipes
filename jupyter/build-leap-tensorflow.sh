#!/bin/bash
(module load conda/jupyterhub && ./tensorflow-leap.py --packager anaconda --environment environment-tensorflow.1-14.yml --notebook notebook.ipynb --image localhost:5000/cuda-10.2-devel-opensuse-leap15.1 --format singularity > /home/software/containers/tensorflow-leap.def )
if [ -f /home/software/containers/tensorflow-leap.sif ];then
echo /home/software/containers/tensorflow-leap.sif already exists 
exit 1
fi
singularity build   /home/software/containers/tensorflow-leap.sif  /home/software/containers/tensorflow-leap.def  

