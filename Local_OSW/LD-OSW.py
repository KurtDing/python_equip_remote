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
# Use correct resource name of your device to open it
osw = rm.open_resource('ASRL7::INSTR', write_termination='\r', read_termination='>')
#osw = rm.open_resource('TCPIP0::192.168.1.100::inst0::INSTR', read_termination='>')
osw.baud_rate = 19200
osw.stop_bits = pyvisa.constants.StopBits.one
osw.parity = pyvisa.constants.Parity.none
#osw.write_termination = '>'    # another way to set terminal
osw.timeout = 5000     #msec

cmd = {'S01':'<AD01_S_01>',     # SW01 set to channel 01, return ok
       'S13':'<AD01_S_13>',     # SW01 set to channel 13, return ok
       'C04':'<AD01_C_04>',     # SW01 set to channel 02, and return void
       'qChn':'<AD01_T_CHN?>',      # SW01 query channel position
       'sScanRange':'<AD01_B_001_E_018>',   # SW01 set scan range from chn01 to chn 18
       'qScanRange':'<AD01_B_E_?>',         # SW01 query scan range
       'Scan':'<AD01_A_10>',        # SW01 start scan, interval 10*100ms
       'tScan':'<AD01_A_T_00_01_30>',       # SW01 start scan, trigger switch every 00:01:30
       'qChan':'<AD01_MAX_?>',      # SW01 query max channel counts
       'ChangStat':'AD01_G_03'}     # Change addr of SW01 to 03

osw.write(cmd['C04'])
osw.write(cmd['Scan'])
byte_count = 0

while True:
    while 1:
        byte_count = osw.bytes_in_buffer
        if byte_count > 0:
            print('Received, byte in port: ', byte_count)
            break
        time.sleep(0.1)
        
    data = osw.read()
    print(data)
    if data == '<AD01_18':
        osw.write('<AD01_M_STA?>')      # Check OSW status and Stop scan
        break

osw.close()
