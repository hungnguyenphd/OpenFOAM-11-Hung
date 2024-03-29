def write_topoSetDict(bc_names, bc_coords):
    header = """
/*--------------------------------*- C++ -*----------------------------------*\
  =========                 |
  \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
   \\    /   O peration     | Website:  https://openfoam.org
    \\  /    A nd           | Version:  11
     \\/     M anipulation  |
\*---------------------------------------------------------------------------*/
FoamFile
{
    format      ascii;
    class       dictionary;
    location    "system";
    object      topoSetDict;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //\n
"""
    f = open("system/topoSetDict", "w")
    f.write(header)
    f.write("actions\n")
    f.write("(\n")
    
    #pointToPointSet
    for i in range(len(bc_names)):
        f.write("   {\n")
        f.write("       name    {}_pointSet;\n".format(bc_names[i]))
        f.write("       type    pointSet;\n")
        f.write("       action  new;\n")
        f.write("       source  nearestToPoint;\n")
        f.write("       points\n")
        f.write("       (\n")
        for j in range(len(bc_coords[i])):
            f.write("           {}\n".format(bc_coords[i][j]))
        
        f.write("       );\n")
        f.write("   }\n")
        
    #pointSetToFace
    for i in range(len(bc_names)):
        f.write("   {\n")
        f.write("       name        {}_faceSet;\n".format(bc_names[i]))
        f.write("       type        faceSet;\n")
        f.write("       action      new;\n")
        f.write("       source      pointToFace;\n")
        f.write("       option      all;\n")
        f.write("       set         {}_pointSet;\n".format(bc_names[i]))
        f.write("   }\n")
    
    for i in range(len(bc_names)):
        f.write("   {\n")
        f.write("       name        {}_faceZone;\n".format(bc_names[i]))
        f.write("       type        faceZoneSet;\n")
        f.write("       action      new;\n")
        f.write("       source      setToFaceZone;\n")
        f.write("       faceSet     {}_faceSet;\n".format(bc_names[i]))
        f.write("   }\n")
    
    f.write(");\n")
    f.write("// ************************************************************************* //")
    
    f.close()
import re
import os
import sys

os.getcwd()

filename = sys.argv[1]

coord_sbm = [line.rstrip('\n') for line in open(filename)]    #Read file line by line

TOTAL = len(coord_sbm)   #Total number of lines
#print(TOTAL)

print('Finish Initial Reading')

BOUNCOND = list()
for i in range(0, TOTAL):
    if 'Zone T="int' in coord_sbm[i]:
        BOUNCOND.append(i)
        #print(coord_sbm[i])

bc_names = list()
bc_coords = list()
for i in BOUNCOND:
    #print(neupart[i+1])
    #print(neupart[i+1].split())
    bc_name = re.search(r'"(.*?)"', coord_sbm[i]).group(1)
    bc_data_number = int(re.search(r'(\d+)', coord_sbm[i+1]).group(1))
    bc_names.append(bc_name)
    #bc_data_numbers.append(bc_data_number)
    print("Boundary condition {} has {} numbers of nodes".format(bc_name, bc_data_number))
    
    bc_coord = list()
    for j in range(i+2, i+bc_data_number+2):
        bc_coord.append("({})".format(coord_sbm[j]))
    bc_coords.append(bc_coord)
    
    write_topoSetDict(bc_names, bc_coords)
    #break

#print(bc_coords)

