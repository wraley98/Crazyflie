"""
Connect and Log Crazyflie Params
William Raley & bitcraze.io
16 Jan 24

Connects to the crazyflie and logs the information.
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

# URI to the Crazyflie to connect to 
uri = uri_helper.uri_from_env(default= 'radio://0/80/2M/E7E7E7E7E7')

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)

# prints parameter information for crazyflie
def param_stab_est_callback(name, value):
    print('The crazyflie has parameter ' + name + ' set at number: ' + value)

# sets crazyflie parameters
def simple_param_async(scf, groupstr, namestr):
    cf = scf.cf
    full_name = groupstr + '.' + namestr

    cf.param.add_update_callback(group=groupstr , name=namestr, cb=param_stab_est_callback)
    
    time.sleep(1) # so crazyflie does not immediately lose connection
    cf.param.set_value(full_name,2)
    time.sleep(1) # so crazyflie does not immediately lose connection
    cf.param.set_value(full_name,1)
    time.sleep(1) # so crazyflie does not immediately lose connection
   
# prints log information
def log_stab_callback(timestamp, data, logconf):
    print('[%d] [%s]: %s' % (timestamp , logconf.name , data))

# logs crazyflie data for a set period of time
def simple_log_async(scf , logconf):
    cf = scf.cf
    cf.log.add_config(logconf)
    logconf.data_received_cb.add_callback(log_stab_callback)
    logconf.start()
    time.sleep(1)
    logconf.stop()

# logs the data of the crazyfli cont. until user selects ctrl + c
def simple_log(scf , logconf):
  with SyncLogger(scf , lg_stab) as logger:
        
        for log_entry in logger:

            timestamp = log_entry[0]
            data = log_entry[1]
            logconf_name = log_entry[2]

            print('[%d] [%s]: %s' % (timestamp , logconf_name , data))


# simple connect function
def simple_connect():

    print("I'm connected! :D")
    time.sleep(3)
    print("Now I will disconnect :P")

# main function
if __name__ == '__main__':
    # Initialize the low-level drivers
    cflib.crtp.init_drivers()

    # Initializes log
    lg_stab = LogConfig(name='Stabilizer' , period_in_ms=10)

   # Initializes the log for roll, pitch, and yaw
    """
    lg_stab.add_variable('stabilizer.roll' , 'float')
    lg_stab.add_variable('stabilizer.pitch' , 'float')
    lg_stab.add_variable('stabilizer.yaw' , 'float')
    """

    # Initializes the log for x, y, and z
    lg_stab = LogConfig(name='Stabilizer' , period_in_ms=10)
    lg_stab.add_variable('kalman.stateX' , 'float')
    lg_stab.add_variable('kalman.stateY' , 'float')
    lg_stab.add_variable('kalman.stateZ' , 'float')


    # variables for params 
    group = "stabilizer"
    name = "estimator"


    with SyncCrazyflie(uri , cf=Crazyflie(rw_cache='./cache')) as scf:

        simple_connect()

       # simple_log(scf , lg_stab)

        #simple_log_async(scf , lg_stab)

        #simple_param_async(scf , group , name)






