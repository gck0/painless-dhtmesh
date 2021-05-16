import serial

TRAPSRV = "192.168.122.180"
LOCALIP = "192.168.122.1"

## PRENDE INPUT DA SERIALE
s = serial.Serial('/dev/ttyUSB0', 115200)
while True:
    #legge, ripulisce e divide in due parti (rifare con regex)
    str = s.readline().decode().strip('rcv from \n').split(" = ",1)
    print(str[0])
    print(str[1])

    ## INVIO NOTIFICA SNMP TRAP AL SERVER ##
    from pysnmp.hlapi import *

    iterator = sendNotification(
        SnmpEngine(),
        CommunityData('public', mpModel=0),
        UdpTransportTarget((TRAPSRV, 162)),
        ContextData(),
        'trap',
        NotificationType(
            ObjectIdentity('1.3.6.1.2.1.1')
        ).addVarBinds(
            ('1.3.6.1.6.3.18.1.3.0', '192.168.122.1'),
            ('1.3.6.1.2.1.1.1', str[1]),        #sysdescr
            ('1.3.6.1.2.1.1.5', str[0]),        #sysname
        )
    )

    errorIndication, errorStatus, errorIndex, varBinds = next(iterator) 
