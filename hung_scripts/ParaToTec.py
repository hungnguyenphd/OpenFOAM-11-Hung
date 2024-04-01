import pandas as pd

# reformat data function
def formatTec(dataset_):
    # change the names of headers
    dataset_ = dataset_.rename(columns = {"U:0" : "u",
					"U:1" : "v",
					"U:2" : "w",
					"U_0:0" : "um",
					"U_0:1" : "vm",
					"U_0:2" : "wm",
					"p" : "p",
                    "nut" : "f",
					"Points:0" : "x",
					"Points:1" : "y",
					"Points:2" : "z"})

    #In OF, it uses pressure as pressure/rho => get the real pressure by multiplying with density
    dataset_["vmag"] = (dataset_["u"]**2 + dataset_["v"]**2 + dataset_["w"]**2)**(1/2)
    dataset_["p"] = dataset_["p"]*1.12e0
    time = dataset_["Time"][0]
    # reorder columns
    dataset_ = dataset_[["x","y","z","u","v","w","p","f", "vmag"]]
    return time, dataset_

def getrootkey(MATCH, coordfile):
    if (MATCH == 0): 
        rootkey = list()
        neupart = [line.rstrip("\n") for line in open(coordfile)]
        print("Finish reading coord.in")
        del neupart[0]  #delete the first line
    return rootkey, neupart
        

####################################

def writefinaldata(MATCH, dataset_, ofdict_, rootkey_, time, Npoint, Nelem, neupart):
    timestep = 2.5e-3
    istart = int(round(time/timestep, 0)/8)
    #print(time, istart, (time - 2.4)/timestep)
    zeros = 6 - len(str(istart))
    name = "it01rb_" + "0" * zeros + str(istart) + ".dat"
    final = open(name, "w")
    final.write('variables="x","y","z","u","v","w","p","f","vmag" \n' +
                'zone T="f_' + "{:e}".format(time) + '"\n' +
				'N=      {} ,E=     {} ,f=fepoint,et=tetrahedron \n '.format(Npoint, Nelem))
    if (MATCH == 0):
        dataset_.to_csv(final, header=None, index=None, sep=' ', lineterminator='\n', mode='a', float_format = '{:E}'.format)
        final.writelines([l for l in elemlines])
        final.close()
    else:
        i = 0
        lil = list()
        for key in rootkey_:
            #print(neupart[i], ofdict.get(key))
            if (ofdict_.get(key) == None):
                print("Dangerous!! It is not working. There are keys not matched.")
                print("non-matched key:", key, "at (x y z)", neupart[i])
                break
            xyz = neupart[i].split()
            upfvmag = ofdict_.get(key).split()
            lil.append(xyz + upfvmag)
            i += 1
        df = pd.DataFrame(lil)
        df = df.astype(float)
        df.to_csv(final, header=None, index=None, sep=' ', lineterminator='\n', mode='a', float_format = '{:E}'.format)
        final.writelines([l for l in elemlines])
        final.close()
            #print(ofdict.get(key))
    print("Done writing file " + name)

# Main code
#############################################################
# USER INITIAL SETUP
# Please carefully modify below variables before running
# for sucessful job

import os

os.getcwd()

coordfile = "coord.in" ##Please modify yourself if needed
elemfile = "elem.in"
MATCH = 0
##############################################################
# READ DATA
elem = open(elemfile, "r")
elemlines = elem.readlines()[1:]

coord = open(coordfile, 'r')
coordlines = coord.readlines()[0]
Npoint = coordlines.split()[0]
Nelem = coordlines.split()[1]

rootkey, neupart = getrootkey(MATCH, coordfile)

lastesttime = 800 #int(endtime/timestep)
starttime = 0
filelist = []
for i in range(starttime, lastesttime + 1):
    data = "u2down_" + str(i) + ".csv"
    filelist.append(data)

#filelist = ["u2down_17.csv"]
for file in filelist:
    dataset = pd.read_csv(file)
    ofdict = dict()
    time, dataset = formatTec(dataset)
    writefinaldata(MATCH, dataset, ofdict, rootkey, time, Npoint, Nelem, neupart)


