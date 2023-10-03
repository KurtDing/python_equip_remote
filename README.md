# Python_equip_remote
Demonstrate ctypes and pyvisa    
    
*Folder "./Local_OSW" :*    
Demonstrates to remote equipment through VISA resourename by pyvisa library.    
Uses VISA write to send SCPI and device specific command to equipment.    
This equipment can communicate through TCP/IP and RS232.
    
*Folder "./Atmega8a_USB_Relay" :*    
Can not see the resourename after board connection to computer.    
Document says using the dll file to control this device.
So this sample demonstrates using ctypes library to connect dll file and remote the device.    
  
*Folder "./ThorLabs_PM100D" :*    
Demonstrates to remote equipment by pyvisa and ctypes library.    
Established the linkage by pyVisa and performes the functions by dll file.    
There are command verion and dll verion in the folder.    
