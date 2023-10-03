'''
Thorlabs,PM100D,P0027168,2.7.0
Sample code that link equip by pyvisa and use Command (SCPI and PM100D specific)
Kurt Ding
'''
import pyvisa
import time

rm = pyvisa.ResourceManager()
print('Availiable equip :', rm.list_resources())
pm100d = rm.open_resource('USB0::0x1313::0x8078::P0027168::INSTR')

# Cmd DICT : my note
cmd = {'INFO':'*idn?',
       'Type':'CONF:POW',
       'AVG':'SENS:AVG:COUN?',
       'WAV':'SENS:CORR:WAV 1310',
       'AutoRange':'SENS:POW:RANG 1',     # AUTO {OFF|0|ON|1}
       'SetRef':'SENS:POW:REF 0.00030W',   # REFerence {MINimum|MAXimum|DEFault|<numeric_value>[W]} Sets a delta reference value in W
       'GetRef':'SENS:POW:REF?',
       'Delta':'SENS:POW:REF:STAT?',    # STATe {OFF|0|ON|1}
       'Unit':'SENS:POW:UNIT DBM',      # UNIT {W|DBM}
       'INIT':'INIT',
       'POW?':'MEAS:POW?',
       'LastVal':'FETC?'}             # Read last measurement data (SCPI Vol.2 §3.2)

pm100d.write('*RST')
pm100d.write(cmd['INFO'])
print(f'Equipment info :{pm100d.read()}')
pm100d.write('SENS:POW:REF:STAT 0; STAT?')
print(f'Delta mode stat: {pm100d.read()}')
print('Attu. Value: ', pm100d.query('CORR?'))

# A semicolon ( ; ) is used to separate commands within the 'SAME' subsystem,
# "CORR:BEAM 1; WAVE 1310" is the same as "CORR:BEAM 1", "CORR:WAVE 1310"
# Use a colon and a semicolon to link commands from different subsystems.
# "CORR:BEAM 1;:AVER 300"

unit = 'DBM'
pm100d.write(f'SENS:POW:UNIT {unit}; UNIT?')     # 設定要在開始新量測前
print(f'Unit setting: {pm100d.read()}')
pm100d.write('SENS:CORR:WAV 1310')
pm100d.write('CONF:POW')        # Set to power measurement, 可省略

# Measurement and read data
pm100d.write(cmd['INIT'])
for i in range(3):       
       pm100d.write('MEAS:POW?')          # read power
       pow = float(pm100d.read())
       if unit == 'W':
              print(f'{pow*10**6} uW')
       elif unit == 'DBM':
              print(f'{pow} dbm')
       time.sleep(0.5)
pm100d.write('ABOR') 

# Another way to read value, start new measurement and read data in one cmd.
# I would like using this for single read.
'''
for i in range(3):  
    pm100d.write('read?')
    print(pm100d.read())
'''

pm100d.write('*CLS')        # 清除設備buffer
pm100d.control_ren(0)       # 取消remote狀態
rm.close()
