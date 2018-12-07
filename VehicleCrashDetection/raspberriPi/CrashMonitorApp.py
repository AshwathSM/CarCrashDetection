from time import sleep
import SensorAdaptor
import CoapServerApp

sensorAdaptor = SensorAdaptor.SensorAdaptor()
waitfornote = CoapServerApp.WaitForNote()
sensorAdaptor.run()

print('THIS IS TO TEST')
waitfornote.waitForNotify()
while(True):
    sleep(5)
    pass
