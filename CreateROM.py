from glife import *
import golly as g

bitOff = pattern('4.DBD$5.B$4.2B$5.D$D.B2.F2.3D$3BD2FD4B$D4.D2.3D$5.B$4.DBD$4.DBD$4.DBD!')
bitOn = pattern('4.DBD$5.B.B$4.2B.2B$5.D.2D$D.B2.F.D2.D$3BD2FDF.2B$D4.D2.B.D$5.B2.B$4.DBD$4.DBD$4.DBD!')

g.addlayer()
g.new('ROM')
g.setrule('Varlife')

code = g.getclipstr()
opcodes = {'MNZ': '0000',
           'MLZ': '0001',
           'ADD': '0010',
           'SUB': '0011',
           'AND': '0100',
           'OR' : '0101',
           'XOR': '0110',
           'ANT': '0111',
           'SL' : '1000',
           'SRL': '1001'}

modes = {'A': '01',
         'B': '10',
         'C': '11'}

x = 0
#Iterate through the instructions, backwards
for line in code.split('\n')[::-1]:
  bincode = []
  y = 1
#Remove starting numbering and comments
  instruction = line.split(';')[0].split('.')[-1].split()
#Parse each argument
  for argument in instruction[:0:-1]:
    if argument[0] in modes:
      bincode.append('{}{:016b}'.format(modes[argument[0]], 65535 & int(argument[1:], 0)))
    else:
      bincode.append('00{:016b}'.format((65535 & int(argument, 0)))
  bincode.append(opcodes[instruction[0]]) #Add opcode at end

#Insert beginning clock generation line
  bitOn.put(11*x, 0)
#Paste ROM bits
  for bit in ''.join(bincode):
    if bit == '0':
      bitOff.put(11*x, 11*y)
    else:
      bitOn.put(11*x, 11*y)
    y += 1
  x += 1

#0. MLZ -1 3 3;
#1. MLZ -1 7 6; preloadCallStack
#2. MLZ -1 2 1; beginDoWhile0_infinite_loop
#3. MLZ -1 1 4; beginDoWhile1_trials
#4. ADD A4 2 4;
#5. MLZ -1 A3 5; beginDoWhile2_repeated_subtraction
#6. SUB A5 A4 5;
#7. SUB 0 A5 2;
#8. MLZ A2 5 0;
#9. MLZ 0 0 0; endDoWhile2_repeated_subtraction
#10. MLZ A5 3 0;
#11. MNZ 0 0 0; endDoWhile1_trials
#12. SUB A4 A3 2;
#13. MNZ A2 15 0; beginIf3_prime_found
#14. MNZ 0 0 0;
#15. MLZ -1 A3 1; endIf3_prime_found
#16. ADD A3 2 3;
#17. MLZ -1 3 0;
#18. MLZ -1 1 4; endDoWhile0_infinite_loop
