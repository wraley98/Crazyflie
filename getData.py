"""
Get Data
William Raley
16 Jan 24

retrieves data from the crazyflie program. 
"""

# standard python libraries
import logging
import time


# crazyflie library
import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.utils import uri_helper

# crazyflie log imports
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncLogger import SyncLogger

# Created import
import plotData

# Takes the information reported from data and puts it in the correct coord array
def log_stab_callback(timestamp, data, logconf):
   
   # converts data to string
   dataString = '%s\n'% data
   # spaces and periods are only allowed characters
   allowedString = '. '
   # removes all characters that are not numbers or in allowedString
   dataStringCut = ''.join(char for char in dataString if char.isdigit() or char in allowedString)
   # removes the excess .
   dataStringFinal = dataStringCut.replace(". ", "")

   # tracks what char in the data is currently on
   charCount = 0
   # tracks which coord is currently on
   coordCount = 0
 
   for char in dataStringFinal:
       # if decimal is found
       if char == ".":
           # create new string that contains the coord location
           coordString = dataStringFinal[charCount - 1: charCount + 5]

           if coordString == '0.0 0.':
               coordFloat = 0.0
           else:
                # creates float from string
                coordFloat = float(coordString)
           
           if coordCount == 0: # adds x coord
               xLocation.append(coordFloat)
           elif coordCount == 1: # adds y coord
               yLocation.append(coordFloat)
           else: # adds z coord
               zLocation.append(coordFloat)
           coordCount += 1 # increments to next coord
        # increments to next char
       charCount += 1
            

# logs crazyflie data for a set period of time
def simple_log_async(scf , logconf):
    cf = scf.cf
    cf.log.add_config(logconf)
    logconf.data_received_cb.add_callback(log_stab_callback)
    logconf.start()
    time.sleep(10) # length of time to take data for 
    logconf.stop()



# URI to the Crazyflie to connect to 
uri = uri_helper.uri_from_env(default= 'radio://0/80/2M/E7E7E7E7E7')

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)

# Arrays for data storage

xLocation = []
yLocation = []
zLocation = []

# main function
if __name__ == '__main__':
    # Initialize the low-level drivers
    cflib.crtp.init_drivers()


    # Initializes the log for x, y, and z
    lg_stab = LogConfig(name='Stabilizer' , period_in_ms=10)
 
    lg_stab.add_variable('kalman.stateX', 'float') # x data point
    lg_stab.add_variable('kalman.stateY', 'float') # y data point
    lg_stab.add_variable('kalman.stateZ' , 'float') # z data point
    """
    lg_stab.add_variable('stateEstimate.x', 'float') # x data point
    lg_stab.add_variable('stateEstimate.y', 'float') # y data point
    lg_stab.add_variable('stateEstimate.z' , 'float') # z data point
    """
    
    with SyncCrazyflie(uri , cf=Crazyflie(rw_cache='./cache')) as scf:
       simple_log_async(scf , lg_stab)


    ### ENTER TRUE LOCATION HERE ###
    ###  Enter Values in Inches  ###

    trueX = 1.784-0.269
    trueY = [2.1-
    #- .177
    # - .177 - 1.419
     - .177 - 1.419 - 0.478
    ]
    trueZ = 0.479-0.528
    trueLocation = [trueX , trueY[0] , trueZ]

    #################################
   
    # runs absolute and relative plots
    plotData.compareData(xLocation, yLocation, zLocation , trueLocation)
  




