header = """/*--------------------------------*- C++ -*----------------------------------*\
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
    location    "constant";
    object      cloudProperties;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //"""

solution = """

type        cloud;

solution
{
    //- Flag to indicate whether parcels are coupled to the carrier
    //  phase, i.e. whether or not to generate source terms for
    //  carrier phase
    coupled         false;

    transient       yes;

    //- Flag to correct cell values with latest transfer information
    //  during the lagrangian timestep
    cellValueSourceCorrection on;

    interpolationSchemes
    {
        rho             cell;
        U               cellPoint;
        mu              cell;
    }
    
    averagingMethod basic;

    //- Base for a set of schemes which integrate simple ODEs which arise from
    //  semi-implcit rate expressions. (Euler, analytical)
    //-- Euler: Euler-implicit integration scheme.
    integrationSchemes
    {
        U               Euler;
    }

    sourceTerms
    {
        schemes
        {
            U semiImplicit 1;
        }
    }
}
"""

constantProperties = """
constantProperties
{
    rho0            1000;
}
"""

subModel = """
subModels
{
    particleForces
    {
       sphereDrag;
       gravity;
    }

    injectionModels
    {
        model
        {
            type                patchInjection;
            SOI                 0;
            duration            0.1;
            nParticle           1;
            parcelsPerSecond    1000000;
            patchName           entry;
            U0                  (0.0154396 1.02835 0.294469);
            flowRateProfile     constant 1;
            sizeDistribution
            {
                type    fixedValue;
                value   5e-6;
            }
        }
    }
    
    dispersionModel         none;

    patchInteractionModel   localInteraction;

    localInteractionCoeffs
    {
        patches
        (
            "wall.*"
            {
                type stick;
            }

            "entry|exit.*"
            {
                type escape;
            }
        );
    }
    
    stochasticCollisionModel    none;
    
    surfaceFilmModel            none;
}
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

import re
import os
import sys

if (len(sys.argv) < 2):
    print("Please provide argument!")
    print("0: Not do the post processing; 1: Do the post processing")
    sys.exit(1)

if (int(sys.argv[1]) == 0):
    post_processing = sys.argv[1]
    print("Do not add cloudFunctions for post processing.")
elif (int(sys.argv[1]) == 1):
    post_processing = sys.argv[1]
    print("Add cloudFunctions for post processing.")
else:
    print("The argument {} is incorrect! Please run again!".format(sys.argv[1:]))
    print("0: Not do the post processing; 1: Do the post processing")
    sys.exit(1)

os.getcwd()

f = open("constant/cloudProperties", "w")
f.write(header)
f.write(solution)
f.write(constantProperties)
f.write(subModel)
if post_processing == 1:
    coord_sbm, BOUNCOND = read_coord_sbm()
    f.write("""
    cloudFunctions
    {\n""")

    f.write("   facePostProcessing1\n")
    f.write("   {\n")
    f.write("       type            facePostProcessing;\n")
    f.write("       surfaceFormat   vtk;\n")
    f.write("       resetOnWrite    no;\n")
    f.write("       log             yes;\n")
    f.write("       faceZones\n")
    f.write("       (\n")
    for i in range(len(BOUNCOND)):
        bc_name = re.search(r'"(.*?)"', coord_sbm[BOUNCOND[i]]).group(1)
        f.write("           {}_faceZone\n".format(bc_name))
    f.write("       );\n")
    f.write("   }\n")

    f.write("}")
else:
    f.write("""
cloudFunctions
{}
""")
f.close()