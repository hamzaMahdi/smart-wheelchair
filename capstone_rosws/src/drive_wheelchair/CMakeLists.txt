cmake_minimum_required(VERSION 2.8.3)
project(drive_wheelchair)


find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  sensor_msgs
  std_msgs
)


catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES drive_wheelchair
#  CATKIN_DEPENDS roscpp rospy sensor_msgs std_msgs
#  DEPENDS system_lib
)

###########
## Build ##
###########

## Specify additional locations of header files
## Your package locations should be listed before other locations
include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)
#add_executable(drive_wheelchair src/wheelchair.py)
#target_link_libraries(drive_wheelchair ${catkin_LIBRARIES})

