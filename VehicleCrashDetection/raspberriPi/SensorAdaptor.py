import RPi.GPIO as IO
from time import sleep
import CoapClientApp
class SensorAdaptor():

    
    IO.setwarnings(False)
    IO.setmode(IO.BCM)
    IO.setup(18,IO.IN) 
   

  #  def __init__(self):
            
        
    
    def run(self):
        while 1:    
            if(IO.input(18)==True):
                print("object")
                CoapClientApp.startApp()                
                break 
            #`:else:
                # print("no object")
        








