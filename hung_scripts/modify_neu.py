#!/opt/anaconda3/bin/python3.6
###########################################################################
#-------------------------------------------------------------------------#
# Modify the .neu file for OpenFOAM                                       #
# ------------------------------------------------------------------------#
# Hung Nguyen                                                             #
# ICFM, School of Mechanical Engineering, Kyungpook National University   #
# Dec 01, 2023                                                            #
###########################################################################

import sys

inp_filename = sys.argv[1]

original_neu = inp_filename + ".neu"
complete_neu = inp_filename + "_OpenFOAM.neu"

neupart = [line.rstrip('\n') for line in open(original_neu)]    #Read file line by line

TOTAL = sum(1 for line in open(original_neu))   #Total number of lines

print('Finish Initial Reading')

NBSETS_old = int(neupart[6].split()[3])

## Get each block position

ELEMGROU = list()
BOUNCOND = list()
Nintn = list()
for i in range(0, TOTAL):
    if 'NODAL COORDINATES' in neupart[i]:
        NODACOOR = i
    elif 'intn' in neupart[i]:
        Nintn.append(i)
    elif 'ELEMENTS/CELLS ' in neupart[i]:
        ELEMCELL = i
    elif 'ELEMENT GROUP'   in neupart[i]:
        ELEMGROU.append(i)
    elif 'BOUNDARY CONDIT' in neupart[i]:
        BOUNCOND.append(i)
        #break
    #print(i)

NBSETS_new = NBSETS_old - len(Nintn)
mylist = neupart[6].split()
mylist[3] = NBSETS_new
neupart[6] = "     ".join(str(item) for item in mylist)

#print(NODACOOR, ELEMCELL, ELEMGROU, BOUNCOND)

ELEMGROU.append(BOUNCOND[0])

## Start re-writing .neu
    
neu_out = open(complete_neu,'w')
  
## write head
    
i = 0

while i < NODACOOR + 1 :
    neu_out.write(str(neupart[i]).rstrip())
    neu_out.write('\n')
    i = i + 1
    
## Read coordinates and write modified values

while i < ELEMCELL - 1:
    Temp_Line = neupart[i].split()
    neu_out.write(Temp_Line[0].rjust(10))   ## node num
    
    x = str('{:.11e}'.format(float(Temp_Line[1])))
    y = str('{:.11e}'.format(float(Temp_Line[2])))
    z = str('{:.11e}'.format(float(Temp_Line[3])))
    
    neu_out.write(x.rjust(20))  ## x coordinate
    neu_out.write(y.rjust(20))  ## y coordinate
    neu_out.write(z.rjust(20))  ## z coordinate
    neu_out.write('\n')
    
    i = i + 1
    
print('Finish Coordinates')

## Output element cells head

neu_out.write(str(neupart[ELEMCELL -1]).rstrip())
neu_out.write('\n' )
neu_out.write('   ')
neu_out.write(str(neupart[ELEMCELL]).rstrip())
neu_out.write('\n' )

## Output element cell numbers

i = ELEMCELL + 1

while i < ELEMGROU[0] - 1:
    
    Temp_Line = neupart[i].split()
    neu_out.write(Temp_Line[0].rjust(8))   ## elem num
    neu_out.write(Temp_Line[1].rjust(3))   ## elem def1
    neu_out.write(Temp_Line[2].rjust(3))   ## elem def2
    
    neu_out.write(Temp_Line[3].rjust(9))   ## connect1
    neu_out.write(Temp_Line[4].rjust(8))   ## connect2
    neu_out.write(Temp_Line[5].rjust(8))   ## connect3
    neu_out.write(Temp_Line[6].rjust(8))   ## connect4
    
    neu_out.write('\n')
    
    i = i + 1

print('Finish Connectivity')
    
## output element group

neu_out.write(neupart[ELEMGROU[0] - 1])  ## start of ENDOFSECTION
neu_out.write('\n')

group_num = 1

while group_num < len(ELEMGROU):
    
    ## head
    
    order = ELEMGROU[group_num - 1]
    
    neu_out.write((neupart[order    ].rstrip()).ljust( 7))
    neu_out.write('\n')
    neu_out.write((neupart[order + 1].rstrip()).ljust( 0))
    neu_out.write('\n')
    neu_out.write((neupart[order + 2].rstrip()).ljust(27))
    neu_out.write('\n')
    
    p = 0
    
    group_start = list()
    group_start.append(ELEMCELL)
    
    ## If not single group, append each group start point 
    
    if len(ELEMGROU)>1:
        while p < len(ELEMGROU):
            
            group_start.append(ELEMGROU[p])
            p = p + 1
            
    i = group_start[group_num] + 3
  
    while i < ELEMGROU[group_num]:
            
        Temp_Line = neupart[i].split()
           
        k = 0
        while k < len(Temp_Line):
                
            neu_out.write(Temp_Line[k].rjust(8))  
            k = k + 1
            
        neu_out.write('\n')
            
        i = i + 1
    
    progress = int(int(group_num) + 1)/int(len(ELEMGROU))
    
    group_num = group_num + 1
    
print('Finish Groups')

## Output boundary conditions

i = BOUNCOND[0]

while i < Nintn[0] - 1:
    
    neu_out.write(neupart[i])
    neu_out.write('\n')

    i = i + 1

print('Finish Boundary Conditions')
    
neu_out.close()

print('Finish All')

