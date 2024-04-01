default = """
/*--------------------------------*- C++ -*----------------------------------*\\
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
    object      controlDict;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

solver              incompressibleFluid;

startFrom           startTime;

startTime           0;

stopAt              endTime;

endTime             2;

deltaT              1e-7;

writeControl        adjustableRunTime;

writeInterval       2.5e-3;

purgeWrite          401;

writeFormat         binary;

writePrecision      6;

writeCompression    off;

timeFormat          general;

timePrecision       6;

runTimeModifiable   true;

//beginTime           0;

adjustTimeStep      on;

maxCo               50;

"""

OptimisationSwitches = """
OptimisationSwitches
{
    //- Parallel IO file handler
    // uncollated (default), collated or masterUncollated
    fileHandler collated;

    //- collated: thread buffer size for queued file writes.
    // If set to 0 or not sufficient for the file size threading is not used.
    // Default: 2e9
    maxThreadFileBufferSize 2e9;

    //- masterUncollated: non-blocking buffer size.
    // If the file exceeds this buffer size scheduled transfer is used.
    // Default: 2e9
    maxMasterFileBufferSize 2e9;
}
// ************************************************************************* //
"""

def read_coord_sbm():
    filename = "../coord_sbm.dat"

    coord_sbm = [line.rstrip('\n') for line in open(filename)]    #Read file line by line

    TOTAL = len(coord_sbm)   #Total number of lines
    #print(TOTAL)

    print('Finish Initial Reading')

    BOUNCOND = list()
    for i in range(0, TOTAL):
        if 'Zone T="' in coord_sbm[i]:
            BOUNCOND.append(i)
            #print(coord_sbm[i])
    return coord_sbm, BOUNCOND


import os
import re

os.getcwd()

if os.path.exists("system/controlDict"):
    if os.path.exists("system/controlDict_bk"):
        rename_option = input(f"controlDict_bk exists. Do you want to proceed? ".strip().lower())
        if rename_option == 'yes':
            os.rename("system/controlDict", "system/controlDict_bk")
    else:
        os.rename("system/controlDict", "system/controlDict_bk")

coord_sbm, BOUNCOND = read_coord_sbm()

f = open("system/controlDict", "w")
f.write(default)
f.write("functions\n")
f.write("{\n")
f.write("""
    clouds
    {
        type            fvModel;
        #includeModel   clouds(name=fvModel)
    }

""")
for i in range(len(BOUNCOND)):
    bc_name = re.search(r'"(.*?)"', coord_sbm[BOUNCOND[i]]).group(1)
    #print(bc_name)
    #break
    if "entry" in bc_name or "exit" in bc_name or "wall" in bc_name:
        f.write("   #includeFunc patchFlowRate(patch={}, cloud::numberFlux)\n".format(bc_name))
    else:
        f.write("   #includeFunc faceZoneFlowRate(faceZone={}_faceZone, cloud::numberFlux)\n".format(bc_name))
f.write("}\n")
f.write(OptimisationSwitches)
f.close()