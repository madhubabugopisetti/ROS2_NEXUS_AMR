from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch.substitutions import PathJoinSubstitution, Command
from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import Node
from launch_ros.actions import Node


def generate_launch_description():

    pkg_share = FindPackageShare('robot_description')

    world_path = PathJoinSubstitution([
        pkg_share,
        'worlds',
        'world.sdf'
    ])

    urdf_path = PathJoinSubstitution([
        pkg_share,
        'urdf',
        'robot.xacro'
    ])

    gazebo = ExecuteProcess(
        cmd=['gz', 'sim', '-r', world_path],
        output='screen'
    )

    spawn_robot = ExecuteProcess(
        cmd=[
            'ros2', 'run', 'ros_gz_sim', 'create',
            '-name', 'nexus_amr',
            '-file', urdf_path
        ],
        output='screen'
    )

    bridge = ExecuteProcess(
        cmd=[
            'ros2', 'run', 'ros_gz_bridge', 'parameter_bridge',
            '/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist',
            '/joint_states@sensor_msgs/msg/JointState@gz.msgs.Model',
            '/odom@nav_msgs/msg/Odometry@gz.msgs.Odometry',
            '/tf@tf2_msgs/msg/TFMessage@gz.msgs.Pose_V',
            '/scan@sensor_msgs/msg/LaserScan@gz.msgs.LaserScan',
            '/camera/image@sensor_msgs/msg/Image@gz.msgs.Image',
            '/camera/camera_info@sensor_msgs/msg/CameraInfo@gz.msgs.CameraInfo'
        ],
        output='screen'
    )

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{
            'robot_description': Command(['xacro ', urdf_path])
        }],
        output='screen'
    )

    rviz = Node(
        package='rviz2',
        executable='rviz2',
        arguments=[
            '-d',
            PathJoinSubstitution([
                pkg_share,
                'rviz',
                'nexus.rviz'
            ])
        ],
        output='screen'
    )

    return LaunchDescription([
        gazebo,
        spawn_robot,
        bridge,
        robot_state_publisher,
        rviz
    ])
