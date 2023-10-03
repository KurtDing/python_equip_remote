'''
Thorlabs,PM100D,P0027168,2.7.0
Sample code that link equip by pyvisa and use SCPI (Standard Commands for Pro-grammable Instruments)
Use FATCH? , change unit function is not okay
Kurt Ding
'''
import pyvisa
import ctypes
import time

rm = pyvisa.ResourceManager()
print('Availiable equip :', rm.list_resources())
pm100d = rm.open_resource('USB0::0x1313::0x8078::P0027168::INSTR')

cmd = {'INFO':'*idn?',
       'Type':'CONF:POW',
       'AutoRange':'POW:RANG 1',     # AUTO {OFF|0|ON|1}
       'SetRef':'POW:REF 1',   # REFerence {MINimum|MAXimum|DEFault|<numeric_value>[W]} Sets a delta reference value in W
       'GetRef':'POW:REF?',
       'Delta':'POW:REF:STAT?',    # STATe {OFF|0|ON|1}
       'Unit':'POW:UNIT DBM',      # UNIT {W|DBM}
       'INIT':'INIT',
       'POW?':'MEAS:POW',
       'LastVal':'FETC?'}             # Read last measurement data (SCPI Vol.2 §3.2)

pm100d.write(cmd['INFO'])
print('Equipment info :', pm100d.read())
pm100d.write(cmd['GetRef'])
print(f'Ref: {pm100d.read()}, Unit: W')

unit = 'DBM'
pm100d.write(f'CONF:POW')     # A semicolon ( ; ) is used to separate commands within the 'SAME' subsystem,

for i in range(3):
       pm100d.write(cmd['INIT'])   # 沒有初始化會一直FETCH到舊的值
       pm100d.write(f'POW:UNIT {unit}')
       pm100d.write(f'POW:UNIT?')
       print(f'Unit =  {pm100d.read()}')
       pm100d.write(cmd['LastVal'])
       pow = float(pm100d.read())
       if unit == 'W':
              print(f'{pow*10**6} uW')
       elif unit == 'DBM':
              print(f'{pow} dbm')
       time.sleep(0.5)

pm100d.write('*CLS') 
pm100d.control_ren(0)
rm.close()
