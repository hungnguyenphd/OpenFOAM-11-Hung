import pandas as pd

df = pd.read_csv("../xflx_1d.dat", delim_whitespace=True, header=None, skiprows=1)
#print(df.iloc[1:,1].sum()-1)
inlet_flowrate = 3.33333333e-04
df.iloc[:,1] = df.iloc[:,1]*inlet_flowrate
df.iloc[1:,1] = -df.iloc[1:,1]

#print(df.head())
#print(len(df.index))
#print(df.iloc[1,0])

f = open("../bcflowrates", "w")
flow_sum=0
for i in range(len(df.index)):
    f.write("{:16} {:.14E};\n".format(df.iloc[i,0], df.iloc[i,1]))
    flow_sum += df.iloc[i,1]
print(flow_sum)
f.close()
