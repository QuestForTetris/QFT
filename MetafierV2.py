# Metafier V2: writes directly to output.mc
# Uses numpy and memoization to speed up a crap ton & compress data a bit
# ===REQUIRES metatemplate11.mc===

import golly as g
import numpy as np
from shutil import copyfile

#Get the selection
selection = g.getselrect()
if not selection: g.exit("No selection.")

#Get the cells in the selection
cells = g.getcells(selection)
if not cells: g.exit("No pattern in selection")
if len(cells) % 3: cells = cells[:-1]

selw = selection[2]
selh = selection[3]

patternsize = 1 << int(np.ceil(np.log2(selh | selw)))

metapattern = np.zeros((patternsize, patternsize))

#Pseudo-convolution, to detect diagonal neighbors
# +1  +0  +2
# +0  *16 +0
# +4  +0  +8
for cell in np.reshape(cells, (-1, 3)):
    selx = cell[0] - selection[0]
    sely = cell[1] - selection[1]

    metapattern[sely][selx] += 16 * cell[2]
    if sely:
        if selx:
            metapattern[sely - 1][selx - 1] += 8
        if selx + 1 < selw:
            metapattern[sely - 1][selx + 1] += 4
    if sely + 1 < selh:
        if selx:
            metapattern[sely + 1][selx - 1] += 2
        if selx + 1 < selw:
            metapattern[sely + 1][selx + 1] += 1

#Remove all B/S cells
metapattern[metapattern < 32] = np.nan
metapattern += 5630 - 32 #5632 is starting point of 11s in template
metapattern[np.isnan(metapattern)] = 0
metapattern = metapattern.astype(int)

#Using metatemplate11, memoization, and some recursion
def createLine(pattern, outfile, linenum = [5726], memo = {}): #linenum and memo are mutable function arguments, which are only initialized during function definition
    if tuple(pattern.ravel().tolist()) not in memo: #If we haven't seen this type of pattern before, let's remember it
        if pattern.shape[0] == 2: #Pattern is a leaf, write leaf line
            outfile.write('{} {} {} {} {}\n'.format(pattern.shape[0].bit_length() + 10,
                                                    pattern[0, 0],
                                                    pattern[0, 1],
                                                    pattern[1, 0],
                                                    pattern[1, 1]))
        else: #Pattern is a branch, keep going down quadtree
            subpatterns = pattern.reshape(2, pattern.shape[0] >> 1, 2, pattern.shape[0] >> 1).swapaxes(1,2)
            outfile.write('{} {} {} {} {}\n'.format(pattern.shape[0].bit_length() + 10,
                                                    createLine(subpatterns[0, 0], outfile),
                                                    createLine(subpatterns[0, 1], outfile),
                                                    createLine(subpatterns[1, 0], outfile),
                                                    createLine(subpatterns[1, 1], outfile)))
        memo[tuple(pattern.ravel().tolist())] = linenum[0]
        linenum[0] += 1
    return memo[tuple(pattern.ravel().tolist())]

copyfile('metatemplate11.mc', 'output.mc')
with open('output.mc', 'a') as outputfile:
    createLine(metapattern, outputfile)

#Display output.mc
g.addlayer()
g.open('output.mc')
#TODO: Use metatemplate10?
