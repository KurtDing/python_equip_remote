'''
台式光學開關控制, read不能指定讀取byte數, 要設終止符號
Sample code of pyvisa 
MIC local 20 channel OSW, termination is '>', not '\n'.
Kurt Ding
'''
import pyvisa
import time

rm = pyvisa.ResourceManager()
print(rm.list_resources())
osw = rm.open_resource('ASRL7::INSTR', write_termination='\r', read_termination='>')
#osw = rm.open_resource('TCPIP0::192.168.1.100::inst0::INSTR', read_termination='>')
osw.baud_rate = 19200
osw.stop_bits = pyvisa.constants.StopBits.one
osw.parity = pyvisa.constants.Parity.none
#osw.write_termination = '>'    # another way to set terminal
osw.timeout = 5000     #msec

cmd = {'S01':'<AD01_S_01>',
       'S13':'<AD01_S_13>',
       'C02':'<AD01_C_02>',     # return void
       'sScanRange':'<AD01_B_001_E_018>',
       'qScanRange':'<AD01_B_E_?>',
       'Scan':'<AD01_A_10>',
       'qChan':'<AD01_MAX_?>',
       'ChangStat':'AD01_G_03'}

osw.write(cmd['Scan'])
byte_count = 0

while 1:
    while 1:
        byte_count = osw.bytes_in_buffer
        if byte_count > 0:
            print('byte in port: ', byte_count)
            break
        time.sleep(0.3)
        
    data = osw.read()
    print(data)
    if data == '<AD01_18':
        osw.write(cmd['C02'])
        break

osw.close()
