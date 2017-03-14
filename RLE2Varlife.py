import golly

selrect = golly.getselrect()
if len(selrect) == 0: golly.show("No selection to be converted")
else:
  gridNums = []
  gridNum = 0
  blockNum = 0
  for j in range(selrect[1] + selrect[3] - 1, selrect[1] - 1, -1):
    for i in range(selrect[0] + selrect[2] - 1, selrect[0] - 1, -1):
      if gridNum * 8 > pow(2,24):
        gridNums.append(blockNum)
        gridNums.append(gridNum)
        blockNum = 0
        gridNum = 0
      blockNum += 1
      gridNum *= 2
      gridNum += golly.getcell(i,j) % 2
      gridNum *= 4
      gridNum += golly.getcell(i,j) / 2
  gridNums.append(blockNum)
  gridNums.append(gridNum)
  golly.note('http://play.starmaninnovations.com/varlife/#data={{"cs":4,"r":[{{"b":[],"s":[],"a":"#FFFFFF","d":"#000000"}},{{"b":[1],"s":[],"a":"#00ffff","d":"#0000ff"}},{{"b":[2],"s":[],"a":"#ffff00","d":"#00ff00"}},{{"b":[1,2],"s":[1],"a":"#ff8000","d":"#ff0000"}}],"w":{},"h":{},"gN":[{}]}}'.format(str(selrect[2]), str(selrect[3]), ','.join(str(x) for x in gridNums)))
  golly.show('URL sucessfully copied')

