import pyrealsense2 as rs
import numpy as np

pipeline = rs.pipeline()

# Start streaming
pipeline.start()
"""
frames = pipeline.wait_for_frames()
depth = frames.get_depth_frame()

width = depth.get_width()
height = depth.get_height()

dist = depth.get_distance(int(width/2), int(height/2))
print(dist)
"""
# Stop streaming
pipeline.stop()