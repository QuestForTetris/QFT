import golly
import re

cliplines = golly.getclipstr().splitlines()
data = list(''.join(cliplines[1:])[:-1])
#golly.note(''.join(data))

digitsi = '0123456789.ABCDEFG$'
digitso = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-_'

output = ''

while data != list(digitsi[0] * len(data)):
  dividend = 0
  for i in range(len(data)):
    dividend = dividend * len(digitsi) + digitsi.index(data[i])
    data[i] = digitsi[dividend / len(digitso)]
    dividend = dividend % len(digitso)
  output += digitso[dividend]
#  golly.note('{} {}'.format(''.join(data), str(dividend)))

#golly.note('https://electroredstoner.github.io/QFT/downloadrle.html?w={}&h={}&d={}'.format(*(re.match('x = (\d+), y = (\d+)', cliplines[0]).groups() + tuple([output[::-1]]))))
golly.setclipstr('https://electroredstoner.github.io/QFT/downloadrle.html?w={}&h={}&d={}'.format(*(re.match('x = (\d+), y = (\d+)', cliplines[0]).groups() + tuple([output[::-1]]))))
golly.show('URL copied to clipboard')
