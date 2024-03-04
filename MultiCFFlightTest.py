"""
Multi CF Flight Test
William Raley
29 Jan 24

Test for flying multiple crazyflies at once.
"""

# Python Imports
import threading
import time

# Crazyflie Import
import cflib.crtp
from cflib.utils import uri_helper
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.position_hl_commander import PositionHlCommander
from cflib.crazyflie.log import LogConfig

class MultiCfFlight:
    xLocation = []
    yLocation = []
    zLocation = []
    position_estimate = []
    
    def __init__ (self):
        # Storage for location data
        self.xLocation = []
        self.yLocation = []
        self.zLocation = []

        self.position_estimate = [0 , 0 , 0]

    # Creates log
    def createLog(self , scf):
            # prepares log data
            logconf = LogConfig(name = 'Position', period_in_ms=10)
        
            logconf.add_variable('kalman.stateX' , 'float')
            logconf.add_variable('kalman.stateY' , 'float')
            logconf.add_variable('kalman.stateZ' , 'float')
            """
            logconf.add_variable('stateEstimate.x' , 'float')
            logconf.add_variable('stateEstimate.y' , 'float')
            logconf.add_variable('stateEstimate.z' , 'float')
            """
            scf.cf.log.add_config(logconf)
            # prints position data
            logconf.data_received_cb.add_callback(self.log_pos_callback)
            #logconf.data_received_cb.add_callback(log_stab_callback)
            # logs position data for graphing
            #logconf.data_received_cb.add_callback(log_stab_callback)

            return logconf

    # Sets the current position
    def setPos(self , logConf ,  scf):
        # Starts the log
        logConf.start()
        time.sleep(0.1)
        logConf.stop()
        logConf.delete()
        
        return self.createLog(scf)

    def activate_led_bit_mask(self , scf):
        scf.cf.param.set_value('led.bitmask', 255)

    def deactivate_led_bit_mask(self, scf):
        scf.cf.param.set_value('led.bitmask', 0)

    def light_check(self , scf):
        self.activate_led_bit_mask(scf)
        time.sleep(1)
        self.deactivate_led_bit_mask(scf)
        time.sleep(1)

    def fly(self, scf):
        with PositionHlCommander(scf) as pc:
            # Sets Position
            pc._x = self.position_estimate[0]
            pc._y = self.position_estimate[1]
            pc._z = self.position_estimate[2]
            # height to land at
            lh = pc._y

            # Sets flying status to off
            pc._is_flying = False

            # Take Off
            #pc.take_off(height=1.0 , velocity = speed)
            pc.go_to(pc._x , pc._y , 1)
            time.sleep(5)

            # move
            pc.go_to(pc._x , pc._y + 1 , 1)
            time.sleep(5)

            # landing sequence
            pc.go_to(pc._x , pc._y + 1  , 0.55)
            time.sleep(2)
            pc._is_flying = True
            pc.land(velocity = 0.1)

    # Sets location to current estimate
    def log_pos_callback(self , timestamp, data, logconf):
        
        #print(data)
    
        self.position_estimate[0] = data['kalman.stateX']
        self.position_estimate[1] = data['kalman.stateY']
        self.position_estimate[2] = data['kalman.stateZ']
        """
        position_estimate[0] = data['stateEstimate.x']
        position_estimate[1] = data['stateEstimate.y']
        position_estimate[2] = data['stateEstimate.z']
        """
        self.xLocation.append(self.position_estimate[0])
        self.yLocation.append(self.position_estimate[1])
        self.zLocation.append(self.position_estimate[2]) 

    def run(self , uri):

        cflib.crtp.init_drivers()
        
        with SyncCrazyflie(uri , cf=Crazyflie(rw_cache='./cache')) as scf:
            # Creates log and sets initial estimate on postion
            logConf = self.createLog(scf)
            logConf = self.setPos(logConf ,  scf) 
            print(self.position_estimate)
        
            #light_check(scf)
        
            self.fly(scf)
