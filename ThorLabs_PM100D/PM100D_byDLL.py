'''
Thorlabs,PM100D,P0027168,2.7.0
Sample code that equip controlled by dll, use library pyvisa and ctypes
Kurt Ding
'''
import pyvisa
import ctypes
import time

# 載入 dll
pm100d_dll = ctypes.CDLL('./PM100D_64.dll')

# 聲明函數簽名
# ViStatus _VI_FUNC PM100D_init (ViRsrc resourceName, ViBoolean IDQuery, ViBoolean resetDevice, ViPSession instrumentHandle);
PM100D_init = pm100d_dll.PM100D_init
PM100D_init.restype = ctypes.c_int
PM100D_init.argtypes = [ctypes.c_char_p, ctypes.c_bool, ctypes.c_bool, ctypes.POINTER(ctypes.c_void_p)]

# ViStatus _VI_FUNC PM100D_findRsrc (ViSession instrumentHandle, ViUInt32 *resourceCount);
PM100D_findRsrc = pm100d_dll.PM100D_findRsrc
PM100D_findRsrc.restype = ctypes.c_int
PM100D_findRsrc.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint32)]

# ViStatus _VI_FUNC PM100D_getRsrcName (ViSession instrumentHandle, ViUInt32 index, ViChar resourceName[]);
PM100D_getRsrcName = pm100d_dll.PM100D_getRsrcName
PM100D_getRsrcName.restype = ctypes.c_int
PM100D_getRsrcName.argtypes = [ctypes.c_void_p, ctypes.c_uint32, ctypes.c_char_p]

# ViStatus _VI_FUNC PM100D_getRsrcInfo (ViSession instrumentHandle, ViUInt32 index, ViChar modelName[], 
# ViChar serialNumber[], ViChar manufacturer[], ViBoolean *deviceAvailable);
PM100D_getRsrcInfo = pm100d_dll.PM100D_getRsrcInfo
PM100D_getRsrcInfo.restype = ctypes.c_int
PM100D_getRsrcInfo.argtypes = [ctypes.c_void_p, ctypes.c_uint32, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_bool)]

# ViStatus _VI_FUNC PM100D_getSensorInfo (ViSession instr, ViChar _VI_FAR name[], ViChar _VI_FAR snr[], 
# ViChar _VI_FAR message[], ViPInt16 pType, ViPInt16 pStype, ViPInt16 pFlags);
PM100D_getSensorInfo = pm100d_dll.PM100D_getSensorInfo
PM100D_getSensorInfo.restype = ctypes.c_int
PM100D_getSensorInfo.argtypes = [
    ctypes.c_void_p,
    ctypes.c_char_p,
    ctypes.c_char_p,
    ctypes.c_char_p,
    ctypes.POINTER(ctypes.c_int16),
    ctypes.POINTER(ctypes.c_int16),
    ctypes.POINTER(ctypes.c_int16)
    ]

# ViStatus _VI_FUNC PM100D_errorMessage (ViSession instrumentHandle, ViStatus statusCode, ViChar _VI_FAR description[]);
PM100D_errorMessage = pm100d_dll.PM100D_errorMessage
PM100D_errorMessage.restype = ctypes.c_int
PM100D_errorMessage.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_char_p]

# ViStatus _VI_FUNC PM100D_setAttenuation (ViSession instrumentHandle, ViReal64 attenuation);
PM100D_setAtt = pm100d_dll.PM100D_setAttenuation
PM100D_setAtt.restype = ctypes.c_int
PM100D_setAtt.argtypes = [ctypes.c_void_p, ctypes.c_double]
# ViStatus _VI_FUNC PM100D_getAttenuation (ViSession instrumentHandle, ViInt16 attribute, ViPReal64 attenuation);
PM100D_getAtt = pm100d_dll.PM100D_getAttenuation
PM100D_getAtt.restype = ctypes.c_int
PM100D_getAtt.argtypes = [ctypes.c_void_p, ctypes.c_int16, ctypes.POINTER(ctypes.c_double)]

# ViStatus _VI_FUNC PM100D_setWavelength (ViSession instrumentHandle, ViReal64 wavelength);
PM100D_setWL = pm100d_dll.PM100D_setWavelength
PM100D_setWL.restype = ctypes.c_int
PM100D_setWL.argtypes = [ctypes.c_void_p, ctypes.c_double]
# ViStatus _VI_FUNC PM100D_getWavelength (ViSession instrumentHandle, ViInt16 attribute, ViPReal64 wavelength);
PM100D_getWL = pm100d_dll.PM100D_getWavelength
PM100D_getWL.restype = ctypes.c_int
PM100D_getWL.argtypes = [ctypes.c_void_p, ctypes.c_int16, ctypes.POINTER(ctypes.c_double)]

# ViStatus _VI_FUNC PM100D_setPowerAutoRange (ViSession instrumentHandle, ViBoolean powerAutorangeMode);
PM100D_setPowerAutorange = pm100d_dll.PM100D_setPowerAutoRange
PM100D_setPowerAutorange.restype = ctypes.c_int
PM100D_setPowerAutorange.argtypes = [ctypes.c_void_p, ctypes.c_bool]
# ViStatus _VI_FUNC PM100D_getPowerAutorange (ViSession instrumentHandle, ViPBoolean powerAutorangeMode);
PM100D_getPowerAutorange = pm100d_dll.PM100D_getPowerAutorange
PM100D_getPowerAutorange.restype = ctypes.c_int
PM100D_getPowerAutorange.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_bool)]
# ViStatus _VI_FUNC PM100D_setPowerRange (ViSession instrumentHandle, ViReal64 power_to_Measure);
PM100D_setPowerRange = pm100d_dll.PM100D_setPowerRange
PM100D_setPowerRange.restype = ctypes.c_int
PM100D_setPowerRange.argtypes =[ctypes.c_void_p, ctypes.c_double]
# ViStatus _VI_FUNC PM100D_getPowerRange (ViSession instrumentHandle, ViInt16 attribute, ViPReal64 powerValue);
PM100D_getPowerRange = pm100d_dll.PM100D_getPowerRange
PM100D_getPowerRange.restype = ctypes.c_int
PM100D_getPowerRange.argtypes =[ctypes.c_void_p, ctypes.c_int16, ctypes.POINTER(ctypes.c_double)]

# ViStatus _VI_FUNC PM100D_setPowerRef (ViSession instrumentHandle, ViReal64 powerReferenceValue);
PM100D_setPowerRef = pm100d_dll.PM100D_setPowerRef
PM100D_setPowerRef.restype = ctypes.c_int
PM100D_setPowerRef.argtypes =[ctypes.c_void_p, ctypes.c_double]
# ViStatus _VI_FUNC PM100D_getPowerRef (ViSession instrumentHandle, ViInt16 attribute, ViPReal64 powerReferenceValue);
PM100D_getPowerRef = pm100d_dll.PM100D_getPowerRef
PM100D_getPowerRef.restype = ctypes.c_int
PM100D_getPowerRef.argtypes =[ctypes.c_void_p, ctypes.c_int16, ctypes.POINTER(ctypes.c_double)]
# ViStatus _VI_FUNC PM100D_setPowerRefState (ViSession instrumentHandle, ViBoolean powerReferenceState);
PM100D_setPowerRefState = pm100d_dll.PM100D_setPowerRefState
PM100D_setPowerRefState.restype = ctypes.c_int
PM100D_setPowerRefState.argtypes =[ctypes.c_void_p, ctypes.c_bool]
# ViStatus _VI_FUNC PM100D_getPowerRefState (ViSession instrumentHandle, ViPBoolean powerReferenceState);
PM100D_getPowerRefState = pm100d_dll.PM100D_getPowerRefState
PM100D_getPowerRefState.restype = ctypes.c_int
PM100D_getPowerRefState.argtypes =[ctypes.c_void_p, ctypes.POINTER(ctypes.c_bool)]

# ViStatus _VI_FUNC PM100D_setPowerUnit (ViSession instrumentHandle, ViInt16 powerUnit);
PM100D_setPowerUnit = pm100d_dll.PM100D_setPowerUnit
PM100D_setPowerUnit.restype = ctypes.c_int
PM100D_setPowerUnit.argtypes = [ctypes.c_void_p, ctypes.c_int16]
# ViStatus _VI_FUNC PM100D_getPowerUnit (ViSession instrumentHandle, ViPInt16 powerUnit);
PM100D_getPowerUnit = pm100d_dll.PM100D_getPowerUnit
PM100D_getPowerUnit.restype = ctypes.c_int
PM100D_getPowerUnit.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int16)]

# ViStatus _VI_FUNC PM100D_measPower (ViSession instrumentHandle, ViPReal64 power);
PM100D_measPower = pm100d_dll.PM100D_measPower
PM100D_measPower.restype = ctypes.c_int
PM100D_measPower.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_double)]

# ViStatus _VI_FUNC PM100D_close (ViSession instrumentHandle);
PM100D_close = pm100d_dll.PM100D_close
PM100D_close.restype = ctypes.c_int
PM100D_close.argtypes = [ctypes.c_void_p]

# =============================================================================
def decode_err(instrument_handle, status_code):
    msg_buffer = ctypes.create_string_buffer(256)
    status = PM100D_errorMessage(instrument_handle, status_code, msg_buffer)
    if status != 0:
        print(f"PM100D_errorMessage failed with status code {status}")
    else:
        print(f"Error Message: {msg_buffer.value.decode('utf-8')}")

# =============================================================================
# 初始化 VISA
rm = pyvisa.ResourceManager()

# 打開設備
resource_name = 'USB0::0x1313::0x8078::P0027168::INSTR'  # 設備資源名稱
instrument = rm.open_resource(resource_name)
instrument_handle = ctypes.c_void_p(instrument.session)

# 調用 PM100D_init 初始化函數
status = PM100D_init(resource_name.encode('utf-8'), True, True, ctypes.byref(instrument_handle))
if status != 0:
    print(f"PM100D_init failed with status code {status}")

'''
# 找設備資源
resource_count = ctypes.c_uint32(0)
status = PM100D_findRsrc(instrument_handle, ctypes.byref(resource_count))
print(f"Resource Count: {resource_count.value}")

# 獲取設備資源名稱
index = 0  # 要找的設備索引
resource_name_buffer = ctypes.create_string_buffer(256)  # 緩衝區
status = PM100D_getRsrcName(instrument_handle, index, resource_name_buffer)
print(f"Resource Name: {resource_name_buffer.value.decode('utf-8')}\n")

# 取得設備資源訊息
model_name_buffer = ctypes.create_string_buffer(256)  # 适当大小的缓冲区
serial_number_buffer = ctypes.create_string_buffer(256)
manufacturer_buffer = ctypes.create_string_buffer(256)
device_available = ctypes.c_bool(False)
status = PM100D_getRsrcInfo(instrument_handle, index, model_name_buffer, serial_number_buffer, manufacturer_buffer, ctypes.byref(device_available))
print(f"Model Name: {model_name_buffer.value.decode('utf-8')}")
print(f"Serial Number: {serial_number_buffer.value.decode('utf-8')}")
print(f"Manufacturer: {manufacturer_buffer.value.decode('utf-8')}")
print(f"Device Available: {device_available.value}\n")

# 取得sensor資訊
name_buffer = ctypes.create_string_buffer(256)
snr_buffer = ctypes.create_string_buffer(256)
message_buffer = ctypes.create_string_buffer(256)
pType = ctypes.c_int16(0)
pStype = ctypes.c_int16(0)
pFlags = ctypes.c_int16(0)
status = PM100D_getSensorInfo(instrument_handle, name_buffer, snr_buffer, message_buffer, ctypes.byref(pType), ctypes.byref(pStype), ctypes.byref(pFlags))
print(f"Sensor Name: {name_buffer.value.decode('utf-8')}")
print(f"Sensor Serial Number: {snr_buffer.value.decode('utf-8')}")
print(f"Sensor Message: {message_buffer.value.decode('utf-8')}")
print(f"Sensor Type: {pType.value}")
print(f"Sensor Subtype: {pStype.value}")
print(f"Sensor Flags: {pFlags.value}\n")'''

# 設定及顯示參考值狀態及數值, 單位W
attribute = ctypes.c_int16(0)  # 0 = set value, 1 = MIN, 2 = MAX
ref_state = ctypes.c_bool(False)
PM100D_setPowerRefState(instrument_handle, ref_state)
PM100D_getPowerRefState(instrument_handle, ctypes.byref(ref_state))
print(f"Delta mode State: {ref_state.value}")
ref_value = ctypes.c_double(0.0001)     # 必須>0, 單位W
PM100D_setPowerRef(instrument_handle, ref_value)
status = PM100D_getPowerRef(instrument_handle, attribute, ctypes.byref(ref_value))
print(f"Reference Value: {ref_value.value*10**6} uW\n")

'''# AutoRange設定,初始化後會設為AUTO
power_autorange_mode = ctypes.c_bool(False)
PM100D_setPowerAutorange(instrument_handle, power_autorange_mode)
status = PM100D_getPowerAutorange(instrument_handle, ctypes.byref(power_autorange_mode))
print(f"Power Autorange Mode: {power_autorange_mode.value}")

# 設定及顯示功率上限, 設定值10**0 ~ 10**-5, 關閉autorange才有作用
attribute = ctypes.c_int16(0)  # 0 = set value, 1 = MIN, 2 = MAX
power_value = ctypes.c_double(0.1)
PM100D_setPowerRange(instrument_handle, power_value)
status = PM100D_getPowerRange(instrument_handle, attribute, ctypes.byref(power_value))
if status != 0:
    print(f"PM100D_getPowerRange failed with status code {status}")
else:
    print(f"Power Value: {power_value.value}\n")'''

# 設定波長
attribute = ctypes.c_int16(0)  # 0 = set value, 1 = MIN, 2 = MAX
wavlength = ctypes.c_double(1310)
PM100D_setWL(instrument_handle, wavlength)
status = PM100D_getWL(instrument_handle, attribute, ctypes.byref(wavlength))
if status != 0:
    print(f"PM100D_getWavelength failed with status code {status}")
else:
    print(f"Wavelength Value: {wavlength.value}\n")
time.sleep(0.5) # 需要等待切換完成

# 單位設定,初始化後會設為Watt, [0]=WATT, [1]=DBM
pow_unit = 'DBM'
power_unit = ctypes.c_int16(1 if pow_unit == 'DBM' else 0)
PM100D_setPowerUnit(instrument_handle, power_unit)
status = PM100D_getPowerUnit(instrument_handle, ctypes.byref(power_unit))
print(f"Power Unit: {power_unit.value}")
time.sleep(0.5) # 需要等待切換完成

# 調用 PM100D_measPower 測量功率函數
power = ctypes.c_double(0.0)
status = PM100D_measPower(instrument_handle, ctypes.byref(power))
if status != 0:
    print(f"PM100D_measPower failed with status code {status}")
else:
    print(f"Measured Power: {power.value} {pow_unit}")

# 調用 PM100D_close 關閉設備函數
status = PM100D_close(instrument_handle)
if status != 0:
    print(f"PM100D_close failed with status code {status}")

# 關閉 VISA
rm.close()
