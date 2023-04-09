# ble_scan_connect.py:
from bluepy.btle import Peripheral, UUID, AssignedNumbers
from bluepy.btle import Scanner, DefaultDelegate
class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)
    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print ("Discovered device", dev.addr)
        elif isNewData:
            print ("Received new data from", dev.addr)
scanner = Scanner().withDelegate(ScanDelegate())
devices = scanner.scan(10.0)
n=0
addr = []
for dev in devices:
    print ("%d: Device %s (%s), RSSI=%d dB" % (n, dev.addr,
    dev.addrType, dev.rssi))
    addr.append(dev.addr)
    n += 1
    for (adtype, desc, value) in dev.getScanData():
        print (" %s = %s" % (desc, value))

number = input('Enter your device number: ')
print ('Device', number)
num = int(number)
print (addr[num])
#
print ("Connecting...")
dev = Peripheral(addr[num], 'random')
#
print ("Services...")
for svc in dev.services:
    print (str(svc))
#

CharHandel2Svc = {}
Data = {}

print ("Setting CCCDs...")
for svc in dev.services:
    for ch in svc.getCharacteristics():
        desc = ch.getDescriptors(0x2902)
        if(len(desc)):
            dev.writeCharacteristic(desc[0].handle, b"\x01\x00")
            Data[svc.uuid] = 0
            CharHandel2Svc[ch.getHandle()] = svc.uuid
            


def print_data(cHandle, data):
    Data[CharHandel2Svc[cHandle]] = data[-1]
dev.delegate.handleNotification = print_data

print ("Waiting notifications...")

try:
    while True:
        if not dev.waitForNotifications(10):
            continue
        for key in Data:
            print(key, Data[key])
        print("")

#
finally:
    dev.disconnect()