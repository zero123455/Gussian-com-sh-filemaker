# Gussian-com-sh-filemaker
## Warning: The input file must have a '_opt' within its file name and this is not designed to work with manually altered opt.com files when using the 'opt' option within the program. 
### Diclaimer: If you ignore the warning from the warning, this program can break the opt.com file by deleting half of the z-matrix from the .com file

Program works on output gaussian-view files storing information in z matrix form for the 'opt' option

The opt option generates a new optimisation.com gaussian filewith the connectivity list is removed, 
with and new system charge and e- multiplicity. It is possible to use the script to just change the 
chare and multiplicity using the 'opt' option, provided the input 'opt' file is either 
from gaussian-view output or has ran through the program once

If other options is chosen, it will generate new .com files using the checkpoint 
produced from the optimisation. (using filename of the '_opt' file).

.sh script generated by the program is designed for use on cluster using the 
slurm workload manager (sbatch).

## Use
Place the program within the folder containing all '_opt.com' (that does not vilolate warning) run the program

