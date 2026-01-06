from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():

    world_path = PathJoinSubstitution([
        FindPackageShare('robot_description'),
        'worlds',
        'world.sdf'
    ])

    urdf_path = PathJoinSubstitution([
        FindPackageShare('robot_description'),
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

    return LaunchDescription([
        gazebo,
        spawn_robot
    ])
