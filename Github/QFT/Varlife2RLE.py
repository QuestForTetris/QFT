import golly
import urllib
import re

url = urllib.unquote(golly.getclipstr())
try:
  width = int(re.search(r'"(w|width)":(\d+)', url).group(2))
  height = int(re.search(r'"(h|height)":(\d+)', url).group(2))
  gridNums = map(int, re.search(r'"(gN|gridNums)":\[(\d+(,\d+)*)\]', url).group(2).split(','))
except AttributeError:
  golly.exit('Invalid URL given')
i = j = 0
rle = 'x = ' + str(width) + ', y = ' + str(height) + ', rule = Varlife\n'
grid = [[0] * width for x in range(height)]
while gridNums:
  gridNum = gridNums.pop()
  blockNum = gridNums.pop()
  for k in range(blockNum):
    rle += chr(ord('A') - 1 + gridNum % 4 * 2 + gridNum / 4 % 2) if gridNum % 8 else '.'
    gridNum = gridNum / 8
    i += 1
    if i >= width:
      rle += '$'
      j += 1
      i = 0
golly.setclipstr(rle)
golly.show('URL converted successfully')
