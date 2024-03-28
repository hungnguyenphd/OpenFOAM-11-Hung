import os
import re

def extract_number(string):
    # Define a regular expression pattern to match digits
    pattern = r'\d+'
    
    # Use re.findall() to find all occurrences of the pattern in the string
    numbers = re.findall(pattern, string)
    
    # If numbers are found, return the first one
    if numbers:
        return int(numbers[0])  # Convert the number from string to integer
    
    # If no numbers are found, return None
    return None

def gen_U(exit_num):
    """
    Create a "U" file for the Lung_CFD single phase
    """
    # Open file
    os.getcwd()
    f = open("0/U", "w")
    # Write file
    f.write("/*--------------------------------*- C++ -*----------------------------------*\ \n"
            "  =========                 |                                                  \n"
            "  \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox            \n"
            "   \\    /   O peration     | Website:  https://openfoam.org                   \n"
            "    \\  /    A nd           | Version:  11                                     \n"
            "     \\/     M anipulation  |                                                  \n"
            "\*---------------------------------------------------------------------------*/\n"
            "FoamFile\n"
            "{\n"
            "   format      ascii;\n"
            "   class       volVectorField;\n"
            "   object      U;\n"
            "}\n"
            "// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //\n")
##########################---------Parabolic_velocity (Flow type = 1)-----------#########################
    f.write(    '#include        "include/bcflowrates"\n'
                "\n"
                "dimensions      [0 1 -1 0 0 0 0];\n"
                "\n"
                "internalField   uniform (0 0 0);\n"
                "\n"
                "boundaryField\n"
                "{\n"
                "    entry\n"
                "    {\n"
                "        type                    flowRateInletOutletVelocity;\n"
                "        volumetricFlowRate      $entry;\n"
                "        profile                 laminarBL;\n"
                "        value                   uniform (0 0 0);\n"
                "    }\n"
                "\n")
    for i in exit_num:
        f.write("    exit_{}\n".format(i))
        f.write("    {\n"
                "        type                    flowRateInletOutletVelocity;\n")
        f.write("        volumetricFlowRate      $exit_{};\n".format(i))
        f.write("        profile                 laminarBL;\n")
        f.write("        value                   uniform (0 0 0);\n"
                "    }\n"
                "\n")
    f.write('    "wall_.*"\n'
            "    {\n"
            "        type                    noSlip;\n"
            "    }\n"
            "}\n"
            "\n"
            "// ************************************************************************* //")

os.getcwd()
file_constant = 'constant/polyMesh/boundary'

with open(file_constant, 'r') as file:
    lines = file.readlines()

exit_num = []
for line in lines:
    if "exit" in line:
        exit_num.append(extract_number(line))

gen_U(exit_num)
