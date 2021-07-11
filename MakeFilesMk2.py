"""
-----------------------------------------------
Script written by : S.Wan
Please acknowledge if using this script for research activities
------------------------------------------------
"""
import os
import glob
def comsFileformat(name,charge,multi,function,cpu=12,meme=92):
    """
    Function containing standard format used for the .com file
    input:
        name: filename of opt.com 
        charge: system charge
        multi: e- multiplicity
        function: the purpose of the generating .com file
        cpu: number of cores - defaults 12 cores
        meme: how much ram - defaults 92 GB
    output:
        string with all the relivent parameters filled in
    """
    text = f"%nprocshared={cpu}\n"\
            f"%mem={meme}GB\n"\
            f"%chk={name}.chk\n"\
            "#Geom=Checkpoint Guess=Read\n"\
            f"#wb97xd/6-31+g(d,p) {type_dict[function]}\n"\
            "\n"\
            "Title Card Required\n"\
            "\n"\
            f"{charge} {multi}\n"\
            "\n"
    if function == "optwfn":
        text +=f"{name}.wfn\n"\
                "\n"
    return(text)    
    

def shFileformat(name,function,uName,cpu=12,meme=96):
    """
    Contains standard format of .sh
    input:
        name: filename of opt.com 
        function: the purpose of the generating .sh file
        cpu: number of cores - defaults 12 cores
        meme: how much ram - defaults 96 GB
    output:
        string with all the relivent parameters filled in
    """
    name=name.replace("_opt","")
    text = "#!/bin/bash\n"\
            f"#SBATCH --mem={meme}G\n"\
            "#SBATCH --time=06-23:59\n"\
            f"#SBATCH --account={uName}\n"\
            f"#SBATCH --cpus-per-task={cpu}\n"\
            "module load gaussian/g09.e01\n"\
            f"g09 < {name}_{function}.com >& {name}_{function}.log" 
    return(text)

def generateSh(f_name,f_type,processor,ram,user_name):
    
    output = shFileformat(f_name,f_type,user_name,processor,ram)
    f_name=f_name.replace("_opt","")
    f = open(f"{f_name}_{f_type}.sh","w",newline="\n")
    f.write(output)  
     
def writeComs(FileType,FileEnding,sys_charge,e_multi,cpu,meme,user_name,wantSh='n'):
    for filename in glob.iglob(ROOT_DIR + '\**\*opt.com',recursive=True):
        filename = os.path.basename(filename).split('.')[0]
        if FileEnding == '.sh':
            generateSh(filename,FileType,cpu,meme,user_name)
        else:
            output = comsFileformat(filename,sys_charge,e_multi,FileType,cpu,meme-4)
            filename=filename.replace("_opt","")
            f = open(f"{filename}_{FileType}{FileEnding}","w",newline="\n")
            f.write(output)
            if wantSh == 'y':
                generateSh(filename,FileType,cpu,meme,user_name)


def WriteOptComs(sys_charge,e_multi,user_name,cpu=12,meme=92,wantSh='n'):
    """
    Generates opt.com removing the redundant informations (connection list)
    and appends parameters requires for specifly calculation
    input:
        sys_charge: charge of the system
        e_multi: e- multiplicity of the system
        cpu: number of cores defaults 12 cores
        meme: amount of ram defaults 92 GB
        wantSh: storing if user wants to also generates the corresponding sh file
    output:
        com file with all correct input parameters for the cluster
    """
    def OptFormat(name,zMatrix):
        """
        Function containing standard format used for the .com file
        input:
            name: filename of opt.com 
            charge: system charge
            multi: e- multiplicity
            function: the purpose of the generating .com file
        output:
            string with all the relivent parameters filled in    
        """
        text = f"%nprocshared={cpu}\n"\
            f"%mem={meme-4}GB\n"\
            f"%chk={name}.chk\n"\
            "# wB97XD/6-31+g(d,p) SCF=(tight, maxcycle=10000) opt int=ultrafine\n"\
            "\n"\
            "Title Card Required\n"\
            "\n"\
            f"{sys_charge} {e_multi}\n"
        for i in zMatrix:
            text+=i
        text+="\n"
        return(text)
    
    for filename in glob.iglob(ROOT_DIR + '\**\*opt.com',recursive=True):
        f = open(filename).readlines()
        InterestedIndex = [i for i,val in enumerate(f) if val=='\n']
        if len(InterestedIndex) == 4:
            f[7]=f"{sys_charge} {e_multi}\n"
            output=str()
            for i in f:
                output+=i
            file = open(f"{filename}","w",newline="\n")
            file.write(output)
        else:
            wantedText = f[InterestedIndex[1]+2:InterestedIndex[3]]
            filename = os.path.basename(filename).split('.')[0]
            output=OptFormat(filename,wantedText)
            file = open(f"{filename}.com","w",newline="\n")
            file.write(output)
        if wantSh == 'y':
            generateSh(os.path.basename(filename).split('.')[0],'opt',cpu,meme,user_name)
       
 

PROCESSORS = 8
RAM = 32    
ROOT_DIR = os.getcwd()
USERNAME = "username"

try:
    glob.iglob(ROOT_DIR + '\**\*opt.com', recursive=True)
except:
    ROOT_DIR = input("Please manually enter filepath")
    

file_ending = input("Please type file ending (.com or .sh): ")
possible_types=['.sh', '.com']
if file_ending not in possible_types:
    raise ValueError ("Not available file type: ")


type_dict={"f":"freq=noraman scf=tight int=ultrafine",\
           "optwfn":"output=wfn scf=tight",\
           "td":"TD=(50-50,NStates=50) scf=tight int=ultrafine",\
           "MO":"POP=FULL formcheck",\
           "opt":""}

file_type = input("Please enter which file is wanted\n"\
             "frequency: f\n"\
             "Wave function: optwfn\n"\
             "UV-Vis absorption: td\n"\
             "Molecular orbital: MO\n"\
             "optimisation: opt\n"    
             ": ")

 
if file_type not in type_dict.keys():
    raise ValueError ("Selected function is not available")


if file_ending == '.com':
    s_charge = input("Please enter system charge: ")
    e_mul = input("Please enter e- multiplicity: ")
    try:
        int(s_charge)
        int(e_mul)
        wantshFiles = input("Do you want to generate the corresponding sh file?\n"\
                    "y or n: ")  
    except:
        raise ValueError("Charge and multiplicty needs to be integer")
    if wantshFiles not in ['y','n']:
        raise ValueError("Please select y or n")
else:
    s_charge = None
    e_mul = None
    wantshFiles = 'n'

if file_ending == '.com' and file_type == 'opt':
    WriteOptComs(s_charge,e_mul,USERNAME,PROCESSORS,RAM,wantshFiles)
else:
    writeComs(file_type,file_ending,s_charge,e_mul,USERNAME,PROCESSORS,RAM,wantshFiles)

print("Files generated") 

