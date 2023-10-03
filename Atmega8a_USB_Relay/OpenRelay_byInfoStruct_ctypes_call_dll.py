'''
USB-RELAY-(1,2,4,8) Board
MCU: Atmega8a U-KR
Relay:SRD-05VDC-SL-C, DC:30V/ 10A, AC:250V/ 10A
Sample Code : Open relay by device info through struct pointer
Kurt Ding
'''
import ctypes


# 載入儀器控制的 DLL, 從.h file找到所有 function 及參數定義
instrument_dll = ctypes.CDLL('./usb_relay_device.dll')

# 宣告函數簽名, 初始化library, returns 0 on success and -1 on error
# int EXPORT_API usb_relay_init(void);
relay_init = instrument_dll.usb_relay_init
relay_init.restype = ctypes.c_int

# 釋放library用到的記憶體, returns 0 on success and -1 on error
# int EXPORT_API usb_relay_exit(void);
relay_exit = instrument_dll.usb_relay_exit
relay_exit.restype = ctypes.c_int

# 以下5個是有相關的功能, 要一起使用
# 定義枚舉類型及結構體, ctypes使用class來表示c資料類型
class device_type(ctypes.Structure):    # enum已在dll內定義,只要定義資料型態就可以用ctypes取得
    _fields_ = [('type', ctypes.c_int)]

class device_info(ctypes.Structure):
    _fields_ = [
        ('serial_number', ctypes.POINTER(ctypes.c_ubyte)),  # 使用指向字節的指針表示 unsigned char*
        ('device_path', ctypes.c_char_p),
        ('type', device_type),
        ('next', ctypes.POINTER('device_info')),  # 使用指針
    ]
# 列舉連接設備枚舉列表, 不須輸入參數就不用宣告argtypes, return type是usb_relay_device_info的pointer
# struct usb_relay_device_info EXPORT_API * usb_relay_device_enumerate(void);
info_enum = instrument_dll.usb_relay_device_enumerate
info_enum.restype = ctypes.POINTER(device_info)

# 釋放enum資料記憶體
# void EXPORT_API usb_relay_device_free_enumerate(struct usb_relay_device_info*);
free_enum = instrument_dll.usb_relay_device_free_enumerate
free_enum.restype = None
free_enum.argtypes = [ctypes.POINTER(device_info)]

# 開啟relay連結, 回傳handle
# int EXPORT_API usb_relay_device_open(struct usb_relay_device_info* device_info);
relay_open = instrument_dll.usb_relay_device_open
relay_open.restype = ctypes.c_int
relay_open.argtypes = [ctypes.POINTER(device_info)]

# 關閉設備連結
# void EXPORT_API usb_relay_device_close(int hHandle);
relay_close = instrument_dll.usb_relay_device_close
relay_close.restype = None
relay_close.argtypes = [ctypes.c_int]

# int EXPORT_API usb_relay_device_get_status(int hHandle, unsigned int *status);
relay_status = instrument_dll.usb_relay_device_get_status
relay_status.restype = ctypes.c_int
relay_status.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_uint)]

# int EXPORT_API usb_relay_device_open_one_relay_channel(int hHandle, int index);
relay_open_one_channel = instrument_dll.usb_relay_device_open_one_relay_channel
relay_open_one_channel.restype = ctypes.c_int
relay_open_one_channel.argtypes = [ctypes.c_int, ctypes.c_int]

# int EXPORT_API usb_relay_device_close_one_relay_channel(int hHandle, int index);
relay_close_one_channel = instrument_dll.usb_relay_device_close_one_relay_channel
relay_close_one_channel.restype = ctypes.c_int
relay_close_one_channel.argtypes = [ctypes.c_int, ctypes.c_int]

# int EXPORT_API usb_relay_device_open_all_relay_channel(int hHandle);
relay_open_all_channel = instrument_dll.usb_relay_device_open_all_relay_channel
relay_open_all_channel.restype = ctypes.c_int
relay_open_all_channel.argtypes = [ctypes.c_int]

# int EXPORT_API usb_relay_device_close_all_relay_channel(int hHandle);
relay_close_all_channel = instrument_dll.usb_relay_device_close_all_relay_channel
relay_close_all_channel.restype = ctypes.c_int
relay_close_all_channel.argtypes = [ctypes.c_int]

# 調用 usb_relay_init 函數
open_dll = relay_init()
print('usb_relay_init result:', open_dll)

info_list = info_enum()
current_device_info = info_list
handle = relay_open(current_device_info)    # 建立第一個設備的連結
print('usb_relay_device_open result:', handle)

while current_device_info:      # 窮舉所有設備
    print('Serial Number:', ctypes.string_at(current_device_info.contents.serial_number).decode('utf-8'))
    print(f"Device Path: {current_device_info.contents.device_path.decode('utf-8')}")
    print(f"Device Type: {current_device_info.contents.type.type}")
    print("---")
    current_device_info = current_device_info.contents.next

free_enum(info_list)
print('Free enum from memory')

index = -1
while index != 0:
    cmd = input('Keyin "O" for Open, "C" for Close: ')
    try:
        index = int(input('Keyin channel 1-4, 255 for all, 0 for exit: '))
    except ValueError:
        print('Fails value input.')
        index = 0
    if index == 255:
        result = relay_open_all_channel(handle) if cmd == 'O' else relay_close_all_channel(handle)
        if result == 0:
            show_res = 'OK'
        elif result == 2:
            show_res = 'Input is outnumber'
        else:
            show_res = 'Error'
        print('usb_relay_device_open_one_relay_channel result:', show_res)   
    elif index in range(1,9):
    # 調用 usb_relay_device_open_one_relay_channel 函數       
        result = relay_open_one_channel(handle, index) if cmd == 'O' else relay_close_one_channel(handle, index)
        show_res = 'OK' if result ==0 else 'Error or input outnumber'
        print('usb_relay_device_open_one_relay_channel result:', show_res)
    elif index == None:
        print('Index can not be null')
        break

    # 調用 usb_relay_device_get_status 函數
    status = ctypes.c_uint()
    result = relay_status(handle, ctypes.byref(status))
    show_res = 'OK' if result ==0 else 'Error'
    print('usb_relay_device_get_status result:', show_res)
    print('Status:', status.value)


# 調用 usb_relay_device_close 函數
relay_close(handle)

# 調用 usb_relay_exit 函數, 釋放記憶體
result = relay_exit()
print('usb_relay_exit result:', result)


