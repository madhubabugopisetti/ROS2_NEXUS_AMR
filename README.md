# ROS2_NEXUS_AMR

## Installation
- ROS2 JAZZY: https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html
- GAZEBO HARMONIC: https://gazebosim.org/docs/harmonic/install_ubuntu
- ROS–Gazebo bridge: ``` sudo apt install ros-jazzy-ros-gz-sim ros-jazzy-ros-gz-bridge ros-jazzy-ros-gz ```
- OTHERS: ``` sudo apt install python3-colcon-common-extensions ros-jazzy-joint-state-publisher ros-jazzy-joint-state-publisher-gui ```
- CHECKING: ``` sudo apt install liburdfdom-tools ```


### BUILD
```
cd ~/ros2_nexus_amr_ws
source /opt/ros/jazzy/setup.bash
colcon build --symlink-install
source install/setup.bash
clear
```

Gazebo (physics)
    ├── DiffDrive plugin
    ├── JointStatePublisher (gz)
    └── Internal TF
            ↓ (bridge)
ROS
    ├── robot_state_publisher
    ├── joint_state_publisher (optional)
    ├── /tf
    ├── /joint_states
    └── RViz


# GOAL 1: Render model in Gazebo

## STEP 1: Creating a workspace
```
mkdir -p ~/ros2_nexus_amr_ws/src
cd ~/ros2_nexus_amr_ws/src
source /opt/ros/jazzy/setup.bash
ros2 pkg create robot_description --build-type ament_cmake
```

## STEP 2: Create an empty world
* Create a folder worlds with file world.sdf<br />
* Add worlds to CMakeLists.txt<br />
* add a .gitignore<br />
* [BUILD](#build)<br />
* gz sim world.sdf<br />

## STEP 3: Creating a model with xacro
- Create a folder urdf with file robot.xacro<br />
- Add folder name to CMakeLists.txt<br />
- [BUILD](#build)<br />
- Terminal 1: gz sim -r ~/ros2_nexus_amr_ws/src/robot_description/worlds/world.sdf<br />
- Terminal 2: ros2 run ros_gz_sim create   -name nexus_amr   -file ~/ros2_nexus_amr_ws/src/robot_description/urdf/robot.xacro<br/>

## STEP 4: Move model in linear using /cmd_vel via shell
- Add plugin at ending of robot.xacro
- Add physics, gravity, and ground plane in the world.sdf
- Terminal 1(Start Gazebo): gz sim -r ~/ros2_nexus_amr_ws/src/robot_description/worlds/world.sdf<br />
- Terminal 2(Spawn Robot): ros2 run ros_gz_sim create   -name nexus_amr   -file ~/ros2_nexus_amr_ws/src/robot_description/urdf/robot.xacro<br/>
- Terminal 3(Create Bridge): ros2 run ros_gz_bridge parameter_bridge   /cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist<br/>
- Terminal 4(Move Robot linear): ros2 topic pub /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.5}, angular: {z: 0.0}}"<br/>

## STEP 5: Replace shell commands with keyboard
- Create a new folder robot_control with keyboard_teleop.py file
- Code in github
- Terminal 1(Start Gazebo): gz sim -r ~/ros2_nexus_amr_ws/src/robot_description/worlds/world.sdf<br />
- Terminal 2(Spawn Robot): ros2 run ros_gz_sim create   -name nexus_amr   -file ~/ros2_nexus_amr_ws/src/robot_description/urdf/robot.xacro<br/>
- Terminal 3(Create Bridge): ros2 run ros_gz_bridge parameter_bridge   /cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist<br/>
- Terminal 4(Move Robot linear): 
```
chmod +x src/robot_description/robot_control/keyboard_teleop.py
python3 ~/ros2_nexus_amr_ws/src/robot_description/robot_control/keyboard_teleop.py
```

## STEP 6: Render model in GAZEBO & RVIZ2 and move it by keyboard
- Terminal 1(Start Gazebo): gz sim -r ~/ros2_nexus_amr_ws/src/robot_description/worlds/world.sdf<br />
- Terminal 2(Convert & Spawn Robot): 
```
xacro ~/ros2_nexus_amr_ws/src/robot_description/urdf/robot.xacro > /tmp/nexus.urdf
ros2 run ros_gz_sim create \
    -name nexus_amr \
    -file /tmp/nexus.urdf

```
- Terminal 3(Create Bridge): 
```
ros2 run ros_gz_bridge parameter_bridge \
    /cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist \
    /joint_states@sensor_msgs/msg/JointState@gz.msgs.Model \
    /odom@nav_msgs/msg/Odometry@gz.msgs.Odometry \
    /tf@tf2_msgs/msg/TFMessage@gz.msgs.Pose_V


```
- Terminal 4
```
ros2 run robot_state_publisher robot_state_publisher \
    --ros-args \
    -p robot_description:="$(cat /tmp/nexus.urdf)"
```
- Terminal 5
```
rviz2
```
- Terminal 6
```
python3 ~/ros2_nexus_amr_ws/src/robot_description/robot_control/keyboard_teleop.py
```

## STEP 7: Automate every terminal to launch file
- Launches Gazebo with a custom world
- Spawns the robot from a Xacro-based URDF
- Bridges control, state, odometry, and TF between Gazebo and ROS 2
- Runs robot_state_publisher for TF generation
- Opens RViz with a predefined configuration
- [BUILD](#build)
- ros2 launch robot_description bridges.launch.py
- python3 ~/ros2_nexus_amr_ws/src/robot_description/robot_control/keyboard_teleop.py

## STEP 8: Create a map from world
- Add lidar link and join in robot.xacro
- Add lidar plugin in robot.xacro
- Create new file slam.launch.py to generate map
- Add '/scan@sensor_msgs/msg/LaserScan@gz.msgs.LaserScan' in bridge node
- [BUILD](#build)
- Terminal 1: ros2 launch robot_description all.launch.py
- Terminal 2: ros2 launch robot_description slam.launch.py
- Terminal 3: ros2 lifecycle set /slam_toolbox configure ros2 lifecycle set /slam_toolbox activate
```
In rviz, select Fixed Frame as map, Add map, topic /map
```
- Terminal 4: python3 ~/ros2_nexus_amr_ws/src/robot_description/robot_control/keyboard_teleop.py
- Terminal 5: ros2 run nav2_map_server map_saver_cli -f ~/ros2_nexus_amr_ws/src/robot_description/maps/my_map

## STEP 9: Adding a camera
- Add camera link + joint in robot.xacro
- Add gazebo plugin in same file
- Add ```/camera/image@sensor_msgs/msg/Image@gz.msgs.Image``` in bridges in all.launch.py
- [BUILD](#build)
- Termianl 1: ros2 launch robot_description all.launch.py
- Termianl 2: python3 ~/ros2_nexus_amr_ws/src/robot_description/robot_control/keyboard_teleop.py
- RViz:
```
Add → Image
Topic: /camera/image
```