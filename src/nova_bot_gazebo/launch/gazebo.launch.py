import os
import xacro

from launch import LaunchDescription
from launch.actions import ExecuteProcess, TimerAction
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import PathJoinSubstitution


def generate_launch_description():

    pkg_desc = get_package_share_directory('nova_bot_description')
    pkg_gz   = get_package_share_directory('nova_bot_gazebo')

    # xacro → URDF
    xacro_file = os.path.join(pkg_desc, 'urdf', 'nova_robot.urdf.xacro')
    robot_description = xacro.process_file(xacro_file).toxml()

    world_file = os.path.join(pkg_gz, 'worlds', 'hospital.world')

    return LaunchDescription([

        # 1. Start Gazebo
        ExecuteProcess(
            cmd=[
                'gazebo', '--verbose', world_file,
                '-s', 'libgazebo_ros_init.so',
                '-s', 'libgazebo_ros_factory.so'
            ],
            output='screen'
        ),

        # 2. Robot State Publisher
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{
                'robot_description': robot_description,
                'use_sim_time': True
            }]
        ),

        # 3. Spawn robot after delay
        TimerAction(
            period=3.0,
            actions=[
                Node(
                    package='gazebo_ros',
                    executable='spawn_entity.py',
                    arguments=[
                        '-topic', 'robot_description',
                        '-entity', 'my_robot',
                        '-x', '0.0', '-y', '0.0', '-z', '0.01'
                    ],
                    output='screen'
                ),
            ]
        ),

        
    ])