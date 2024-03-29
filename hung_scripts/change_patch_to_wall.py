import numpy as np
import os
import sys
import shutil
import argparse

# Fix polyMesh file
os.getcwd()
filename = "constant/polyMesh/boundary"
with open(filename, 'r') as file:
    lines = file.readlines()

line_wall_num = []
line_num = 0
for line in lines:
    if "wall" in line:
        line_wall_num.append(line_num + 2)
    line_num += 1

modified_lines = []
for i in range (len(lines)):
    if (i in line_wall_num):
        add = lines[i].replace("patch", "wall")
    else:
        add = lines[i]
    modified_lines.append(add)

shutil.copy("constant/polyMesh/boundary", "constant/polyMesh/boundary_old")

with open("constant/polyMesh/boundary", 'w') as file:
    file.writelines(modified_lines)

