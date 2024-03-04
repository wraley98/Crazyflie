"""
Multi CF Flight Test
William Raley
29 Jan 24

Test for flying multiple crazyflies at once.
"""

# Python Imports
import threading
import time
import multiprocessing as mp

# CF Import
from cflib.utils import uri_helper

# Self Created Import
import MultiCFFlightTest as mcft


# URI to the Crazyflie to connect to 
cf1 = uri_helper.uri_from_env(default= 'radio://0/80/2M/E7E7E7E701')
cf2 = uri_helper.uri_from_env(default= 'radio://0/80/2M/E7E7E7E702')
cfList = [cf1 , cf2]
threads = []

for cf in cfList:
    newMCFT = mcft.MultiCfFlight()
    thread = threading.Thread(target=newMCFT.run , args=(cf,))
    threads.append(thread)
    thread.start()
    time.sleep(1)

for thread in threads:
    thread.join()

print('complete')

